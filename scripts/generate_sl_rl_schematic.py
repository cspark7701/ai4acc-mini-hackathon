"""
scripts/generate_sl_rl_schematic.py
Generate the schematic comparing Forward Supervised Learning (surrogate digital
twin and online inversion, Track 1) with Reinforcement Learning (closed-loop
policy control, Track 2).

The figure is drawn at roughly the size it appears on the Lecture 1 slide
(about 12 x 4.6 in), so the font sizes below are close to the sizes the audience
sees. Keep the text short when editing: there is no room for long sentences.

Usage (from the repository root):
    python scripts/generate_sl_rl_schematic.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["mathtext.fontset"] = "dejavusans"

W, H = 12.4, 4.6
fig = plt.figure(figsize=(W, H), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")

TITLE_FS = 14.5   # panel titles
BADGE_FS = 10.5   # paradigm and phase badges
BOX_T_FS = 12     # box titles
BOX_FS = 11       # box body text
NOTE_FS = 10.5    # arrow labels and footnotes


def card(x, y, w, h, fill, edge, lw=1.4, radius=0.12):
    ax.add_patch(patches.FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=edge, linewidth=lw, zorder=1))


def badge(x, y, w, h, text, fill, color, fs=BADGE_FS):
    """Badge with its left edge at x and vertical centre at y."""
    ax.add_patch(patches.FancyBboxPatch(
        (x, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.07",
        facecolor=fill, edgecolor="none", zorder=3))
    ax.text(x + w / 2, y, text, fontsize=fs, fontweight="bold",
            ha="center", va="center", color=color, zorder=4)


def box(x, y, w, h, title, body, fill, edge, title_color, body_color="#334155"):
    card(x, y, w, h, fill, edge, lw=1.6, radius=0.09)
    ax.text(x + w / 2, y + h - 0.27, title, fontsize=BOX_T_FS, fontweight="bold",
            ha="center", va="center", color=title_color, zorder=4)
    ax.text(x + w / 2, y + (h - 0.45) / 2, body, fontsize=BOX_FS,
            ha="center", va="center", color=body_color, zorder=4, linespacing=1.35)


def arrow(x0, y0, x1, y1, color):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, mutation_scale=16), zorder=5)


# ------------------------------------------------------------------------------
# Left panel: Paradigm 1 - Forward Supervised Learning (Track 1)
# ------------------------------------------------------------------------------
LX, LW = 0.10, 6.05
card(LX, 0.10, LW, 4.40, "#F8FAFC", "#94A3B8", lw=1.5, radius=0.18)
badge(LX + 0.20, 4.18, 1.35, 0.36, "PARADIGM 1", "#0284C7", "#FFFFFF")
ax.text(LX + 1.70, 4.18, "Forward Supervised Learning", fontsize=TITLE_FS,
        fontweight="bold", ha="left", va="center", color="#0369A1")

# Phase 1: offline training
ax.text(LX + 0.25, 3.72, "PHASE 1  Offline training", fontsize=BADGE_FS,
        fontweight="bold", ha="left", va="center", color="#0369A1")
y1, h1 = 2.42, 1.08
box(LX + 0.20, y1, 1.70, h1, "Data", "1,500 shots\n$I \\rightarrow Y$",
    "#F0F9FF", "#7DD3FC", "#0369A1")
box(LX + 2.18, y1, 1.70, h1, "Surrogate", "MLP $f_\\theta(I)$",
    "#EEF2FF", "#A5B4FC", "#4338CA")
box(LX + 4.16, y1, 1.70, h1, "Training", "min MSE\n$\\|Y - \\hat{Y}\\|^2$",
    "#FEF2F2", "#FCA5A5", "#B91C1C")
arrow(LX + 1.92, y1 + h1 / 2, LX + 2.16, y1 + h1 / 2, "#0284C7")
arrow(LX + 3.90, y1 + h1 / 2, LX + 4.14, y1 + h1 / 2, "#4338CA")

# Phase 2: online inversion
ax.text(LX + 0.25, 2.12, "PHASE 2  Online inversion (Track 1)", fontsize=BADGE_FS,
        fontweight="bold", ha="left", va="center", color="#4338CA")
y2, h2 = 0.30, 1.52
box(LX + 0.20, y2, 1.45, h2, "Measure", "orbit\n$Y_{obs}$",
    "#F1F5F9", "#CBD5E1", "#334155")
box(LX + 1.93, y2, 2.45, h2, "Optimise (L-BFGS-B)",
    "$\\min_{\\Delta I}\\ \\|Y_{obs} + f_\\theta(\\Delta I)\\|^2$\n$|\\Delta I| \\leq 0.8$ A",
    "#F5F3FF", "#C4B5FD", "#6D28D9")
box(LX + 4.66, y2, 1.20, h2, "Apply", "$\\Delta I^{*}$ to\n6 correctors",
    "#ECFDF5", "#6EE7B7", "#047857")
arrow(LX + 1.67, y2 + h2 / 2, LX + 1.91, y2 + h2 / 2, "#475569")
arrow(LX + 4.40, y2 + h2 / 2, LX + 4.64, y2 + h2 / 2, "#6D28D9")

# ------------------------------------------------------------------------------
# Right panel: Paradigm 2 - Reinforcement Learning (Track 2)
# ------------------------------------------------------------------------------
RX, RW = 6.25, 6.05
card(RX, 0.10, RW, 4.40, "#F8FAFC", "#94A3B8", lw=1.5, radius=0.18)
badge(RX + 0.20, 4.18, 1.35, 0.36, "PARADIGM 2", "#16A34A", "#FFFFFF")
ax.text(RX + 1.70, 4.18, "Reinforcement Learning", fontsize=TITLE_FS,
        fontweight="bold", ha="left", va="center", color="#15803D")
ax.text(RX + 0.25, 3.72, "Closed loop: sense, act, learn (Track 2)", fontsize=BADGE_FS,
        fontweight="bold", ha="left", va="center", color="#15803D")

ax_x, ax_w = RX + 1.55, 3.0
box(ax_x, 2.42, ax_w, 1.08, "Policy agent $\\pi_\\phi$",
    "$\\Delta I = \\gamma(t)\\,[-\\alpha (R^T)^{+} Y + W Y + b]$",
    "#F0FDF4", "#86EFAC", "#166534")
box(ax_x, 0.62, ax_w, 1.08, "Beamline environment",
    "$Y = I R - 0.015\\, I^3 R + Y_0 + \\epsilon$",
    "#F1F5F9", "#CBD5E1", "#1E293B")

# action (down, right side) and state / reward (up, left side)
arrow(ax_x + ax_w - 0.45, 2.40, ax_x + ax_w - 0.45, 1.72, "#DC2626")
ax.text(ax_x + ax_w - 0.30, 2.06, "action\n$a_t = \\Delta I$", fontsize=NOTE_FS, fontweight="bold",
        ha="left", va="center", color="#B91C1C")
arrow(ax_x + 0.45, 1.72, ax_x + 0.45, 2.40, "#0284C7")
ax.text(ax_x + 0.30, 2.06, "state $s_t = Y$\nreward $r_t$", fontsize=NOTE_FS, fontweight="bold",
        ha="right", va="center", color="#0369A1")

ax.text(RX + RW / 2, 0.33, "$r_t = -\\mathrm{RMS} - 0.01\\,\\|\\Delta I\\| + 50$ on success",
        fontsize=NOTE_FS, ha="center", va="center", color="#475569")

save_path = "img/forward_sl_and_rl_schematic.png"
fig.savefig(save_path, dpi=300, facecolor="#FFFFFF")
plt.close(fig)
print(f"SUCCESS: Generated {save_path}")
