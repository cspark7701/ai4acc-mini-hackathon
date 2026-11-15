"""
scripts/generate_sl_rl_schematic.py
Generate the three-panel schematic of the learning paradigms used in the challenge:
Paradigm 1, supervised surrogate with online inversion (Track 1); Paradigm 2,
reinforcement learning (Track 2); Paradigm 3, Bayesian optimization with a Gaussian
process (Track 3), including the optional online GP refit.

The figure is drawn at roughly the size it appears on the Lecture 1 slide
(12.4 x 4.6 in), so the font sizes below are close to the sizes the audience sees.
Keep the text short when editing: each panel is only 4 in wide.

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

def setup(W=12.4, H=4.6):
    fig = plt.figure(figsize=(W, H), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")
    return fig, ax

def card(ax, x, y, w, h, fill, edge, lw=1.4, radius=0.12, ls="-"):
    ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=1))

def badge(ax, x, y, w, h, text, fill, color, fs=10.5):
    ax.add_patch(patches.FancyBboxPatch((x, y - h/2), w, h, boxstyle="round,pad=0,rounding_size=0.07",
        facecolor=fill, edgecolor="none", zorder=3))
    ax.text(x + w/2, y, text, fontsize=fs, fontweight="bold", ha="center", va="center", color=color, zorder=4)

def box(ax, x, y, w, h, title, body, fill, edge, tcolor, bcolor="#334155", tfs=12, bfs=11, title_off=0.27):
    card(ax, x, y, w, h, fill, edge, lw=1.6, radius=0.09)
    ax.text(x + w/2, y + h - title_off, title, fontsize=tfs, fontweight="bold", ha="center", va="center", color=tcolor, zorder=4)
    ax.text(x + w/2, y + (h - title_off - 0.18)/2, body, fontsize=bfs, ha="center", va="center", color=bcolor, zorder=4, linespacing=1.35)

def arrow(ax, x0, y0, x1, y1, color, ls="-", rad=0.0, lw=2.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=16,
        linestyle=ls, connectionstyle=f"arc3,rad={rad}"), zorder=5)


fig, ax = setup()
TITLE, BADGE, NOTE, TFS, BFS = 13, 9.5, 10, 11.5, 10.5
PW, GAP = 4.0, 0.10
def panel(i, color, tcolor, title, sub):
    x = 0.10 + i * (PW + GAP)
    card(ax, x, 0.10, PW, 4.40, "#F8FAFC", "#94A3B8", lw=1.5, radius=0.18)
    badge(ax, x + 0.18, 4.18, 1.25, 0.34, f"PARADIGM {i+1}", color, "#FFFFFF", fs=BADGE)
    ax.text(x + 1.55, 4.18, title, fontsize=TITLE, fontweight="bold", ha="left", va="center", color=tcolor)
    ax.text(x + 0.20, 3.75, sub, fontsize=BADGE, fontweight="bold", ha="left", va="center", color=tcolor)
    return x
def stack(x, items, right=0.25):
    """Vertical chain of boxes with down arrows."""
    top, gap = 3.50, 0.22
    h = (top - 0.25 - gap * (len(items) - 1)) / len(items)
    for k, (t, b, fill, edge, tc) in enumerate(items):
        y = top - (k + 1) * h - k * gap
        bw = PW - 0.25 - right
        box(ax, x + 0.25, y, bw, h, t, b, fill, edge, tc, tfs=TFS, bfs=BFS, title_off=0.22)
        if k:
            arrow(ax, x + 0.25 + bw/2, y + h + gap - 0.01, x + 0.25 + bw/2, y + h + 0.01, "#64748B", lw=1.8)
    return h
# panel 1: supervised (Track 1)
x1 = panel(0, "#0284C7", "#0369A1", "Supervised", "Offline MLP + online inversion (Track 1)")
stack(x1, [("Train offline", "MLP $f_\\theta(I)$ on 1,500 shots", "#EEF2FF", "#A5B4FC", "#4338CA"),
           ("Measure", "orbit $Y_{obs}$", "#F1F5F9", "#CBD5E1", "#334155"),
           ("Optimize (L-BFGS-B)", "$\\min_{\\Delta I}\\ \\|Y_{obs} + f_\\theta(\\Delta I)\\|^2$", "#F5F3FF", "#C4B5FD", "#6D28D9")])
# panel 2: RL (Track 2)
x2 = panel(1, "#16A34A", "#15803D", "Reinforcement", "Learns by interacting (Track 2)")
bw = PW - 0.50
box(ax, x2 + 0.25, 2.30, bw, 1.15, "Policy agent $\\pi_\\phi$", "$\\Delta I = \\gamma(t)[-\\alpha (R^T)^{+}Y$\n$+\\, W Y + b]$", "#F0FDF4", "#86EFAC", "#166534", tfs=TFS, bfs=BFS, title_off=0.22)
box(ax, x2 + 0.25, 0.55, bw, 1.05, "Beamline", "$Y = IR - 0.015\\,I^3R + Y_0 + \\epsilon$", "#F1F5F9", "#CBD5E1", "#1E293B", tfs=TFS, bfs=BFS, title_off=0.22)
arrow(ax, x2 + PW - 0.85, 2.28, x2 + PW - 0.85, 1.62, "#DC2626")
ax.text(x2 + PW - 0.75, 1.95, "action\n$\\Delta I$", fontsize=NOTE, fontweight="bold", ha="left", va="center", color="#B91C1C")
arrow(ax, x2 + 0.85, 1.62, x2 + 0.85, 2.28, "#0284C7")
ax.text(x2 + 0.75, 1.95, "state $Y$\nreward $r$", fontsize=NOTE, fontweight="bold", ha="right", va="center", color="#0369A1")
ax.text(x2 + PW/2, 0.30, "$r = -\\mathrm{RMS} - 0.01\\|\\Delta I\\| + 50$ on success", fontsize=9.5, ha="center", va="center", color="#475569")
# panel 3: Bayesian optimization (Track 3)
x3 = panel(2, "#7C3AED", "#6D28D9", "Bayesian Opt.", "GP model + uncertainty (Track 3)")
h = stack(x3, [("Fit GP offline", "$\\mu(I) \\pm \\sigma(I)$ on ~300 shots", "#F5F3FF", "#C4B5FD", "#6D28D9"),
               ("Measure", "orbit $Y_{obs}$", "#F1F5F9", "#CBD5E1", "#334155"),
               ("Minimize LCB", "$\\mathrm{RMS}(Y_{obs} + \\mu) - \\kappa\\,\\bar{\\sigma} + \\lambda\\|\\Delta I\\|^2$", "#FEF2F2", "#FCA5A5", "#B91C1C")], right=0.62)
# dashed refit loop on the right edge: from the LCB box back to the GP box
arrow(ax, x3 + PW - 0.48, 0.25 + h/2, x3 + PW - 0.48, 3.50 - h/2, "#7C3AED", ls="--", rad=0.0, lw=1.5)
ax.text(x3 + PW - 0.22, 1.84, "optional refit = online BO", fontsize=9.5, fontweight="bold", ha="center", va="center", color="#7C3AED", style="italic", rotation=90)
save_path = "img/forward_sl_and_rl_schematic.png"
fig.savefig(save_path, dpi=300, facecolor="#FFFFFF")
plt.close(fig)
print(f"SUCCESS: Generated {save_path}")
