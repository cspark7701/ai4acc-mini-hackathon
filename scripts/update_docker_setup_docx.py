"""
Update docx guides for participants with the official Docker run command:
cspark7701/ai4acc-hackathon-2026:latest
"""
import docx
from docx.shared import Pt, RGBColor, Inches
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCKER_CMD = (
    'docker run -it --rm \\\n'
    '    -p 8888:8888 \\\n'
    '    -v "${PWD}/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb" \\\n'
    '    -v "${PWD}/src:/workspace/src" \\\n'
    '    cspark7701/ai4acc-hackathon-2026:latest'
)

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
    p30.text = "If running via standard Docker CLI, ensure you execute from the project root directory. To preserve attendees' live progress while keeping the reference solution private, only the participant notebook (Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb) and src directory are mounted:"
    for r in p30.runs:
        r.font.name = "Calibri"
        
    # Update Table 2 (Bash/PowerShell/macOS/Linux)
    t2_cell = doc.tables[2].rows[0].cells[0]
    t2_p = t2_cell.paragraphs[0]
    t2_p.text = DOCKER_CMD
    for r in t2_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        
    # Update Table 3 (Command Prompt cmd.exe)
    t3_cell = doc.tables[3].rows[0].cells[0]
    t3_p = t3_cell.paragraphs[0]
    t3_p.text = (
        'docker run -it --rm -p 8888:8888 '
        '-v "%cd%\\notebooks\\Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb" '
        '-v "%cd%\\src:/workspace/src" '
        'cspark7701/ai4acc-hackathon-2026:latest'
    )
    for r in t3_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        
    # Update P45 (port troubleshooting)
    p45 = doc.paragraphs[45]
    if "docker run -it --rm -p 8889:8888" in p45.text:
        p45.text = (
            "Port 8888 in use error: If port 8888 is already occupied by a local Jupyter instance, change the port mapping to 8889: "
            "docker run -it --rm -p 8889:8888 -v \"${PWD}/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb\" -v \"${PWD}/src:/workspace/src\" cspark7701/ai4acc-hackathon-2026:latest "
            "... and browse to http://localhost:8889."
        )
        
    # Update P46
    p46 = doc.paragraphs[46]
    p46.clear()
    r1 = p46.add_run("Empty notebooks directory or missing file: ")
    r1.font.name = "Calibri"
    r1.bold = True
    r2 = p46.add_run("Ensure your terminal is located inside the repository root directory before running docker run with -v. Alternatively, use docker compose up which avoids shell path issues entirely and automatically mounts only the participant notebook.")
    r2.font.name = "Calibri"
    
    doc.save(path)
    print("Successfully updated docs/Docker Desktop Setup Guide.docx")


def update_participant_instructions_docx():
    path = "docs/Mini-Hackathon Participant Instructions.docx"
    doc = docx.Document(path)
    
    # Update Step 1 (P7)
    for p in doc.paragraphs:
        if "Step 1: Open Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb" in p.text:
            p.clear()
            r_title = p.add_run("Step 1: Launch Environment & Open Participant Notebook\n")
            r_title.bold = True
            r_title.font.name = "Calibri"
            r_title.font.size = Pt(10.5)
            
            r_desc = p.add_run(
                "Open Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb. "
                "For local container deployment, execute the official Docker command from the repository root directory:\n"
            )
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(10)
            
            r_code = p.add_run(DOCKER_CMD + "\n")
            r_code.font.name = "Consolas"
            r_code.font.size = Pt(8.5)
            r_code.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            
            r_foot = p.add_run("Once launched, navigate to http://localhost:8888 in your web browser to start the challenge.")
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
