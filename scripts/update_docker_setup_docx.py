"""
Update docx guides for participants with the universal Docker run command:
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
"""
import docx
from docx.shared import Pt, RGBColor

DOCKER_CMD = "docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest"

def find_paragraph(doc, predicate, description):
    """Return (index, paragraph) of the first paragraph matching predicate.

    Paragraphs are located by content rather than position so that inserting
    or reordering paragraphs fails loudly instead of editing the wrong text.
    """
    for i, p in enumerate(doc.paragraphs):
        if predicate(p.text):
            return i, p
    raise LookupError(f"Paragraph not found in docx: {description}")


def set_text(paragraph, text, font="Calibri", size=None):
    paragraph.text = text
    for r in paragraph.runs:
        r.font.name = font
        if size is not None:
            r.font.size = size


def update_docker_guide_docx():
    path = "docs/Docker Desktop Setup Guide.docx"
    doc = docx.Document(path)

    # Subtitle
    _, p_sub = find_paragraph(doc, lambda t: "Container:" in t, "subtitle containing 'Container:'")
    set_text(p_sub, "AI Applications in Accelerators Tutorial & Mini-Hackathon • Container: cspark7701/ai4acc-hackathon-2026:latest")

    # Intro paragraph directly below the "Method B" heading
    i_b, _ = find_paragraph(doc, lambda t: t.startswith("Method B:"), "heading 'Method B:'")
    set_text(
        doc.paragraphs[i_b + 1],
        "You can launch the official container by double-clicking run_hackathon_windows.bat (on Windows) or running the command below in any terminal. All required Python packages, simulation models, and the participant challenge notebook are pre-installed:",
    )

    # Command tables (Bash/PowerShell/macOS/Linux and cmd.exe)
    cmd_cells = [t.rows[0].cells[0] for t in doc.tables if t.rows[0].cells[0].text.startswith("docker run")]
    if len(cmd_cells) != 2:
        raise LookupError(f"Expected 2 'docker run' command tables in docx, found {len(cmd_cells)}")
    for cell in cmd_cells:
        set_text(cell.paragraphs[0], DOCKER_CMD, font="Consolas", size=Pt(9.5))

    # Port troubleshooting
    _, p_port = find_paragraph(doc, lambda t: t.startswith("Port 8888 in use error"), "'Port 8888 in use error'")
    set_text(
        p_port,
        "Port 8888 in use error: If port 8888 is already occupied by a local Jupyter instance, change the port mapping to 8889: "
        "docker run -it --rm -p 8889:8888 cspark7701/ai4acc-hackathon-2026:latest "
        "... and browse to http://localhost:8889.",
    )

    # Saving your work
    _, p46 = find_paragraph(doc, lambda t: t.startswith("Saving your work"), "'Saving your work'")
    p46.clear()
    r1 = p46.add_run("Saving your work: ")
    r1.font.name = "Calibri"
    r1.bold = True
    r2 = p46.add_run(
        "Inside JupyterLab, you can save your changes and download a copy of your completed notebook at any time via File -> Download. "
        "Running the benchmark cells automatically logs your official challenge score and convergence telemetry to the cloud W&B leaderboard."
    )
    r2.font.name = "Calibri"
    
    doc.save(path)
    print("Successfully updated docs/Docker Desktop Setup Guide.docx")


def update_participant_instructions_docx():
    path = "docs/Mini-Hackathon Participant Instructions.docx"
    doc = docx.Document(path)
    
    # Update Step 1 (P7)
    for p in doc.paragraphs:
        if "Step 1:" in p.text:
            p.clear()
            r_title = p.add_run("Step 1: Launch Environment & Open Participant Notebook\n")
            r_title.bold = True
            r_title.font.name = "Calibri"
            r_title.font.size = Pt(10.5)
            
            r_desc = p.add_run(
                "Windows users can simply double-click run_hackathon_windows.bat. Or run the official container in any terminal (no git clone or virtual environment required):\n"
            )
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(10)
            
            r_code = p.add_run(DOCKER_CMD + "\n")
            r_code.font.name = "Consolas"
            r_code.font.size = Pt(9)
            r_code.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            r_code.bold = True
            
            r_foot = p.add_run("Once launched, browse to http://localhost:8888 and open Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb to begin.")
            r_foot.font.name = "Calibri"
            r_foot.font.size = Pt(9.5)
            r_foot.italic = True
            print("Updated Step 1 in Mini-Hackathon Participant Instructions.docx")
            break
            
    doc.save(path)
    print("Successfully updated docs/Mini-Hackathon Participant Instructions.docx")


if __name__ == "__main__":
    update_docker_guide_docx()
    update_participant_instructions_docx()
