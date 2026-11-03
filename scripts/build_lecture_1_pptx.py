"""Build the updated, comprehensive 27-slide PPTX presentation for Lecture 1.

AI Applications in Accelerators Tutorial & Mini-Hackathon
Lecture 1: AI/ML Foundations and Closed-Loop Control for Particle Accelerators
Author: Chong Shik Park, Ph.D. (Korea University, Sejong)
Date: November 3, 2026

Design enhancements:
- Single-column, full-width slide layout to eliminate excessive white space
- Increased font sizes (13-16pt body, 16-18pt section headers, 22-26pt slide titles)
- Generous line spacing and deep domain content
- Title slide redesigned on a clean white background with navy/blue framing (no logo background clash)
- Dedicated full-width slides for large MLP and RL schematics (11.2 - 11.5 inches wide)
- "Tested Leaderboard" branding replacing "Official Leaderboard"
"""

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
NAVY = RGBColor(0, 32, 96)            # Deep Navy (#002060)
PRIMARY = RGBColor(24, 76, 120)       # Primary Blue (#184C78)
ACCENT = RGBColor(41, 128, 185)       # Secondary Accent Blue (#2980B9)
DARK_GRAY = RGBColor(44, 62, 80)      # Text Dark Gray (#2C3E50)
LIGHT_BG = RGBColor(245, 247, 250)    # Shaded Card (#F5F7FA)
BORDER_GRAY = RGBColor(200, 205, 210) # Border Outline (#C8CDD2)
MUTED = RGBColor(127, 140, 141)       # Muted text (#7F8C8D)
WHITE = RGBColor(255, 255, 255)
CRIMSON = RGBColor(158, 22, 54)       # Highlight Red (#9E1636)
SUCCESS_GREEN = RGBColor(39, 174, 96) # Green (#27AE60)
GOLD = RGBColor(180, 140, 20)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)
TOTAL_SLIDES = 27


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
        # KU Logo
        if KU_LOGO.exists():
            slide.shapes.add_picture(str(KU_LOGO), Inches(0.5), Inches(0.2), width=Inches(0.9))

        # Vertical Divider Bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(0.22), Inches(0.06), Inches(0.95))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT

        # Title & Subtitle Box
        tb = slide.shapes.add_textbox(Inches(1.68), Inches(0.18), Inches(11.1), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        if tag_text:
            add_text_run(p0, tag_text.upper() + "  |  ", bold=True, size=Pt(11.5), color=ACCENT)
        add_text_run(p0, title_text, bold=True, size=Pt(22), color=NAVY)

        if subtitle_text:
            p1 = tf.add_paragraph()
            p1.space_before = Pt(3)
            add_text_run(p1, subtitle_text, size=Pt(13.5), color=DARK_GRAY)

    def add_footer(slide, slide_num):
        # Footer dividing line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.0), Inches(12.333), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.color.rgb = BORDER_GRAY

        # Left date
        tb_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(2.5), Inches(0.35))
        tf_l = tb_left.text_frame
        add_text_run(tf_l.paragraphs[0], "November 3, 2026", size=Pt(10), color=MUTED)

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
            add_text_run(tf.paragraphs[0], title, bold=True, size=Pt(16), color=NAVY)
        return shape

    # ==========================================
    # SLIDE 1: Title Slide (Seamless White Background)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)

    # Clean framing border
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

    # KU Logo with seamless white background
    if KU_LOGO.exists():
        s1.shapes.add_picture(str(KU_LOGO), Inches(1.0), Inches(0.9), width=Inches(1.5))

    # Event badge text next to logo
    tb_tag = s1.shapes.add_textbox(Inches(2.8), Inches(1.1), Inches(9.5), Inches(0.9))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    add_text_run(tf_tag.paragraphs[0], "AI APPLICATIONS IN ACCELERATORS TUTORIAL & MINI-HACKATHON", bold=True, size=Pt(14), color=PRIMARY)
    p_tag2 = tf_tag.add_paragraph()
    p_tag2.space_before = Pt(3)
    add_text_run(p_tag2, "Host: KOMAC / KAERI (Korea Multi-purpose Accelerator Complex)", size=Pt(12), color=MUTED)

    # Title line
    line_div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(11.333), Inches(0.02))
    line_div.fill.solid()
    line_div.fill.fore_color.rgb = BORDER_GRAY
    line_div.line.fill.background()

    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(11.333), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    add_text_run(tf_title.paragraphs[0], "Lecture 1: AI/ML Foundations and Closed-Loop Control\nfor Particle Accelerators", bold=True, size=Pt(32), color=NAVY)

    p2_t = tf_title.add_paragraph()
    p2_t.space_before = Pt(12)
    add_text_run(p2_t, "Physics Foundations, Neural Surrogates, Reinforcement Learning, and Bayesian Optimization", size=Pt(18), color=ACCENT)

    # Author & Affiliation Card
    add_card(s1, Inches(1.0), Inches(4.7), Inches(11.333), Inches(1.9), bg_color=LIGHT_BG)
    tb_auth = s1.shapes.add_textbox(Inches(1.3), Inches(4.85), Inches(10.7), Inches(1.6))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True

    add_text_run(tf_auth.paragraphs[0], "Chong Shik Park, Ph.D.", bold=True, size=Pt(20), color=NAVY)

    p_a2 = tf_auth.add_paragraph()
    p_a2.space_before = Pt(5)
    add_text_run(p_a2, "• Department of Accelerator Science, Korea University, Sejong 30019, Republic of Korea\n"
                       "• Center for Accelerator Research, Korea University, Sejong 30019, Republic of Korea", size=Pt(13.5), color=DARK_GRAY)

    p_a3 = tf_auth.add_paragraph()
    p_a3.space_before = Pt(6)
    add_text_run(p_a3, "Date: November 3, 2026   |   Audience: Accelerator Physicists, Postdocs, Engineers & Graduate Students", size=Pt(11.5), color=MUTED)

    add_footer(s1, 1)

    # ==========================================
    # SLIDE 2: Executive Motivation & The Accelerator Challenge
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Operational Context", "Why AI in Modern Particle Accelerators?", 
               "Meeting stringent sub-micron stability tolerances while managing non-linear actuator dynamics")

    add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Operational Challenge: High-Precision Orbit Stabilization")
    tb2 = s2.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    add_text_run(p, "• Extreme Beam Stability Demands:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "  -- Modern synchrotron light sources, colliders, and FELs require transverse orbit stabilization to within < 10% of beam size (sub-micron RMS tolerances).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf2.add_paragraph()
    add_text_run(p2, "• High-Power Hadron Linacs (KOMAC, SNS, ESS):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- Uncorrected trajectory offsets through RF cavities and quadrupoles induce non-linear space-charge forces and beam halo.\n"
                     "  -- Fractional beam loss exceeding 1 W/m (~10⁻⁵ of total beam power) causes severe structural radioactivation, prohibiting hands-on maintenance.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf2.add_paragraph()
    add_text_run(p3, "• Limitations of Purely Classical Linear Control:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "  -- Analytical linear response matrices (ORM) ignore magnetic core saturation at high currents, inducing overshoot and limit cycles.\n"
                     "  -- Physical diagnostics carry 10 μm noise floors; naive feedback amplifies measurement noise into erratic actuator jitter.\n"
                     "  -- Multi-parameter coupling requires fast non-linear digital twins and adaptive closed-loop policies.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s2, 2)

    # ==========================================
    # SLIDE 3: Curricular Architecture & Master Schedule
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Workshop Curriculum", "Integrated Morning Lectures & Afternoon Hackathon",
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
    # SLIDE 4: 5 Pillars of AI in Accelerators (Part 1)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Domain Overview", "Five Pillars of AI in Accelerators (Part 1: Surrogates & Optimization)",
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
    # SLIDE 5: 5 Pillars of AI in Accelerators (Part 2)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Domain Overview", "Five Pillars of AI in Accelerators (Part 2: Diagnostics, Protection & Agents)",
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
    # SLIDE 6: Accelerator Physics Foundations: Hill's Equation
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Physics Foundations", "Transverse Beam Dynamics & Hill's Equation",
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
    # SLIDE 7: Betatron Oscillations & Courant-Snyder Optics
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Beam Optics", "Betatron Oscillations, Beta Function & Betatron Tune",
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
    # SLIDE 8: Orbit Response Matrix (ORM) Derivation
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Analytical Optics", "Derivation of the Orbit Response Matrix (ORM)",
               "Mathematical formulation linking localized steering kicks to downstream BPM readings")

    add_card(s8, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Analytical ORM Transfer Function")
    tb8 = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    add_text_run(p, "Closed-Orbit Perturbation from a Localized Steerer Kick:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "When a steering dipole at position s_j applies an angular kick θ_j = e B L / p, the orbit shift at BPM position s_i is:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf8.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "R_ij = Δx(s_i) / θ_j = [ √(β_i β_j) / (2 sin(π ν)) ] · cos( |ψ_i - ψ_j| - π ν )\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf8.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Global Matrix Superposition Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- For N corrector magnets and M Beam Position Monitors, the linear response is encapsulated as:\n", size=Pt(13.5), color=DARK_GRAY)

    p_mat = tf8.add_paragraph()
    p_mat.alignment = PP_ALIGN.CENTER
    add_text_run(p_mat, "Y_linear = I · R\n", bold=True, size=Pt(18), color=PRIMARY)

    p3 = tf8.add_paragraph()
    add_text_run(p3, "  -- I ∈ ℝ⁶: Vector of corrector coil currents (Amperes), mapped to kicks via magnetic field integration.\n"
                     "  -- R ∈ ℝ⁶ˣ¹²: The linear Orbit Response Matrix (ORM).\n"
                     "  -- Y ∈ ℝ¹²: Transverse displacements measured at all 12 downstream BPM stations.\n"
                     "  -- Cross-plane coupling: Any single corrector deflection alters the entire beam trajectory downstream.", size=Pt(13), color=DARK_GRAY)

    add_footer(s8, 8)

    # ==========================================
    # SLIDE 9: The Hackathon 15-Meter Transport Lattice Architecture
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Hackathon Benchmark", "The 15-Meter Transport Lattice Architecture",
               "Physical arrangement of quadrupole doublets, dipole correctors, and beam position monitors")

    beamline_img = IMG_DIR / "beamline.png"
    if beamline_img.exists():
        s9.shapes.add_picture(str(beamline_img), Inches(0.8), Inches(1.4), width=Inches(11.733))

    add_card(s9, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4), "Transport Line Specifications & Component Placement", bg_color=LIGHT_BG)
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
    # SLIDE 10: Hardware Constraints & Actuator Bounds
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Physical Limits", "Hardware Constraints & Actuator Bounds",
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
    # SLIDE 11: Non-Linear Magnetic Core Saturation
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Non-Linear Physics", "Magnetic Core Saturation & Initial Distortion",
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
                     "  -- Y₀: Initial orbit distortion caused by random quadrupole transverse misalignments (producing 0.40 mm to 1.10 mm RMS error across seeds).\n"
                     "  -- ε: Diagnostic Gaussian measurement jitter (σ = 10 μm).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf11.add_paragraph()
    add_text_run(p3, "• Convergence Target: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "Drive orbit error below RMS < 0.030 mm (30 μm) within 20 control steps.", bold=True, size=Pt(14), color=SUCCESS_GREEN)

    add_footer(s11, 11)

    # ==========================================
    # SLIDE 12: Machine Learning Fundamentals: The Artificial Neuron
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ML Foundations", "Machine Learning Foundations: Artificial Neurons & Layers",
               "Mathematical anatomy of feedforward perceptrons and non-linear activation functions")

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
    add_text_run(p3, "3. Activation Function Selection: Rectified Linear Unit (ReLU):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "   • σ(z) = max(0, z): Yields constant derivative = 1 for z > 0, completely resolving the vanishing gradient problem inherent to sigmoid/tanh activations in deep networks.\n"
                     "   • Computationally ultra-efficient, enabling fast backpropagation.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s12, 12)

    # ==========================================
    # SLIDE 13: Loss Formulation & Adam Optimization
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "ML Foundations", "Loss Functions & The Adam Optimizer",
               "Formulating surrogate objective functions and adaptive gradient descent mechanics")

    add_card(s13, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Objective Formulation and Adaptive Momentum Updates")
    tb13 = s13.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    p = tf13.paragraphs[0]
    add_text_run(p, "Supervised Loss Formulation (Mean Squared Error + L2 Regularization):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "To train a neural surrogate on offline simulation data (I_i, Y_true,i), we minimize the regularized loss:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf13.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "ℒ(θ) = (1 / N) ∑ || Y_true,i - f_θ(I_i) ||²  +  λ ||θ||²\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf13.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "The Adam Optimization Algorithm (Adaptive Moment Estimation):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "• First Moment m_t: Exponentially moving average of gradients (momentum):\n"
                     "  m_t = β₁ m_{t-1} + (1 - β₁) g_t,   (β₁ = 0.9)\n\n"
                     "• Second Moment v_t: Exponentially moving average of squared gradients (adaptive learning scale):\n"
                     "  v_t = β₂ v_{t-1} + (1 - β₂) g_t²,   (β₂ = 0.999)\n\n"
                     "• Parameter Update with Bias Correction:\n"
                     "  θ_{t+1} = θ_t - [ η / ( √(v̂_t) + ε ) ] · m̂_t\n\n"
                     "• Advantage for Accelerators: Automatically adapts individual parameter steps across varying magnet coupling scales without tedious manual learning rate schedules.", size=Pt(13), color=DARK_GRAY)

    add_footer(s13, 13)

    # ==========================================
    # SLIDE 14: Neural Surrogate Digital Twin Architecture (LARGE IMAGE)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Surrogate Modeling", "Neural Surrogate Digital Twin Architecture",
               "Deep Multi-Layer Perceptron (128-64-32) modeling non-linear beam response")

    mlp_img = IMG_DIR / "mlp_schematic.png"
    if mlp_img.exists():
        s14.shapes.add_picture(str(mlp_img), Inches(1.0), Inches(1.4), width=Inches(11.333))

    add_card(s14, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2), bg_color=LIGHT_BG)
    tb14 = s14.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.95))
    tf14 = tb14.text_frame
    tf14.word_wrap = True
    add_text_run(tf14.paragraphs[0], 
                 "• Input Layer: 6 Corrector Magnet Currents [HCM1-3, VCM1-3] in Amperes.\n"
                 "• Hidden Architecture: Dense layers (128 → 64 → 32) with ReLU activations capturing cubic iron-core saturation.\n"
                 "• Output Layer: 12 Beam Position Monitor readings [BPM1-12] in millimeters, evaluated in < 0.2 milliseconds.", 
                 size=Pt(13), color=DARK_GRAY)

    add_footer(s14, 14)

    # ==========================================
    # SLIDE 15: Neural Surrogate Training & Holdout Verification
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Digital Twin Validation", "Surrogate Dataset Generation & Holdout Verification",
               "Ensuring digital twin fidelity across linear and saturated magnetic operating regimes")

    add_card(s15, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Offline Dataset Generation and Model Verification")
    tb15 = s15.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    add_text_run(p, "1. Synthetic Tracking Dataset Generation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "   • 2,000 synthetic simulation runs generated by uniformly sampling corrector currents across I ∈ [-3.0, +3.0]⁶ A.\n"
                    "   • Full non-linear response computed including the cubic soft-saturation term -0.015 · (I³ · R).\n"
                    "   • Dataset partitioned into 80% Training (1,600 samples) and 20% Holdout Testing (400 samples).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf15.add_paragraph()
    add_text_run(p2, "2. MLPRegressor Training Configuration:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "   • Architecture: hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam'.\n"
                    "   • Regularization: alpha=1e-4, max_iter=500, early_stopping=True.\n"
                    "   • Loss convergence reached in under 180 epochs (~3.5 seconds CPU training time).\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf15.add_paragraph()
    add_text_run(p3, "3. Holdout Verification Metrics:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "   • Holdout Test MSE: < 2.5 × 10⁻⁴ mm² across all 12 BPM stations.\n"
                    "   • Sub-Millisecond Execution: Forward inference takes < 0.2 ms per call, 10,000× faster than numerical tracking.", bold=True, size=Pt(13.5), color=PRIMARY)

    add_footer(s15, 15)

    # ==========================================
    # SLIDE 16: Closed-Loop Control Flow Architecture (LARGE IMAGE)
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Closed-Loop Control", "Forward Digital Twin vs Closed-Loop Feedback Flow",
               "Transitioning from predictive surrogate modeling to active closed-loop trajectory correction")

    ctrl_img = IMG_DIR / "forward_sl_and_rl_schematic.png"
    if ctrl_img.exists():
        s16.shapes.add_picture(str(ctrl_img), Inches(0.9), Inches(1.4), width=Inches(11.533))

    add_card(s16, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2), bg_color=LIGHT_BG)
    tb16 = s16.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.95))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    add_text_run(tf16.paragraphs[0], 
                 "• Forward Supervised Model (Top): Maps steerer current commands ΔI to predicted BPM displacement vectors Ŷ.\n"
                 "• Closed-Loop Control Loop (Bottom): Senses true BPM displacement Y, passes error through controller policy, updates magnet power supplies, and repeats until convergence.", 
                 size=Pt(13), color=DARK_GRAY)

    add_footer(s16, 16)

    # ==========================================
    # SLIDE 17: Baseline 0: Classical Linear SVD Controller
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Benchmark Baselines", "Baseline 0: Classical Linear SVD Controller",
               "Inverting the linear Orbit Response Matrix via Moore-Penrose pseudo-inverse")

    add_card(s17, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Mathematical Formulation & Operational Vulnerabilities")
    tb17 = s17.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf17 = tb17.text_frame
    tf17.word_wrap = True

    p = tf17.paragraphs[0]
    add_text_run(p, "Singular Value Decomposition (SVD) Pseudo-Inverse Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "Computes corrective kick vector ΔI directly by inverting the transpose of the linear ORM:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf17.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "ΔI = - α · ( Rᵀ )⁺ · Y_obs,       with ( Rᵀ )⁺ = V Σ⁺ Uᵀ\n", bold=True, size=Pt(17), color=PRIMARY)

    p2 = tf17.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Operational Profile & Limitations:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- Static feedback gain: Typically α ≈ 0.45, with kicks hard clipped to [-0.8, +0.8] A.\n"
                     "  -- Execution latency: < 0.1 ms (instantaneous analytical matrix-vector product).\n"
                     "  -- Vulnerability in Non-Linear Regimes: Completely oblivious to cubic iron core saturation. When magnets operate at high currents, the true response is much weaker than linear R predicts, leading to over-correction, slow convergence (5.6 mean steps), and high final current demands.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf17.add_paragraph()
    add_text_run(p3, "• Tested Benchmark Performance: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "100.0% success rate, 5.6 mean steps, 1,013.1 total score (Rank #3).", bold=True, size=Pt(14), color=PRIMARY)

    add_footer(s17, 17)

    # ==========================================
    # SLIDE 18: Baseline 1: Supervised Neural Inversion
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Benchmark Baselines", "Baseline 1: Supervised Neural Surrogate Inversion",
               "Model-based bounded optimization via SciPy L-BFGS-B on the trained neural digital twin")

    add_card(s18, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Optimization Formulation on Forward Surrogate")
    tb18 = s18.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf18 = tb18.text_frame
    tf18.word_wrap = True

    p = tf18.paragraphs[0]
    add_text_run(p, "Per-Step Bounded Numerical Optimization Problem:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "Instead of inverting an analytical matrix, Baseline 1 leverages the non-linear MLP twin f_θ:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf18.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "min_{ΔI} ℒ(ΔI) = || Y_obs + f_θ(ΔI) ||²  +  λ ||ΔI||²\nsubject to ΔI ∈ [-5.0, +5.0]⁶ A\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf18.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Why Supervised Inversion Outperforms Classical SVD:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- Because f_θ captures the cubic saturation falloff, the optimizer automatically calculates higher current demands for saturated correctors.\n"
                     "  -- Solver: SciPy L-BFGS-B converges in 8-15 iterations per control step (~15 - 25 ms latency).\n"
                     "  -- Result: Slashes convergence time from 5.6 steps (SVD) down to only 2.3 steps average!\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf18.add_paragraph()
    add_text_run(p3, "• Tested Benchmark Performance: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "100.0% success rate, 2.3 mean steps, 1,016.8 total score (Rank #2).", bold=True, size=Pt(14), color=PRIMARY)

    add_footer(s18, 18)

    # ==========================================
    # SLIDE 19: Track 2: Closed-Loop RL with Physics-Informed Priors
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Track 2 Challenge", "Closed-Loop RL with Physics-Informed Priors",
               "Continuous policy networks combining analytical optics priors with learned residual offsets")

    add_card(s19, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Physics-Informed Residual Architecture")
    tb19 = s19.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf19 = tb19.text_frame
    tf19.word_wrap = True

    p = tf19.paragraphs[0]
    add_text_run(p, "Hybrid Residual Policy Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "Rather than learning control from scratch with unguided exploratory random kicks, our agent uses:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf19.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "ΔI(t) = γ(t) · [ - α ( Rᵀ )⁺ Y  +  W_learned Y  +  b ]\n", bold=True, size=Pt(17), color=PRIMARY)

    p2 = tf19.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Architectural Synergy Breakdown:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  1. Analytical Physics Prior ( - α (Rᵀ)⁺ Y ):\n"
                     "     - Anchors the policy in first-principles beam optics.\n"
                     "     - Guarantees immediate coarse stabilization from step 1 without needing millions of trial steps.\n\n"
                     "  2. Learned Residual Offset ( W_learned Y + b ):\n"
                     "     - Neural network learns to predict non-linear saturation compensation.\n"
                     "     - Balances asymmetric horizontal (HCM) and vertical (VCM) steerer authorities dynamically.\n\n"
                     "  3. Execution Latency: < 0.4 ms (pure feedforward matrix multiply, 50× faster than iterative L-BFGS-B).", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s19, 19)

    # ==========================================
    # SLIDE 20: Dynamic Harmonic Step Damping
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Stability Control", "Dynamic Harmonic Step Damping",
               "Preventing sensor-noise amplification and eliminating limit-cycle oscillations")

    add_card(s20, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Resolving the Sensor Noise Feedback Limit Cycle")
    tb20 = s20.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf20 = tb20.text_frame
    tf20.word_wrap = True

    p = tf20.paragraphs[0]
    add_text_run(p, "The Noise Floor Bottleneck:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "• As the orbit converges toward the sub-30 μm target, true orbit errors become comparable to BPM sensor noise (σ = 10 μm).\n"
                    "• Undamped linear feedback interprets stochastic sensor jitter as real trajectory error, commanding vigorous kicks that induce limit cycles around the boundary.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf20.add_paragraph()
    add_text_run(p2, "Harmonic Damping Schedule:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "We modulate the policy kick authority with a dynamic temporal decay schedule:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf20.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "γ(t) = 1.0 / ( 1.0 + κ · t ),       with κ ≈ 0.03\n", bold=True, size=Pt(17), color=PRIMARY)

    p3 = tf20.add_paragraph()
    p3.space_before = Pt(8)
    add_text_run(p3, "• Step 1 (t = 0, γ = 1.0): Full kick authority rapidly suppresses large millimeter-scale initial distortions.\n"
                     "• Step 5+ (t ≥ 4, γ < 0.88): Attenuated feedback prevents sensor jitter amplification, locking the orbit cleanly below 0.030 mm.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s20, 20)

    # ==========================================
    # SLIDE 21: Track 3: Closed-Loop Bayesian Optimization
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Track 3 Challenge", "Closed-Loop Bayesian Optimization with Gaussian Processes",
               "Sample-efficient probabilistic modeling with epistemic uncertainty estimation")

    add_card(s21, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Probabilistic Gaussian Process Modeling")
    tb21 = s21.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf21 = tb21.text_frame
    tf21.word_wrap = True

    p = tf21.paragraphs[0]
    add_text_run(p, "Gaussian Process Surrogate Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "Instead of deterministic point predictions, a GP models a distribution over candidate orbit response functions:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf21.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "Ŷ(ΔI) ~ 𝒢𝒫( m(ΔI), K(ΔI, ΔI') )\n", bold=True, size=Pt(18), color=PRIMARY)

    p2 = tf21.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Composite Physics-Informed Kernel Architecture:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  k(x, x') = k_Matérn-5/2(x, x') + σ_noise² · δ(x, x')\n\n"
                     "  -- Matérn-5/2 Kernel: Captures smooth, non-linear magnetic saturation falloff without imposing the unrealistic infinite differentiability of RBF kernels.\n"
                     "  -- White Noise Kernel: Explicitly accounts for the 10 μm BPM diagnostic jitter floor, avoiding kernel overfitting to noise.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf21.add_paragraph()
    add_text_run(p3, "• Epistemic Uncertainty Estimation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "  -- For any candidate kick ΔI, the GP provides both posterior mean μ_GP(ΔI) and standard deviation σ_GP(ΔI).", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s21, 21)

    # ==========================================
    # SLIDE 22: Lower Confidence Bound (LCB) Acquisition
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Acquisition Function", "Lower Confidence Bound (LCB) Acquisition & Optimization",
               "Balancing exploration of non-linear saturation against exploitation of predicted orbit corrections")

    add_card(s22, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The LCB Acquisition Strategy")
    tb22 = s22.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf22 = tb22.text_frame
    tf22.word_wrap = True

    p = tf22.paragraphs[0]
    add_text_run(p, "Lower Confidence Bound (LCB) Mathematical Formulation:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "At each step, the controller selects kicks by minimizing the LCB acquisition criterion:\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf22.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "α_LCB(ΔI) = RMS( Y_obs + μ_GP(ΔI) )  -  κ · σ̄_GP(ΔI)  +  λ ||ΔI||²\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf22.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "• Parameter Interpretations:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "  -- μ_GP(ΔI): Posterior mean predicted orbit deviation across all 12 BPM stations.\n"
                     "  -- σ̄_GP(ΔI): Posterior epistemic uncertainty (average standard deviation across BPMs).\n"
                     "  -- κ ≥ 0: Exploration coefficient. When κ > 0, the agent explores uncharted high-current regimes; when κ = 0, it exploits the calibrated posterior mean.\n"
                     "  -- λ ||ΔI||²: Regularization penalty that minimizes actuator heating and avoids saturation.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf22.add_paragraph()
    add_text_run(p3, "• Exceptional Convergence Speed: ", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "When calibrated, Track 3 reaches the convergence threshold in an average of only 1.5 steps!", bold=True, size=Pt(14), color=SUCCESS_GREEN)

    add_footer(s22, 22)

    # ==========================================
    # SLIDE 23: Gymnasium Contract (AcceleratorOrbitGymEnv)
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Benchmark Contract", "Gymnasium Environment Specification",
               "Standard Farama Gymnasium API contract governing state, actions, and rewards")

    add_card(s23, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Farama Gymnasium Environment Interface")
    tb23 = s23.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf23 = tb23.text_frame
    tf23.word_wrap = True

    p = tf23.paragraphs[0]
    add_text_run(p, "Standard Gymnasium Method Signatures:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "obs, info = env.reset(seed=seed)\n"
                    "obs, reward, terminated, truncated, info = env.step(action)\n\n", bold=True, size=Pt(14), color=PRIMARY)

    p2 = tf23.add_paragraph()
    add_text_run(p2, "• Observation Space: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p2, "Box(-10.0, +10.0, shape=(12,), dtype=float32) (12 transverse BPM readings in mm).\n", size=Pt(13), color=DARK_GRAY)

    p3 = tf23.add_paragraph()
    add_text_run(p3, "• Action Space: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p3, "Box(-0.8, +0.8, shape=(6,), dtype=float32) (6 per-step delta kicks ΔI in Amperes).\n", size=Pt(13), color=DARK_GRAY)

    p4 = tf23.add_paragraph()
    add_text_run(p4, "• Step Reward Function:\n", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p4, "  r_t = - RMS_{t+1} - 0.01 · ||action||₂ + ( 50.0 if RMS_{t+1} < 0.030 mm else 0.0 )\n", bold=True, size=Pt(13.5), color=PRIMARY)

    p5 = tf23.add_paragraph()
    add_text_run(p5, "• Termination Criteria: ", bold=True, size=Pt(14), color=NAVY)
    add_text_run(p5, "terminated = True when RMS < 0.030 mm (success); truncated = True when step >= 20 (budget exhausted).", size=Pt(13), color=DARK_GRAY)

    add_footer(s23, 23)

    # ==========================================
    # SLIDE 24: Multi-Objective Challenge Scoring Formula
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Evaluation Protocol", "Standardized 30-Seed Scoring Formula",
               "Multi-objective evaluation metric balancing convergence reliability, speed, precision, and power")

    add_card(s24, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "The Official Hackathon Scoring Formula")
    tb24 = s24.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf24 = tb24.text_frame
    tf24.word_wrap = True

    p = tf24.paragraphs[0]
    add_text_run(p, "Standardized Evaluation Suite: seeds = range(1, 31) (30 evaluation seeds)\n\n", size=Pt(13.5), color=DARK_GRAY)

    p_eq = tf24.add_paragraph()
    p_eq.alignment = PP_ALIGN.CENTER
    add_text_run(p_eq, "Score = ( Success Rate × 10.0 )  -  ( 2.0 × Mean_Steps )\n"
                       "        +  [ 0.03 / max(Mean_RMS, 0.005) ] × 20.0  -  ( 2.0 × Mean_||I|| )\n", bold=True, size=Pt(16), color=PRIMARY)

    p2 = tf24.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "Breakdown of the Four Scoring Components:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "1. Success Rate (+10.0 × %): Rewards 100% convergence across all 30 seeds (+1,000.0 pts).\n"
                     "2. Speed Penalty (-2.0 × Steps): Converging in 1.5 steps costs -3.0 pts, while 10 steps costs -20.0 pts.\n"
                     "3. Sub-Micron Precision Bonus (+[0.03 / RMS] × 20.0): Achieving 0.015 mm yields +40.0 pts bonus.\n"
                     "4. Current Economy Penalty (-2.0 × ||I||): Penalizes excessive steerer current norms to protect hardware.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s24, 24)

    # ==========================================
    # SLIDE 25: Tested Benchmark Leaderboard & Trajectories
    # ==========================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "Evaluation Results", "Tested Benchmark Leaderboard & Convergence Trajectories",
               "Verified comparative benchmark results across the 30 standardized evaluation seeds")

    traj_img = IMG_DIR / "benchmark_trajectories.png"
    if traj_img.exists():
        s25.shapes.add_picture(str(traj_img), Inches(0.8), Inches(1.4), width=Inches(11.733))

    add_card(s25, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4), "Tested Benchmark Leaderboard (30 Standardized Seeds)", bg_color=LIGHT_BG)
    tb25 = s25.shapes.add_textbox(Inches(1.1), Inches(4.8), Inches(11.1), Inches(1.8))
    tf25 = tb25.text_frame
    tf25.word_wrap = True

    rows = [
        ("🥇 Rank #1: Track 3 — Bayesian Optimization (BO)", "100.0%", "1.5 steps", "0.0149 mm", "0.93 A", "1,035.4 pts", GOLD),
        ("🥈 Rank #2: Baseline 1 — Supervised Neural Inversion (MLP)", "100.0%", "2.3 steps", "0.0257 mm", "1.21 A", "1,016.8 pts", PRIMARY),
        ("🥉 Rank #3: Baseline 0 — Classical Linear SVD", "100.0%", "5.6 steps", "0.0230 mm", "1.16 A", "1,013.1 pts", DARK_GRAY),
        ("4️⃣ Rank #4: Track 2 — Closed-Loop RL Policy Agent", "100.0%", "6.1 steps", "0.0239 mm", "1.18 A", "1,011.1 pts", DARK_GRAY),
    ]

    for i, (rank, succ, steps, rms, curr, score, col) in enumerate(rows):
        p_r = tf25.paragraphs[0] if i == 0 else tf25.add_paragraph()
        if i > 0:
            p_r.space_before = Pt(3)
        add_text_run(p_r, f"{rank}: ", bold=True, size=Pt(12), color=col)
        add_text_run(p_r, f"Success {succ} | Mean Steps: {steps} | Final RMS: {rms} | Current: {curr} | Score: ", size=Pt(11.5), color=DARK_GRAY)
        add_text_run(p_r, f"{score}", bold=True, size=Pt(12), color=col)

    add_footer(s25, 25)

    # ==========================================
    # SLIDE 26: Strategic Advice for Hackathon Competitors
    # ==========================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "Competitor Strategy", "Strategic Advice & Practical Recipes for the Hackathon",
               "Practical engineering guidance to maximize benchmark score and avoid common failure modes")

    add_card(s26, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Engineering Best Practices for Orbit Control")
    tb26 = s26.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf26 = tb26.text_frame
    tf26.word_wrap = True

    p = tf26.paragraphs[0]
    add_text_run(p, "1. If Your Controller Oscillates or Diverges Near Target:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "   • Check your feedback gain α. Any gain > 0.6 will overcorrect when magnets enter saturated regions.\n"
                    "   • Implement harmonic step damping: γ(t) = 1.0 / (1.0 + κ · t). Attenuating authority at step 4+ eliminates sensor-noise limit cycles.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf26.add_paragraph()
    add_text_run(p2, "2. If Your Neural Surrogate Has High Generalization Error:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "   • Ensure your training dataset covers steerer excitations across [-3.0, +3.0] A so that non-linear cubic saturation is well-sampled.\n"
                    "   • Use ReLU activations and small L2 penalty (alpha=1e-4) to avoid overfitting.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf26.add_paragraph()
    add_text_run(p3, "3. Real-Time Telemetry Logging:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p3, "   • Connect your notebook runs to Weights & Biases (wandb.ai) to visualize step-by-step RMS decay against reference baselines on the live leaderboard.", size=Pt(13.5), color=DARK_GRAY)

    add_footer(s26, 26)

    # ==========================================
    # SLIDE 27: Summary & Transition to Lecture 2
    # ==========================================
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "Conclusion & Roadmap", "Summary Takeaways & Transition to Lecture 2",
               "Key conclusions from Lecture 1 and orientation for the upcoming agentic AI session")

    add_card(s27, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Key Takeaways & What Comes Next")
    tb27 = s27.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.4))
    tf27 = tb27.text_frame
    tf27.word_wrap = True

    p = tf27.paragraphs[0]
    add_text_run(p, "Four Core Takeaways from Lecture 1:\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p, "1. Physics Guides the AI: Analytical optics priors (ORM pseudo-inverse) guarantee early stability and avoid millions of blind exploratory steps.\n"
                    "2. Surrogates Capture Non-Linearities: Compact deep MLPs accurately predict cubic core saturation, enabling 2-step bounded inversions.\n"
                    "3. Probabilistic Uncertainty Wins: Gaussian Process BO with LCB acquisition balances exploration against exploitation, leading tested scores in 1.5 steps.\n"
                    "4. Dynamic Damping Prevents Limit Cycles: Attenuating feedback near the 10 μm sensor noise floor locks residual orbit error.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p2 = tf27.add_paragraph()
    add_text_run(p2, "Next Session (10:40 - 12:00):\n", bold=True, size=Pt(15), color=NAVY)
    add_text_run(p2, "Lecture 2: Agentic AI for Accelerator Research (Osprey Applications)\n", bold=True, size=Pt(16), color=PRIMARY)
    add_text_run(p2, "Speaker: Thorsten Hellert, Ph.D. (Lawrence Berkeley National Laboratory)\n"
                    "Topic: Autonomous operational agents, dynamic tool calling, and automated scientific workflows.\n\n", size=Pt(13.5), color=DARK_GRAY)

    p3 = tf27.add_paragraph()
    add_text_run(p3, "Q & A Discussion", bold=True, size=Pt(16), color=ACCENT)

    add_footer(s27, 27)

    # Save presentation
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT_PATH))
    print(f"Successfully generated 27-slide presentation: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
