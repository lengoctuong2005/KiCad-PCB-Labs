import argparse
import csv
import json
import math
import re
import socket
import sys
import time
from collections import Counter, deque
from dataclasses import dataclass

import numpy as np
from scipy.signal import butter, find_peaks, sosfiltfilt


@dataclass(frozen=True)
class Packet:
    seq: int
    timestamp_us: int
    ecg_raw: int
    ppg_ir: int
    lead_off: int
    quality_flags: int
    sync_skew_us: int
    ppg_timestamp_us: int | None = None
    sample_type: str = 'E'


def parse_packet(line):
    if isinstance(line, bytes):
        line = line.decode('ascii', errors='strict')
    fields = line.strip().split(',')
    if len(fields) not in (7, 8):
        raise ValueError('expected seven or eight CSV fields')
    numeric = fields[:7]
    if any(not re.fullmatch(r'-?\d{1,20}', field) for field in numeric):
        raise ValueError('expected integer CSV fields')
    seq, timestamp, ecg, ppg, lod, flags, skew = map(int, numeric)
    sample_type = 'E'
    if len(fields) == 8:
        if not re.fullmatch(r'[A-Za-z]', fields[7]):
            raise ValueError('expected single-letter sample type')
        sample_type = fields[7].upper()
        if sample_type not in ('E', 'P'):
            raise ValueError('unsupported sample type')
    flag_limit = 256 if len(fields) == 8 else 128
    if not (0 <= seq < 2**32 and 0 <= timestamp < 2**64 and
            -32768 <= ecg <= 32767 and 0 <= ppg <= 262143 and
            0 <= lod <= 3 and 0 <= flags < flag_limit and -2**31 <= skew < 2**31):
        raise ValueError('telemetry field out of range')
    return Packet(seq, timestamp, ecg, ppg, lod, flags, skew, sample_type=sample_type)


def quality_error(packet):
    if packet.lead_off or (packet.quality_flags & 3):
        return 'lead_off'
    if packet.quality_flags & 8:
        return 'i2c_error'
    ppg_present = packet.ppg_ir != 0 or packet.sample_type == 'P'
    if ((packet.quality_flags & 4) or abs(packet.ecg_raw) >= 32700 or
            (ppg_present and not 100 < packet.ppg_ir < 262000)):
        return 'saturation_or_contact'
    if packet.quality_flags & 16:
        return 'fifo_overflow'
    if packet.quality_flags & 32:
        return 'queue_drop'
    if packet.quality_flags & 64:
        return 'fifo_burst'
    if packet.quality_flags & 128:
        return 'timestamp_uncertain'
    if abs(packet.sync_skew_us) > 2000:
        return 'mcu_skew_large'
    return None


class Monitor:
    def __init__(self):
        self.counts = Counter()
        self.previous = None
        self.previous_by_type = {}

    def add(self, packet):
        self.counts['packets'] += 1
        self.counts['packets_e' if packet.sample_type == 'E' else 'packets_p'] += 1
        if self.previous is not None:
            delta = (packet.seq - self.previous.seq) % 2**32
            if delta == 0:
                self.counts['duplicate_seq'] += 1
            elif delta != 1:
                self.counts['sequence_discontinuities'] += 1
                if delta < 2**31:
                    self.counts['missing_packets_lower_bound'] += delta - 1
        previous = self.previous_by_type.get(packet.sample_type)
        if previous is not None and packet.timestamp_us <= previous.timestamp_us:
            key = 'nonmonotonic_ecg_timestamps' if packet.sample_type == 'E' else 'nonmonotonic_ppg_timestamps'
            self.counts[key] += 1
        self.previous_by_type[packet.sample_type] = packet
        error = quality_error(packet)
        if error:
            self.counts[error] += 1
        self.previous = packet


def read_firmware_csv(path):
    packets = []
    with open(path, newline='', encoding='ascii') as handle:
        for line in handle:
            if not line.strip() or line.lstrip().startswith('seq,'):
                continue
            try:
                packets.append(parse_packet(line))
            except (ValueError, UnicodeError):
                packets.append(None)
    return packets


