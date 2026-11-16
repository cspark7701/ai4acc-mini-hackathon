"""Build the updated, comprehensive 29-slide PPTX presentation for Lecture 1.

AI Applications in Accelerators Tutorial & Mini-Hackathon
Lecture 1: AI/ML Foundations & Closed-Loop Control
Author: Chong Shik Park, Ph.D. (Korea University, Sejong)
Date: November 19, 2026

Design enhancements addressing user requests:
1) Title page title font size adjusted so it fits on a single unwrapped line.
2) Title page KU logo resized to a clean, elegant scale (0.95 inches).
3) Slide titles and subtitles vertically centered with the blue accent bar. Short, non-wrapping titles.
4) Dedicated slides explaining all major activation functions and optimization algorithms.
5) Images of MLP, RL, and trajectories resized and positioned with guaranteed zero overlap.
6) "Tested Benchmark Leaderboard" formatted as a clean, structured table without line wrapping.
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img"
KU_LOGO = IMG_DIR / "ku_logo.png"
OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "presentations" / "Lecture_1_AI_ML_Foundations_and_Control_Slides.pptx"

# Color Palette
NAVY = RGBColor(0, 32, 96)            # Deep Navy (#002060)
PRIMARY = RGBColor(24, 76, 120)       # Primary Blue (#184C78)
ACCENT = RGBColor(41, 128, 185)       # Secondary Accent Blue (#2980B9)
DARK_GRAY = RGBColor(44, 62, 80)      # Text Dark Gray (#2C3E50)
LIGHT_BG = RGBColor(245, 247, 250)    # Shaded Card (#F5F7FA)
BORDER_GRAY = RGBColor(200, 205, 210) # Border Outline (#C8CDD2)
MUTED = RGBColor(127, 140, 141)       # Muted text (#7F8C8D)
WHITE = RGBColor(255, 255, 255)
CRIMSON = RGBColor(158, 22, 54)       # Highlight Red (#9E1636)
TUNABLE_RED = RGBColor(192, 57, 43)   # Tunable Hyperparameter Red (#C0392B)
SUCCESS_GREEN = RGBColor(39, 174, 96) # Green (#27AE60)
GOLD = RGBColor(180, 140, 20)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)
TOTAL_SLIDES = 34

# Line spacing (multiple of single spacing) for the body text of each slide, matching the
# per-slide \slidespread values of the LaTeX deck so that text fills each content card.
LINE_SPACING = {
    1: 1.22, 2: 1.31, 3: 1.35, 4: 1.80, 5: 1.27, 6: 1.14, 7: 1.14, 8: 1.11, 9: 1.22, 10: 1.50,
    11: 1.12, 12: 1.38, 13: 1.25, 14: 1.18, 15: 1.18, 16: 1.25, 17: 1.14, 18: 1.22, 19: 1.38,
    20: 1.22, 21: 1.55, 22: 1.58, 23: 1.14, 24: 1.30, 25: 1.75, 26: 1.14, 27: 1.08, 28: 1.40,
    29: 1.50, 30: 1.22, 31: 1.22, 32: 1.22, 33: 1.39, 34: 1.18
}


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
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # Top-left KU Logo, vertically aligned with the blue column bar
        # Blue bar: top=0.25in, height=0.90in -> vertical center = 0.70in
        # KU Logo: height=0.82in, width=0.70in -> top = 0.70 - 0.82/2 = 0.29in -> vertical center = 0.70in
        if KU_LOGO.exists():
            slide.shapes.add_picture(str(KU_LOGO), Inches(0.50), Inches(0.29), width=Inches(0.70), height=Inches(0.82))

        # Vertical Divider Bar aligned with KU logo and title: left=1.35in, top=0.25in, height=0.90in
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.35), Inches(0.25), Inches(0.06), Inches(0.90))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT

        # Title & Subtitle Box centered with the bar and logo
        tb = slide.shapes.add_textbox(Inches(1.55), Inches(0.22), Inches(11.2), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        if tag_text:
            add_text_run(p0, tag_text.upper() + "  |  ", bold=True, size=Pt(11), color=ACCENT)
        add_text_run(p0, title_text, bold=True, size=Pt(20.5), color=NAVY)

        if subtitle_text:
            p1 = tf.add_paragraph()
            p1.space_before = Pt(3)
            add_text_run(p1, subtitle_text, size=Pt(13), color=DARK_GRAY)

    def add_footer(slide, slide_num):
        # Footer dividing line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.0), Inches(12.333), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.color.rgb = BORDER_GRAY

        # Left date
        tb_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(2.5), Inches(0.35))
        tf_l = tb_left.text_frame
        add_text_run(tf_l.paragraphs[0], "November 19, 2026", size=Pt(10), color=MUTED)

        # Center citation
        tb_center = slide.shapes.add_textbox(Inches(3.0), Inches(7.05), Inches(7.333), Inches(0.35))
        tf_c = tb_center.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        add_text_run(p_c, "Chong Shik Park, Ph.D.  |  Korea University, Sejong  |  AI Applications in Accelerators", size=Pt(10), color=MUTED)

        # Right slide number
        tb_right = slide.shapes.add_textbox(Inches(11.3), Inches(7.05), Inches(1.5), Inches(0.35))
        tf_r = tb_right.text_frame
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        add_text_run(p_r, f"{slide_num} / {TOTAL_SLIDES}", bold=True, size=Pt(10), color=PRIMARY)

    def add_card(slide, left, top, width, height, title="", bg_color=LIGHT_BG, border_color=BORDER_GRAY):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            add_text_run(tf.paragraphs[0], title, bold=True, size=Pt(15.5), color=NAVY)
        return shape

    # ==========================================
    # SLIDE 1: Title Slide (No Text Wrap, Elegantly Scaled KU Logo)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)

    # Clean outer border
    border = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.5), Inches(12.333), Inches(6.5))
    border.fill.solid()
    border.fill.fore_color.rgb = WHITE
    border.line.color.rgb = PRIMARY
    border.line.width = Pt(2)

    # Accent top color bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), Inches(12.333), Inches(0.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ACCENT
    top_bar.line.fill.background()

    # Elegantly scaled KU Logo (0.95 inch width)
    if KU_LOGO.exists():
        s1.shapes.add_picture(str(KU_LOGO), Inches(1.0), Inches(0.85), width=Inches(0.95))

    # Vertical accent bar aligned with logo
    bar_s1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.10), Inches(0.85), Inches(0.06), Inches(1.05))
    bar_s1.fill.solid()
    bar_s1.fill.fore_color.rgb = ACCENT
    bar_s1.line.color.rgb = ACCENT

    # Event badge text next to logo & bar
    tb_tag = s1.shapes.add_textbox(Inches(2.28), Inches(0.85), Inches(9.8), Inches(1.05))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
    add_text_run(tf_tag.paragraphs[0], "AI APPLICATIONS IN ACCELERATORS TUTORIAL & MINI-HACKATHON", bold=True, size=Pt(13.5), color=PRIMARY)

    # Horizontal dividing line
    line_div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.0), Inches(11.333), Inches(0.02))
    line_div.fill.solid()
    line_div.fill.fore_color.rgb = BORDER_GRAY
    line_div.line.fill.background()

    # Title box (sized to fit on a single unwrapped line at 26pt)
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.25), Inches(11.333), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    add_text_run(tf_title.paragraphs[0], "Lecture 1: AI/ML Foundations & Closed-Loop Control", bold=True, size=Pt(26), color=NAVY)

    p2_t = tf_title.add_paragraph()
    p2_t.space_before = Pt(8)
    add_text_run(p2_t, "Physics Foundations, Neural Surrogates, Reinforcement Learning, and Bayesian Optimization", size=Pt(15), color=ACCENT)

    # Author & Affiliation Card
    add_card(s1, Inches(1.0), Inches(4.7), Inches(11.333), Inches(1.9), bg_color=LIGHT_BG)
    tb_auth = s1.shapes.add_textbox(Inches(1.3), Inches(4.75), Inches(10.7), Inches(1.8))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True
    tf_auth.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_text_run(tf_auth.paragraphs[0], "Chong Shik Park, Ph.D.", bold=True, size=Pt(19), color=NAVY)

    p_a2 = tf_auth.add_paragraph()
    p_a2.space_before = Pt(9)
    add_text_run(p_a2, "• Department of Accelerator Science, Korea University, Sejong 30019, Republic of Korea", size=Pt(13), color=DARK_GRAY)
    p_a2b = tf_auth.add_paragraph()
    p_a2b.space_before = Pt(3)
    add_text_run(p_a2b, "• Center for Accelerator Research, Korea University, Sejong 30019, Republic of Korea", size=Pt(13), color=DARK_GRAY)

    p_a3 = tf_auth.add_paragraph()
    p_a3.space_before = Pt(9)
    add_text_run(p_a3, "Date: November 19, 2026", size=Pt(11.5), color=MUTED)

    add_footer(s1, 1)

    # ==========================================
    # SLIDE 2: Operational Context
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Operational Context", "Why AI in Particle Accelerators?", 
               "Meeting stringent sub-micron stability tolerances while managing non-linear actuator dynamics")

    add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Operational Challenge: High-Precision Orbit Stabilization")
    tb2 = s2.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    add_text_run(p, "• Extreme Beam Stability Demands:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "  -- Modern synchrotron light sources, colliders, and FELs require transverse orbit stabilization to within < 10% of beam size (sub-micron RMS tolerances).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf2.add_paragraph()
    add_text_run(p2, "• High-Intensity Hadron Linacs (e.g., SNS, ESS):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- Uncorrected trajectory offsets through RF cavities and quadrupoles induce non-linear space-charge forces and beam halo.\n"
                     "  -- Fractional beam loss exceeding 1 W/m (~10⁻⁵ of total beam power) causes severe structural radioactivation, prohibiting hands-on maintenance.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf2.add_paragraph()
    add_text_run(p3, "• Limitations of Purely Classical Linear Control:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "  -- Analytical linear response matrices (ORM) ignore magnetic core saturation at high currents, inducing overshoot and limit cycles.\n"
                     "  -- Physical diagnostics carry 10 μm noise floors; naive feedback amplifies measurement noise into erratic actuator jitter.\n"
                     "  -- Multi-parameter coupling requires fast non-linear digital twins and adaptive closed-loop policies.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s2, 2)

    # ==========================================
    # SLIDE 3: Master Curriculum & Schedule
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Workshop Curriculum", "Master Curriculum & Program Schedule",
               "Cohesive one-day curriculum connecting physics foundations directly to competitive simulation benchmarks")

    add_card(s3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Program Schedule & Learning Objectives")
    tb3 = s3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    add_text_run(p, "1. Lecture 1: AI/ML Foundations & Closed-Loop Control (09:10 - 10:30)\n", bold=True, size=Pt(15), color=PRIMARY)
    add_text_run(p, "   • Lecturer: Chong Shik Park, Ph.D. (Korea University, Sejong)\n"
                    "   • Focus: Transverse beam dynamics, Hill's equation, Orbit Response Matrix (ORM), non-linear cubic saturation, MLP surrogate modeling, SVD vs bounded inversion, RL with physics priors, and Bayesian optimization.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf3.add_paragraph()
    add_text_run(p2, "2. Lecture 2: Agentic AI for Accelerator Research (10:40 - 12:00)\n", bold=True, size=Pt(15), color=PRIMARY)
    add_text_run(p2, "   • Lecturer: Thorsten Hellert, Ph.D. (Lawrence Berkeley National Laboratory / Osprey)\n"
                    "   • Focus: LLM agents, dynamic Python API tool execution, automated scientific workflows, simulation orchestration, and human-in-the-loop operational safety guardrails.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf3.add_paragraph()
    add_text_run(p3, "3. Afternoon Mini-Hackathon: Beam Orbit Alignment Benchmark (13:30 - 17:00)\n", bold=True, size=Pt(15), color=PRIMARY)
    add_text_run(p3, "   • 15-meter transport lattice, 12 BPMs, 6 steerers, 3 parallel challenge tracks (MLP, RL, BO).\n"
                    "   • Real-time experiment tracking with Weights & Biases (W&B) and live global leaderboard.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s3, 3)

    # ==========================================
    # SLIDE 4: AI Pillars: Surrogates & Optimization
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Domain Overview", "AI Pillars: Surrogates & Optimization",
               "Foundational applications revolutionizing beam physics simulations and online tuning")

    add_card(s4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Pillars 1 & 2: Fast Digital Twins & Autonomous Multi-Objective Tuning")
    tb4 = s4.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    add_text_run(p, "Pillar 1: Neural Surrogate Digital Twins (Fast Forward Simulation)\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "• High-fidelity particle tracking codes (ELEGANT, MAD-X, OPAL) simulate detailed collective space-charge forces, but require minutes to hours per run.\n"
                    "• Deep Neural Networks (MLPs, PINNs) learn compact, high-accuracy representations capable of sub-millisecond execution times (< 0.2 ms).\n"
                    "• Impact: Enables real-time model-predictive control (MPC), online orbit feedback, fast virtual diagnostics, and parameter sensitivity scans.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf4.add_paragraph()
    add_text_run(p2, "Pillar 2: Autonomous Multi-Objective Optimization & Tuning\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "• Accelerator operations require simultaneously balancing conflicting objectives: maximizing transmission and photon brightness while minimizing emittance and beam halo.\n"
                    "• Bayesian Optimization (BO) with Gaussian Processes leverages epistemic uncertainty and exploration-exploitation acquisition functions.\n"
                    "• Impact: Achieves optimal machine operating points directly on physical beamlines in dozens of shots rather than thousands of manual scan steps.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s4, 4)

    # ==========================================
    # SLIDE 5: AI Pillars: Diagnostics, Protection & Agents
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Domain Overview", "AI Pillars: Diagnostics, Protection & Agents",
               "Expanding AI applications into beam instrumentation, uptime preservation, and autonomous agents")

    add_card(s5, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Pillars 3, 4 & 5: Virtual Diagnostics, Protection & Agentic Control")
    tb5 = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    add_text_run(p, "Pillar 3: Virtual Diagnostics & Non-Destructive Phase Space Reconstruction\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "• Interceptive diagnostics (wire scanners, screens, deflecting cavities) destroy or disrupt the beam during measurement.\n"
                    "• Supervised ML reconstructs 6D phase space, bunch slice emittance, and current profiles shot-by-shot from non-invasive upstream RF probes and BPM readings.\n\n", size=Pt(13), color=DARK_GRAY)

    p2 = tf5.add_paragraph()
    add_text_run(p2, "Pillar 4: Anomaly Detection, Fault Prediction & Machine Protection\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "• Unscheduled downtime in multi-megawatt facilities incurs catastrophic financial and scientific operational costs.\n"
                    "• Unsupervised autoencoders detect precursor thermal drift; deep recurrent networks predict RF breakdown and superconducting cavity quenches milliseconds before failure.\n\n", size=Pt(13), color=DARK_GRAY)

    p3 = tf5.add_paragraph()
    add_text_run(p3, "Pillar 5: Agentic AI & Autonomous Operational Workflows\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "• Modern agent frameworks (e.g. Osprey) couple Large Language Model reasoning engines with standardized Python control APIs and simulation codes.\n"
                    "• Translates high-level natural language goals into validated, safe operational sequences under strict domain guardrails.", size=Pt(13), color=DARK_GRAY)

    add_footer(s5, 5)

    # ==========================================
    # SLIDE 6: Hill's Equation & Transverse Motion
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Physics Foundations", "Hill's Equation & Transverse Motion",
               "The fundamental second-order differential equation governing transverse betatron motion")

    add_card(s6, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Derivation and Physical Interpretation of Hill's Equation")
    tb6 = s6.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    add_text_run(p, "Governing Equation of Motion:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "For an uncoupled linear magnetic transport line, particle displacement x(s) along coordinate s satisfies:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf6.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "d²x(s) / ds² + K(s) x(s) = 0\n", bold=True, size=Pt(18), color=PRIMARY)

    p2 = tf6.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Quadrupole Focusing Function K(s):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- K(s) = (e / p) · (∂By / ∂x) defines the alternating gradient magnetic focusing strength.\n"
                     "  -- K > 0 represents horizontally focusing quadrupoles (QF) that horizontally compress the beam envelope.\n"
                     "  -- K < 0 represents horizontally defocusing quadrupoles (QD) that vertically focus the beam envelope.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf6.add_paragraph()
    add_text_run(p3, "• Periodic Focusing Principle (Courant-Snyder Invariance):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "  -- Even though K(s) varies piecewise along the beam axis, alternating QF and QD pairs yield net focusing in both transverse planes simultaneously.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s6, 6)

    # ==========================================
    # SLIDE 7: Betatron Motion & Courant-Snyder Optics
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Beam Optics", "Betatron Motion & Courant-Snyder Optics",
               "Analytical solution to Hill's equation and Courant-Snyder envelope parameters")

    add_card(s7, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Betatron Oscillation Solution & Envelope Dynamics")
    tb7 = s7.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    add_text_run(p, "General Pseudo-Harmonic Betatron Solution:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "The exact analytical solution to Hill's equation is expressed as a modulated harmonic wave:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf7.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "x(s) = √[ ε · β(s) ] · cos( ψ(s) + φ₀ )\n", bold=True, size=Pt(18), color=PRIMARY)

    p2 = tf7.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Physical Parameter Definitions:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- β(s) [m]: Courant-Snyder beta function, describing the transverse beam envelope geometry along the lattice.\n"
                     "  -- ε [m·rad]: Beam emittance, representing the conserved area occupied by the beam in transverse phase space (x, x').\n"
                     "  -- ψ(s) = ∫ ds / β(s): The betatron phase advance accrued along the longitudinal coordinate.\n"
                     "  -- ν = (1 / 2π) ∮ ds / β(s): The betatron tune, representing the total number of transverse oscillations per machine turn.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf7.add_paragraph()
    add_text_run(p3, "• Key Insight for Orbit Correction:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "  -- Any localized angular deflection propagates downstream as a betatron oscillation modulated by √(β(s)).", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s7, 7)

    # ==========================================
    # SLIDE 8: Orbit Response Matrix Derivation
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Analytical Optics", "Orbit Response Matrix Derivation",
               "Mathematical formulation linking localized steering kicks to downstream BPM readings")

    add_card(s8, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Analytical ORM Transfer Function")
    tb8 = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    add_text_run(p, "Orbit Response of a Single-Pass Transport Line to a Steerer Kick:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "When a steering dipole at position s_j applies an angular kick θ_j = e B L / p, the orbit shift at BPM position s_i is:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf8.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "R_ij = Δx(s_i) / θ_j = √(β_i β_j) · sin( ψ_i - ψ_j )   for s_i > s_j  (0 upstream)\n", bold=True, size=Pt(16), color=PRIMARY)
    add_text_run(p_eq, "(A ring has the closed-orbit form √(β_i β_j)/(2 sin πν) · cos(|ψ_i - ψ_j| - πν); the hackathon line uses phase advance 2π·0.18 rad/m.)\n", size=Pt(12), color=MUTED)

    p2 = tf8.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Global Matrix Superposition Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- For N corrector magnets and M Beam Position Monitors, the linear response is encapsulated as:\n", size=Pt(13.5), color=DARK_GRAY)

    p_mat = tf8.add_paragraph()
    p_mat.alignment = PP_ALIGN.CENTER
    add_text_run(p_mat, "Y_linear = I · R\n", bold=True, size=Pt(18), color=PRIMARY)

    p3 = tf8.add_paragraph()
    add_text_run(p3, "  -- I ∈ ℝ⁶: Vector of corrector coil currents in Amperes, mapped to kicks via magnetic field integration.\n"
                     "  -- R ∈ ℝ⁶ˣ¹²: The linear Orbit Response Matrix (ORM).\n"
                     "  -- Y ∈ ℝ¹²: Transverse displacements measured at all 12 downstream BPM stations.\n"
                     "  -- Cross-plane coupling: Any single corrector deflection alters the entire beam trajectory downstream.", size=Pt(13), color=DARK_GRAY)

    add_footer(s8, 8)

    # ==========================================
    # SLIDE 9: 15-Meter Transport Lattice Architecture (ZERO OVERLAP)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Hackathon Benchmark", "15-Meter Transport Lattice Architecture",
               "Physical arrangement of quadrupole doublets, dipole correctors, and beam position monitors")

    # Proportional image: Width = 10.0 in, Height = 2.5 in (Top: 1.45 to 3.95in)
    beamline_img = IMG_DIR / "beamline.png"
    if beamline_img.exists():
        s9.shapes.add_picture(str(beamline_img), Inches(1.66), Inches(1.45), width=Inches(10.0), height=Inches(2.5))

    # Card below at Top = 4.25in (0.3in margin, Zero Overlap!)
    add_card(s9, Inches(0.8), Inches(4.25), Inches(11.733), Inches(2.45), "Transport Line Specifications & Component Placement", bg_color=LIGHT_BG)
    tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(4.8), Inches(11.1), Inches(1.8))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    add_text_run(p, "• 12 Beam Position Monitors (BPMs): ", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p, "Evenly distributed from s = 1.0 m to s = 15.0 m, measuring transverse displacement Y in millimeters.\n", size=Pt(13), color=DARK_GRAY)

    p2 = tf9.add_paragraph()
    p2.space_before = Pt(4)
    add_text_run(p2, "• 6 Dipole Steering Magnets: ", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p2, "3 Horizontal (HCM1-3) and 3 Vertical (VCM1-3) steerers positioned between s = 0.2 m and s = 8.0 m.\n", size=Pt(13), color=DARK_GRAY)

    p3 = tf9.add_paragraph()
    p3.space_before = Pt(4)
    add_text_run(p3, "• Alternating Quadrupole Doublets: ", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p3, "Pairs of QF and QD focusing magnets shaping the betatron phase advance and maintaining envelope stability.", size=Pt(13), color=DARK_GRAY)

    add_footer(s9, 9)

    # ==========================================
    # SLIDE 10: Hardware Limits & Actuator Bounds
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Physical Limits", "Hardware Limits & Actuator Bounds",
               "Realistic power supply operational boundaries and sensor measurement jitter")

    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Power Supply Limits and Diagnostic Noise Specifications")
    tb10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    add_text_run(p, "1. Cumulative Corrector Current Bounds (Thermal & Magnetic Saturation Limit):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "   • Total current state: I_k ∈ [-5.0 A, +5.0 A] for all 6 correctors.\n"
                    "   • Magnets entering currents |I| > 3.0 A experience pronounced iron core saturation.\n"
                    "   • Hardware protection interlocks trip power supplies if current demands exceed ±5.0 A.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf10.add_paragraph()
    add_text_run(p2, "2. Per-Step Delta Current Bounds (Inductive Slew Rate Limit):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "   • Single-step control action: ΔI_k ∈ [-0.8 A, +0.8 A].\n"
                    "   • Prevents high inductive back-EMF spikes (L · di/dt) that stress magnet coils and trigger power supply voltage limits.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf10.add_paragraph()
    add_text_run(p3, "3. Gaussian Diagnostic Measurement Noise (Sensor Resolution Floor):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "   • Sensor noise: ε_i ~ 𝒩(0, σ²), with σ = 0.010 mm (10 μm RMS resolution).\n"
                    "   • Crucial for control design: Naive controllers misinterpret sensor jitter as physical orbit errors, commanding false kicks.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s10, 10)

    # ==========================================
    # SLIDE 11: Magnetic Core Non-Linear Saturation
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Non-Linear Physics", "Magnetic Core Non-Linear Saturation",
               "Departing from idealized linear optics: modeling cubic saturation and quadrupole errors")

    add_card(s11, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Mathematical Formulation of Non-Linear Beamline Response")
    tb11 = s11.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    add_text_run(p, "Complete Beam Position Response Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "The actual BPM observation vector Y in the simulation environment is governed by:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf11.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "Y = I · R  -  0.015 · ( I³ · R )  +  Y₀  +  ε\n", bold=True, size=Pt(18), color=PRIMARY)

    p2 = tf11.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Physical Breakdown of Response Terms:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- I · R: Ideal linear betatron wave response predicted by transfer matrix.\n"
                     "  -- -0.015 · (I³ · R): Non-linear iron core soft saturation. At high excitation currents, the iron yoke reaches magnetic saturation, decreasing steerer kick efficiency by 6% (at 2 A) up to 24% (at 4 A).\n"
                     "  -- Y₀ = a · R: Initial distortion from unknown kicks aₖ ~ U(-2.5, 2.5) A at all six correctors, drawn per episode (0.93-3.59 mm RMS on the evaluation seeds; cancelling it needs up to 2.8 A).\n"
                     "  -- ε: Diagnostic Gaussian measurement jitter (σ = 10 μm).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf11.add_paragraph()
    add_text_run(p3, "• Convergence Target: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "Drive orbit error below RMS < 0.030 mm (30 μm) within 50 control steps.", bold=True, size=Pt(14), color=SUCCESS_GREEN)

    add_footer(s11, 11)

    # ==========================================
    # SLIDE 12: Artificial Neurons & Layer Composition
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ML Foundations", "Artificial Neurons & Layer Composition",
               "Mathematical anatomy of feedforward perceptrons and deep neural layer stacking")

    add_card(s12, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Neuron Transformation and Multi-Layer Composition")
    tb12 = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    add_text_run(p, "1. The Artificial Neuron Transformation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "   • Takes input vector x ∈ ℝᵈ, computes affine combination, and applies non-linear activation σ:\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf12.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "z = ∑ w_j x_j + b = wᵀ x + b,       a = σ(z)\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf12.add_paragraph()
    p2.space_before = Pt(6)
    add_text_run(p2, "2. Multi-Layer Perceptron (MLP) Deep Architecture:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "   • Stacks L successive layers of affine transformations and non-linear activations:\n"
                     "     h⁽ˡ⁾ = σ( W⁽ˡ⁾ h⁽ˡ⁻¹⁾ + b⁽ˡ⁾ ),   with h⁽⁰⁾ = x,   ŷ = h⁽ᴸ⁾\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf12.add_paragraph()
    add_text_run(p3, "3. Universal Approximation Theorem (Hornik et al., 1989):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "   • A feedforward network with at least one non-linear hidden layer can approximate any continuous non-linear function arbitrarily well, guaranteeing surrogate representability of magnetic saturation.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s12, 12)

    # ==========================================
    # SLIDE 13: Activation Functions: Definition, Roles & Catalog
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "ML Foundations", "Activation Functions: Definition, Roles & Catalog",
               "Non-linear mappings breaking layer linearity and enabling universal function approximation")

    add_card(s13, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Definition, 3 Key Roles & Core Activation Function Zoo")
    act_img = IMG_DIR / "activation_functions.png"
    if act_img.exists():
        pic = s13.shapes.add_picture(str(act_img), Inches(8.3), Inches(1.95), height=Inches(4.62))
        pic.left = Inches(12.30) - pic.width
    tb13 = s13.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(7.15), Inches(4.65))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    p0 = tf13.paragraphs[0]
    add_text_run(p0, "• Definition: ", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p0, "Non-linear mapping σ(z) applied element-wise to pre-activation sum z = wᵀx + b.\n", size=Pt(11.5), color=DARK_GRAY)
    add_text_run(p0, "• 3 Key Roles: ", bold=True, size=Pt(12), color=NAVY)
    add_text_run(p0, "(1) Breaks linearity so deep layers do not collapse. (2) Enables universal approximation of non-linear saturation. (3) Gates backprop gradients via σ'(z).\n", size=Pt(11.5), color=DARK_GRAY)

    acts = [
        ("1. ReLU:", "f(z) = max(0, z)", "• Gradient = 1 for z > 0; fast, no vanishing gradient. Default for hidden layers."),
        ("2. Leaky ReLU:", "f(z) = max(α·z, z), α ≈ 0.01", "• Small slope for z < 0 avoids 'dying' neurons that stop learning."),
        ("3. GELU:", "f(z) = z · Φ(z)", "• Smooth gating by normal CDF; standard in modern Transformers."),
        ("4. Sigmoid:", "σ(z) = 1 / (1 + e⁻ᶻ)", "• Output in (0, 1) for probabilities; gradient vanishes when saturated."),
        ("5. Tanh:", "tanh(z) = (eᶻ - e⁻ᶻ)/(eᶻ + e⁻ᶻ)", "• Zero-centered in (-1, 1); stronger gradients than Sigmoid, still saturates."),
        ("6. Linear / Identity:", "f(z) = z", "• No non-linearity; strictly required in output layer for continuous orbits (BPMs).")
    ]

    for i, (name, formula, desc) in enumerate(acts):
        p_act = tf13.add_paragraph()
        p_act.space_before = Pt(3)
        add_text_run(p_act, f"{name} ", bold=True, size=Pt(11.5), color=NAVY)
        add_text_run(p_act, f"{formula}\n", bold=True, size=Pt(11.5), color=PRIMARY)
        add_text_run(p_act, desc, size=Pt(11), color=DARK_GRAY)

    add_footer(s13, 13)

    # ==========================================
    # SLIDE 14: Basic NN Surrogate Example: Transfer Matrix
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "ML Foundations", "Basic NN Surrogate Example: Transfer Matrix",
               "Surrogating single-particle linear optics: mapping initial phase space coordinates to final coordinates")

    add_card(s14, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Transfer Matrix Surrogate Formulation: [x₀, x'₀] → [x_f, x'_f]")

    # Left Box
    tb14_l = s14.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(5.35), Inches(4.5))
    tf14_l = tb14_l.text_frame
    tf14_l.word_wrap = True

    p = tf14_l.paragraphs[0]
    add_text_run(p, "1. Classical Analytical Transfer Matrix:\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p, "In linear beam optics, transverse particle trajectory through a beamline element is governed by the 2 × 2 transfer matrix M:\n\n", size=Pt(12), color=DARK_GRAY)

    p_eq = tf14_l.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "[x_f, x'_f]ᵀ = M · [x₀, x'₀]ᵀ,      det(M) = 1\n", bold=True, size=Pt(14), color=PRIMARY)

    p2 = tf14_l.add_paragraph()
    p2.space_before = Pt(4)
    add_text_run(p2, "• det(M) = 1 ensures phase-space area preservation (Liouville's theorem / symplecticity).\n\n", size=Pt(11.5), color=DARK_GRAY)

    add_text_run(p2, "2. Neural Network Surrogate Formulation:\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p2, "Instead of numerical tracking, we train a neural network f_θ: ℝ² → ℝ²:\n\n", size=Pt(12), color=DARK_GRAY)

    p_eq2 = tf14_l.add_paragraph()
    p_eq2.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq2, "[x̂_f, x̂'_f]ᵀ = f_θ([x₀, x'₀]ᵀ) = W⁽ᴸ⁾ σ( W⁽ᴸ⁻¹⁾ ... σ( W⁽¹⁾ x + b⁽¹⁾ ) ) + b⁽ᴸ⁾\n", bold=True, size=Pt(13), color=PRIMARY)

    p3 = tf14_l.add_paragraph()
    p3.space_before = Pt(4)
    add_text_run(p3, "3. Supervised Objective & Conservation Target:\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p3, "• MSE Loss: ℒ_MSE = (1/N) ∑ [ (x_f - x̂_f)² + (x'_f - x̂'_f)² ]\n"
                     "• Symplectic Condition: det(J_f) = (∂x̂_f/∂x₀)(∂x̂'_f/∂x'₀) - (∂x̂_f/∂x'₀)(∂x̂'_f/∂x₀) ≡ 1.", size=Pt(11.5), color=DARK_GRAY)

    # Right Box: Architectural Card (ENLARGED to 5.4 in x 4.4 in)
    add_card(s14, Inches(6.75), Inches(1.95), Inches(5.4), Inches(4.4), title="", bg_color=WHITE, border_color=PRIMARY)
    tb14_r = s14.shapes.add_textbox(Inches(6.9), Inches(2.05), Inches(5.1), Inches(4.2))
    tf14_r = tb14_r.text_frame
    tf14_r.word_wrap = True

    p_r0 = tf14_r.paragraphs[0]
    add_text_run(p_r0, "Surrogate Architecture Layout: ℝ² → ℝ²\n\n", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p_r0, "• Input Layer (2 nodes):\n  -- Transverse position x₀ [mm]\n  -- Transverse divergence x'₀ [mrad]\n\n", size=Pt(12), color=DARK_GRAY)
    add_text_run(p_r0, "• Hidden Layers (4 units each):\n  -- Layer 1: W⁽¹⁾ ∈ ℝ⁴ˣ², b⁽¹⁾ ∈ ℝ⁴, σ\n  -- Layer 2: W⁽²⁾ ∈ ℝ⁴ˣ⁴, b⁽²⁾ ∈ ℝ⁴, σ\n  -- Progressive feature abstraction\n\n", size=Pt(12), color=DARK_GRAY)
    add_text_run(p_r0, "• Output Layer (2 nodes):\n  -- Predicted position x̂_f [mm]\n  -- Predicted divergence x̂'_f [mrad]\n  -- W⁽³⁾ ∈ ℝ²ˣ⁴, b⁽³⁾ ∈ ℝ²\n\n", size=Pt(12), color=DARK_GRAY)
    add_text_run(p_r0, "CRITICAL REQUIREMENT:\nOutput activation MUST be Linear/Identity because phase space coordinates (x, x') are unbounded!", bold=True, size=Pt(11.5), color=CRIMSON)

    add_footer(s14, 14)

    # ==========================================
    # SLIDE 15: NN Surrogate: Activation Functions in Beam Transport
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "ML Foundations", "NN Surrogate: Activation Functions in Beam Transport",
               "How choice of activation function governs phase space distortion, symplecticity, and extrapolation")

    add_card(s15, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Behavior of Activation Functions on Phase Space (x, x') and Transfer Matrix M")

    # Left Column: Linear/Identity & ReLU (width 5.4 in)
    tb15_l = s15.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.4), Inches(4.5))
    tf15_l = tb15_l.text_frame
    tf15_l.word_wrap = True

    p_15l1 = tf15_l.paragraphs[0]
    add_text_run(p_15l1, "1. Linear / Identity Activation (σ(z) = z):\n", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_15l1, "• Matrix Collapse: Stacking linear layers collapses to W⁽ᴸ⁾...W⁽¹⁾ x + b_net ≡ M_eff x + b_net. Mathematically identical to a transfer matrix.\n"
                         "• Beam Optics Impact: Exactly preserves linear phase-space ellipses (γ x² + 2α x x' + β x'² = ε) and symplecticity (det M = 1). Extrapolates perfectly to arbitrary beam sizes.\n"
                         "• Limitation: Fundamentally incapable of learning non-linear chromaticity, sextupole kicks (x' ∝ x²), or magnetic core saturation.\n\n", size=Pt(11), color=DARK_GRAY)

    p_15l2 = tf15_l.add_paragraph()
    add_text_run(p_15l2, "2. Rectified Linear Unit (ReLU: σ(z) = max(0, z)):\n", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_15l2, "• Piecewise Linear Facets: Partitions phase space (x, x') into polyhedral regions bounded by hyperplanes wⱼᵀ x + bⱼ = 0.\n"
                         "• Beam Optics Impact: Deforms smooth phase-space ellipses into faceted polygons with sharp slope kinks (non-differentiable points).\n"
                         "• Dying Neurons Risk: Particles entering inactive half-spaces (z < 0) have zero gradient and output 0, locally collapsing phase-space dimensions and violating Liouville area conservation.", size=Pt(11), color=DARK_GRAY)

    # Right Column: Tanh & Output Layer Requirement (width 5.4 in)
    tb15_r = s15.shapes.add_textbox(Inches(6.8), Inches(2.05), Inches(5.4), Inches(4.5))
    tf15_r = tb15_r.text_frame
    tf15_r.word_wrap = True

    p_15r1 = tf15_r.paragraphs[0]
    add_text_run(p_15r1, "3. Hyperbolic Tangent (Tanh: σ(z) = tanh(z)):\n", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_15r1, "• Smooth Non-Linearity: Continuously differentiable (C^∞). Near the beam core (|z| ≪ 1), tanh(z) ≈ z, so the surrogate behaves linearly and learns M accurately.\n"
                         "• Beam Optics Impact: At large amplitudes (beam halo, large steering errors), hidden neurons saturate (tanh(z) → ±1). Squashes phase-space ellipses into S-curves, artificially compressing emittance (det J → 0) and violating symplecticity in the wings.\n\n", size=Pt(11), color=DARK_GRAY)

    p_15r2 = tf15_r.add_paragraph()
    add_text_run(p_15r2, "4. Output Layer Architecture Requirement:\n", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_15r2, "• Strictly Linear (Identity) Output: Transverse coordinates x_f and angles x'_f are unbounded physical quantities.\n"
                         "• Risk of Bounded Activations: Using Sigmoid or Tanh on outputs imposes an unphysical aperture cap, clipping large kicks and destroying model inversion.", size=Pt(11), color=CRIMSON)

    add_footer(s15, 15)

    # ==========================================
    # SLIDE 16: Optimization Algorithms in Machine Learning
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "ML Foundations", "Optimization Algorithms in Machine Learning",
               "First-order stochastic gradient methods, momentum, adaptive learning rates, and quasi-Newton solvers")

    add_card(s16, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Evolution of Solvers: From Standard SGD to Adam and L-BFGS-B")

    # Left Column: SGD, Momentum, AdaGrad, RMSProp (width 5.4 in)
    tb16_l = s16.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.4), Inches(4.5))
    tf16_l = tb16_l.text_frame
    tf16_l.word_wrap = True

    opts_l = [
        ("1. SGD (Stochastic Gradient):", "θ ← θ - η · g", "Basic first-order step. Prone to severe oscillation across ill-conditioned curvatures and high sensitivity to learning rate η."),
        ("2. Momentum SGD:", "v ← γ·v + η·g,  θ ← θ - v", "Accumulates velocity in directions of consistent gradients, dampening oscillations and accelerating through saddle points."),
        ("3. AdaGrad (Adaptive Gradient):", "θ ← θ - [η / √(G + ε)] · g", "Adapts learning rates per-parameter based on historical squared gradients. However, learning rate decays monotonically to zero."),
        ("4. RMSProp:", "v ← β·v + (1-β)·g²,  θ ← θ - [η / √(v + ε)] · g", "Uses exponentially decaying moving average of squared gradients. Solves AdaGrad's premature stopping problem.")
    ]

    for i, (name, formula, desc) in enumerate(opts_l):
        p_opt = tf16_l.paragraphs[0] if i == 0 else tf16_l.add_paragraph()
        if i > 0:
            p_opt.space_before = Pt(4)
        add_text_run(p_opt, f"{name} ", bold=True, size=Pt(11.5), color=NAVY)
        add_text_run(p_opt, f"{formula}\n", bold=True, size=Pt(11), color=PRIMARY)
        add_text_run(p_opt, f"• {desc}", size=Pt(10.5), color=DARK_GRAY)

    # Right Column: Adam, AdamW, L-BFGS-B (width 5.4 in)
    tb16_r = s16.shapes.add_textbox(Inches(6.8), Inches(2.05), Inches(5.4), Inches(4.5))
    tf16_r = tb16_r.text_frame
    tf16_r.word_wrap = True

    opts_r = [
        ("5. Adam (Adaptive Moment Estimation):", "m_t (1st moment) + v_t (2nd moment)", "Combines Momentum and RMSProp with bias correction. Default gold standard for deep neural network surrogate training."),
        ("6. AdamW (Decoupled Weight Decay):", "Direct L2 weight decay subtraction", "Decouples L2 penalty from adaptive gradient scaling. Dramatically improves generalization performance."),
        ("7. L-BFGS-B (Quasi-Newton with Bounds):", "Second-order Hessian approximation", "Highly effective for bounded parameter inversion (Baseline 1 & Track 3) with tight box bounds [-0.8, +0.8] A.")
    ]

    for i, (name, formula, desc) in enumerate(opts_r):
        p_opt = tf16_r.paragraphs[0] if i == 0 else tf16_r.add_paragraph()
        if i > 0:
            p_opt.space_before = Pt(6)
        add_text_run(p_opt, f"{name} ", bold=True, size=Pt(11.5), color=NAVY)
        add_text_run(p_opt, f"{formula}\n", bold=True, size=Pt(11), color=PRIMARY)
        add_text_run(p_opt, f"• {desc}", size=Pt(10.5), color=DARK_GRAY)

    add_footer(s16, 16)

    # ==========================================
    # SLIDE 17: Paradigm 1: Supervised Learning (Terminology & Hyperparameters)
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Paradigm 1: Supervised Learning", "Supervised Learning: Digital Twins & Hyperparameters",
               "Training data-driven accelerator forward surrogates to model complex non-linear optics")

    add_card(s17, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Supervised Learning Workflow, Optimization & Hyperparameter Taxonomy")

    # Left Box: Model Training Terminology
    tb17_l = s17.shapes.add_textbox(Inches(1.05), Inches(2.00), Inches(4.85), Inches(4.5))
    tf17_l = tb17_l.text_frame
    tf17_l.word_wrap = True

    p_17 = tf17_l.paragraphs[0]
    add_text_run(p_17, "1. Core Model Training Terminology:\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p_17, "• Weights W & Biases b: Trainable synaptic multipliers and threshold offsets updated during learning.\n"
                       "• Loss Function ℒ(θ): Error metric (MSE) measuring discrepancy between predicted orbit Ŷ and true BPM vector Y.\n"
                       "• Gradient & Backpropagation: Multivariable chain rule propagating loss gradients ∇_θ ℒ backward to compute weight steps.\n"
                       "• Epoch vs Batch vs Step / Iteration:\n"
                       "  -- Epoch: One complete training pass through the full dataset (N shots).\n"
                       "  -- Batch (B): Subset of training shots evaluated per gradient step.\n"
                       "  -- Step / Iteration: A single weight vector update θ ← θ - Δθ.\n"
                       "• Generalization & Early Stopping: Halts training when validation loss stops improving, avoiding memorizing sensor noise (10 μm).", size=Pt(11.5), color=DARK_GRAY)

    # Right Box: Hyperparameter Table (starts at 6.45 in, 0.55 in gutter)
    sl_table_shape = s17.shapes.add_table(7, 3, Inches(6.45), Inches(2.00), Inches(5.7), Inches(4.1))
    sl_tbl = sl_table_shape.table
    for idx, w in enumerate([Inches(1.45), Inches(1.35), Inches(2.9)]):
        sl_tbl.columns[idx].width = w

    for c_idx, h_text in enumerate(["Hyperparameter", "Typical Value", "Physical Meaning & Effect"]):
        cell = sl_tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p_c = cell.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER if c_idx < 2 else PP_ALIGN.LEFT
        add_text_run(p_c, h_text, bold=True, size=Pt(10.5), color=WHITE)

    sl_rows = [
        ("Learning Rate (η)*", "10⁻³ (Adam)", "Step size along gradient. Too large diverges; too small stagnates in local plateaus."),
        ("Batch Size (B)*", "32 to 128", "Samples per gradient step. Smaller batches provide regularization; larger give speed."),
        ("Architecture*", "(128, 64, 32)", "Depth and width. Must have capacity to capture cubic saturation without overfitting."),
        ("Activation (σ)*", "ReLU / Leaky ReLU", "Non-linearity in hidden layers. Linear activation strictly reserved for output layer."),
        ("L2 Penalty (α)*", "10⁻⁴", "Weight decay penalty (1/2)α||w||². Suppresses overfitting to BPM jitter (10 μm)."),
        ("Max Epochs / Tol*", "400 ep, tol=10⁻⁴", "Halts optimization when validation loss stops improving, avoiding overtraining.")
    ]
    for r_idx, row_vals in enumerate(sl_rows, start=1):
        for c_idx, text_val in enumerate(row_vals):
            cell = sl_tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
            cell.text_frame.word_wrap = True
            p_cell = cell.text_frame.paragraphs[0]
            p_cell.alignment = PP_ALIGN.LEFT
            add_text_run(p_cell, text_val, bold=(c_idx == 0), size=Pt(9.5), color=TUNABLE_RED if c_idx == 0 else DARK_GRAY)

    # Footnote on modifiable hyperparameters
    tb17_fn = s17.shapes.add_textbox(Inches(6.45), Inches(6.18), Inches(5.7), Inches(0.4))
    tb17_fn.text_frame.word_wrap = True
    p_fn17 = tb17_fn.text_frame.paragraphs[0]
    add_text_run(p_fn17, "* Red text: Hyperparameters participants can modify in notebook TODO 1", bold=True, size=Pt(9.5), color=TUNABLE_RED)

    add_footer(s17, 17)

    # ==========================================
    # SLIDE 18: Neural Surrogate Digital Twin (RESIZED IMAGE - ZERO OVERLAP)
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Surrogate Modeling", "Neural Surrogate Digital Twin",
               "Deep Multi-Layer Perceptron (128-64-32) capturing non-linear cubic saturation")

    # Image scaled: Height = 3.85 in, aspect ratio preserved and centered
    mlp_img = IMG_DIR / "mlp_schematic.png"
    if mlp_img.exists():
        pic = s18.shapes.add_picture(str(mlp_img), Inches(0), Inches(1.38), height=Inches(3.85))
        pic.left = int((SLIDE_WIDTH - pic.width) / 2)

    # Card below the image
    add_card(s18, Inches(0.8), Inches(5.38), Inches(11.733), Inches(1.22), bg_color=LIGHT_BG)
    tb18 = s18.shapes.add_textbox(Inches(1.0), Inches(5.42), Inches(11.3), Inches(1.14))
    tf18 = tb18.text_frame
    tf18.word_wrap = True
    tf18.vertical_anchor = MSO_ANCHOR.MIDDLE
    add_text_run(tf18.paragraphs[0], 
                 "• Input Layer: 6 Corrector Magnet Currents [HCM1-3, VCM1-3] in Amperes.\n"
                 "• Hidden Layers: Dense layers (128 → 64 → 32) with ReLU non-linear activations capturing cubic iron-core saturation.\n"
                 "• Output Layer: 12 predicted Beam Position Monitor readings [BPM1-12] in millimeters, evaluated in < 0.2 milliseconds.", 
                 size=Pt(12.5), color=DARK_GRAY)

    add_footer(s18, 18)

    # ==========================================
    # SLIDE 19: Surrogate Training & Holdout Validation
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Digital Twin Validation", "Surrogate Training & Validation",
               "Ensuring digital twin fidelity across linear and saturated magnetic operating regimes")

    add_card(s19, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Offline Dataset Generation and Model Verification")
    tb19 = s19.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf19 = tb19.text_frame
    tf19.word_wrap = True

    p_19 = tf19.paragraphs[0]
    add_text_run(p_19, "1. Synthetic Tracking Dataset Generation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_19, "   • 2,000 synthetic simulation runs generated by uniformly sampling corrector currents across I ∈ [-3.0, +3.0]⁶ A.\n"
                       "   • Full non-linear response computed including the cubic soft-saturation term -0.015 · (I³ · R).\n"
                       "   • Dataset partitioned into 80% Training (1,600 samples) and 20% Holdout Testing (400 samples).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2_19 = tf19.add_paragraph()
    add_text_run(p2_19, "2. MLPRegressor Training Configuration:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_19, "   • Architecture: hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam'.\n"
                        "   • Regularization: alpha=1e-4, max_iter=500, early_stopping=True.\n"
                        "   • Loss convergence reached in under 180 epochs (~3.5 seconds CPU training time).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_19 = tf19.add_paragraph()
    add_text_run(p3_19, "3. Holdout Verification Metrics:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_19, "   • Holdout Test MSE: < 2.5 × 10⁻⁴ mm² across all 12 BPM stations.\n"
                        "   • Sub-Millisecond Execution: Forward inference takes < 0.2 ms per call, 10,000× faster than numerical tracking.", bold=True, size=Pt(13.5), color=PRIMARY)

    add_footer(s19, 19)

    # ==========================================
    # SLIDE 20: Closed-Loop Control Architecture (RESIZED IMAGE - ZERO OVERLAP)
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Closed-Loop Control", "Closed-Loop Control Architecture",
               "Three learning paradigms behind the challenge tracks; all three act on the measured orbit at every step")

    # Image scaled: Height = 3.85 in, aspect ratio preserved and centered
    ctrl_img = IMG_DIR / "forward_sl_and_rl_schematic.png"
    if ctrl_img.exists():
        pic = s20.shapes.add_picture(str(ctrl_img), Inches(0), Inches(1.38), height=Inches(3.85))
        pic.left = int((SLIDE_WIDTH - pic.width) / 2)

    # Card below the image
    add_card(s20, Inches(0.8), Inches(5.38), Inches(11.733), Inches(1.22), bg_color=LIGHT_BG)
    tb20 = s20.shapes.add_textbox(Inches(1.0), Inches(5.42), Inches(11.3), Inches(1.14))
    tf20 = tb20.text_frame
    tf20.word_wrap = True
    tf20.vertical_anchor = MSO_ANCHOR.MIDDLE
    add_text_run(tf20.paragraphs[0],
                 "• Supervised (Track 1): trains an MLP surrogate offline, then inverts it at each step for the kick ΔI.\n"
                 "• Reinforcement (Track 2): a policy acts on the measured orbit Y and improves from the reward it receives.\n"
                 "• Bayesian Optimization (Track 3): a GP models the response with uncertainty; each step minimizes the LCB.",
                 size=Pt(12.5), color=DARK_GRAY)

    add_footer(s20, 20)

    # ==========================================
    # SLIDE 21: Baseline 0: Classical Linear SVD
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Benchmark Baselines", "Baseline 0: Classical Linear SVD",
               "Inverting the linear Orbit Response Matrix via Moore-Penrose pseudo-inverse")

    add_card(s21, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Mathematical Formulation & Operational Vulnerabilities")
    tb21 = s21.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf21 = tb21.text_frame
    tf21.word_wrap = True

    p_21 = tf21.paragraphs[0]
    add_text_run(p_21, "Singular Value Decomposition (SVD) Pseudo-Inverse Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_21, "Computes corrective kick vector ΔI directly by inverting the transpose of the linear ORM:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_21 = tf21.add_paragraph()
    p_eq_21.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_21, "ΔI = - α · ( Rᵀ )⁺ · Y_obs,       with ( Rᵀ )⁺ = V Σ⁺ Uᵀ\n", bold=True, size=Pt(17), color=PRIMARY)

    p2_21 = tf21.add_paragraph()
    p2_21.space_before = Pt(8)
    add_text_run(p2_21, "• Operational Profile & Limitations:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_21, "  -- Static feedback gain: Typically α ≈ 0.45, with kicks hard clipped to [-0.8, +0.8] A.\n"
                        "  -- Execution latency: < 0.1 ms (instantaneous analytical matrix-vector product).\n"
                        "  -- Vulnerability in Non-Linear Regimes: Completely oblivious to cubic iron core saturation. When magnets operate at high currents, the true response is much weaker than linear R predicts, leading to over-correction, slow convergence (5.6 mean steps), and high final current demands.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_21 = tf21.add_paragraph()
    add_text_run(p3_21, "• Tested Benchmark Performance: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_21, "100.0% success rate, 9.4 mean steps, 635.277 total score (Rank #3).", bold=True, size=Pt(14), color=PRIMARY)

    add_footer(s21, 21)

    # ==========================================
    # SLIDE 22: Baseline 1 (Track 1): Supervised Neural Inversion
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Benchmark Baselines", "Baseline 1 (Track 1): Supervised Neural Inversion",
               "Model-based bounded optimization via SciPy L-BFGS-B on the trained neural digital twin")

    add_card(s22, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Optimization Formulation on Forward Surrogate")
    tb22 = s22.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf22 = tb22.text_frame
    tf22.word_wrap = True

    p_22 = tf22.paragraphs[0]
    add_text_run(p_22, "Per-Step Bounded Numerical Optimization Problem:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_22, "Instead of inverting an analytical matrix, Baseline 1 leverages the non-linear MLP twin f_θ:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_22 = tf22.add_paragraph()
    p_eq_22.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_22, "min_{ΔI} ℒ(ΔI) = || Y_obs − f_θ(I) + f_θ(I + ΔI) ||²  +  λ ||ΔI||²\nsubject to ΔI ∈ [-5.0, +5.0]⁶ A\n", bold=True, size=Pt(16), color=PRIMARY)

    p2_22 = tf22.add_paragraph()
    p2_22.space_before = Pt(8)
    add_text_run(p2_22, "• Why Supervised Inversion Outperforms Classical SVD:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_22, "  -- Because f_θ captures the cubic saturation falloff, the optimizer automatically calculates higher current demands for saturated correctors.\n"
                        "  -- Solver: SciPy L-BFGS-B converges in 8-15 iterations per control step (~15 - 25 ms latency).\n"
                        "  -- I is the present total current from info[\"currents\"], so the objective uses the predicted next orbit at every step.\n"
                        "  -- Result: With the reference MLP (test RMSE 0.11 mm) it succeeds on all 30 seeds; a more accurate surrogate (TODO 1) lands closer to the noise floor.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_22 = tf22.add_paragraph()
    add_text_run(p3_22, "• Tested Benchmark Performance: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_22, "100.0% success rate, 4.0 mean steps, 779.169 total score (Rank #2).", bold=True, size=Pt(14), color=PRIMARY)

    add_footer(s22, 22)

    # ==========================================
    # SLIDE 23: Paradigm 2: Reinforcement Learning (MDP & Hyperparameters)
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Paradigm 2: Reinforcement Learning", "Reinforcement Learning: MDP Formulation & Hyperparameters",
               "Closed-loop sequential decision making: learning optimal control policies from interaction rewards")

    add_card(s23, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Markov Decision Process (MDP) Framework & Policy Hyperparameter Taxonomy")

    # Left Box: MDP formulation
    tb23_l = s23.shapes.add_textbox(Inches(1.05), Inches(2.00), Inches(4.85), Inches(4.5))
    tf23_l = tb23_l.text_frame
    tf23_l.word_wrap = True

    p_23 = tf23_l.paragraphs[0]
    add_text_run(p_23, "1. Closed-Loop MDP Formulation (𝒮, 𝒜, 𝒫, ℛ, γ):\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p_23, "• State Space (𝒮): Measured BPM displacements s_t = Y_t ∈ ℝ¹² (transverse beam orbit errors in mm).\n"
                       "• Action Space (𝒜): Steerer delta kicks a_t = ΔI_t ∈ [-0.8, +0.8]⁶ A.\n"
                       "• Transition Dynamics (𝒫): Non-linear beam transport, steerer integration, cubic saturation, and sensor jitter ε.\n"
                       "• Reward Function (ℛ): Real-time alignment performance:\n"
                       "  r_t = - w_rms·RMS_{t+1} - w_act·||a_t||² - c_step + b_term\n"
                       "• Policy Objective: Maximize expected cumulative return:\n"
                       "  J(θ) = 𝔼_{π_θ} [ ∑ γᵗ r_t ]\n"
                       "• Policy Architecture: Physics prior (Rᵀ)⁺ + learned residual W_learned.", size=Pt(11.5), color=DARK_GRAY)

    # Right Box: Hyperparameter Table (starts at 6.45 in, 0.55 in gutter)
    rl_table_shape = s23.shapes.add_table(7, 3, Inches(6.45), Inches(2.00), Inches(5.7), Inches(4.1))
    rl_tbl = rl_table_shape.table
    for idx, w in enumerate([Inches(1.45), Inches(1.35), Inches(2.9)]):
        rl_tbl.columns[idx].width = w

    for c_idx, h_text in enumerate(["Hyperparameter", "Typical Value", "Role in Orbit Control"]):
        cell = rl_tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p_c = cell.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER if c_idx < 2 else PP_ALIGN.LEFT
        add_text_run(p_c, h_text, bold=True, size=Pt(10.5), color=WHITE)

    rl_rows = [
        ("Discount Factor (γ)*", "0.95 - 0.99", "Temporal horizon weight. High γ prioritizes final sub-30 μm landing over per-step penalty."),
        ("Policy LR (η_π)*", "10⁻⁴ - 10⁻³", "Step size for policy / actor updates. Must be stable against stochastic sensor noise."),
        ("Exploration Noise (σ)*", "𝒩(0, 0.05²) A", "Action perturbations during training to probe saturation; decays towards zero."),
        ("Harmonic Damping (κ)*", "κ ≈ 0.03", "Temporal authority schedule γ(t) = 1/(1+κ t) suppressing sensor jitter amplification."),
        ("Reward Weights*", "w_rms=10, w_act=0.01", "Balances orbit error penalty against coil resistive heating and power supply strain."),
        ("Step Penalty (c_step)*", "0.5 pts/step", "Incentivizes fastest convergence to maximize hackathon speed score (up to 300 pts).")
    ]
    for r_idx, row_vals in enumerate(rl_rows, start=1):
        for c_idx, text_val in enumerate(row_vals):
            cell = rl_tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
            cell.text_frame.word_wrap = True
            p_cell = cell.text_frame.paragraphs[0]
            p_cell.alignment = PP_ALIGN.LEFT
            add_text_run(p_cell, text_val, bold=(c_idx == 0), size=Pt(9.5), color=TUNABLE_RED if c_idx == 0 else DARK_GRAY)

    # Footnote on modifiable hyperparameters
    tb23_fn = s23.shapes.add_textbox(Inches(6.45), Inches(6.18), Inches(5.7), Inches(0.4))
    tb23_fn.text_frame.word_wrap = True
    p_fn23 = tb23_fn.text_frame.paragraphs[0]
    add_text_run(p_fn23, "* Red text: Hyperparameters participants can modify in notebook TODO 2", bold=True, size=Pt(9.5), color=TUNABLE_RED)

    add_footer(s23, 23)

    # ==========================================
    # SLIDE 24: Track 2: Closed-Loop RL with Physics Priors
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Track 2 Challenge", "Track 2: Closed-Loop RL with Physics Priors",
               "Continuous policy networks combining analytical optics priors with learned residual offsets")

    add_card(s24, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Physics-Informed Residual Architecture")
    tb24_rl = s24.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf24_rl = tb24_rl.text_frame
    tf24_rl.word_wrap = True

    p_24 = tf24_rl.paragraphs[0]
    add_text_run(p_24, "Hybrid Residual Policy Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_24, "Rather than learning control from scratch with unguided exploratory random kicks, our agent uses:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_24 = tf24_rl.add_paragraph()
    p_eq_24.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_24, "ΔI(t) = γ(t) · [ - α ( Rᵀ )⁺ Y  +  W_learned Y  +  b ]\n", bold=True, size=Pt(17), color=PRIMARY)

    p2_24 = tf24_rl.add_paragraph()
    p2_24.space_before = Pt(8)
    add_text_run(p2_24, "• Architectural Synergy Breakdown:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_24, "  1. Analytical Physics Prior ( - α (Rᵀ)⁺ Y ):\n"
                        "     - Anchors the policy in first-principles beam optics.\n"
                        "     - Guarantees immediate coarse stabilization from step 1 without needing millions of trial steps.\n\n"
                        "  2. Learned Residual Offset ( W_learned Y + b ):\n"
                        "     - Trainable correction; it starts at zero in the reference agent (a damped pseudo-inverse). Learning or tuning it to compensate saturation is the Track 2 task.\n"
                        "     - Balances asymmetric horizontal (HCM) and vertical (VCM) steerer authorities dynamically.\n\n"
                        "  3. Execution Latency: < 0.4 ms (pure feedforward matrix multiply, 50× faster than iterative L-BFGS-B).", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s24, 24)

    # ==========================================
    # SLIDE 25: Dynamic Harmonic Step Damping
    # ==========================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Stability Control", "Dynamic Harmonic Step Damping",
               "Preventing sensor-noise amplification and eliminating limit-cycle oscillations")

    add_card(s25, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Resolving the Sensor Noise Feedback Limit Cycle")
    tb25_d = s25.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf25_d = tb25_d.text_frame
    tf25_d.word_wrap = True

    p_25 = tf25_d.paragraphs[0]
    add_text_run(p_25, "The Noise Floor Bottleneck:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_25, "• As the orbit converges toward the sub-30 μm target, true orbit errors become comparable to BPM sensor noise (σ = 10 μm).\n"
                       "• Undamped linear feedback interprets stochastic sensor jitter as real trajectory error, commanding vigorous kicks that induce limit cycles around the boundary.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2_25 = tf25_d.add_paragraph()
    add_text_run(p2_25, "Harmonic Damping Schedule:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_25, "We modulate the policy kick authority with a dynamic temporal decay schedule:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_25 = tf25_d.add_paragraph()
    p_eq_25.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_25, "γ(t) = 1.0 / ( 1.0 + κ · t ),       with κ ≈ 0.03\n", bold=True, size=Pt(17), color=PRIMARY)

    p3_25 = tf25_d.add_paragraph()
    p3_25.space_before = Pt(8)
    add_text_run(p3_25, "• Step 1 (t = 0, γ = 1.0): Full kick authority rapidly suppresses large millimeter-scale initial distortions.\n"
                        "• Step 5+ (t ≥ 4, γ < 0.88): Attenuated feedback prevents sensor jitter amplification, locking the orbit cleanly below 0.030 mm.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s25, 25)

    # ==========================================
    # SLIDE 26: Paradigm 3: Bayesian Optimization (GP & Hyperparameters)
    # ==========================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "Paradigm 3: Bayesian Optimization", "Bayesian Optimization: Probabilistic GPs & Hyperparameters",
               "Sample-efficient black-box tuning: modeling response uncertainty to guide global exploration")

    add_card(s26, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Gaussian Process Surrogate Modeling, Acquisition Decisions & Hyperparameter Taxonomy")

    # Left Box: How BO Works
    tb26_l = s26.shapes.add_textbox(Inches(1.05), Inches(2.00), Inches(4.85), Inches(4.5))
    tf26_l = tb26_l.text_frame
    tf26_l.word_wrap = True

    p_26 = tf26_l.paragraphs[0]
    add_text_run(p_26, "1. How Bayesian Optimization Works:\n", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p_26, "• Step 1: Non-Parametric GP Prior: Assumes unknown orbit response is drawn from a Gaussian Process:\n"
                       "  f(x) ~ 𝒢𝒫( m(x), k(x, x') + σ_n² δ(x, x') )\n"
                       "• Step 2: Posterior Conditioning: Given t measured shots 𝒟_t, analytical Gaussian conditioning yields predicted mean μ(x) and epistemic uncertainty σ(x).\n"
                       "• Step 3: Acquisition Function Optimization:\n"
                       "  x_{t+1} = argmin_x α_LCB(x) = μ(x) - κ · σ(x) + λ ||x||²\n"
                       "  Balances exploitation (low μ) vs exploration (high σ).\n"
                       "• Step 4: Machine Evaluation & Iteration: Query real beamline at x_{t+1}, update 𝒟_{t+1}, and refit hyperparameters.", size=Pt(11.5), color=DARK_GRAY)

    # Right Box: Hyperparameter Table (starts at 6.45 in, 0.55 in gutter)
    bo_table_shape = s26.shapes.add_table(7, 3, Inches(6.45), Inches(2.00), Inches(5.7), Inches(4.1))
    bo_tbl = bo_table_shape.table
    for idx, w in enumerate([Inches(1.45), Inches(1.35), Inches(2.9)]):
        bo_tbl.columns[idx].width = w

    for c_idx, h_text in enumerate(["Hyperparameter", "Typical Value", "Role in Beam Alignment"]):
        cell = bo_tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p_c = cell.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER if c_idx < 2 else PP_ALIGN.LEFT
        add_text_run(p_c, h_text, bold=True, size=Pt(10.5), color=WHITE)

    bo_rows = [
        ("Kernel Function (k)*", "Matérn-5/2", "Models twice-differentiable magnetic saturation without unrealistic C^∞ stiffness of RBF.", True),
        ("Lengthscale (ℓ_k)*", "ℓ ~ 1.0 - 2.5 A", "Actuator correlation length per magnet. Dictates how rapidly orbit decorrelates in current space.", True),
        ("Signal Variance (σ_f²)*", "σ_f ~ 1.5 mm", "Overall vertical variance scale of beam trajectory deviations across typical operating kicks.", True),
        ("Noise Variance (σ_n²)", "σ_n = 0.010 mm", "Fixed sensor noise floor (10 μm); do not modify. Prevents GP interpolation from overfitting noise.", False),
        ("Exploration (κ)*", "κ = 0.0 → 1.5", "Trade-off parameter in LCB. κ > 0 probes unmapped saturation; κ = 0 exploits calibrated mean.", True),
        ("Regularizer (λ)*", "λ = 10⁻⁴", "Actuator norm penalty ||ΔI||² protecting power supplies and preventing coil heating.", True)
    ]
    for r_idx, row_vals in enumerate(bo_rows, start=1):
        name_val, typ_val, desc_val, is_tunable = row_vals
        for c_idx, text_val in enumerate([name_val, typ_val, desc_val]):
            cell = bo_tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
            cell.text_frame.word_wrap = True
            p_cell = cell.text_frame.paragraphs[0]
            p_cell.alignment = PP_ALIGN.LEFT
            col = (TUNABLE_RED if is_tunable else NAVY) if c_idx == 0 else DARK_GRAY
            add_text_run(p_cell, text_val, bold=(c_idx == 0), size=Pt(9.5), color=col)

    # Footnote on modifiable hyperparameters
    tb26_fn = s26.shapes.add_textbox(Inches(6.45), Inches(6.18), Inches(5.7), Inches(0.4))
    tb26_fn.text_frame.word_wrap = True
    p_fn26 = tb26_fn.text_frame.paragraphs[0]
    add_text_run(p_fn26, "* Red text: Hyperparameters participants can modify in notebook TODO 3", bold=True, size=Pt(9.5), color=TUNABLE_RED)

    add_footer(s26, 26)

    # ==========================================
    # SLIDE 27: Track 3: Closed-Loop Bayesian Optimization
    # ==========================================
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "Track 3 Challenge", "Track 3: Closed-Loop Bayesian Optimization",
               "Sample-efficient probabilistic modeling with epistemic uncertainty estimation")

    add_card(s27, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Probabilistic Gaussian Process Modeling")
    tb27_bo = s27.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf27_bo = tb27_bo.text_frame
    tf27_bo.word_wrap = True

    p_27 = tf27_bo.paragraphs[0]
    add_text_run(p_27, "Gaussian Process Surrogate Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_27, "Instead of deterministic point predictions, a GP models a distribution over candidate orbit response functions:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_27 = tf27_bo.add_paragraph()
    p_eq_27.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_27, "Ŷ(ΔI) ~ 𝒢𝒫( m(ΔI), K(ΔI, ΔI') )\n", bold=True, size=Pt(18), color=PRIMARY)

    p2_27 = tf27_bo.add_paragraph()
    p2_27.space_before = Pt(8)
    add_text_run(p2_27, "• Composite Physics-Informed Kernel Architecture:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_27, "  k(x, x') = k_Matérn-5/2(x, x') + σ_noise² · δ(x, x')\n\n"
                        "  -- Matérn-5/2 Kernel: Captures smooth, non-linear magnetic saturation falloff without imposing the unrealistic infinite differentiability of RBF kernels.\n"
                        "  -- White Noise Kernel: Explicitly accounts for the 10 μm BPM diagnostic jitter floor, avoiding kernel overfitting to noise.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_27 = tf27_bo.add_paragraph()
    add_text_run(p3_27, "• Epistemic Uncertainty Estimation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_27, "  -- For any candidate kick ΔI, the GP provides both posterior mean μ_GP(ΔI) and standard deviation σ_GP(ΔI).", size=Pt(13.5), color=DARK_GRAY)

    p4_27 = tf27_bo.add_paragraph()
    p4_27.space_before = Pt(8)
    add_text_run(p4_27, "• Closed-Loop Control, Offline Model:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p4_27, "  -- Each step re-solves the acquisition from the latest BPM reading, but the reference GP is fitted once on ~300 "
                        "calibration shots and stays fixed. Refitting it with every new step (e.g. from a step_callback) turns Track 3 "
                        "into true online Bayesian optimization.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s27, 27)

    # ==========================================
    # SLIDE 28: Lower Confidence Bound Acquisition
    # ==========================================
    s28 = prs.slides.add_slide(blank_layout)
    add_header(s28, "Acquisition Function", "Lower Confidence Bound Acquisition",
               "Balancing exploration of non-linear saturation against exploitation of predicted orbit corrections")

    add_card(s28, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The LCB Acquisition Strategy")
    tb28_lcb = s28.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf28_lcb = tb28_lcb.text_frame
    tf28_lcb.word_wrap = True

    p_28 = tf28_lcb.paragraphs[0]
    add_text_run(p_28, "Lower Confidence Bound (LCB) Mathematical Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_28, "At each step, the controller selects kicks by minimizing the LCB acquisition criterion:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq_28 = tf28_lcb.add_paragraph()
    p_eq_28.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq_28, "α_LCB(ΔI) = RMS( Y_obs − μ_GP(I) + μ_GP(I + ΔI) )  -  κ · σ̄_GP(ΔI)  +  λ ||ΔI||²\n", bold=True, size=Pt(16), color=PRIMARY)

    p2_28 = tf28_lcb.add_paragraph()
    p2_28.space_before = Pt(8)
    add_text_run(p2_28, "• Parameter Interpretations:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_28, "  -- μ_GP(ΔI): Posterior mean predicted orbit deviation across all 12 BPM stations.\n"
                        "  -- σ̄_GP(ΔI): Posterior epistemic uncertainty (average standard deviation across BPMs).\n"
                        "  -- κ ≥ 0: Exploration coefficient. When κ > 0, the agent explores uncharted high-current regimes; when κ = 0, it exploits the calibrated posterior mean.\n"
                        "  -- λ ||ΔI||²: Regularization penalty that minimizes actuator heating and avoids saturation.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_28 = tf28_lcb.add_paragraph()
    add_text_run(p3_28, "• Exceptional Convergence Speed: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_28, "When calibrated, Track 3 reaches the convergence threshold in about 3.6 steps on average (878.384 points).", bold=True, size=Pt(14), color=SUCCESS_GREEN)

    add_footer(s28, 28)

    # ==========================================
    # SLIDE 29: Gymnasium Environment Contract
    # ==========================================
    s29 = prs.slides.add_slide(blank_layout)
    add_header(s29, "Benchmark Contract", "Gymnasium Environment Contract",
               "Standard Farama Gymnasium API contract governing state, actions, and rewards")

    add_card(s29, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Farama Gymnasium Environment Interface")
    tb29_gym = s29.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf29_gym = tb29_gym.text_frame
    tf29_gym.word_wrap = True

    p_29 = tf29_gym.paragraphs[0]
    add_text_run(p_29, "Standard Gymnasium Method Signatures:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_29, "obs, info = env.reset(seed=seed)\n"
                       "obs, reward, terminated, truncated, info = env.step(action)\n\n", bold=True, size=Pt(14), color=PRIMARY)

    p2_29 = tf29_gym.add_paragraph()
    add_text_run(p2_29, "• Observation Space: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p2_29, "Box(-10.0, +10.0, shape=(12,), dtype=float32) (12 transverse BPM readings in mm).\n", size=Pt(13), color=DARK_GRAY)

    p3_29 = tf29_gym.add_paragraph()
    add_text_run(p3_29, "• Action Space: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p3_29, "Box(-0.8, +0.8, shape=(6,), dtype=float32) (6 per-step delta kicks ΔI in Amperes).\n", size=Pt(13), color=DARK_GRAY)

    p4_29 = tf29_gym.add_paragraph()
    add_text_run(p4_29, "• Step Reward Function:\n", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p4_29, "  r_t = - 10·RMS_{t+1} - 0.01·||ΔI||² - c_step + ( 50 if RMS_{t+1} < 0.030 mm else 0 )\n", bold=True, size=Pt(13.5), color=PRIMARY)
    add_text_run(p4_29, "  Default weights, all adjustable (rms_weight, action_weight, step_penalty, success_bonus, reward_fn); the reward guides RL training only and does not affect the official score.\n", size=Pt(12), color=MUTED)

    p5_29 = tf29_gym.add_paragraph()
    add_text_run(p5_29, "• Termination Criteria: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p5_29, "terminated = True when RMS < 0.030 mm (success); truncated = True when step >= 50 (budget exhausted).", size=Pt(13), color=DARK_GRAY)

    add_footer(s29, 29)

    # ==========================================
    # SLIDE 30: Standardized 30-Seed Scoring Formula
    # ==========================================
    s30 = prs.slides.add_slide(blank_layout)
    add_header(s30, "Evaluation Protocol", "Standardized 30-Seed Scoring Formula",
               "Per-seed 0-1000 point score balancing convergence reliability, speed, and precision")

    add_card(s30, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Official Hackathon Scoring Formula")
    tb30_sc = s30.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf30_sc = tb30_sc.text_frame
    tf30_sc.word_wrap = True

    p_30 = tf30_sc.paragraphs[0]
    add_text_run(p_30, "Standardized Evaluation Suite: seeds = range(1, 31) (30 evaluation seeds)", size=Pt(13.5), color=DARK_GRAY)

    p_eq_30 = tf30_sc.add_paragraph()
    p_eq_30.alignment = PP_ALIGN.CENTER
    p_eq_30.space_before = Pt(8)
    add_text_run(p_eq_30, "Score = mean over 30 seeds of s_k,  s_k = 0 if seed k fails, otherwise\n"
                          "s_k = 400  +  300 × max(0, (20 - n_k) / 19)  +  300 × clip( ln(0.030 / RMS_k) / ln 3, 0, 1 )\n", bold=True, size=Pt(16), color=PRIMARY)

    p2_30 = tf30_sc.add_paragraph()
    p2_30.space_before = Pt(8)
    add_text_run(p2_30, "Each seed scores 0-1000 points; the official score is the mean over 30 seeds:", bold=True, size=Pt(15), color=NAVY)

    # Scoring components table
    score_rows = [
        ("Success", "400", "The seed reaches RMS < 0.030 mm within 50 steps. A failed seed scores 0 overall."),
        ("Speed", "up to 300", "300 for converging in 1 step, falling linearly to 0 at 20 steps or more (episodes run up to 50 steps)."),
        ("Precision", "up to 300", "0 at the 0.030 mm target, 300 at the 0.010 mm sensor noise floor, on a log scale (0.017 mm earns about 150)."),
    ]
    st_shape_30 = s30.shapes.add_table(4, 3, Inches(1.1), Inches(3.75), Inches(11.1), Inches(1.9))
    st_30 = st_shape_30.table
    for idx, w in enumerate([Inches(1.6), Inches(1.5), Inches(8.0)]):
        st_30.columns[idx].width = w
    for c_idx, h_text in enumerate(["Part", "Points", "How it is earned"]):
        cell = st_30.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p_cell = cell.text_frame.paragraphs[0]
        p_cell.alignment = PP_ALIGN.LEFT if c_idx == 2 else PP_ALIGN.CENTER
        add_text_run(p_cell, h_text, bold=True, size=Pt(12.5), color=WHITE)
    for r_idx, row_vals in enumerate(score_rows, start=1):
        for c_idx, text_val in enumerate(row_vals):
            cell = st_30.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
            cell.text_frame.word_wrap = True
            p_cell = cell.text_frame.paragraphs[0]
            p_cell.alignment = PP_ALIGN.LEFT if c_idx == 2 else PP_ALIGN.CENTER
            add_text_run(p_cell, text_val, bold=(c_idx == 0), size=Pt(12.5), color=NAVY if c_idx == 0 else DARK_GRAY)

    tb30n = s30.shapes.add_textbox(Inches(1.1), Inches(5.95), Inches(11.1), Inches(0.5))
    tb30n.text_frame.word_wrap = True
    p_n_30 = tb30n.text_frame.paragraphs[0]
    add_text_run(p_n_30, "Current norm: ", bold=True, size=Pt(12.5), color=DARK_GRAY)
    add_text_run(p_n_30, "Reported on the leaderboard but not scored; it varies by only a few percent between controllers.", size=Pt(12.5), color=DARK_GRAY)

    add_footer(s30, 30)

    # ==========================================
    # SLIDE 31: Tested Benchmark Leaderboard & Trajectories (ZERO OVERLAP + NATIVE TABLE)
    # ==========================================
    s31 = prs.slides.add_slide(blank_layout)
    add_header(s31, "Evaluation Results", "Tested Benchmark Leaderboard & Trajectories",
               "Verified comparative benchmark results across the 30 standardized evaluation seeds")

    # Image scaled: Width = 8.6 in, Height = 2.9 in (Top: 1.4 to 4.3in)
    traj_img = IMG_DIR / "benchmark_trajectories.png"
    if traj_img.exists():
        s31.shapes.add_picture(str(traj_img), Inches(2.36), Inches(1.4), width=Inches(8.6), height=Inches(2.9))

    # Native PowerPoint Table: 5 rows, 7 columns at Top = 4.55in (Zero Overlap, No Text Wrap!)
    t_left = Inches(0.56)
    t_top = Inches(4.55)
    t_width = Inches(12.2)
    t_height = Inches(2.2)

    table_shape_31 = s31.shapes.add_table(5, 7, t_left, t_top, t_width, t_height)
    tbl_31 = table_shape_31.table

    col_widths = [Inches(1.0), Inches(4.2), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4)]
    for idx, w in enumerate(col_widths):
        tbl_31.columns[idx].width = w

    headers = ["Rank", "Controller Paradigm", "Success", "Mean Steps", "Final RMS", "Current", "Score"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl_31.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        tf_cell = cell.text_frame
        tf_cell.word_wrap = False
        p_cell = tf_cell.paragraphs[0]
        p_cell.alignment = PP_ALIGN.CENTER
        add_text_run(p_cell, h_text, bold=True, size=Pt(11.5), color=WHITE)

    data_rows = [
        ("Rank 1", "Track 3: Bayesian Optimization (BO)", "100.0%", "3.6 steps", "0.0136 mm", "3.85 A", "878.384 pts", GOLD),
        ("Rank 2", "Baseline 1 (Track 1): Supervised Neural Inversion (MLP)", "100.0%", "4.0 steps", "0.0197 mm", "3.84 A", "779.169 pts", PRIMARY),
        ("Rank 3", "Baseline 0: Classical Linear SVD", "100.0%", "9.4 steps", "0.0235 mm", "3.80 A", "635.277 pts", DARK_GRAY),
        ("Rank 4", "Track 2: Closed-Loop RL Policy Agent", "100.0%", "10.8 steps", "0.0256 mm", "3.79 A", "590.559 pts", DARK_GRAY),
    ]

    for r_idx, row_data in enumerate(data_rows, start=1):
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        rank_val, name_val, succ_val, step_val, rms_val, curr_val, score_val, col = row_data
        cells_text = [rank_val, name_val, succ_val, step_val, rms_val, curr_val, score_val]

        for c_idx, text_val in enumerate(cells_text):
            cell = tbl_31.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            tf_cell = cell.text_frame
            tf_cell.word_wrap = False
            p_cell = tf_cell.paragraphs[0]
            p_cell.alignment = PP_ALIGN.LEFT if c_idx == 1 else PP_ALIGN.CENTER
            is_bold = c_idx in [0, 6]
            font_color = col if c_idx in [0, 6] else DARK_GRAY
            add_text_run(p_cell, text_val, bold=is_bold, size=Pt(11), color=font_color)

    add_footer(s31, 31)

    # ==========================================
    # SLIDE 32: Method Comparison Summary (Baselines & Tracks)
    # ==========================================
    s32 = prs.slides.add_slide(blank_layout)
    add_header(s32, "Evaluation Results", "Method Comparison Summary",
               "How the two baselines and the two challenge tracks differ, and how they score on the 30 seeds")

    cmp_rows = [
        ("Baseline 0\nClassical SVD", "ΔI = −α (Rᵀ)⁺ Y, fixed gain α = 0.45", "Analytic ORM; no training data",
         "Instant, robust, interpretable", "Ignores saturation; slow at low gain; fixed reference", "635.277 / —"),
        ("Baseline 1 (Track 1)\nSupervised inversion", "Minimize ‖Y − f_θ(I) + f_θ(I+ΔI)‖² with L-BFGS-B each step", "MLP digital twin; 1,500 offline shots",
         "Learns the non-linear response", "Only as good as the surrogate; slowest per step", "779.169 / 924.2"),
        ("Track 2\nRL / adaptive policy", "Physics prior + learned residual + damping", "Policy parameters; tuned in closed loop",
         "Fastest per step; adapts online", "Gain and damping tuning; overshoot risk", "590.559 / 940.0"),
        ("Track 3\nBayesian optimization", "Minimize LCB of GP-predicted RMS each step", "Gaussian process; ~300 calibration shots",
         "Sample-efficient; models uncertainty", "GP cost grows with data; per-step optimization", "878.384 / 909.9"),
    ]
    cmp_headers = ["Method", "Control law", "Model & data", "Strengths", "Limitations", "Score: ref. / solution"]
    cmp_shape_32 = s32.shapes.add_table(5, 6, Inches(0.8), Inches(1.55), Inches(11.733), Inches(4.5))
    cmp_tbl_32 = cmp_shape_32.table
    for idx, w in enumerate([Inches(2.05), Inches(2.35), Inches(1.85), Inches(1.95), Inches(2.1), Inches(1.433)]):
        cmp_tbl_32.columns[idx].width = w
    for c_idx, h_text in enumerate(cmp_headers):
        cell = cmp_tbl_32.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        add_text_run(cell.text_frame.paragraphs[0], h_text, bold=True, size=Pt(12.5), color=WHITE)
    for r_idx, row_vals in enumerate(cmp_rows, start=1):
        for c_idx, text_val in enumerate(row_vals):
            cell = cmp_tbl_32.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 1 else WHITE
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.text_frame.word_wrap = True
            p_cell = cell.text_frame.paragraphs[0]
            p_cell.alignment = PP_ALIGN.CENTER if c_idx == 5 else PP_ALIGN.LEFT
            if c_idx == 0:
                name, sub_name = text_val.split("\n")
                add_text_run(p_cell, name + "\n", bold=True, size=Pt(12.5), color=NAVY)
                add_text_run(p_cell, sub_name, size=Pt(12), color=DARK_GRAY)
            else:
                add_text_run(p_cell, text_val, size=Pt(12), color=DARK_GRAY)

    tb_cmp_32 = s32.shapes.add_textbox(Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.6))
    tb_cmp_32.text_frame.word_wrap = True
    add_text_run(tb_cmp_32.text_frame.paragraphs[0],
                 "Reference: unmodified notebook controllers (per-seed 0–1000 scoring, mean over 30 seeds). Solution: the organizers' worked "
                 "solution, which inverts the model on the total current. "
                 "Baseline 0 is a fixed reference and is not tuned by participants.", size=Pt(11), color=MUTED)

    add_footer(s32, 32)

    # ==========================================
    # SLIDE 33: Strategic Advice for Competitors
    # ==========================================
    s33 = prs.slides.add_slide(blank_layout)
    add_header(s33, "Competitor Strategy", "Strategic Advice for Competitors",
               "Practical engineering guidance to maximize benchmark score and avoid common failure modes")

    add_card(s33, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Engineering Best Practices for Orbit Control")
    tb33_strat = s33.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf33_strat = tb33_strat.text_frame
    tf33_strat.word_wrap = True

    p_33 = tf33_strat.paragraphs[0]
    add_text_run(p_33, "1. If Your Controller Oscillates or Diverges Near Target:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_33, "   • Check your feedback gain α. With the plain pseudo-inverse, gains up to about 1.2 converge fastest (3.7 steps at 1.2 vs. 9.4 at 0.45); above that the controller overshoots.\n"
                       "   • Compensate the cubic saturation on the total current from info[\"currents\"]: with gain 1.0 this lands in about 3.7 steps at 924 points.\n"
                       "   • Without compensation, harmonic step damping γ(t) = 1.0 / (1.0 + κ · t) suppresses sensor-noise limit cycles near the target.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2_33 = tf33_strat.add_paragraph()
    add_text_run(p2_33, "2. If Your Neural Surrogate Has High Generalization Error:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_33, "   • Ensure your training dataset covers steerer excitations across [-3.0, +3.0] A so that non-linear cubic saturation is well-sampled.\n"
                        "   • Use ReLU activations and small L2 penalty (alpha=1e-4) to avoid overfitting.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_33 = tf33_strat.add_paragraph()
    add_text_run(p3_33, "3. Real-Time Telemetry Logging:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3_33, "   • Connect your notebook runs to Weights & Biases (wandb.ai) to visualize step-by-step RMS decay against reference baselines on the live leaderboard.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s33, 33)

    # ==========================================
    # SLIDE 34: Summary & Transition to Lecture 2
    # ==========================================
    s34 = prs.slides.add_slide(blank_layout)
    add_header(s34, "Conclusion & Roadmap", "Summary & Transition to Lecture 2",
               "Key conclusions from Lecture 1 and orientation for the upcoming agentic AI session")

    add_card(s34, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Key Takeaways & What Comes Next")
    tb34_sum = s34.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf34_sum = tb34_sum.text_frame
    tf34_sum.word_wrap = True

    p_34 = tf34_sum.paragraphs[0]
    add_text_run(p_34, "Four Core Takeaways from Lecture 1:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p_34, "1. Physics Guides the AI: Analytical optics priors (ORM pseudo-inverse) guarantee early stability and avoid millions of blind exploratory steps.\n"
                       "2. Surrogates Capture Non-Linearities: Compact deep MLPs accurately predict cubic core saturation, enabling 2-step bounded inversions.\n"
                       "3. Probabilistic Uncertainty Wins: Gaussian Process BO with LCB acquisition balances exploration against exploitation, leading the reference scores in about 3.6 steps.\n"
                       "4. Dynamic Damping Prevents Limit Cycles: Attenuating feedback near the 10 μm sensor noise floor locks residual orbit error.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2_34 = tf34_sum.add_paragraph()
    add_text_run(p2_34, "Next Session (10:40 - 12:00):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2_34, "Lecture 2: Agentic AI for Accelerator Research (Osprey Applications)\n", bold=True, size=Pt(16), color=PRIMARY)
    add_text_run(p2_34, "Speaker: Thorsten Hellert, Ph.D. (Lawrence Berkeley National Laboratory)\n"
                        "Topic: Autonomous operational agents, dynamic tool calling, and automated scientific workflows.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3_34 = tf34_sum.add_paragraph()
    add_text_run(p3_34, "Q & A Discussion", bold=True, size=Pt(16), color=ACCENT)

    add_footer(s34, 34)

    # Body-text line spacing per slide: every text box between the header and the footer,
    # excluding tables, so that the text fills its content card (see LINE_SPACING).
    for slide_num, slide in enumerate(prs.slides, start=1):
        spacing = LINE_SPACING.get(slide_num)
        if not spacing:
            continue
        for shape in slide.shapes:
            if not shape.has_text_frame or shape.top < Inches(1.3) or shape.top >= Inches(6.95):
                continue
            for para in shape.text_frame.paragraphs:
                para.line_spacing = spacing

    # Save presentation
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT_PATH))
    print(f"Successfully generated {len(prs.slides)}-slide presentation: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
