"""Build the editable PPTX presentation for Lecture 1.

AI Applications in Accelerators Tutorial & Mini-Hackathon
Lecture 1: AI/ML Foundations and Closed-Loop Control for Particle Accelerators
Author: Chong Shik Park, Ph.D. (Korea University, Sejong)
Date: November 3, 2026

Usage:
    python scripts/build_lecture_1_pptx.py [output.pptx]
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img"
KU_LOGO = IMG_DIR / "ku_logo.png"
OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "presentations" / "Lecture_1_AI_ML_Foundations_and_Control.pptx"

# Color Palette
NAVY = RGBColor(0, 32, 96)          # Primary Deep Navy (#002060)
PRIMARY = RGBColor(24, 76, 120)     # Primary Blue (#184C78)
ACCENT = RGBColor(41, 128, 185)     # Secondary Accent Blue (#2980B9)
DARK_GRAY = RGBColor(44, 62, 80)    # Text Dark Gray (#2C3E50)
LIGHT_BG = RGBColor(245, 247, 250)  # Shaded Card (#F5F7FA)
BORDER_GRAY = RGBColor(200, 205, 210) # Border Outline
MUTED = RGBColor(127, 140, 141)     # Muted text (#7F8C8D)
WHITE = RGBColor(255, 255, 255)
CRIMSON = RGBColor(158, 22, 54)     # Highlight Red (#9E1636)
SUCCESS_GREEN = RGBColor(39, 174, 96) # Green (#27AE60)
GOLD = RGBColor(180, 140, 20)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def add_text_run(paragraph, text, bold=False, size=None, color=None):
    """Helper to add a formatted run to a python-pptx paragraph."""
    run = paragraph.add_run()
    run.text = text
    run.font.bold = bold
    if size is not None:
        run.font.size = size
    if color is not None:
        run.font.color.rgb = color
    return run


def create_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6] # blank layout

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # KU Logo
        if KU_LOGO.exists():
            slide.shapes.add_picture(str(KU_LOGO), Inches(0.4), Inches(0.2), width=Inches(0.9))

        # Vertical Divider Bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.4), Inches(0.25), Inches(0.06), Inches(0.95))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT

        # Title & Subtitle Box
        tb = slide.shapes.add_textbox(Inches(1.55), Inches(0.18), Inches(11.3), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category Tag & Title
        p0 = tf.paragraphs[0]
        if tag_text:
            add_text_run(p0, tag_text.upper() + "  |  ", bold=True, size=Pt(11), color=ACCENT)
        add_text_run(p0, title_text, bold=True, size=Pt(22), color=NAVY)

        if subtitle_text:
            p1 = tf.add_paragraph()
            add_text_run(p1, subtitle_text, size=Pt(13), color=DARK_GRAY)

    def add_footer(slide, slide_num):
        # Footer dividing line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(7.0), Inches(12.533), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.color.rgb = BORDER_GRAY

        # Left date
        tb_left = slide.shapes.add_textbox(Inches(0.4), Inches(7.05), Inches(2.5), Inches(0.35))
        tf_l = tb_left.text_frame
        add_text_run(tf_l.paragraphs[0], "November 3, 2026", size=Pt(10), color=MUTED)

        # Center citation
        tb_center = slide.shapes.add_textbox(Inches(3.0), Inches(7.05), Inches(7.333), Inches(0.35))
        tf_c = tb_center.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        add_text_run(p_c, "Chong Shik Park, Ph.D.  |  Korea University, Sejong  |  AI Applications in Accelerators", size=Pt(10), color=MUTED)

        # Right slide number
        tb_right = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.4), Inches(0.35))
        tf_r = tb_right.text_frame
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        add_text_run(p_r, f"{slide_num}", bold=True, size=Pt(10), color=PRIMARY)

    def add_card(slide, left, top, width, height, title="", bg_color=LIGHT_BG, border_color=BORDER_GRAY):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            add_text_run(tf.paragraphs[0], title, bold=True, size=Pt(13.5), color=NAVY)
        return shape

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.8))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY
    banner.line.fill.background()

    if KU_LOGO.exists():
        s1.shapes.add_picture(str(KU_LOGO), Inches(0.8), Inches(0.35), width=Inches(1.2))

    tb_tag = s1.shapes.add_textbox(Inches(2.3), Inches(0.5), Inches(10.0), Inches(0.8))
    tf_tag = tb_tag.text_frame
    add_text_run(tf_tag.paragraphs[0], "AI APPLICATIONS IN ACCELERATORS TUTORIAL & MINI-HACKATHON  |  KOMAC / KAERI", bold=True, size=Pt(14), color=WHITE)

    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(2.4))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    add_text_run(tf_title.paragraphs[0], "Lecture 1: AI/ML Foundations and Closed-Loop Control\nfor Particle Accelerators", bold=True, size=Pt(30), color=PRIMARY)

    p2_t = tf_title.add_paragraph()
    p2_t.space_before = Pt(10)
    add_text_run(p2_t, "Physics Foundations, Neural Surrogates, Reinforcement Learning, and Bayesian Optimization", size=Pt(17), color=DARK_GRAY)

    add_card(s1, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.0), bg_color=LIGHT_BG)
    tb_auth = s1.shapes.add_textbox(Inches(1.0), Inches(4.85), Inches(11.3), Inches(1.7))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True

    add_text_run(tf_auth.paragraphs[0], "Chong Shik Park, Ph.D.", bold=True, size=Pt(18), color=NAVY)

    p_a2 = tf_auth.add_paragraph()
    p_a2.space_before = Pt(4)
    add_text_run(p_a2, "• Department of Accelerator Science, Korea University, Sejong 30019, Republic of Korea\n• Center for Accelerator Research, Korea University, Sejong 30019, Republic of Korea", size=Pt(12), color=DARK_GRAY)

    p_a3 = tf_auth.add_paragraph()
    p_a3.space_before = Pt(6)
    add_text_run(p_a3, "Date: November 3, 2026   |   Target: Accelerator Physicists, Postdocs, Engineers & Graduate Students", size=Pt(11), color=MUTED)

    add_footer(s1, 1)

    # ==========================================
    # SLIDE 2: Curricular Architecture & Overview
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Workshop Curriculum", "Integrated Morning Lectures & Afternoon Hackathon", 
               "Bridging theoretical foundations directly with closed-loop simulation and live W&B tracking")

    c_w = Inches(3.9)
    top_pos = Inches(1.5)
    h_pos = Inches(5.2)

    # Card 1: Lecture 1
    add_card(s2, Inches(0.6), top_pos, c_w, h_pos, "Lecture 1 (09:10 - 10:30)", bg_color=LIGHT_BG)
    tb_c1 = s2.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.6), c_w - Inches(0.4), h_pos - Inches(0.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    add_text_run(p, "Instructor: Chong Shik Park, Ph.D.\n\n", bold=True, color=NAVY)
    add_text_run(p, "• Physics Foundations & Hill's Equation\n"
                    "• Orbit Response Matrix (ORM) Coupling\n"
                    "• Magnetic Core Cubic Saturation\n"
                    "• Neural Surrogate Digital Twins (MLP)\n"
                    "• SVD Pseudo-Inverse vs Bounded Inversion\n"
                    "• Physics-Informed RL & Dynamic Damping\n"
                    "• Gaussian Process Bayesian Optimization\n\n", size=Pt(11), color=DARK_GRAY)
    add_text_run(p, "Target: Sub-micron closed-loop control under non-linear actuator constraints.", bold=True, size=Pt(10), color=PRIMARY)

    # Card 2: Lecture 2
    add_card(s2, Inches(4.7), top_pos, c_w, h_pos, "Lecture 2 (10:40 - 12:00)", bg_color=LIGHT_BG)
    tb_c2 = s2.shapes.add_textbox(Inches(4.9), top_pos + Inches(0.6), c_w - Inches(0.4), h_pos - Inches(0.8))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    add_text_run(p, "Instructor: Thorsten Hellert, Ph.D.\n\n", bold=True, color=NAVY)
    add_text_run(p, "• Agentic AI Frameworks in Accelerators\n"
                    "• Large Language Model (LLM) Agents\n"
                    "• Osprey Autonomous Control System\n"
                    "• Automated Scientific Workflows\n"
                    "• Python API Tool Calling Architecture\n"
                    "• Operational Guardrails & Safety Bounds\n"
                    "• Human-in-the-Loop Supervision\n\n", size=Pt(11), color=DARK_GRAY)
    add_text_run(p, "Target: Autonomous tuning agents and scientific workflow orchestration.", bold=True, size=Pt(10), color=PRIMARY)

    # Card 3: Hackathon
    add_card(s2, Inches(8.8), top_pos, c_w, h_pos, "Mini-Hackathon (13:30 - 17:00)", bg_color=LIGHT_BG)
    tb_c3 = s2.shapes.add_textbox(Inches(9.0), top_pos + Inches(0.6), c_w - Inches(0.4), h_pos - Inches(0.8))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    add_text_run(p, "Hands-On Orbit Alignment Challenge\n\n", bold=True, color=NAVY)
    add_text_run(p, "• 15-meter Transport Lattice (12 BPMs, 6 Steerers)\n"
                    "• 3 Parallel Tracks (MLP, RL, BO)\n"
                    "• Standardized 30-Seed Evaluation Suite\n"
                    "• Sub-30 μm Convergence Target\n"
                    "• Real-time Weights & Biases (W&B) Logging\n"
                    "• Live Global Leaderboard Tracking\n"
                    "• Final Awards & Recognition\n\n", size=Pt(11), color=DARK_GRAY)
    add_text_run(p, "Target: > 1,000 points on standardized evaluation suite.", bold=True, size=Pt(10), color=PRIMARY)

    add_footer(s2, 2)

    # ==========================================
    # SLIDE 3: 5 Pillars of AI in Accelerators
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Domain Overview", "Five Foundational Pillars of AI in Modern Accelerators",
               "How artificial intelligence transforms design, commissioning, and autonomous operations")

    pillars = [
        ("1. Neural Surrogate Digital Twins", 
         "• Replaces slow tracking codes (ELEGANT, MAD-X) with sub-ms deep neural surrogates.\n• Enables real-time model-predictive control, online orbit feedback, and virtual parametric sensitivity analysis."),
        ("2. Multi-Objective Bayesian Optimization", 
         "• Balances trade-offs: beam transmission vs photon brightness vs transverse emittance.\n• Gaussian Processes with acquisition functions find Pareto-optimal set in dozens of shots instead of thousands."),
        ("3. Virtual Diagnostics & Phase Space", 
         "• Reconstructs destructive beam metrics (6D phase space, bunch slice emittance) non-invasively.\n• Neural networks predict shot-by-shot profiles from upstream RF cavities and BPM telemetry."),
        ("4. Anomaly Detection & Machine Protection", 
         "• Unsupervised models monitor sensor drift to prevent multi-megawatt beam downtime.\n• Deep sequence models predict RF breakdown and cavity quenches milliseconds before catastrophic trips."),
        ("5. Agentic AI & Autonomous Operations", 
         "• Integrates LLM reasoning engines with accelerator APIs and diagnostic archives (e.g. Osprey).\n• Executes high-level operational commands safely within strict hardware interlock boundaries.")
    ]

    p_w = Inches(12.1)
    p_h = Inches(0.92)
    start_y = Inches(1.5)

    for i, (title, desc) in enumerate(pillars):
        y = start_y + Inches(i * 1.05)
        add_card(s3, Inches(0.6), y, p_w, p_h, title, bg_color=LIGHT_BG)
        tb = s3.shapes.add_textbox(Inches(0.8), y + Inches(0.35), p_w - Inches(0.4), Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        add_text_run(tf.paragraphs[0], desc, size=Pt(10.5), color=DARK_GRAY)

    add_footer(s3, 3)

    # ==========================================
    # SLIDE 4: Beam Physics & Hill's Equation
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Physics Foundations", "Transverse Beam Dynamics & Hill's Equation",
               "Theoretical governing equation shaping betatron oscillations in linear magnetic lattices")

    add_card(s4, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Hill's Equation Formulation")
    tb_h = s4.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p = tf_h.paragraphs[0]
    add_text_run(p, "Transverse motion along coordinate s in uncoupled lattice:\n\n", size=Pt(11))
    add_text_run(p, "d²x(s)/ds² + K(s) x(s) = 0\n\n", bold=True, size=Pt(14), color=PRIMARY)
    add_text_run(p, "• K(s) = (e/p) · (∂By/∂x) represents alternating quadrupole focusing strength (K > 0 for QF, K < 0 for QD).\n\n"
                    "• General solution is a pseudo-harmonic betatron oscillation:\n", size=Pt(11), color=DARK_GRAY)
    add_text_run(p, "x(s) = √[ε · β(s)] · cos(ψ(s) + φ₀)\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "• β(s): Courant-Snyder beta function (beam envelope)\n"
                    "• ψ(s) = ∫ ds / β(s): Betatron phase advance\n"
                    "• ν = (1/2π) ∮ ds / β(s): Betatron tune (total phase advance)", size=Pt(11), color=DARK_GRAY)

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "The Operational Challenge: Hadron Linacs & Rings")
    tb_r = s4.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    add_text_run(p, "Sub-Micron Stability Tolerances:\n\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "• Modern light sources require orbit stabilization to < 10% of beam size (sub-micron RMS tolerances).\n\n"
                    "• In multi-megawatt hadron linacs (e.g. KOMAC, SNS, ESS):\n"
                    "  - Offsets in quadrupoles/cavities induce non-linear space charge forces and halo.\n"
                    "  - Losses exceeding 1 W/m (10⁻⁵ of total current) cause severe structural radioactivation.\n"
                    "  - Hands-on maintenance is prohibited if orbit deviations remain uncorrected.\n\n"
                    "• Physical Disturbance Mechanisms:\n"
                    "  - Ground motion and mechanical vibrations (pumps, cryocoolers)\n"
                    "  - Thermal girder expansion and diurnal temperature cycles\n"
                    "  - Power supply current ripple and magnet hysteresis", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s4, 4)

    # ==========================================
    # SLIDE 5: Orbit Response Matrix (ORM)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Analytical Optics", "Derivation of the Orbit Response Matrix (ORM)",
               "Mathematical link connecting steerer deflections to downstream diagnostic readings")

    add_card(s5, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Theoretical ORM Derivation")
    tb_orm = s5.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_orm = tb_orm.text_frame
    tf_orm.word_wrap = True
    p = tf_orm.paragraphs[0]
    add_text_run(p, "Localized angular deflection (kick) θj applied by steerer j:\n\n", size=Pt(11))
    add_text_run(p, "R_ij = Δx(s_i) / θ_j\n"
                    "     = [√(β_i β_j) / (2 sin(π ν))] · cos(|ψ_i - ψ_j| - π ν)\n\n", bold=True, size=Pt(12), color=PRIMARY)
    add_text_run(p, "Linear Response Formulation:\n", bold=True, size=Pt(11))
    add_text_run(p, "Y_linear = I · R\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "• I ∈ ℝ⁶: Vector of 6 corrector currents (Amperes)\n"
                    "• R ∈ ℝ⁶ˣ¹²: Linear Orbit Response Matrix\n"
                    "• Y ∈ ℝ¹²: Transverse displacements measured at 12 BPMs\n\n"
                    "Coupling Mechanism:\n"
                    "Deflecting a single steerer perturbs the entire downstream trajectory through betatron phase advance.", size=Pt(10.5), color=DARK_GRAY)

    add_card(s5, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Why Pure Linear Inversion Breaks Down")
    tb_fail = s5.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_fail = tb_fail.text_frame
    tf_fail.word_wrap = True
    p = tf_fail.paragraphs[0]
    add_text_run(p, "Classical Singular Value Decomposition (SVD):\n\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "ΔI = - α · (Rᵀ)⁺ · Y\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "Key Vulnerabilities in Real Operations:\n\n"
                    "1. Magnetic Core Saturation:\n"
                    "   High coil currents drive yoke iron into non-linear saturation. The true response departs significantly from R.\n\n"
                    "2. Limit Cycles & Overshoot:\n"
                    "   High static feedback gains (α > 0.5) cause severe overshoot and persistent oscillatory limit cycles.\n\n"
                    "3. Diagnostic Sensor Noise:\n"
                    "   Sensor jitter (σ = 10 μm) is inverted as false physical errors, commanding unnecessary actuator kicks.", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s5, 5)

    # ==========================================
    # SLIDE 6: Transport Lattice Geometry (With Diagram)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Hackathon Benchmark", "The 15-Meter Transport Lattice Architecture",
               "Layout of quadrupole doublets, dipole steering magnets, and beam position monitors")

    beamline_img = IMG_DIR / "beamline.png"
    if beamline_img.exists():
        s6.shapes.add_picture(str(beamline_img), Inches(0.6), Inches(1.5), width=Inches(12.1))

    c_w2 = Inches(5.9)
    top_y = Inches(4.7)
    h_y = Inches(2.0)

    add_card(s6, Inches(0.6), top_y, c_w2, h_y, "Diagnostics & Actuators", bg_color=LIGHT_BG)
    tb_da = s6.shapes.add_textbox(Inches(0.8), top_y + Inches(0.4), c_w2 - Inches(0.4), h_y - Inches(0.5))
    tf_da = tb_da.text_frame
    tf_da.word_wrap = True
    add_text_run(tf_da.paragraphs[0], 
                 "• 12 Diagnostic BPMs: Evenly spaced from s = 1.0 m to s = 15.0 m\n"
                 "• 6 Dipole Steering Magnets: 3 Horizontal (HCM1-3) & 3 Vertical (VCM1-3)\n"
                 "• Quadrupole Doublets: Alternating QF & QD magnets shaping transverse beta", 
                 size=Pt(11), color=DARK_GRAY)

    add_card(s6, Inches(6.8), top_y, c_w2, h_y, "Hardware Constraints", bg_color=LIGHT_BG)
    tb_hc = s6.shapes.add_textbox(Inches(7.0), top_y + Inches(0.4), c_w2 - Inches(0.4), h_y - Inches(0.5))
    tf_hc = tb_hc.text_frame
    tf_hc.word_wrap = True
    add_text_run(tf_hc.paragraphs[0], 
                 "• Cumulative Current Bounds: I ∈ [-5.0 A, +5.0 A] (Power supply thermal limit)\n"
                 "• Single-Step Delta Bounds: ΔI ∈ [-0.8 A, +0.8 A] (Rate of change limit)\n"
                 "• Sensor Noise Floor: Gaussian jitter ε ~ 𝒩(0, 0.010² mm) (10 μm RMS)", 
                 size=Pt(11), color=DARK_GRAY)

    add_footer(s6, 6)

    # ==========================================
    # SLIDE 7: Non-Linear Saturation & Imperfections
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Physical Realism", "Non-Linear Magnetic Saturation & Misalignments",
               "Modeling realistic iron-core saturation and random quadrupole alignment errors")

    add_card(s7, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Mathematical Response Formulation")
    tb_form = s7.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_form = tb_form.text_frame
    tf_form.word_wrap = True
    p = tf_form.paragraphs[0]
    add_text_run(p, "Physical Beam Position Monitor Reading Y:\n\n", size=Pt(11))
    add_text_run(p, "Y = I · R - 0.015 · (I³ · R) + Y₀ + ε\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "Components Breakdown:\n\n"
                    "1. I · R: Pure linear betatron response\n\n"
                    "2. -0.015 · (I³ · R): Non-linear iron core soft saturation\n"
                    "   - At I = 2.0 A: 6% drop in effective steerer authority\n"
                    "   - At I = 4.0 A: 24% authority loss (linear model severely overshoots)\n\n"
                    "3. Y₀: Initial orbit distortion from misaligned quadrupoles\n\n"
                    "4. ε ~ 𝒩(0, 0.010² mm): BPM Gaussian sensor noise (10 μm)", size=Pt(10.5), color=DARK_GRAY)

    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Initial Distortion & Noise Profiles")
    tb_dist = s7.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_dist = tb_dist.text_frame
    tf_dist.word_wrap = True
    p = tf_dist.paragraphs[0]
    add_text_run(p, "Initial Distortion Generation (Y₀):\n\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "Quadrupole misalignments induce harmonic betatron waves:\n\n"
                    "Y₀,k = A₁ sin(2π s_k / λ₁ + φ₁) + A₂ cos(2π s_k / λ₂ + φ₂)\n\n", bold=True, size=Pt(12), color=PRIMARY)
    add_text_run(p, "• Produces realistic initial RMS orbit errors between 0.40 mm and 1.10 mm across seeds.\n\n"
                    "The Benchmark Convergence Target:\n\n", size=Pt(11), color=DARK_GRAY)
    add_text_run(p, "Target RMS: < 0.030 mm (30 μm)\n\n", bold=True, size=Pt(14), color=SUCCESS_GREEN)
    add_text_run(p, "To achieve success, policies must reduce initial orbit distortion by 93% to 97% within a strict budget of 20 control steps.", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s7, 7)

    # ==========================================
    # SLIDE 8: Machine Learning Fundamentals
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "ML Core Theory", "Deep Neural Networks & Supervised Learning Foundations",
               "Architectural principles of artificial neurons, non-linear activations, and loss optimization")

    add_card(s8, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Anatomy of an Artificial Neural Network")
    tb_ann = s8.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_ann = tb_ann.text_frame
    tf_ann.word_wrap = True
    p = tf_ann.paragraphs[0]
    add_text_run(p, "Artificial Neuron Transformation:\n", size=Pt(11))
    add_text_run(p, "z = ∑ w_j x_j + b = wᵀ x + b\n"
                    "a = σ(z)\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "Multi-Layer Perceptron (MLP):\n"
                    "Chaining L affine transformations with element-wise non-linear activations:\n\n"
                    "h⁽ˡ⁾ = σ(W⁽ˡ⁾ h⁽ˡ⁻¹⁾ + b⁽ˡ⁾)\n\n"
                    "Activation Function: Rectified Linear Unit (ReLU)\n"
                    "σ(z) = max(0, z)\n"
                    "• Constant gradient = 1 for z > 0 (prevents vanishing gradients)\n"
                    "• Computationally efficient; introduces piecewise linearity", size=Pt(10.5), color=DARK_GRAY)

    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Loss Formulation & Adam Optimizer")
    tb_opt = s8.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_opt = tb_opt.text_frame
    tf_opt.word_wrap = True
    p = tf_opt.paragraphs[0]
    add_text_run(p, "Objective Function (Mean Squared Error + L2 Penalty):\n\n", bold=True, size=Pt(11), color=NAVY)
    add_text_run(p, "ℒ(θ) = (1/N) ∑ ||y_true - f_θ(I)||² + λ ||θ||²\n\n", bold=True, size=Pt(12), color=PRIMARY)
    add_text_run(p, "Adam (Adaptive Moment Estimation):\n\n"
                    "• Tracks exponentially decaying first moment m_t (mean gradient) and second moment v_t (uncentered variance):\n\n"
                    "  m_t = β₁ m_{t-1} + (1 - β₁) g_t\n"
                    "  v_t = β₂ v_{t-1} + (1 - β₂) g_t²\n\n"
                    "• Parameter update:\n"
                    "  θ_{t+1} = θ_t - [η / (√(v̂_t) + ε)] · m̂_t\n\n"
                    "• Enables robust convergence without manual per-parameter learning rate tuning.", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s8, 8)

    # ==========================================
    # SLIDE 9: Neural Surrogate Digital Twin (With Diagram)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Surrogate Modeling", "Designing the Neural Surrogate Digital Twin",
               "Capturing non-linear cubic saturation with MLPRegressor for sub-millisecond execution")

    mlp_img = IMG_DIR / "mlp_schematic.png"
    if mlp_img.exists():
        s9.shapes.add_picture(str(mlp_img), Inches(0.6), Inches(1.5), width=Inches(5.9))

    add_card(s9, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Surrogate Architecture & Training")
    tb_mlp = s9.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_mlp = tb_mlp.text_frame
    tf_mlp.word_wrap = True
    p = tf_mlp.paragraphs[0]
    add_text_run(p, "Dataset Generation:\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "• 2,000 synthetic tracking runs sampling steerer currents uniformly across I ∈ [-3.0, 3.0]⁶ A.\n"
                    "• Captures both linear coupling and cubic core saturation.\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "MLPRegressor Hyperparameters:\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "• Input: 6 Corrector currents [HCM1-3, VCM1-3]\n"
                    "• Hidden Layers: (128, 64, 32) neurons\n"
                    "• Activation: ReLU; Solver: Adam\n"
                    "• Regularization: α_L2 = 10⁻⁴, max_iter = 500\n"
                    "• Output: 12 predicted BPM readings [BPM1-12]\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "Performance Verification:\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "• Holdout Test MSE: < 2.5 × 10⁻⁴ mm²\n"
                    "• Inference Execution Latency: < 0.2 ms per call", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s9, 9)

    # ==========================================
    # SLIDE 10: Closed-Loop Control Architecture (With Diagram)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Closed-Loop Control", "Forward Prediction vs Closed-Loop Orbit Control",
               "Transitioning from predictive surrogate twins to continuous closed-loop feedback policies")

    ctrl_img = IMG_DIR / "forward_sl_and_rl_schematic.png"
    if ctrl_img.exists():
        s10.shapes.add_picture(str(ctrl_img), Inches(0.6), Inches(1.5), width=Inches(6.2))

    add_card(s10, Inches(7.1), Inches(1.5), Inches(5.6), Inches(5.2), "Closed-Loop Control Dynamics")
    tb_dyn = s10.shapes.add_textbox(Inches(7.3), Inches(2.1), Inches(5.2), Inches(4.4))
    tf_dyn = tb_dyn.text_frame
    tf_dyn.word_wrap = True
    p = tf_dyn.paragraphs[0]
    add_text_run(p, "The Closed-Loop Feedback Cycle:\n\n", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p, "1. Beam Position Monitors measure current transverse displacement Y_t ∈ ℝ¹².\n\n"
                    "2. Orbit Controller computes corrective kick vector ΔI_t ∈ [-0.8, 0.8]⁶ A.\n\n"
                    "3. Power supplies update cumulative magnet currents:\n"
                    "   I_{t+1} = clip(I_t + ΔI_t, -5.0, 5.0) A\n\n"
                    "4. Updated magnetic fields deflect beam; new orbit Y_{t+1} is established.\n\n"
                    "5. Terminate when RMS < 0.030 mm or step count reaches 20.", size=Pt(11), color=DARK_GRAY)

    add_footer(s10, 10)

    # ==========================================
    # SLIDE 11: Baseline 0 vs Baseline 1 Comparison
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Benchmark Baselines", "Baseline 0 (Linear SVD) vs Baseline 1 (Neural Inversion)",
               "Comparing classical pseudo-inverse control with model-based bounded optimization")

    add_card(s11, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Baseline 0: Classical Linear SVD")
    tb_b0 = s11.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_b0 = tb_b0.text_frame
    tf_b0.word_wrap = True
    p = tf_b0.paragraphs[0]
    add_text_run(p, "Mathematical Form:\n", size=Pt(11))
    add_text_run(p, "ΔI = - α · (Rᵀ)⁺ · Y\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "Characteristics:\n"
                    "• Gain: α ≈ 0.45, hard clipped to [-0.8, 0.8] A\n"
                    "• Latency: < 0.1 ms (instantaneous)\n\n"
                    "Strengths & Weaknesses:\n"
                    "✓ Mathematically exact in purely linear regimes\n"
                    "✗ Completely blind to cubic core saturation\n"
                    "✗ High current demands cause magnetic saturation\n"
                    "✗ Sluggish convergence (Mean steps: 5.6)\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "Official Score: 1,013.1 points (Rank #3)", bold=True, size=Pt(11), color=PRIMARY)

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Baseline 1: Supervised Neural Inversion")
    tb_b1 = s11.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    p = tf_b1.paragraphs[0]
    add_text_run(p, "Mathematical Optimization:\n", size=Pt(11))
    add_text_run(p, "min_{ΔI} ||Y_obs + f_θ(ΔI)||² + λ ||ΔI||²\n"
                    "subject to ΔI ∈ [-5.0, 5.0]⁶\n\n", bold=True, size=Pt(12), color=PRIMARY)
    add_text_run(p, "Characteristics:\n"
                    "• Solver: SciPy L-BFGS-B on trained MLP twin\n"
                    "• Latency: ~15 - 25 ms per step\n\n"
                    "Why It Outperforms Classical SVD:\n"
                    "✓ Accurately anticipates non-linear core saturation\n"
                    "✓ Computes optimal kicks in non-linear regimes\n"
                    "✓ Reaches convergence in just 2.3 steps average\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "Official Score: 1,016.8 points (Rank #2)", bold=True, size=Pt(11), color=PRIMARY)

    add_footer(s11, 11)

    # ==========================================
    # SLIDE 12: Track 2 - Closed-Loop RL Policy
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Track 2 Challenge", "Closed-Loop RL with Physics-Informed Priors",
               "Continuous policy networks combining analytical optics priors with dynamic step damping")

    add_card(s12, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Physics-Informed Residual Architecture")
    tb_rl = s12.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_rl = tb_rl.text_frame
    tf_rl.word_wrap = True
    p = tf_rl.paragraphs[0]
    add_text_run(p, "Residual Policy Formulation:\n\n", size=Pt(11))
    add_text_run(p, "ΔI(t) = γ(t) · [ - α (Rᵀ)⁺ Y + W_learned Y + b ]\n\n", bold=True, size=Pt(12.5), color=PRIMARY)
    add_text_run(p, "Two Core Components:\n\n"
                    "1. Analytical Physics Prior (- α (Rᵀ)⁺ Y):\n"
                    "   - Guarantees immediate coarse stabilization.\n"
                    "   - Prevents unguided random exploratory actions.\n\n"
                    "2. Learned Residual Offset (W_learned Y + b):\n"
                    "   - Compensates for non-linear saturation deficit.\n"
                    "   - Learns asymmetric corrections across HCM/VCM.", size=Pt(10.5), color=DARK_GRAY)

    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Dynamic Harmonic Step Damping")
    tb_damp = s12.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_damp = tb_damp.text_frame
    tf_damp.word_wrap = True
    p = tf_damp.paragraphs[0]
    add_text_run(p, "The Sensor Noise Amplification Problem:\n\n", bold=True, size=Pt(11), color=NAVY)
    add_text_run(p, "Near the 0.030 mm target boundary, sensor noise ε ~ 10 μm creates spurious apparent gradients, causing limit cycles.\n\n"
                    "Harmonic Damping Schedule:\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "γ(t) = 1.0 / (1.0 + κ · t),   κ ≈ 0.03\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "• Step 1 (t = 0, γ = 1.0): Full kick authority rapidly eliminates millimeter-scale orbit error.\n\n"
                    "• Step 5+ (t ≥ 4, γ < 0.88): Attenuated feedback prevents sensor noise amplification and locks RMS below 0.030 mm.", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s12, 12)

    # ==========================================
    # SLIDE 13: Track 3 - Closed-Loop Bayesian Optimization
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Track 3 Challenge", "Closed-Loop Bayesian Optimization with Gaussian Processes",
               "Sample-efficient probabilistic modeling with Lower Confidence Bound (LCB) acquisition")

    add_card(s13, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Probabilistic Gaussian Process Modeling")
    tb_gp = s13.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_gp = tb_gp.text_frame
    tf_gp.word_wrap = True
    p = tf_gp.paragraphs[0]
    add_text_run(p, "GP Mapping: ΔI ↦ Transverse Orbit Deviation Y:\n\n", size=Pt(11))
    add_text_run(p, "Ŷ(ΔI) ~ 𝒢𝒫( m(ΔI), K(ΔI, ΔI') )\n\n", bold=True, size=Pt(13), color=PRIMARY)
    add_text_run(p, "Composite Kernel Architecture:\n"
                    "k(x, x') = k_Matérn-5/2(x, x') + σ_noise² δ(x, x')\n\n"
                    "• Matérn-5/2 Kernel: Captures smooth, non-linear iron core saturation dynamics without unrealistic infinite differentiability.\n\n"
                    "• White Noise Kernel: Explicitly models the 10 μm BPM diagnostic jitter floor.", size=Pt(10.5), color=DARK_GRAY)

    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Lower Confidence Bound (LCB) Acquisition")
    tb_lcb = s13.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_lcb = tb_lcb.text_frame
    tf_lcb.word_wrap = True
    p = tf_lcb.paragraphs[0]
    add_text_run(p, "LCB Acquisition Function:\n\n", bold=True, size=Pt(11), color=NAVY)
    add_text_run(p, "α_LCB(ΔI) = RMS( Y_obs + μ_GP(ΔI) ) - κ · σ̄_GP(ΔI) + λ ||ΔI||²\n\n", bold=True, size=Pt(12), color=PRIMARY)
    add_text_run(p, "Exploration vs Exploitation Trade-off:\n\n"
                    "• μ_GP(ΔI): Posterior mean predicted orbit\n"
                    "• σ̄_GP(ΔI): Posterior epistemic uncertainty across BPMs\n"
                    "• κ ≥ 0: Exploration coefficient\n\n"
                    "Benchmark Outcome:\n"
                    "When calibrated, Track 3 achieves optimal convergence in just 1.5 steps average, with highest current economy.", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s13, 13)

    # ==========================================
    # SLIDE 14: Hackathon Contract & Scoring
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Competition Rules", "Gymnasium Contract & Official Scoring Formula",
               "Standardized Farama Gymnasium environment interface and multi-objective performance metric")

    add_card(s14, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Gymnasium Contract (AcceleratorOrbitGymEnv)")
    tb_gym = s14.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_gym = tb_gym.text_frame
    tf_gym.word_wrap = True
    p = tf_gym.paragraphs[0]
    add_text_run(p, "Environment Interface:\n", size=Pt(11))
    add_text_run(p, "obs, info = env.reset(seed=s)\n"
                    "obs, reward, terminated, truncated, info = env.step(action)\n\n", bold=True, size=Pt(11), color=PRIMARY)
    add_text_run(p, "• obs: np.ndarray shape (12,) in [-10, 10] mm\n"
                    "• action: np.ndarray shape (6,) clipped to [-0.8, 0.8] A\n"
                    "• Step reward:\n"
                    "  r_t = - RMS_{t+1} - 0.01 ||action||₂ + (50.0 if success)\n"
                    "• Termination: RMS < 0.030 mm (success!)\n"
                    "• Truncation: step >= 20 (failed to converge)", size=Pt(10.5), color=DARK_GRAY)

    add_card(s14, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Official Hackathon Scoring Formula")
    tb_sco = s14.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_sco = tb_sco.text_frame
    tf_sco.word_wrap = True
    p = tf_sco.paragraphs[0]
    add_text_run(p, "Score Formula (Across 30 Standardized Seeds):\n\n", bold=True, size=Pt(11), color=NAVY)
    add_text_run(p, "Score = (Success% × 10.0) - (2.0 × Mean_Steps)\n"
                    "        + [0.03 / max(Mean_RMS, 0.005)] × 20.0\n"
                    "        - (2.0 × Mean_||I||)\n\n", bold=True, size=Pt(11.5), color=PRIMARY)
    add_text_run(p, "Four Scoring Components:\n"
                    "1. Success Rate: Up to +1,000 pts (100% convergence)\n"
                    "2. Speed Penalty: -2 pts per step taken\n"
                    "3. Sub-Micron Precision Bonus: Up to +120 pts for ultra-low residual RMS\n"
                    "4. Current Economy Penalty: -2 pts per Ampere of cumulative current norm", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s14, 14)

    # ==========================================
    # SLIDE 15: 30-Seed Benchmark Leaderboard (With Diagram)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Evaluation Results", "30-Seed Benchmark Leaderboard & Trajectories",
               "Comparison of Classical SVD, Supervised MLP, Closed-Loop RL, and Bayesian Optimization")

    traj_img = IMG_DIR / "benchmark_trajectories.png"
    if traj_img.exists():
        s15.shapes.add_picture(str(traj_img), Inches(0.6), Inches(1.5), width=Inches(6.0))

    add_card(s15, Inches(6.9), Inches(1.5), Inches(5.8), Inches(5.2), "Official Benchmark Leaderboard")
    tb_lb = s15.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.5))
    tf_lb = tb_lb.text_frame
    tf_lb.word_wrap = True

    rows = [
        ("🥇 Rank #1: Bayesian Opt (Track 3)", "100.0%", "1.5 steps", "0.0149 mm", "0.93 A", "1,035.4 pts", GOLD),
        ("🥈 Rank #2: Supervised MLP (Baseline 1)", "100.0%", "2.3 steps", "0.0257 mm", "1.21 A", "1,016.8 pts", PRIMARY),
        ("🥉 Rank #3: Classical SVD (Baseline 0)", "100.0%", "5.6 steps", "0.0230 mm", "1.16 A", "1,013.1 pts", DARK_GRAY),
        ("4️⃣ Rank #4: Closed-Loop RL (Track 2)", "100.0%", "6.1 steps", "0.0239 mm", "1.18 A", "1,011.1 pts", DARK_GRAY),
    ]

    for i, (rank, succ, steps, rms, curr, score, col) in enumerate(rows):
        p_r = tf_lb.paragraphs[0] if i == 0 else tf_lb.add_paragraph()
        if i > 0:
            p_r.space_before = Pt(8)
        add_text_run(p_r, f"{rank}\n", bold=True, size=Pt(12), color=col)
        add_text_run(p_r, f"  • Success: {succ}  |  Steps: {steps}\n"
                          f"  • Final RMS: {rms}  |  Current Norm: {curr}\n"
                          f"  • Challenge Score: {score}\n", size=Pt(10), color=DARK_GRAY)

    add_footer(s15, 15)

    # ==========================================
    # SLIDE 16: Summary & Practical Takeaways
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Conclusion & Roadmap", "Key Takeaways, Practical Advice & Next Steps",
               "Strategic advice for afternoon hackathon competitors and transition to Lecture 2")

    add_card(s16, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), "Key Takeaways from Lecture 1")
    tb_t1 = s16.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    add_text_run(p, "1. Physics Guides the AI:\n"
                    "   Never train from scratch when the analytical ORM is known. Using pseudo-inverse priors guarantees early stability.\n\n"
                    "2. Surrogates Capture Non-Linearities:\n"
                    "   When iron yokes saturate, compact MLPs accurately represent cubic falloff and enable 2-step bounded inversions.\n\n"
                    "3. Probabilistic Uncertainty Wins:\n"
                    "   Gaussian Process BO balances exploration against exploitation, leading the 30-seed leaderboard in 1.5 steps.\n\n"
                    "4. Adaptive Damping Locks Stability:\n"
                    "   Attenuating feedback near the 10 μm noise floor prevents sensor-induced limit cycles.", size=Pt(10.5), color=DARK_GRAY)

    add_card(s16, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), "Practical Hackathon Advice & Next Session")
    tb_t2 = s16.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.5), Inches(4.4))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]
    add_text_run(p, "Practical Competitor Advice:\n\n", bold=True, size=Pt(11), color=NAVY)
    add_text_run(p, "• If your policy oscillates: Check feedback gain α. Introduce harmonic damping γ(t) = 1 / (1 + 0.03t).\n\n"
                    "• If surrogate error is high: Ensure training data covers [-3.0, 3.0] A with cubic non-linearities.\n\n"
                    "• Log Telemetry to W&B: Compare your run curves against the official benchmark on the live leaderboard.\n\n"
                    "Next Session (10:40 - 12:00):\n\n", size=Pt(10.5), color=DARK_GRAY)
    add_text_run(p, "Lecture 2: Agentic AI for Accelerator Research (Osprey Applications)\n", bold=True, size=Pt(11.5), color=PRIMARY)
    add_text_run(p, "Speaker: Thorsten Hellert, Ph.D. (LBNL)", size=Pt(11), color=DARK_GRAY)

    add_footer(s16, 16)

    # Save presentation
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT_PATH))
    print(f"Successfully generated editable presentation: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