def read_timed_csv(path):
    required = {'seq', 'timestamp_us', 'ppg_timestamp_us', 'ecg_raw', 'ppg_ir',
                'lead_off', 'quality_flags', 'sync_skew_us'}
    packets = []
    with open(path, newline='', encoding='ascii') as handle:
        rows = csv.DictReader(handle)
        if not rows.fieldnames or not required.issubset(rows.fieldnames):
            raise ValueError('timed CSV requires columns: ' + ', '.join(sorted(required)))
        for row in rows:
            try:
                values = [row[k] for k in ('seq', 'timestamp_us', 'ecg_raw', 'ppg_ir',
                                            'lead_off', 'quality_flags', 'sync_skew_us')]
                packet = parse_packet(','.join(values))
                ppg_ts = row['ppg_timestamp_us']
                if not re.fullmatch(r'\d{1,20}', ppg_ts) or int(ppg_ts) >= 2**64:
                    raise ValueError('invalid PPG timestamp')
                packets.append(Packet(*list(packet.__dict__.values())[:7], int(ppg_ts)))
            except (ValueError, TypeError):
                packets.append(None)
    return packets


def segments_for_analysis(packets, expected_in_fs=None, jitter_fraction=0.35):
    if expected_in_fs is not None and (not math.isfinite(expected_in_fs) or not 40 < expected_in_fs <= 5000):
        raise ValueError('expected input fs must be between 40 and 5000 Hz')
    intervals = []
    previous = None
    for packet in packets:
        if packet is not None and packet.ppg_timestamp_us is None:
            raise ValueError('PPG sample timestamps are absent: firmware timing is unverified')
        if packet and previous and (packet.seq - previous.seq) % 2**32 == 1:
            dt = packet.timestamp_us - previous.timestamp_us
            if dt > 0:
                intervals.append(dt)
        previous = packet

    in_fs = expected_in_fs
    if in_fs is None:
        if not intervals:
            raise ValueError('cannot infer sampling rate from timestamps')
        in_fs = 1e6 / float(np.median(intervals))
        if not 40 < in_fs <= 5000:
            raise ValueError('inferred sampling rate outside supported range')
    period = 1e6 / in_fs

    segments, current = [], []
    monitor = Monitor()
    previous = None
    for packet in packets:
        if packet is None:
            monitor.counts['malformed'] += 1
            if current:
                segments.append(current)
            current, previous = [], None
            continue
        monitor.add(packet)
        good = quality_error(packet) is None
        if previous is not None:
            de = packet.timestamp_us - previous.timestamp_us
            dp = packet.ppg_timestamp_us - previous.ppg_timestamp_us
            continuous = ((packet.seq - previous.seq) % 2**32 == 1 and
                          abs(de - period) <= jitter_fraction * period and
                          abs(dp - period) <= jitter_fraction * period)
            if not continuous:
                monitor.counts['segment_breaks'] += 1
                if current:
                    segments.append(current)
                current = []
        if good:
            current.append(packet)
        elif current:
            segments.append(current)
            current = []
        previous = packet
    if current:
        segments.append(current)
    return segments, in_fs, monitor.counts


def detect_r_peaks(filtered, fs):
    deriv = np.gradient(filtered)
    n = max(1, round(0.150 * fs))
    envelope = np.convolve(deriv**2, np.ones(n) / n, mode='same')
    level = np.median(envelope)
    threshold = level + 0.25 * (np.percentile(envelope, 99.5) - level)
    if not np.isfinite(threshold) or threshold <= np.finfo(float).eps:
        return np.array([], dtype=int)
    candidates, _ = find_peaks(envelope, height=threshold, distance=max(1, round(0.30 * fs)))
    peaks = []
    radius = round(0.100 * fs)
    for candidate in candidates:
        start = max(0, candidate - radius)
        stop = min(len(filtered), candidate + radius + 1)
        index = start + int(np.argmax(np.abs(filtered[start:stop])))
        if not peaks or index - peaks[-1] >= round(0.30 * fs):
            peaks.append(index)
    return np.asarray(peaks, dtype=int)


