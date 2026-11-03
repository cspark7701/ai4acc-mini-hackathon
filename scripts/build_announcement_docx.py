"""
scripts/build_announcement_docx.py
Generates docs/Announcement.docx in synchronization with docs/Announcement.md.
Eliminates '행사' words, removes Google Colab references, promotes Docker, and clarifies Docker Desktop requirements.
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("w:top", top), ("w:bottom", bottom), ("w:left", left), ("w:right", right)]:
        node = OxmlElement(m)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)

def build_docx():
    doc = docx.Document()

    # Page setup
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    # Colors
    PRIMARY = RGBColor(24, 76, 120)     # Navy Blue
    SECONDARY = RGBColor(41, 128, 185)  # Accent Blue
    DARK_GRAY = RGBColor(44, 62, 80)
    MUTED = RGBColor(100, 110, 120)

    # Styles
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = DARK_GRAY

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("워크숍 공지사항 / Workshop Announcement\n")
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY

    run_sub = p_title.add_run("AI Applications in Accelerators Tutorial & Mini-Hackathon\n가속기 분야 AI 활용 튜토리얼 & 미니 해커톤")
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = SECONDARY

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("2026년 11월 3일 (화) 09:00 – 17:00 | KOMAC / KAERI (한국원자력연구원 양성자과학연구단)")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ================= KOREAN SECTION =================
    h1_ko = doc.add_heading(level=1)
    r_h1_ko = h1_ko.add_run("[한국어] 워크숍 안내 및 참가자 준비 사항")
    r_h1_ko.font.color.rgb = PRIMARY
    r_h1_ko.font.size = Pt(15)

    p_intro_ko = doc.add_paragraph()
    p_intro_ko.add_run(
        "가속기 분야 AI 활용 튜토리얼 & 미니 해커톤에 참가하시는 연구원, 엔지니어, 대학원생 여러분을 환영합니다. "
        "본 워크숍은 가속기 빔 물리 모델링, 신경망 대리모델 디지털 트윈, 폐루프 궤도 정렬 제어(RL, BO), 그리고 "
        "에이전틱 자율 운전 워크플로우를 포괄하는 1일 집중 이론 교육 및 실습 챌린지입니다."
    )

    # Callout Box for Key Prep in Korean
    box = doc.add_table(rows=1, cols=1)
    box.alignment = WD_TABLE_ALIGNMENT.CENTER
    box.autofit = False
    box.columns[0].width = Inches(6.7)
    cell = box.cell(0, 0)
    set_cell_background(cell, "EBF5FB")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p_box = cell.paragraphs[0]
    r_box_title = p_box.add_run("📌 참가자 핵심 준비 사항 요약\n")
    r_box_title.font.bold = True
    r_box_title.font.color.rgb = PRIMARY
    r_box_title.font.size = Pt(11)

    r_b1 = p_box.add_run("1. 개인 노트북 지참 (BYOD): ")
    r_b1.bold = True
    p_box.add_run("실습 및 오후 미니 해커톤 참가를 위해 개인 노트북과 전원 충전기를 반드시 지참해 주십시오.\n")

    r_b2 = p_box.add_run("2. 운영체제 및 실습 환경 (Docker 권장 / Windows, Mac, Linux 지원): ")
    r_b2.bold = True
    p_box.add_run(
        "모든 OS를 완벽히 지원하며, 시뮬레이션 환경이 사전 패키징된 Docker 사용을 적극 권장합니다. "
        "저장소 복제 후 'docker compose up' 명령으로 즉시 JupyterLab(포트 8888)에 접속할 수 있습니다. "
        "(Windows/macOS는 가상화 백엔드를 위해 Docker Desktop 설치가 필요하며, Linux는 기본 Docker CLI 엔진만으로 구동됩니다. "
        "로컬 Python 3.10+ 가상환경 실행도 완벽히 지원됩니다.)\n"
    )

    r_b3 = p_box.add_run("3. Weights & Biases (W&B) 무료 계정 사전 생성: ")
    r_b3.bold = True
    p_box.add_run(
        "실시간 벤치마크 및 리더보드 연동을 위해 wandb.ai에서 무료 개인 계정을 생성하고 API 키를 확인해 오시기 바랍니다. "
        "(오프라인 모드도 지원하므로 미가입자도 벤치마크 실행 가능)"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Korean Schedule
    h2_sch_ko = doc.add_heading(level=2)
    r_sch_ko = h2_sch_ko.add_run("프로그램 일정표")
    r_sch_ko.font.color.rgb = SECONDARY
    r_sch_ko.font.size = Pt(12.5)

    table_ko = doc.add_table(rows=6, cols=3)
    table_ko.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_ko.autofit = False
    widths = [Inches(1.5), Inches(1.8), Inches(3.4)]

    headers = ["시간", "세션", "세부 내용 및 연사"]
    for i, h in enumerate(headers):
        c = table_ko.cell(0, i)
        c.width = widths[i]
        set_cell_background(c, "184C78")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    rows_ko = [
        ("09:00 – 09:10", "개회 및 오리엔테이션", "워크숍 목표 소개, Docker/실습 환경 점검 및 챌린지 가이드"),
        ("09:10 – 10:30", "강의 1 (80분)", "입자 가속기를 위한 AI/ML 기초 및 폐루프 제어\n(박종식 박사, 고려대학교 세종캠퍼스)"),
        ("10:40 – 12:00", "강의 2 (80분)", "가속기 연구를 위한 에이전틱 AI: Osprey 프레임워크 응용\n(Thorsten Hellert 박사, LBNL)"),
        ("12:00 – 13:30", "점심 식사 및 네트워킹", "점심 식사 및 참가자 간 교류"),
        ("13:30 – 17:00", "미니 해커톤 및 시상", "빔 궤도 정렬 챌린지 (트랙 1/2/3)\nW&B 실시간 리더보드 평가, 우수자 시상 및 총평")
    ]

    for row_idx, data in enumerate(rows_ko, start=1):
        bg = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            c = table_ko.cell(row_idx, col_idx)
            c.width = widths[col_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)

    doc.add_page_break()

    # ================= ENGLISH SECTION =================
    h1_en = doc.add_heading(level=1)
    r_h1_en = h1_en.add_run("[English] Workshop Announcement & Participant Guide")
    r_h1_en.font.color.rgb = PRIMARY
    r_h1_en.font.size = Pt(15)

    p_intro_en = doc.add_paragraph()
    p_intro_en.add_run(
        "We cordially invite researchers, engineers, postdoctoral scholars, and graduate students to the "
        "AI Applications in Accelerators Tutorial & Mini-Hackathon at KOMAC / KAERI. This intensive, one-day workshop "
        "covers the full arc from beam physics foundations and neural surrogate digital twins to closed-loop orbit control "
        "(RL, Bayesian Optimization) and agentic operations."
    )

    # Callout Box for Key Prep in English
    box_en = doc.add_table(rows=1, cols=1)
    box_en.alignment = WD_TABLE_ALIGNMENT.CENTER
    box_en.autofit = False
    box_en.columns[0].width = Inches(6.7)
    cell_en = box_en.cell(0, 0)
    set_cell_background(cell_en, "EBF5FB")
    set_cell_margins(cell_en, top=140, bottom=140, left=200, right=200)

    p_box_en = cell_en.paragraphs[0]
    r_box_title_en = p_box_en.add_run("📌 Essential Participant Requirements\n")
    r_box_title_en.font.bold = True
    r_box_title_en.font.color.rgb = PRIMARY
    r_box_title_en.font.size = Pt(11)

    r_eb1 = p_box_en.add_run("1. Bring Your Own Laptop (BYOD): ")
    r_eb1.bold = True
    p_box_en.add_run("Please bring your personal laptop and power adapter for hands-on exercises and the afternoon hackathon.\n")

    r_eb2 = p_box_en.add_run("2. Operating Systems & Recommended Docker Setup: ")
    r_eb2.bold = True
    p_box_en.add_run(
        "All platforms (Windows, macOS, Linux) are fully supported. We strongly recommend using Docker ('docker compose up') "
        "for a turnkey, reproducible workspace without package conflicts. Note: Windows and macOS require Docker Desktop (or equivalent) "
        "to supply container virtualization, whereas Linux runs natively via the standard Docker engine CLI. "
        "(Local Python 3.10+ environments are also fully supported.)\n"
    )

    r_eb3 = p_box_en.add_run("3. Create a Free Weights & Biases Account: ")
    r_eb3.bold = True
    p_box_en.add_run(
        "Sign up for a free account at wandb.ai and obtain your API key from wandb.ai/authorize before the event "
        "for live competition leaderboard logging. (Offline and anonymous modes are also supported)."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # English Schedule
    h2_sch_en = doc.add_heading(level=2)
    r_sch_en = h2_sch_en.add_run("Master Program Schedule")
    r_sch_en.font.color.rgb = SECONDARY
    r_sch_en.font.size = Pt(12.5)

    table_en = doc.add_table(rows=6, cols=3)
    table_en.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_en.autofit = False

    headers_en = ["Time (KST)", "Session", "Description & Lecturer"]
    for i, h in enumerate(headers_en):
        c = table_en.cell(0, i)
        c.width = widths[i]
        set_cell_background(c, "184C78")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    rows_en = [
        ("09:00 – 09:10", "Welcome & Setup", "Workshop orientation, Docker/environment checks & W&B intro"),
        ("09:10 – 10:30", "Lecture 1 (80 min)", "AI/ML Foundations and Closed-Loop Control for Particle Accelerators\n(Chong Shik Park, Ph.D., Korea University, Sejong)"),
        ("10:40 – 12:00", "Lecture 2 (80 min)", "Agentic AI for Accelerator Research: Osprey Applications\n(Thorsten Hellert, Ph.D., LBNL)"),
        ("12:00 – 13:30", "Lunch & Networking", "Lunch break and scientific networking"),
        ("13:30 – 17:00", "Mini-Hackathon & Awards", "Beam Orbit Alignment Benchmark Challenge (Tracks 1, 2, 3)\nW&B Live Leaderboard review, awards presentation & closing")
    ]

    for row_idx, data in enumerate(rows_en, start=1):
        bg = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            c = table_en.cell(row_idx, col_idx)
            c.width = widths[col_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)

    doc.save("docs/Announcement.docx")
    print("Successfully generated docs/Announcement.docx")

if __name__ == "__main__":
    build_docx()
