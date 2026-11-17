#!/usr/bin/env python3
"""Build the 12-slide PPTX presentation for Session 2: Mini-Hackathon.

AI Applications in Accelerators Tutorial & Mini-Hackathon
Session 2: Beam Orbit Alignment Mini-Hackathon
Author: Chong Shik Park, Ph.D. (Korea University, Sejong)
Date: November 19, 2026
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
BEAMLINE_IMG = IMG_DIR / "beamline.png"
OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "presentations" / "Mini_Hackathon_Beam_Orbit_Alignment_Slides.pptx"

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
TOTAL_SLIDES = 10


def add_text_run(paragraph, text, bold=False, size=None, color=None, font_name=None):
    run = paragraph.add_run()
    run.text = text
    run.font.bold = bold
    if size is not None:
        run.font.size = size
    if color is not None:
        run.font.color.rgb = color
    if font_name is not None:
        run.font.name = font_name
    return run


def create_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        if KU_LOGO.exists():
            slide.shapes.add_picture(str(KU_LOGO), Inches(0.50), Inches(0.29), width=Inches(0.70), height=Inches(0.82))

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.35), Inches(0.25), Inches(0.06), Inches(0.90))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT

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
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.0), Inches(12.333), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.color.rgb = BORDER_GRAY

        tb_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(2.5), Inches(0.35))
        tf_l = tb_left.text_frame
        add_text_run(tf_l.paragraphs[0], "November 19, 2026", size=Pt(10), color=MUTED)

        tb_center = slide.shapes.add_textbox(Inches(3.0), Inches(7.05), Inches(7.333), Inches(0.35))
        tf_c = tb_center.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        add_text_run(p_c, "Chong Shik Park, Ph.D.  |  Korea University, Sejong  |  Mini-Hackathon Session", size=Pt(10), color=MUTED)

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

    def add_code_card(slide, left, top, width, height, code_lines):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = WHITE
        shape.line.color.rgb = BORDER_GRAY
        shape.line.width = Pt(0.9)

        tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.10), width - Inches(0.3), height - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for i, line in enumerate(code_lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            add_text_run(p, line, size=Pt(9.5), color=DARK_GRAY, font_name="Courier New")
        return shape

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    border = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.5), Inches(12.333), Inches(6.5))
    border.fill.solid()
    border.fill.fore_color.rgb = WHITE
    border.line.color.rgb = PRIMARY
    border.line.width = Pt(2)

    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), Inches(12.333), Inches(0.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ACCENT
    top_bar.line.fill.background()

    if KU_LOGO.exists():
        s1.shapes.add_picture(str(KU_LOGO), Inches(1.0), Inches(0.85), width=Inches(0.95))

    tb_sub = s1.shapes.add_textbox(Inches(2.1), Inches(0.90), Inches(10.2), Inches(0.8))
    tf_sub = tb_sub.text_frame
    p_inst = tf_sub.paragraphs[0]
    add_text_run(p_inst, "AI Applications in Accelerators Tutorial & Mini-Hackathon", bold=True, size=Pt(13), color=PRIMARY)
    p_dept = tf_sub.add_paragraph()
    p_dept.space_before = Pt(3)
    add_text_run(p_dept, "Department of Accelerator Science · Center for Accelerator Research · Korea University, Sejong", size=Pt(11), color=MUTED)

    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.0), Inches(11.333), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = BORDER_GRAY
    div.line.fill.background()

    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.25), Inches(11.333), Inches(1.0))
    tf_t = tb_title.text_frame
    p_title = tf_t.paragraphs[0]
    add_text_run(p_title, "Session 2: Beam Orbit Alignment Mini-Hackathon", bold=True, size=Pt(26), color=NAVY)
    p_desc = tf_t.add_paragraph()
    p_desc.space_before = Pt(5)
    add_text_run(p_desc, "Closed-Loop Neural Surrogates, Reinforcement Learning, and Bayesian Optimization", size=Pt(15), color=ACCENT)

    add_card(s1, Inches(1.0), Inches(3.3), Inches(11.333), Inches(2.2))
    tb_c = s1.shapes.add_textbox(Inches(1.3), Inches(3.55), Inches(10.7), Inches(1.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p1 = tf_c.paragraphs[0]
    add_text_run(p1, "Challenge Objective: ", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p1, "Stabilize an unknown distorted beam orbit in a non-linear 15-meter transport line to sub-30 µm RMS precision within a 50-step budget, using constrained magnetic actuators under cubic core saturation.", size=Pt(13.5), color=DARK_GRAY)
    p2 = tf_c.add_paragraph()
    p2.space_before = Pt(8)
    add_text_run(p2, "Unified Benchmark: ", bold=True, size=Pt(13.5), color=NAVY)
    add_text_run(p2, "Participants develop and evaluate four competitor controllers simultaneously (Baseline 0, Baseline 1, Track 2, and Track 3) across 30 standardized seeds with live Weights & Biases leaderboard telemetry.", size=Pt(13.5), color=DARK_GRAY)

    tb_meta = s1.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.333), Inches(0.8))
    tf_m = tb_meta.text_frame
    p_org = tf_m.paragraphs[0]
    add_text_run(p_org, "Organizer & Session Lead: ", bold=True, size=Pt(12.5), color=DARK_GRAY)
    add_text_run(p_org, "Chong Shik Park, Ph.D.  |  Korea University, Sejong", size=Pt(12.5), color=DARK_GRAY)
    p_dt = tf_m.add_paragraph()
    p_dt.space_before = Pt(3)
    add_text_run(p_dt, "Date & Venue: ", bold=True, size=Pt(12.5), color=DARK_GRAY)
    add_text_run(p_dt, "November 19, 2026  |  Hands-on Computational Session (13:30 – 17:00 KST)", size=Pt(12.5), color=DARK_GRAY)

    # ==========================================
    # SLIDE 2: Afternoon Schedule & Milestones
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Schedule & Roadmap", "Afternoon Mini-Hackathon Timeline (13:30 – 17:00)", "Open hands-on optimization: participants can run and iterate on all tracks simultaneously")
    add_footer(s2, 2)

    add_card(s2, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Mini-Hackathon Operational Milestones")

    rows, cols = 5, 3
    left, top, width, height = Inches(1.1), Inches(2.15), Inches(11.1), Inches(4.0)
    tbl_shape = s2.shapes.add_table(rows, cols, left, top, width, height)
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(2.8)
    tbl.columns[2].width = Inches(6.1)

    headers = ["Time Window", "Session Milestone", "Operational Focus & Hands-on Activities"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        cell.text_frame.margin_left = cell.text_frame.margin_top = cell.text_frame.margin_right = cell.text_frame.margin_bottom = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        add_text_run(p, h, bold=True, size=Pt(11.5), color=WHITE)

    schedule_data = [
        ("13:30 – 13:45 (15 min)", "Environment & Setup", "Unpack offline bundle, launch Docker container via launcher scripts, open participant notebook, set TEAM_NAME, and verify Baseline 0 reference."),
        ("13:45 – 16:15 (2.5 hrs)", "Multi-Track Optimization (Open Hackathon)", "Open development window: participants develop, tune, and benchmark all tracks concurrently without sequential restrictions (surrogate, RL, BO, and callbacks)."),
        ("16:15 – 16:30 (15 min)", "Final Submission & Score Freeze", "Execute final 30-seed benchmark in Step 5, confirm telemetry on live W&B leaderboard, and inspect trajectory alignment plots."),
        ("16:30 – 17:00 (30 min)", "Showcase & Awards Ceremony", "3-minute lightning presentations per team, live leaderboard review, and presentation of hackathon champion awards."),
    ]
    for i, (col0, col1, col2) in enumerate(schedule_data):
        row_idx = i + 1
        bg = WHITE if i % 2 == 0 else LIGHT_BG
        for j, val in enumerate([col0, col1, col2]):
            cell = tbl.cell(row_idx, j)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.margin_left = cell.text_frame.margin_top = cell.text_frame.margin_right = cell.text_frame.margin_bottom = Inches(0.08)
            p = cell.text_frame.paragraphs[0]
            bold = True if j < 2 else False
            color = PRIMARY if j == 0 and i < 3 else (GOLD if j == 0 else DARK_GRAY)
            add_text_run(p, val, bold=bold, size=Pt(11), color=color)

    # ==========================================
    # SLIDE 3: Environment & Setup (Offline Bundle & Container Execution)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Environment & Setup", "Offline Bundle Structure & Container Execution", "Zero-dependency offline distribution, one-click platform launchers, and container workspace")
    add_footer(s3, 3)

    # Left Card: Bundle Structure
    add_card(s3, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "Offline Distribution Package Structure")
    tb_s3lt = s3.shapes.add_textbox(Inches(1.05), Inches(2.00), Inches(5.2), Inches(0.55))
    tf_s3lt = tb_s3lt.text_frame
    tf_s3lt.word_wrap = True
    p_s3lta = tf_s3lt.paragraphs[0]
    add_text_run(p_s3lta, "100% Self-Contained Offline Bundle (ai4acc-hackathon.zip):\n", bold=True, size=Pt(11.5), color=NAVY)
    add_text_run(p_s3lta, "Everything required to run the hackathon is pre-packaged locally:", size=Pt(10.5), color=DARK_GRAY)

    code_s3l = [
        "ai4acc-hackathon/",
        "|-- ai4acc-image.tar.gz       # Docker image (~400 MB)",
        "|-- run_hackathon_windows.bat # Windows launcher",
        "|-- run_hackathon_mac_linux.sh# macOS/Linux launcher",
        "|-- wandb.apikey             # Shared W&B key",
        "|-- image-id.txt             # Image cache hash",
        "`-- README.txt               # Offline instructions",
    ]
    add_code_card(s3, Inches(1.05), Inches(2.62), Inches(5.2), Inches(1.60), code_s3l)

    tb_s3lb = s3.shapes.add_textbox(Inches(1.05), Inches(4.35), Inches(5.2), Inches(2.15))
    tf_s3lb = tb_s3lb.text_frame
    tf_s3lb.word_wrap = True
    items_s3l = [
        ("• No Downloads Needed: ", "The image loads from the bundle. Internet is needed only for the live leaderboard; without it, scores are reported locally."),
        ("• Pre-Configured Telemetry: ", "The launcher automatically injects wandb.apikey as WANDB_API_KEY for live leaderboard sync."),
        ("• Pre-Loaded Environment: ", "Python 3.12, scikit-learn, Gymnasium, JupyterLab and the simulation, plus the lecture PDFs, the modification and callback guides, and a transfer-matrix companion notebook."),
    ]
    for i, (hd, body) in enumerate(items_s3l):
        p = tf_s3lb.paragraphs[0] if i == 0 else tf_s3lb.add_paragraph()
        p.space_before = Pt(5) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(11), color=NAVY)
        add_text_run(p, body, size=Pt(10), color=DARK_GRAY)

    # Right Card: How to Launch Docker
    add_card(s3, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "How to Launch Docker & JupyterLab")
    tb_s3rt = s3.shapes.add_textbox(Inches(7.05), Inches(2.00), Inches(5.2), Inches(0.55))
    tf_s3rt = tb_s3rt.text_frame
    tf_s3rt.word_wrap = True
    p_s3rta = tf_s3rt.paragraphs[0]
    add_text_run(p_s3rta, "Step 1: Ensure Docker Desktop is Running\n", bold=True, size=Pt(11.5), color=NAVY)
    add_text_run(p_s3rta, "Verify Docker Desktop is active (whale icon in system tray).", size=Pt(10.5), color=DARK_GRAY)

    code_s3r = [
        "# Windows: Double-click launcher",
        "run_hackathon_windows.bat",
        "",
        "# macOS / Linux (in terminal):",
        "./run_hackathon_mac_linux.sh",
        "# Browser opens automatically: http://localhost:8888/lab",
    ]
    add_code_card(s3, Inches(7.05), Inches(2.62), Inches(5.2), Inches(1.60), code_s3r)

    tb_s3rb = s3.shapes.add_textbox(Inches(7.05), Inches(4.35), Inches(5.2), Inches(2.15))
    tf_s3rb = tb_s3rb.text_frame
    tf_s3rb.word_wrap = True
    items_s3r = [
        ("• Step 2: Instant Browser Access: ", "JupyterLab opens automatically in your browser. Token authentication is disabled for instant entry."),
        ("• Step 3: Open Participant Notebook: ", "In the JupyterLab file browser, open Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb."),
        ("★ Step 4: Configure Team Name: ", "Set your team name in Step 0: TEAM_NAME = 'Team_Alpha' before running Baseline 0!"),
    ]
    for i, (hd, body) in enumerate(items_s3r):
        p = tf_s3rb.paragraphs[0] if i == 0 else tf_s3rb.add_paragraph()
        p.space_before = Pt(5) if i > 0 else Pt(0)
        color = PRIMARY if "★" in hd else NAVY
        add_text_run(p, hd, bold=True, size=Pt(11), color=color)
        add_text_run(p, body, size=Pt(10), color=DARK_GRAY)

    # ==========================================
    # SLIDE 4: The Four Benchmark Controllers
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Benchmark Controllers", "The Four Competitor Control Paradigms", "From classical pseudo-inverse baseline to neural surrogates, RL policies, and Bayesian optimization")
    add_footer(s4, 4)
    add_card(s4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Comparative Controller Specifications")

    rows, cols = 5, 4
    left, top, width, height = Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.3)
    tbl4_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    tbl4 = tbl4_shape.table
    tbl4.columns[0].width = Inches(2.2)
    tbl4.columns[1].width = Inches(2.3)
    tbl4.columns[2].width = Inches(4.6)
    tbl4.columns[3].width = Inches(2.0)

    headers4 = ["Controller Track", "Algorithmic Law", "Mechanism & Optimization", "Benchmark Score"]
    for j, h in enumerate(headers4):
        cell = tbl4.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        cell.text_frame.margin_left = cell.text_frame.margin_top = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        add_text_run(p, h, bold=True, size=Pt(12), color=WHITE)

    ctrl_data = [
        ("Baseline 0\nClassical Linear SVD", "ΔI = -α (Rᵀ)⁺ Y", "Moore-Penrose pseudo-inverse with fixed gain α=0.45. Ignores saturation; oscillates at high gains.", "635.277 pts\n(9.4 steps, 100% succ)"),
        ("Baseline 1 / Track 1\nSupervised Surrogate", "min_ΔI ||Y - f_θ(I) + f_θ(I+ΔI)||²", "Trains MLP digital twin Ŷ = f_θ(I) on offline shots; per-step SciPy L-BFGS-B bounded inversion.", "779.169 pts\n(Tuned: 924.192 pts)"),
        ("Track 2\nClosed-Loop Policy RL", "ΔI = d(t)[-α (Rᵀ)⁺ Y + WY + b]", "Physics-informed prior + learned residual with dynamic damping schedule d(t) = 1/(1+γt).", "590.559 pts\n(Tuned: 939.981 pts)"),
        ("Track 3\nBayesian Optimization", "min_ΔI RMS(Y − μ(I) + μ(I+ΔI)) − κ σ̄ + λ ||ΔI||²", "GaussianProcessRegressor (Matérn-5/2) with Lower Confidence Bound (LCB) under epistemic uncertainty.", "878.384 pts\n(Tuned: 909.942 pts)"),
    ]
    for i, (col0, col1, col2, col3) in enumerate(ctrl_data):
        row_idx = i + 1
        bg = WHITE if i % 2 == 0 else LIGHT_BG
        for j, val in enumerate([col0, col1, col2, col3]):
            cell = tbl4.cell(row_idx, j)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.margin_left = cell.text_frame.margin_top = Inches(0.06)
            p = cell.text_frame.paragraphs[0]
            bold = True if j == 0 or j == 3 else False
            color = NAVY if j == 0 else (PRIMARY if j == 3 else DARK_GRAY)
            add_text_run(p, val, bold=bold, size=Pt(11), color=color)

    # ==========================================
    # SLIDE 5: Official Scoring Formula
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Evaluation & Scoring", "Official Hackathon Scoring Formula (0 to 1000 Points)", "Balancing robust convergence, rapid iteration speed, and landing precision")
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "Mathematical Scoring Formulation")
    tb_s5l = s5.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s5l = tb_s5l.text_frame
    tf_s5l.word_wrap = True
    p_score = tf_s5l.paragraphs[0]
    add_text_run(p_score, "• Overall Score: ", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_score, "Score = (1/30) ∑ s_k\nEvaluated strictly across 30 standardized seeds (seeds = range(1, 31)).\n\n", size=Pt(12.5), color=DARK_GRAY)
    p_sk = tf_s5l.add_paragraph()
    add_text_run(p_sk, "• Per-Seed Score s_k Breakdown:\n", bold=True, size=Pt(13), color=NAVY)
    add_text_run(p_sk, "s_k = 0  if seed fails (≥ 50 steps or RMS ≥ 0.030 mm).\nIf seed succeeds in n_k steps with final RMS_k:\n\n", size=Pt(12), color=DARK_GRAY)
    add_text_run(p_sk, "s_k = 400 (Success)\n    + 300 · max(0, (20 - n_k)/19)  [Speed]\n    + 300 · clip(ln(0.030/RMS_k)/ln(3), 0, 1)  [Precision]", bold=True, size=Pt(12), color=PRIMARY)

    add_card(s5, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Component Analysis & Strategic Trade-offs")
    tb_s5r = s5.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s5r = tb_s5r.text_frame
    tf_s5r.word_wrap = True
    items_s5r = [
        ("1. Success Foundation (400 pts):\n", "Robustness is paramount. A single divergence sets seed score to 0 and costs 33.3 total benchmark points."),
        ("2. Speed Component (up to 300 pts):\n", "Full 300 pts earned at 1 step; decays linearly to 0 at 20 steps. Each saved step earns ~15.8 points."),
        ("3. Precision Component (up to 300 pts):\n", "Logarithmic bonus for landing closer to the noise floor. Earns 0 at 0.030 mm boundary, up to 300 pts at 0.010 mm sensor noise floor (0.017 mm earns ~150 pts)."),
        ("Current Norm:\n", "Reported in telemetry but not scored."),
    ]
    for i, (hd, body) in enumerate(items_s5r):
        p = tf_s5r.paragraphs[0] if i == 0 else tf_s5r.add_paragraph()
        p.space_before = Pt(6) if i > 0 else Pt(0)
        color = MUTED if "Norm" in hd else NAVY
        add_text_run(p, hd, bold=True, size=Pt(12.5), color=color)
        p_b = tf_s5r.add_paragraph()
        add_text_run(p_b, body, size=Pt(11.5), color=DARK_GRAY)

    # ==========================================
    # SLIDE 6: Participant Modification Rules
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Modification Rules", "What Participants CAN and CANNOT Modify", "Clear operational boundary preserving scientific ground truth while maximizing design freedom")
    add_footer(s6, 6)

    add_card(s6, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "Permitted Modifications [CAN MODIFY]")
    tb_s6l = s6.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s6l = tb_s6l.text_frame
    tf_s6l.word_wrap = True
    items_s6l = [
        ("✓ TODO 1 (Surrogate Digital Twin):\n", "MLP hidden layers (e.g. (128, 64, 32)), activation (relu, tanh), solver (adam, lbfgs), training samples (n=1500 → 3000), current bounds [-3.0, 3.0] A."),
        ("✓ TODO 2 (Track 2 RL Policy Agent):\n", "Full act() design: starting gain α₀, adaptive gain schedules, residual weights W, saturation compensation on I_t, chatter damping."),
        ("✓ TODO 3 (Track 3 Bayesian Optimization):\n", "GP kernel specification (Matern52, WhiteKernel), calibration shots, acquisition exploration κ, regularizer λ."),
        ("✓ Step 4 Callbacks:\n", "Register step_callback and episode_callback for B1, Track 2, and Track 3."),
    ]
    for i, (hd, body) in enumerate(items_s6l):
        p = tf_s6l.paragraphs[0] if i == 0 else tf_s6l.add_paragraph()
        p.space_before = Pt(6) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(12), color=SUCCESS_GREEN)
        p_b = tf_s6l.add_paragraph()
        add_text_run(p_b, body, size=Pt(11.5), color=DARK_GRAY)

    add_card(s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Strict Ground Truth Boundaries [DO NOT MODIFY]")
    tb_s6r = s6.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s6r = tb_s6r.text_frame
    tf_s6r.word_wrap = True
    items_s6r = [
        ("✗ Baseline 0 Reference:\n", "The gain=0.45 and classical SVD formulation must not be altered. Baseline 0 always runs without callbacks."),
        ("✗ Physical Simulation Ground Truths:\n", "Do not modify R, target RMS = 0.030 mm, max_steps = 50, cubic saturation factor 0.015, or noise σ = 0.010 mm."),
        ("✗ Evaluation Protocol:\n", "Benchmark evaluation must run on standardized seeds range(1, 31) via the locked Step 5 harness."),
        ("✗ Action Hardware Limits:\n", "Actions must respect [-0.8, +0.8] A per step and total magnet current limits [-5.0, +5.0] A."),
    ]
    for i, (hd, body) in enumerate(items_s6r):
        p = tf_s6r.paragraphs[0] if i == 0 else tf_s6r.add_paragraph()
        p.space_before = Pt(6) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(12), color=CRIMSON)
        p_b = tf_s6r.add_paragraph()
        add_text_run(p_b, body, size=Pt(11.5), color=DARK_GRAY)

    # ==========================================
    # SLIDE 7: Advanced Strategy: Callbacks (FIXED BALANCED)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Strategic Tuning", "Online Callbacks: Mechanics & Measured Effects", "Hooks after every step and every seed; always reset what you change, and measure the result")
    add_footer(s7, 7)

    # Left Card: Step Callback
    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "Step Callback: Runs After Every Step")
    tb_s7lt = s7.shapes.add_textbox(Inches(1.05), Inches(2.00), Inches(5.2), Inches(0.55))
    tf_s7lt = tb_s7lt.text_frame
    tf_s7lt.word_wrap = True
    p_s7lta = tf_s7lt.paragraphs[0]
    add_text_run(p_s7lta, "Adaptive Near-Target Damping (step_callback):\n", bold=True, size=Pt(11.5), color=NAVY)
    add_text_run(p_s7lta, "Reduce the gain near the target (needs the reset on the right):", size=Pt(10.5), color=DARK_GRAY)

    code_s7l = [
        "def my_step_callback(step_data, agent):",
        "    rms = step_data[\"info\"][\"rms\"]",
        "    if rms < 0.040 and hasattr(agent, \"gain\"): ",
        "        agent.gain *= 0.94  # brake near the target",
    ]
    add_code_card(s7, Inches(1.05), Inches(2.62), Inches(5.2), Inches(1.45), code_s7l)

    tb_s7lb = s7.shapes.add_textbox(Inches(1.05), Inches(4.25), Inches(5.2), Inches(2.25))
    tf_s7lb = tb_s7lb.text_frame
    tf_s7lb.word_wrap = True

    items_s7l = [
        ("• Measured:\n", "This pair is about neutral (744 vs. 747 points). Without the reset it scores 323 (53% success): the gain keeps shrinking from seed to seed."),
        ("• Step Telemetry Access:\n", "step_data exposes 'step', 'obs', 'action', and 'info' ('rms' and total 'currents')."),
        ("• What helped:\n", "Refitting the Track 3 GP online from a step callback: 882.9 vs. 878.4. Throttling above 2.5 A lowered the score."),
    ]
    for i, (hd, body) in enumerate(items_s7l):
        p = tf_s7lb.paragraphs[0] if i == 0 else tf_s7lb.add_paragraph()
        p.space_before = Pt(5) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(11), color=NAVY)
        p_b = tf_s7lb.add_paragraph()
        add_text_run(p_b, body, size=Pt(10), color=DARK_GRAY)

    # Right Card: Episode Callback
    add_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Episode Callback: Runs After Every Seed")
    tb_s7rt = s7.shapes.add_textbox(Inches(7.05), Inches(2.00), Inches(5.2), Inches(0.55))
    tf_s7rt = tb_s7rt.text_frame
    tf_s7rt.word_wrap = True
    p_s7rta = tf_s7rt.paragraphs[0]
    add_text_run(p_s7rta, "Per-Seed State Reset (episode_callback):\n", bold=True, size=Pt(11.5), color=NAVY)
    add_text_run(p_s7rta, "Restore the starting gain and any per-episode state between seeds:", size=Pt(10.5), color=DARK_GRAY)

    code_s7r = [
        "def my_episode_callback(ep_data, agent):",
        "    if hasattr(agent, \"gain\"): ",
        "        agent.gain = 1.05  # the gain b2 was created with",
    ]
    add_code_card(s7, Inches(7.05), Inches(2.62), Inches(5.2), Inches(1.45), code_s7r)

    tb_s7rb = s7.shapes.add_textbox(Inches(7.05), Inches(4.25), Inches(5.2), Inches(2.25))
    tf_s7rb = tb_s7rb.text_frame
    tf_s7rb.word_wrap = True

    items_s7r = [
        ("• Cross-Seed Tuning:\n", "Adapting the gain from earlier seeds is allowed. Check that your rules actually fire, and compare with a better constant gain."),
        ("• Episode Telemetry Access:\n", "ep_data exposes 'seed', 'final_rms', 'steps', 'is_success', and 'current_norm'."),
        ("• Disclosure Rule:\n", "Any cross-seed state retention must be disclosed during your team's 3-minute lightning presentation!"),
    ]
    for i, (hd, body) in enumerate(items_s7r):
        p = tf_s7rb.paragraphs[0] if i == 0 else tf_s7rb.add_paragraph()
        p.space_before = Pt(5) if i > 0 else Pt(0)
        color = CRIMSON if "Disclosure" in hd else NAVY
        add_text_run(p, hd, bold=True, size=Pt(11), color=color)
        p_b = tf_s7rb.add_paragraph()
        add_text_run(p_b, body, size=Pt(10), color=DARK_GRAY)

    # ==========================================
    # SLIDE 8: Zero-Friction W&B Workflow (FIXED)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Live Leaderboard", "Zero-Friction Weights & Biases Workflow", "Automated telemetry streaming, 30-seed breakdown tables, and real-time competition standings")
    add_footer(s8, 8)

    # Left Card: Authentication Setup
    add_card(s8, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "Zero-Friction Authentication Setup")
    tb_s8lt = s8.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(1.5))
    tf_s8lt = tb_s8lt.text_frame
    tf_s8lt.word_wrap = True
    p_s8lta = tf_s8lt.paragraphs[0]
    add_text_run(p_s8lta, "• No W&B Account Required:\n", bold=True, size=Pt(12.5), color=NAVY)
    add_text_run(p_s8lta, "The offline distribution bundle contains the shared leaderboard key in wandb.apikey. Launchers pass it automatically.\n\n", size=Pt(12), color=DARK_GRAY)
    p_s8ltb = tf_s8lt.add_paragraph()
    add_text_run(p_s8ltb, "• Step 0: Set Team Identifier:\n", bold=True, size=Pt(12.5), color=NAVY)
    add_text_run(p_s8ltb, "In Step 0 of the notebook, configure your unique team name:", size=Pt(12), color=DARK_GRAY)

    code_s8 = [
        "TEAM_NAME = \"Team_Alpha\"",
        "WANDB_PROJECT = \"ai4acc-mini-hackathon-2026\"",
    ]
    add_code_card(s8, Inches(1.05), Inches(3.7), Inches(5.2), Inches(1.0), code_s8)

    tb_s8lb = s8.shapes.add_textbox(Inches(1.05), Inches(4.95), Inches(5.2), Inches(1.5))
    tf_s8lb = tb_s8lb.text_frame
    tf_s8lb.word_wrap = True
    p_s8lba = tf_s8lb.paragraphs[0]
    add_text_run(p_s8lba, "• Seamless Local Fallback:\n", bold=True, size=Pt(12.5), color=NAVY)
    add_text_run(p_s8lba, "If offline or in isolated network environments, the benchmark executes locally and prints complete scorecard tables.", size=Pt(12), color=DARK_GRAY)

    # Right Card: Leaderboard & Telemetry
    add_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Automated Telemetry & Live Leaderboard")
    tb_s8r = s8.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s8r = tb_s8r.text_frame
    tf_s8r.word_wrap = True
    items_s8r = [
        ("• Step 5 Benchmark Execution:\n", "Running Step 5 evaluates all 4 controllers across seeds 1–30 simultaneously and streams telemetry to W&B."),
        ("• Tracked Metrics in W&B:\n", "challenge_score, score_success, score_speed, score_precision, mean_steps, mean_final_rms_mm, seed_breakdown_table."),
        ("• Central Live Leaderboard URL:\n", "https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026\nSort by challenge_score to view live workshop ranks!"),
    ]
    for i, (hd, body) in enumerate(items_s8r):
        p = tf_s8r.paragraphs[0] if i == 0 else tf_s8r.add_paragraph()
        p.space_before = Pt(8) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(12.5), color=NAVY)
        p_b = tf_s8r.add_paragraph()
        color = PRIMARY if "https" in body else DARK_GRAY
        add_text_run(p_b, body, size=Pt(12), color=color)

    # ==========================================
    # SLIDE 9: Team Lightning Showcase & Awards
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Showcase & Awards", "Team Lightning Presentations & Hackathon Awards (16:30 – 17:00)", "Celebrating technical excellence, control innovation, and practical beam alignment performance")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3), "3-Minute Lightning Team Presentations")
    tb_s9l = s9.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s9l = tb_s9l.text_frame
    tf_s9l.word_wrap = True
    items_s9l = [
        ("Presentation Format: ", "3 minutes per team directly from your laptop or W&B run dashboard."),
        ("1. Architecture Overview: ", "Which track did you focus on? (MLP surrogate, RL policy, or Bayesian Opt?)"),
        ("2. Strategic Innovations: ", "What hyperparameter, damping schedule, or callback gave your biggest score boost?"),
        ("3. Scorecard Display: ", "Display your team's W&B run URL and trajectory plot (img/benchmark_trajectories.png)."),
        ("4. Architectural Disclosure: ", "Did your agent use callbacks or cross-seed memory?"),
    ]
    for i, (hd, body) in enumerate(items_s9l):
        p = tf_s9l.paragraphs[0] if i == 0 else tf_s9l.add_paragraph()
        p.space_before = Pt(6) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(12), color=NAVY)
        p_b = tf_s9l.add_paragraph()
        add_text_run(p_b, body, size=Pt(11.5), color=DARK_GRAY)

    add_card(s9, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Official Hackathon Award Categories")
    tb_s9r = s9.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.3))
    tf_s9r = tb_s9r.text_frame
    tf_s9r.word_wrap = True
    awards = [
        ("[Grand Champion Award]\n", "Highest official benchmark score across all 30 seeds.", GOLD),
        ("[Speed Demon Award]\n", "Fastest average convergence step count among robust controllers achieving 100% success rate.", PRIMARY),
        ("[Sub-Micron Precision Master]\n", "Lowest mean residual orbit error (RMS closest to the 0.010 mm electronic noise floor).", ACCENT),
        ("[Most Innovative Control Policy]\n", "Most creative algorithm design, physics prior integration, or novel callback architecture.", CRIMSON),
    ]
    for i, (hd, body, col) in enumerate(awards):
        p = tf_s9r.paragraphs[0] if i == 0 else tf_s9r.add_paragraph()
        p.space_before = Pt(8) if i > 0 else Pt(0)
        add_text_run(p, hd, bold=True, size=Pt(13), color=col)
        p_b = tf_s9r.add_paragraph()
        add_text_run(p_b, body, size=Pt(12), color=DARK_GRAY)

    # ==========================================
    # SLIDE 10: Hands-on Execution Checklist (Concurrent Tracks)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Execution Checklist", "Ready, Set, Align! Hands-on Participant Action Plan", "Five key computational milestones to guide your development during the mini-hackathon")
    add_footer(s10, 10)
    add_card(s10, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3), "Your 5-Step Hackathon Roadmap (Run All Tracks Concurrently)")

    tb_s10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.3))
    tf_s10 = tb_s10.text_frame
    tf_s10.word_wrap = True
    roadmap = [
        ("Phase 1: Environment Launch & Baseline Check (Step 0–2)\n", "Double-click launcher → open http://localhost:8888 → run Steps 0–2 → verify Baseline 0 reference (~635 pts)."),
        ("Phase 2: Simultaneous Controller Tuning (Step 3 & 4: Work on any or all tracks concurrently)\n", "• Track 1: Improve the MLP surrogate in TODO 1 (try activation='tanh', solver='lbfgs'); holdout RMSE near 0.012 mm → B1 scores about 900 pts.\n• Track 2: In TODO 2, increase initial gain (α ≈ 1.0), compensate cubic saturation on I_t, apply step damping → verify >900 pts.\n• Track 3: In TODO 3, tune GP Matérn kernel, acquisition exploration κ, and regularizer λ → verify BO controller.\n• Step 4 Callbacks: Optional. Always pair a gain change with a reset after each seed, and compare the score with and without the callback."),
        ("Phase 3: Unified Benchmark & Iteration (Step 5)\n", "Run locked Step 5 benchmark to evaluate all 4 controllers in parallel across 30 seeds; compare leaderboard ranks and iterate."),
        ("Phase 4: Trajectory Alignment Visualization (Step 6 & 7)\n", "Generate img/benchmark_trajectories.png showing all controllers side-by-side; inspect convergence curves for your team showcase."),
        ("Phase 5: Official Submission & Showcase Presentation (16:15 – 17:00)\n", "Verify submission on live W&B dashboard; connect to room projector for 3-minute lightning talk!"),
    ]
    for i, (hd, body) in enumerate(roadmap):
        p = tf_s10.paragraphs[0] if i == 0 else tf_s10.add_paragraph()
        p.space_before = Pt(6) if i > 0 else Pt(0)
        color = GOLD if i == 4 else PRIMARY
        add_text_run(p, hd, bold=True, size=Pt(12.5), color=color)
        p_b = tf_s10.add_paragraph()
        add_text_run(p_b, body, size=Pt(11.5), color=DARK_GRAY)

    prs.save(OUTPUT_PATH)
    print(f"Presentation saved successfully to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