def tangent_foot(ppg, fs, r_index, stop_index):
    first = r_index + round(0.08 * fs)
    if stop_index <= first + 3:
        return None
    peak = first + int(np.argmax(ppg[first:stop_index]))
    start = max(first, peak - round(0.30 * fs))
    if peak <= start + 3:
        return None
    before = ppg[start:peak]
    valley = start + len(before) - 1 - int(np.argmin(before[::-1]))
    rising = ppg[valley:peak + 1]
    if len(rising) < 4 or np.ptp(rising) <= np.finfo(float).eps:
        return None
    slopes = np.gradient(rising)
    slope_idx = valley + int(np.argmax(slopes))
    slope = slopes[slope_idx - valley]
    if slope <= np.finfo(float).eps:
        return None
    foot = slope_idx - (ppg[slope_idx] - ppg[valley]) / slope
    return float(foot) if valley <= foot <= slope_idx else None


def analyze(packets, target_fs=1000.0, correction_ms=None, expected_in_fs=None):
    if not math.isfinite(target_fs) or not 200 <= target_fs <= 5000:
        raise ValueError('target_fs must be between 200 and 5000 Hz')
    if correction_ms is not None and not math.isfinite(correction_ms):
        raise ValueError('delay correction must be finite')

    segments, in_fs, counts = segments_for_analysis(packets, expected_in_fs=expected_in_fs)
    ecg_sos = butter(2, [5, 15], fs=target_fs, btype='bandpass', output='sos')
    ppg_sos = butter(2, [0.5, 8], fs=target_fs, btype='bandpass', output='sos')
    beats = []

    for segment in segments:
        if len(segment) < round(4 * in_fs):
            counts['short_segments_skipped'] += 1
            continue
        origin = segment[0].timestamp_us
        te = np.array([p.timestamp_us - origin for p in segment], dtype=float) / 1e6
        tp = np.array([p.ppg_timestamp_us - origin for p in segment], dtype=float) / 1e6
        start, stop = max(te[0], tp[0]), min(te[-1], tp[-1])
        if stop - start < 4.0:
            counts['short_segments_skipped'] += 1
            continue

        grid = np.arange(start, stop, 1.0 / target_fs)
        ecg = np.interp(grid, te, [p.ecg_raw for p in segment])
        ppg = np.interp(grid, tp, [p.ppg_ir for p in segment])
        ecg = sosfiltfilt(ecg_sos, ecg)
        ppg = sosfiltfilt(ppg_sos, ppg)
        peaks = detect_r_peaks(ecg, target_fs)
        last_foot = -math.inf

        for n, r in enumerate(peaks):
            if grid[r] < start + 0.5 or grid[r] + 0.5 > stop - 0.5:
                counts['edge_beats_skipped'] += 1
                continue
            end = min(len(grid), r + round(0.5 * target_fs), peaks[n + 1] if n + 1 < len(peaks) else len(grid))
            foot = tangent_foot(ppg, target_fs, r, end)
            if foot is None or foot <= last_foot:
                counts['foot_not_found'] += 1
                continue
            raw_ms = (foot - r) * 1000.0 / target_fs
            if not 120 <= raw_ms <= 450:
                counts['pat_out_of_window'] += 1
                continue
            last_foot = foot
            beat = {
                'r_time_us': round(origin + grid[r] * 1e6),
                'ppg_foot_time_us': round(origin + (grid[int(math.floor(foot))] if int(math.floor(foot)) < len(grid) else grid[-1]) * 1e6),
                'pat_raw_ms': raw_ms,
                'pat_corrected_ms': raw_ms + correction_ms if correction_ms is not None else None,
            }
            beats.append(beat)

    counts['analyzed_segments'] = len(segments) - counts['short_segments_skipped']
    return beats, target_fs, dict(counts)


def simulation(in_fs=500, duration=12, ecg_drift=0.0, ppg_drift=0.0):
    fs_e = in_fs * (1.0 + ecg_drift)
    fs_p = in_fs * (1.0 + ppg_drift)
    n_samples = round(duration * in_fs)
    te = np.arange(n_samples) / fs_e
    tp = np.arange(n_samples) / fs_p

    ecg = np.zeros(n_samples)
    ppg = np.zeros(n_samples)
    for beat in np.arange(0.8, duration - 0.6, 0.8):
        ecg += 11000.0 * np.exp(-((te - beat) / 0.018)**2)
        phase = tp - beat - 0.230
        pulse = (phase >= 0) & (phase < 0.22)
        ppg[pulse] += 12000.0 * np.sin(np.pi * phase[pulse] / 0.22)**2

    return [
        Packet(i, round(x_e * 1e6), round(e), round(100000.0 + p), 0, 0, 0, round(x_p * 1e6))
        for i, (x_e, x_p, e, p) in enumerate(zip(te, tp, ecg, ppg))
    ]


