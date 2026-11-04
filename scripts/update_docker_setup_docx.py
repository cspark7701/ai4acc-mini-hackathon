"""
Update docx guides for participants with the universal Docker run command:
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest
"""
import docx
from docx.shared import Pt, RGBColor

DOCKER_CMD = "docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest"

def update_docker_guide_docx():
    path = "docs/Docker Desktop Setup Guide.docx"
    doc = docx.Document(path)
    
    # Update subtitle P1
    p1 = doc.paragraphs[1]
    if "Container:" in p1.text:
        p1.text = "AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI) • Container: cspark7701/ai4acc-hackathon-2026:latest"
        for r in p1.runs:
            r.font.name = "Calibri"
    
    # Update P30
    p30 = doc.paragraphs[30]
    p30.text = "You can launch the official container by double-clicking run_hackathon_windows.bat (on Windows) or running the command below in any terminal. All required Python packages, simulation models, and the participant challenge notebook are pre-installed:"
    for r in p30.runs:
        r.font.name = "Calibri"
        
    # Update Table 2 (Bash/PowerShell/macOS/Linux)
    t2_cell = doc.tables[2].rows[0].cells[0]
    t2_p = t2_cell.paragraphs[0]
    t2_p.text = DOCKER_CMD
    for r in t2_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        
    # Update Table 3 (Command Prompt cmd.exe)
    t3_cell = doc.tables[3].rows[0].cells[0]
    t3_p = t3_cell.paragraphs[0]
    t3_p.text = DOCKER_CMD
    for r in t3_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        
    # Update P45 (port troubleshooting)
    p45 = doc.paragraphs[45]
    if "8888" in p45.text:
        p45.text = (
            "Port 8888 in use error: If port 8888 is already occupied by a local Jupyter instance, change the port mapping to 8889: "
            "docker run -it --rm -p 8889:8888 cspark7701/ai4acc-hackathon-2026:latest "
            "... and browse to http://localhost:8889."
        )
        for r in p45.runs:
            r.font.name = "Calibri"
        
    # Update P46
    p46 = doc.paragraphs[46]
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
