"""
scripts/generate_sl_rl_schematic.py
Generate publication-quality schematic comparing Forward Supervised Learning
(Surrogate Digital Twin & Inversion) vs. Reinforcement Learning (Closed-Loop Orbit Control).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig = plt.figure(figsize=(15.5, 8.5), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 15.5)
ax.set_ylim(0, 8.5)
ax.axis('off')

# Background canvas
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

# ------------------------------------------------------------------------------
# 1. Main Header Title & Subtitle
# ------------------------------------------------------------------------------
ax.text(7.75, 8.12, 'MACHINE LEARNING PARADIGMS IN PARTICLE ACCELERATOR CONTROL',
        fontsize=15, fontweight='bold', ha='center', va='center', color='#0F172A')
ax.text(7.75, 7.80, 'Forward Supervised Learning (Digital Twin Inversion) vs. Reinforcement Learning (Closed-Loop Adaptive Policy)',
        fontsize=10.5, ha='center', va='center', color='#475569')
ax.plot([1.5, 14.0], [7.55, 7.55], color='#CBD5E1', lw=1.2)

# Helper function to draw rounded boxes with soft fill and borders
def draw_card(ax, x, y, w, h, bg_color, border_color, radius=0.18, lw=1.5, linestyle='-'):
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=lw,
        linestyle=linestyle,
        zorder=1
    )
    ax.add_patch(card)
    return card

# Helper function to draw pills / badges
def draw_badge(ax, cx, cy, text, bg_color, text_color, fontsize=8.5, pad_w=0.65, pad_h=0.26):
    badge = patches.FancyBboxPatch(
        (cx - pad_w/2, cy - pad_h/2), pad_w, pad_h,
        boxstyle="round,pad=0,rounding_size=0.10",
        facecolor=bg_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(badge)
    ax.text(cx, cy, text, fontsize=fontsize, fontweight='bold',
            ha='center', va='center', color=text_color, zorder=4)

# ------------------------------------------------------------------------------
# 2. Left Panel: Forward Supervised Learning (Surrogate Modeling & Inversion)
# ------------------------------------------------------------------------------
# Left container card
draw_card(ax, 0.6, 0.45, 6.9, 6.85, '#F8FAFC', '#94A3B8', radius=0.25, lw=1.5)

# Panel Header
draw_badge(ax, 2.3, 7.05, 'PARADIGM 1', '#0284C7', '#FFFFFF', fontsize=9, pad_w=1.4, pad_h=0.32)
ax.text(4.3, 7.05, 'Forward Supervised Learning (Digital Twin)',
        fontsize=12, fontweight='bold', ha='left', va='center', color='#0369A1')
ax.text(4.05, 6.68, 'Offline dataset collection -> Neural Surrogate training -> Online model inversion',
        fontsize=8.5, ha='center', va='center', color='#64748B', style='italic')

# Sub-card 1: Offline Training
draw_card(ax, 0.9, 4.35, 6.3, 2.1, '#FFFFFF', '#BAE6FD', radius=0.15, lw=1.2)
draw_badge(ax, 2.2, 6.25, 'PHASE 1: OFFLINE TRAINING', '#E0F2FE', '#0369A1', fontsize=8, pad_w=2.3, pad_h=0.25)

# Elements in Phase 1
draw_card(ax, 1.1, 4.55, 1.4, 1.45, '#F0F9FF', '#7DD3FC', radius=0.12)
ax.text(1.8, 5.75, 'Simulation /\nExperiment', fontsize=8.5, fontweight='bold', ha='center', va='center', color='#0369A1')
ax.text(1.8, 5.0, 'Inputs: I in R^6\nTargets: Y in R^12\n(1,500 shots)', fontsize=7.5, ha='center', va='center', color='#475569')

# Arrow from Data to Model
ax.annotate('', xy=(2.9, 5.25), xytext=(2.5, 5.25),
            arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.8, shrinkA=0, shrinkB=0))

draw_card(ax, 2.9, 4.55, 2.1, 1.45, '#EEF2FF', '#A5B4FC', radius=0.12)
ax.text(3.95, 5.75, 'Neural Surrogate (MLP)', fontsize=8.5, fontweight='bold', ha='center', va='center', color='#4338CA')
ax.text(3.95, 5.15, 'f_theta(I): 128->64->32\nNon-linear ReLU\nCaptures B ~ I - 0.015*I^3', fontsize=7.2, ha='center', va='center', color='#334155')

# Arrow from Model to Loss
ax.annotate('', xy=(5.35, 5.25), xytext=(5.0, 5.25),
            arrowprops=dict(arrowstyle="->", color="#4338CA", lw=1.8, shrinkA=0, shrinkB=0))

draw_card(ax, 5.35, 4.55, 1.65, 1.45, '#FEF2F2', '#FECACA', radius=0.12)
ax.text(6.17, 5.75, 'Supervised Loss', fontsize=8.5, fontweight='bold', ha='center', va='center', color='#B91C1C')
ax.text(6.17, 5.05, 'L_MSE = ||Y - Y_hat||^2\nBackprop (Adam)\nTarget RMSE < 0.015mm', fontsize=7.2, ha='center', va='center', color='#475569')

# Sub-card 2: Online Inversion for Control
draw_card(ax, 0.9, 0.65, 6.3, 3.45, '#FFFFFF', '#C7D2FE', radius=0.15, lw=1.2)
draw_badge(ax, 2.45, 3.88, 'PHASE 2: ONLINE SURROGATE INVERSION (TRACK 1)', '#EEF2FF', '#4338CA', fontsize=8, pad_w=2.8, pad_h=0.25)

# Step-by-step inversion workflow
draw_card(ax, 1.1, 2.35, 1.6, 1.25, '#F1F5F9', '#CBD5E1', radius=0.10)
ax.text(1.9, 3.25, 'Current State', fontsize=8.2, fontweight='bold', ha='center', va='center', color='#334155')
ax.text(1.9, 2.75, 'BPM Offset Y_obs\n(Residual Orbit)', fontsize=7.5, ha='center', va='center', color='#64748B')

# Arrow from State to Optimizer
ax.annotate('', xy=(3.1, 2.95), xytext=(2.7, 2.95),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.8, shrinkA=0, shrinkB=0))

draw_card(ax, 3.1, 2.15, 2.3, 1.5, '#F5F3FF', '#C4B5FD', radius=0.10)
ax.text(4.25, 3.35, 'SciPy Optimizer (L-BFGS-B)', fontsize=8.2, fontweight='bold', ha='center', va='center', color='#6D28D9')
ax.text(4.25, 2.75, 'min_dI ||Y_obs + f_theta(dI)||^2\n+ lambda * ||dI||^2\nBounds: [-0.8, 0.8] A', fontsize=7.2, ha='center', va='center', color='#475569')

# Arrow from Optimizer to Actuators
ax.annotate('', xy=(5.8, 2.95), xytext=(5.4, 2.95),
            arrowprops=dict(arrowstyle="->", color="#6D28D9", lw=1.8, shrinkA=0, shrinkB=0))

draw_card(ax, 5.8, 2.35, 1.2, 1.25, '#ECFDF5', '#6EE7B7', radius=0.10)
ax.text(6.4, 3.25, 'Actuator Kick', fontsize=8.2, fontweight='bold', ha='center', va='center', color='#047857')
ax.text(6.4, 2.75, 'Optimal dI*\nApplied to 6\nCorrectors', fontsize=7.2, ha='center', va='center', color='#065F46')

# Bottom Key Characteristics Box for SL
draw_card(ax, 1.1, 0.85, 5.9, 1.05, '#F8FAFC', '#E2E8F0', radius=0.08)
ax.text(4.05, 1.62, 'KEY CHARACTERISTICS & STRENGTHS:', fontsize=7.8, fontweight='bold', ha='center', va='center', color='#0F172A')
ax.text(4.05, 1.20, '* Fast convergence (often reaches RMS < 0.03mm in 2-3 control steps).\n* Stable & robust because surrogate is strictly bounded and pre-trained.\n* Latency: ~15-30 ms per step (numerical optimization loop).',
        fontsize=7.2, ha='center', va='center', color='#334155')


# ------------------------------------------------------------------------------
# 3. Right Panel: Reinforcement Learning (Closed-Loop Policy Control)
# ------------------------------------------------------------------------------
# Right container card
draw_card(ax, 8.0, 0.45, 6.9, 6.85, '#F8FAFC', '#94A3B8', radius=0.25, lw=1.5)

# Panel Header
draw_badge(ax, 9.7, 7.05, 'PARADIGM 2', '#16A34A', '#FFFFFF', fontsize=9, pad_w=1.4, pad_h=0.32)
ax.text(11.7, 7.05, 'Reinforcement Learning (Closed-Loop Agent)',
        fontsize=12, fontweight='bold', ha='left', va='center', color='#15803D')
ax.text(11.45, 6.68, 'Interactive trial-and-error policy -> Direct sensing & action -> Reward maximization',
        fontsize=8.5, ha='center', va='center', color='#64748B', style='italic')

# Sub-card: Closed-Loop Agent-Environment Interaction
draw_card(ax, 8.3, 2.2, 6.3, 4.25, '#FFFFFF', '#BBF7D0', radius=0.15, lw=1.2)
draw_badge(ax, 9.9, 6.25, 'CLOSED-LOOP INTERACTIVE MDP (TRACK 2)', '#DCFCE7', '#15803D', fontsize=8, pad_w=3.0, pad_h=0.25)

# Agent Box (Top)
draw_card(ax, 9.4, 4.35, 4.1, 1.65, '#F0FDF4', '#86EFAC', radius=0.14, lw=1.4)
ax.text(11.45, 5.72, 'RL Policy Agent pi_phi(a | s)', fontsize=9.5, fontweight='bold', ha='center', va='center', color='#166534')
ax.text(11.45, 5.12, 'Action dI_t = gamma(t) * [ -alpha * (R^T)+ Y_t + W_tune Y_t + b ]',
        fontsize=7.5, fontweight='bold', ha='center', va='center', color='#0F172A')
ax.text(11.45, 4.62, 'Physics-informed prior (SVD) + Learned residual + Dynamic damping',
        fontsize=7.2, ha='center', va='center', color='#15803D')

# Environment Box (Bottom)
draw_card(ax, 9.4, 2.5, 4.1, 1.35, '#F1F5F9', '#CBD5E1', radius=0.14, lw=1.4)
ax.text(11.45, 3.52, 'Gymnasium Environment (Accelerator Beamline)', fontsize=9, fontweight='bold', ha='center', va='center', color='#1E293B')
ax.text(11.45, 2.95, 'Lattice Transport: Y = I*R - 0.015*(I^3*R) + Y_0 + epsilon\nState: Y in [-10, 10]^12 mm | Bounds: [-0.8, 0.8] A',
        fontsize=7.2, ha='center', va='center', color='#475569')

# Feedback Loops (Action Arrow Down, State/Reward Arrow Up)
# Action arrow: Agent -> Environment
ax.annotate('', xy=(12.8, 3.9), xytext=(12.8, 4.3),
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.2, shrinkA=0, shrinkB=0))
ax.text(13.6, 4.1, 'Action a_t = dI_t\n(Corrector Kicks)', fontsize=7.5, fontweight='bold', ha='center', va='center', color='#B91C1C')

# State & Reward arrow: Environment -> Agent
ax.annotate('', xy=(10.0, 4.3), xytext=(10.0, 3.9),
            arrowprops=dict(arrowstyle="->", color="#0284C7", lw=2.2, shrinkA=0, shrinkB=0))
ax.text(9.0, 4.1, 'State s_t = Y_t (BPMs)\nReward r_t (Scalar)', fontsize=7.5, fontweight='bold', ha='center', va='center', color='#0369A1')

# Bottom Key Characteristics Box for RL
draw_card(ax, 8.3, 0.65, 6.3, 1.35, '#FFFFFF', '#E2E8F0', radius=0.10)
ax.text(11.45, 1.75, 'REWARD SIGNAL & BENCHMARK DYNAMICS:', fontsize=7.8, fontweight='bold', ha='center', va='center', color='#0F172A')
ax.text(11.45, 1.15, '* r_t = - w_rms*RMS - w_act*||dI||^2 - c_step + (Bonus if RMS < 0.03mm)\n* Ultra-low latency: ~0.2 ms per step (direct matrix-vector policy evaluation).\n* Dynamic damping gamma(t) prevents noise amplification near 0.030 mm target boundary.',
        fontsize=7.2, ha='center', va='center', color='#334155')

# ------------------------------------------------------------------------------
# 4. Save Image
# ------------------------------------------------------------------------------
save_path = "img/forward_sl_and_rl_schematic.png"
fig.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
plt.close(fig)
print(f"SUCCESS: Generated {save_path}")
