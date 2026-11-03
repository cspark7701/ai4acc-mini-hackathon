"""
Update docs/Docker Desktop Setup Guide.docx to reflect mounting only the participant notebook.
"""
import docx
from docx.shared import Pt

def update_docker_guide_docx():
    path = "docs/Docker Desktop Setup Guide.docx"
    doc = docx.Document(path)
    
    # Update P30
    p30 = doc.paragraphs[30]
    p30.text = "If running via standard Docker CLI, ensure you execute from the project root directory. To preserve attendees' live progress while keeping the reference solution private, only the participant notebook (Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb) and src directory are mounted:"
    for r in p30.runs:
        r.font.name = "Calibri"
        
    # Update Table 2 (Bash/PowerShell/macOS/Linux)
    t2_cell = doc.tables[2].rows[0].cells[0]
    t2_p = t2_cell.paragraphs[0]
    t2_p.text = 'docker run -it --rm -p 8888:8888 -v "${PWD}/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb" -v "${PWD}/src:/workspace/src" ai4acc-hackathon-2026'
    for r in t2_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        
    # Update Table 3 (Command Prompt cmd.exe)
    t3_cell = doc.tables[3].rows[0].cells[0]
    t3_p = t3_cell.paragraphs[0]
    t3_p.text = 'docker run -it --rm -p 8888:8888 -v "%cd%\\notebooks\\Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb" -v "%cd%\\src:/workspace/src" ai4acc-hackathon-2026'
    for r in t3_p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        
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

if __name__ == "__main__":
    update_docker_guide_docx()