def receive_udp(sock, duration, plot=False):
    packets, monitor = [], Monitor()
    sock.settimeout(0.05)
    end = time.monotonic() + duration
    if plot:
        import matplotlib.pyplot as plt
        plt.ion()
        fig, axes = plt.subplots(2, 1, sharex=True)
        lines = [axes[0].plot([], [])[0], axes[1].plot([], [])[0]]
        axes[0].set_ylabel('ECG raw')
        axes[1].set_ylabel('PPG raw')
        axes[1].set_xlabel('ECG IRQ time (s), PPG sample time unknown')
        fig.suptitle('Firmware timing unverified: PAT disabled')
        history = deque(maxlen=4000)
    while time.monotonic() < end:
        try:
            data, _ = sock.recvfrom(256)
        except socket.timeout:
            data = None
        if data is not None:
            try:
                packet = parse_packet(data)
            except (ValueError, UnicodeError):
                monitor.counts['malformed'] += 1
                packets.append(None)
            else:
                packets.append(packet)
                monitor.add(packet)
                if plot:
                    history.append(packet)
        if plot:
            if not plt.fignum_exists(fig.number):
                break
            if history:
                origin = history[0].timestamp_us
                x = [(p.timestamp_us - origin) / 1e6 for p in history]
                for ax, line, vals in zip(axes, lines, ([p.ecg_raw for p in history], [p.ppg_ir for p in history])):
                    line.set_data(x, vals)
                    ax.relim()
                    ax.autoscale_view()
            plt.pause(0.001)
    if plot:
        plt.ioff()
        plt.close(fig)
    return packets, dict(monitor.counts)


def main():
    parser = argparse.ArgumentParser(description='Experimental ECG-to-PPG PAT, not a medical device')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--file', help='firmware seven-column CSV: quality audit only')
    source.add_argument('--timed-csv', help='independently validated sample timestamps for both channels')
    source.add_argument('--udp', nargs='?', const=5005, type=int, metavar='PORT', help='firmware UDP quality audit')
    source.add_argument('--simulate', action='store_true', help='synthetic timing data')
    parser.add_argument('--bind', default='0.0.0.0')
    parser.add_argument('--duration', type=float, default=10.0)
    parser.add_argument('--target-fs', type=float, default=1000.0, help='resampling grid frequency (Hz, default 1000)')
    parser.add_argument('--ecg-relative-delay-ms', type=float, help='independently measured ECG-minus-PPG delay')
    parser.add_argument('--live', action='store_true', help='show UDP waveforms; PAT is disabled for firmware')
    args = parser.parse_args()
    if args.live and args.udp is None:
        parser.error('--live requires --udp')
    if not math.isfinite(args.duration) or args.duration <= 0:
        parser.error('--duration must be positive and finite')
    try:
        if args.udp is not None:
            if not 1 <= args.udp <= 65535:
                parser.error('UDP port must be 1..65535')
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind((args.bind, args.udp))
                packets, counts = receive_udp(sock, args.duration, args.live)
            result = {'source': 'firmware_udp_unverified', 'quality': counts, 'pat': None}
        elif args.file:
            packets = read_firmware_csv(args.file)
            monitor = Monitor()
            for p in packets:
                if p is None:
                    monitor.counts['malformed'] += 1
                    monitor.previous = None
                else:
                    monitor.add(p)
            result = {'source': 'firmware_file_unverified', 'quality': dict(monitor.counts), 'pat': None}
        else:
            packets = simulation(in_fs=500, duration=12) if args.simulate else read_timed_csv(args.timed_csv)
            beats, resampled_fs, counts = analyze(packets, target_fs=args.target_fs, correction_ms=args.ecg_relative_delay_ms)
            result = {
                'source': 'synthetic' if args.simulate else 'external_timed_csv_claimed_valid',
                'resampled_rate_hz': resampled_fs,
                'quality': counts,
                'beats': beats,
                'delay_correction_ms': args.ecg_relative_delay_ms,
            }
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        if result.get('pat', 1) is None:
            print('PAT disabled: firmware PPG sample timing, FIFO and I2C validity are unverified.', file=sys.stderr)
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
