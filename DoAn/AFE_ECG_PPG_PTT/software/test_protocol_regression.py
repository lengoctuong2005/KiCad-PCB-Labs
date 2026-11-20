import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ptt_live_analyzer as m


def test_parse_typed_and_legacy():
    legacy = m.parse_packet('105,123456789,-1204,145203,0,0,120')
    assert legacy.sample_type == 'E'
    assert legacy.ppg_timestamp_us is None
    typed_e = m.parse_packet('1,1000,10,0,0,0,0,E')
    typed_p = m.parse_packet('2,2500,-1,150000,0,192,0,P')
    assert typed_e.sample_type == 'E' and typed_e.ppg_ir == 0
    assert typed_p.sample_type == 'P' and typed_p.ppg_ir == 150000
    for bad in ('1,2,3,4,5,6', '1,2,3,4,5,6,7,X', '1,2,32768,4,0,0,0,E',
                '1,2,3,262144,0,0,0,P', '1,2,3,4,4,0,0,E', '1,2,3,4,0,256,0,E',
                '1,,3,4,5,6,7,E', '1,2,3,4,0,0,999999999999999999999,E',
                '4294967296,2,3,4,0,0,0,E', '1,18446744073709551616,3,4,0,0,0,E',
                '-1,2,3,4,0,0,0,E', '1,2,3,4,0,0,2147483648,E'):
        try:
            m.parse_packet(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('accepted malicious CSV: ' + bad)
    assert m.parse_packet('1,2,3,4,0,127,0').quality_flags == 127
    assert m.parse_packet('1,2,3,4,0,255,0,P').quality_flags == 255


def test_quality_flags():
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 128, 0, sample_type='P')) == 'timestamp_uncertain'
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 64, 0, sample_type='P')) == 'fifo_burst'
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 8, 0, sample_type='P')) == 'i2c_error'
    assert m.quality_error(m.parse_packet('1,1000,0,0,0,136,0,P')) == 'i2c_error'
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 16, 0, sample_type='P')) == 'fifo_overflow'
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 32, 0, sample_type='P')) == 'queue_drop'
    assert m.quality_error(m.Packet(1, 1, 0, 200000, 0, 0, 0, sample_type='P')) is None
    assert m.quality_error(m.Packet(1, 1, 0, 50, 0, 0, 0, sample_type='P')) == 'saturation_or_contact'
    assert m.quality_error(m.Packet(1, 1, 0, 0, 0, 0, 0, sample_type='E')) is None
    assert m.quality_error(m.Packet(1, 1, 33000, 0, 0, 0, 0, sample_type='E')) == 'saturation_or_contact'


def test_monitor_interleaved_paired_stream():
    monitor = m.Monitor()
    pairs = [
        m.Packet(0, 0, 1, 200000, 0, 0, 0, sample_type='E'),
        m.Packet(1, 0, 1, 200000, 0, 0, 0, sample_type='P'),
        m.Packet(2, 2105, 2, 200100, 0, 0, 0, sample_type='E'),
        m.Packet(3, 2500, 2, 200100, 0, 0, 0, sample_type='P'),
    ]
    for packet in pairs:
        monitor.add(packet)
    assert monitor.counts['packets'] == 4
    assert monitor.counts['packets_e'] == 2
    assert monitor.counts['packets_p'] == 2
    assert monitor.counts['sequence_discontinuities'] == 0
    assert monitor.counts['nonmonotonic_ecg_timestamps'] == 0
    assert monitor.counts['nonmonotonic_ppg_timestamps'] == 0

    legacy = m.Monitor()
    legacy.add(m.Packet(0, 1000, 1, 200000, 0, 0, 0, 2105))
    legacy.add(m.Packet(1, 900, 1, 200000, 0, 0, 0, 4200))
    assert legacy.counts['nonmonotonic_ecg_timestamps'] == 1


def test_typed_firmware_csv_audit_only():
    fd, path = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    try:
        with open(path, 'w', encoding='ascii') as handle:
            handle.write('seq,timestamp_us,ecg_raw,ppg_ir,lead_off,quality_flags,sync_skew_us,sample_type\n')
            handle.write('1,1000,10,0,0,0,0,E\n')
            handle.write('2,1000,0,150000,0,192,0,P\n')
            handle.write('3,2000,11,0,0,4,0,E\n')
            handle.write('4,2000,0,150100,0,128,0,P\n')
            handle.write('bad,row\n')
        packets = m.read_firmware_csv(path)
    finally:
        os.unlink(path)
    assert len(packets) == 5 and packets[4] is None
    assert [p.sample_type if p else None for p in packets] == ['E', 'P', 'E', 'P', None]
    try:
        m.segments_for_analysis([p for p in packets if p is not None], expected_in_fs=500.0)
    except ValueError as exc:
        assert 'unverified' in str(exc)
    else:
        raise AssertionError('typed firmware stream must stay audit-only')


def test_simulation_cli_analysis():
    packets = m.simulation(in_fs=500, duration=12)
    assert packets and all(p.ppg_timestamp_us is not None for p in packets)
    beats, fs, counts = m.analyze(packets, target_fs=1000.0, correction_ms=5.6)
    assert fs == 1000.0
    assert counts['analyzed_segments'] >= 1
    assert len(beats) >= 8


def run():
    test_parse_typed_and_legacy()
    test_quality_flags()
    test_monitor_interleaved_paired_stream()
    test_typed_firmware_csv_audit_only()
    test_simulation_cli_analysis()
    print(json.dumps({
        'status': 'ok',
        'checks': ['parse_typed_and_legacy', 'quality_flags',
                   'monitor_interleaved_paired_stream', 'typed_firmware_csv_audit_only',
                   'simulation_cli_analysis'],
    }, sort_keys=True))


if __name__ == '__main__':
    run()
