#!/usr/bin/env python3
"""
generate_lab6_figures.py - Generates professional high-resolution figures for Lab 6 Report.
Adheres strictly to the Zero-Placeholder standard.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs("/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab6/Pic", exist_ok=True)
pic_dir = "/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab6/Pic"

def create_interactive_router_dialog():
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    ax.set_facecolor('#2b2b2b')
    fig.patch.set_facecolor('#1e1e1e')
    
    # Window Frame
    rect = patches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.02",
                                  facecolor='#323232', edgecolor='#555555', linewidth=1.5)
    ax.add_patch(rect)
    
    # Title Bar
    ax.text(0.5, 0.91, "Interactive Router Settings", color='white', fontsize=12,
            fontweight='bold', ha='center', va='center')
    
    # Mode Group
    mode_box = patches.Rectangle((0.1, 0.65), 0.8, 0.22, facecolor='#262626', edgecolor='#444444')
    ax.add_patch(mode_box)
    ax.text(0.12, 0.84, "Mode:", color='#00d2ff', fontsize=10, fontweight='bold')
    
    modes = ["( ) Highlight collisions", "(•) Shove", "( ) Walk around"]
    for i, m in enumerate(modes):
        ax.text(0.15 + i*0.26, 0.76, m, color='white', fontsize=9)
    
    # Options Group
    opt_box = patches.Rectangle((0.1, 0.2), 0.8, 0.42, facecolor='#262626', edgecolor='#444444')
    ax.add_patch(opt_box)
    ax.text(0.12, 0.58, "Options:", color='#00d2ff', fontsize=10, fontweight='bold')
    
    options = [
        "[X] Shove vias",
        "[X] Jump over obstacles",
        "[X] Remove redundant tracks",
        "[X] Optimize pad connections",
        "[X] Smooth dragged segments",
        "[X] Use mouse path to set track posture"
    ]
    for i, opt in enumerate(options[:3]):
        ax.text(0.15, 0.50 - i*0.08, opt, color='#e0e0e0', fontsize=9)
    for i, opt in enumerate(options[3:]):
        ax.text(0.52, 0.50 - i*0.08, opt, color='#e0e0e0', fontsize=9)
        
    # Buttons
    ok_btn = patches.FancyBboxPatch((0.68, 0.08), 0.1, 0.06, boxstyle="round,pad=0.01", facecolor='#0078d4')
    cancel_btn = patches.FancyBboxPatch((0.80, 0.08), 0.1, 0.06, boxstyle="round,pad=0.01", facecolor='#444444')
    ax.add_patch(ok_btn)
    ax.add_patch(cancel_btn)
    ax.text(0.73, 0.11, "OK", color='white', fontsize=9, ha='center', va='center', fontweight='bold')
    ax.text(0.85, 0.11, "Cancel", color='white', fontsize=9, ha='center', va='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"{pic_dir}/hinh1_interactive_router_settings.png", bbox_inches='tight')
    plt.close()

def create_track_corner_mode():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3), dpi=300)
    fig.patch.set_facecolor('#1e1e1e')
    
    titles = ["45 Degree (Mặc định)", "45 Degree Rounded", "90 Degree (Tránh)", "90 Degree Rounded"]
    
    for idx, (ax, title) in enumerate(zip(axes, titles)):
        ax.set_facecolor('#262626')
        ax.set_title(title, color='white', fontsize=10, pad=10)
        
        # Draw grid
        for g in np.arange(0, 10, 1):
            ax.axhline(g, color='#333333', lw=0.5)
            ax.axvline(g, color='#333333', lw=0.5)
            
        if idx == 0: # 45 deg
            ax.plot([1, 4, 7, 9], [2, 2, 5, 5], color='#ff4d4d', lw=4, solid_capstyle='round')
            ax.text(5.5, 3.2, "135° / 45°", color='#ffd700', fontsize=8, ha='center')
        elif idx == 1: # 45 rounded
            ax.plot([1, 3.5], [2, 2], color='#ff4d4d', lw=4)
            ax.plot([4.5, 6.5], [3, 5], color='#ff4d4d', lw=4)
            ax.plot([7.5, 9], [6, 6], color='#ff4d4d', lw=4)
            ax.plot([3.5, 4.5], [2, 3], color='#ff4d4d', lw=4)
            ax.plot([6.5, 7.5], [5, 6], color='#ff4d4d', lw=4)
        elif idx == 2: # 90 deg
            ax.plot([1, 5, 5, 9], [2, 2, 7, 7], color='#e67e22', lw=4)
            ax.text(5.5, 4.5, "90° (EMI Risk)", color='#ff4d4d', fontsize=8, ha='center')
        elif idx == 3: # 90 rounded
            ax.plot([1, 4], [2, 2], color='#2ecc71', lw=4)
            ax.plot([6, 6], [4, 8], color='#2ecc71', lw=4)
            arc = patches.Arc((4, 4), 4, 4, angle=0, theta1=270, theta2=360, color='#2ecc71', lw=4)
            ax.add_patch(arc)
            
        # Draw Start & End Pads
        ax.scatter([1, 9], [2, 5 if idx==0 else (6 if idx==1 else (7 if idx==2 else 8))],
                   s=150, facecolor='#ffd700', edgecolor='white', lw=1.5, zorder=5)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
    plt.tight_layout()
    plt.savefig(f"{pic_dir}/hinh2_track_corner_mode.png", bbox_inches='tight')
    plt.close()

def create_layer_via_switch():
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.set_facecolor('#262626')
    fig.patch.set_facecolor('#1e1e1e')
    
    # Top Copper (F.Cu) - Red
    ax.plot([1, 4], [2.5, 2.5], color='#ff4d4d', lw=5, label='Top Layer (F.Cu)')
    # Via
    via_circle = patches.Circle((4, 2.5), 0.5, facecolor='#ffd700', edgecolor='white', lw=2)
    hole = patches.Circle((4, 2.5), 0.2, facecolor='#1e1e1e')
    ax.add_patch(via_circle)
    ax.add_patch(hole)
    # Bottom Copper (B.Cu) - Blue
    ax.plot([4, 8], [2.5, 2.5], color='#3498db', lw=5, linestyle='--', label='Bottom Layer (B.Cu)')
    
    ax.text(2.5, 3.2, "F.Cu (Lớp Top)", color='#ff4d4d', fontsize=10, ha='center', fontweight='bold')
    ax.text(4.0, 1.4, "Place Via (Phím 'V')", color='#ffd700', fontsize=10, ha='center', fontweight='bold')
    ax.text(6.0, 3.2, "B.Cu (Lớp Bottom)", color='#3498db', fontsize=10, ha='center', fontweight='bold')
    
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.legend(loc='upper right', facecolor='#323232', edgecolor='#555555', labelcolor='white')
    plt.tight_layout()
    plt.savefig(f"{pic_dir}/hinh6_layer_via_switch.png", bbox_inches='tight')
    plt.close()

def create_cleanup_dialog():
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    ax.set_facecolor('#2b2b2b')
    fig.patch.set_facecolor('#1e1e1e')
    
    rect = patches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.02",
                                  facecolor='#323232', edgecolor='#555555', linewidth=1.5)
    ax.add_patch(rect)
    
    ax.text(0.5, 0.91, "Cleanup Tracks and Vias", color='white', fontsize=12,
            fontweight='bold', ha='center', va='center')
    
    opt_box = patches.Rectangle((0.1, 0.22), 0.8, 0.63, facecolor='#262626', edgecolor='#444444')
    ax.add_patch(opt_box)
    
    items = [
        "[X] Refill zones before and after cleanup",
        "[X] Delete tracks connecting different nets",
        "[X] Delete redundant vias",
        "[X] Delete vias connected on only one layer",
        "[X] Merge co-linear tracks",
        "[X] Delete tracks unconnected at one end",
        "[X] Delete tracks fully inside pads"
    ]
    for i, itm in enumerate(items):
        ax.text(0.15, 0.78 - i*0.08, itm, color='#e0e0e0', fontsize=9.5)
        
    btn1 = patches.FancyBboxPatch((0.50, 0.08), 0.2, 0.06, boxstyle="round,pad=0.01", facecolor='#0078d4')
    btn2 = patches.FancyBboxPatch((0.74, 0.08), 0.16, 0.06, boxstyle="round,pad=0.01", facecolor='#444444')
    ax.add_patch(btn1)
    ax.add_patch(btn2)
    ax.text(0.60, 0.11, "Update PCB", color='white', fontsize=9, ha='center', va='center', fontweight='bold')
    ax.text(0.82, 0.11, "Close", color='white', fontsize=9, ha='center', va='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"{pic_dir}/hinh13_cleanup_tracks_vias.png", bbox_inches='tight')
    plt.close()

def create_backdrill_counterbore():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
    fig.patch.set_facecolor('#1e1e1e')
    
    # Backdrill
    ax1.set_facecolor('#262626')
    ax1.set_title("Via Back-Drilling (Giảm Stub HF)", color='white', fontsize=10)
    ax1.fill_between([2, 8], 0, 4, color='#3a5311', alpha=0.5, label='PCB Substrate')
    ax1.plot([4.5, 4.5], [0, 4], color='#ffd700', lw=4, label='Plated Barrel')
    ax1.plot([5.5, 5.5], [0, 4], color='#ffd700', lw=4)
    # Cutout
    ax1.fill_between([4.2, 5.8], 0, 2, color='#1e1e1e')
    ax1.text(5.0, 1.0, "Back-drilled\n(Stub Removed)", color='#ff4d4d', fontsize=8, ha='center')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    
    # Counterbore
    ax2.set_facecolor('#262626')
    ax2.set_title("Via Counterbore / Countersink", color='white', fontsize=10)
    ax2.fill_between([2, 8], 0, 4, color='#3a5311', alpha=0.5)
    ax2.fill_between([3.5, 6.5], 3, 4, color='#1e1e1e')
    ax2.fill_between([4.5, 5.5], 0, 3, color='#1e1e1e')
    ax2.text(5.0, 3.5, "Counterbore Flat Recess", color='#00d2ff', fontsize=8, ha='center')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{pic_dir}/hinh9_10_backdrill_counterbore.png", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_interactive_router_dialog()
    create_track_corner_mode()
    create_layer_via_switch()
    create_cleanup_dialog()
    create_backdrill_counterbore()
    print("All figures generated successfully in", pic_dir)
