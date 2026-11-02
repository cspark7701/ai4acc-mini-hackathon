"""
src/visualization.py
Schematic diagram generation for the accelerator transport lattice.
"""
import os
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_beamline(save_path: Optional[str] = "img/beamline.png", show: bool = True) -> plt.Figure:
    """
    Draw 2D schematic diagram of the accelerator lattice layout,
    displaying correctors (HCM/VCM), quadrupoles (QF/QD), and BPMs.
    """
    s_bpm = np.linspace(1.0, 15.0, 12)
    s_corr = np.linspace(0.2, 8.0, 6)

    fig, ax = plt.subplots(figsize=(14, 3.8))

    # Central Beam Axis
    ax.axhline(0, color='royalblue', linestyle='--', linewidth=2.5, zorder=1)
    ax.annotate('', xy=(16.0, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="royalblue", lw=2.5))

    # Quadrupoles (QF / QD)
    quad_positions = [1.5, 3.8, 6.2, 8.5, 11.0, 13.5]
    for idx, sq in enumerate(quad_positions):
        is_qf = (idx % 2 == 0)
        color = '#D9534F' if is_qf else '#337AB7'
        rect = patches.Rectangle((sq - 0.25, -0.55), 0.5, 1.1, facecolor=color, edgecolor='black', lw=1.2, zorder=3)
        ax.add_patch(rect)
        ax.text(sq, 0.75 if is_qf else -0.85, 'QF' if is_qf else 'QD', ha='center', va='center', fontsize=9, fontweight='bold', color=color)

    # Steerers (HCM / VCM)
    for idx, sc in enumerate(s_corr):
        is_h = (idx % 2 == 0)
        corr_color = '#F0AD4E' if is_h else '#E67E22'
        corr_label = f"HCM{idx//2 + 1}" if is_h else f"VCM{idx//2 + 1}"
        rect = patches.Rectangle((sc - 0.18, -0.35), 0.36, 0.7, facecolor=corr_color, edgecolor='black', lw=1.2, zorder=4)
        ax.add_patch(rect)
        ax.text(sc, -0.65 if idx % 2 == 1 else 0.65, corr_label, ha='center', va='center', fontsize=8, fontweight='bold', color='#B95C00')

    # BPMs (1 to 12)
    for idx, sb in enumerate(s_bpm):
        diamond = patches.RegularPolygon((sb, 0), numVertices=4, radius=0.22, facecolor='#2ECC71', edgecolor='black', lw=1.2, zorder=5)
        ax.add_patch(diamond)
        ax.text(sb, 0.38 if idx % 2 == 0 else -0.38, f"BPM{idx+1}", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#196F3D')

    legend_elements = [
        patches.Patch(facecolor='#D9534F', edgecolor='black', label='Focusing Quadrupole (QF)'),
        patches.Patch(facecolor='#337AB7', edgecolor='black', label='Defocusing Quadrupole (QD)'),
        patches.Patch(facecolor='#F0AD4E', edgecolor='black', label='Horiz. Corrector (HCM)'),
        patches.Patch(facecolor='#E67E22', edgecolor='black', label='Vert. Corrector (VCM)'),
        patches.Patch(facecolor='#2ECC71', edgecolor='black', label='Beam Position Monitor (BPM)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.0, 1.28), ncol=5, frameon=True, fontsize=9)
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(-1.3, 1.4)
    ax.set_xlabel("Beamline Longitudinal Position $s$ (m)", fontsize=11, fontweight='bold')
    ax.set_yticks([])
    ax.set_title("Accelerator Lattice Layout: Correctors (HCM/VCM), Quadrupoles (QF/QD), and BPMs", fontsize=12, fontweight='bold', y=1.3)
    ax.grid(True, axis='x', linestyle=':', alpha=0.6)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Lattice schematic saved to {save_path}")

    if show:
        plt.show()

    return fig


if __name__ == "__main__":
    draw_beamline(save_path="img/beamline.png", show=False)
