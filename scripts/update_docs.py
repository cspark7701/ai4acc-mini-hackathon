"""
scripts/update_docs.py
Updates .docx files in docs/ with the new Lecture 1 title and Track 3 Bayesian Optimization.
"""
import docx

def update_technical_preparation():
    path = "docs/Technical Preparation.docx"
    doc = docx.Document(path)
    
    # Update P7
    for p in doc.paragraphs:
        if "Lecture 1: Introduction to AI/ML" in p.text:
            p.text = "Lecture 1: AI/ML Foundations and Closed-Loop Control for Particle Accelerators"
            print("Updated P7 in Technical Preparation.docx")
            
    # Update Table T1
    for t in doc.tables:
        for row in t.rows:
            row_txt = [c.text for c in row.cells]
            if any("Lecture 1 (Extended)" in c for c in row_txt):
                for cell in row.cells:
                    if "Chong Shik Park" in cell.text:
                        cell.text = "Chong Shik Park, Ph.D."
                    if "AI/ML fundamentals, neural networks" in cell.text:
                        cell.text = "AI/ML foundations, neural surrogates, reinforcement learning & Bayesian optimization for accelerators (80 min)"
                print("Updated Table 1 in Technical Preparation.docx")
                
    doc.save(path)
    print("Saved Technical Preparation.docx")

def update_hackathon_project_guide():
    path = "docs/Hackathon Project Guide.docx"
    doc = docx.Document(path)
    
    # Update P4
    for p in doc.paragraphs:
        if "Participants benchmark three distinct control paradigms" in p.text:
            p.text = p.text.replace(
                "Participants benchmark three distinct control paradigms: Baseline 0 (Classical SVD pseudo-inverse), Baseline 1 (Supervised neural surrogate batch inversion), and Track 2 (Closed-loop Reinforcement Learning policy agent).",
                "Participants benchmark four distinct control paradigms: Baseline 0 (Classical SVD pseudo-inverse), Baseline 1 (Supervised neural surrogate batch inversion), Track 2 (Closed-loop Reinforcement Learning policy agent), and Track 3 (Closed-loop Bayesian Optimization controller)."
            )
            print("Updated P4 in Hackathon Project Guide.docx")
            
        if "All competitors adhere to the standard agent interface:" in p.text and "Track 2 (RL Closed-Loop Agent)" in p.text:
            if "Track 3" not in p.text:
                p.text = p.text + "\n4. Track 3 (Bayesian Optimization Controller): Uses a Gaussian Process surrogate with Lower Confidence Bound (LCB) acquisition to actively align the beam under non-linear saturation."
                print("Updated competitor list in Hackathon Project Guide.docx")
                
    # Update Table T1 (Schedule)
    for t in doc.tables:
        # Check if this is the schedule table
        if len(t.rows) >= 5 and any("Supervised Track" in c.text for c in t.rows[2].cells):
            # We can update rows or text
            t.rows[2].cells[0].text = "13:45 – 14:30"
            t.rows[2].cells[1].text = "Track 1: Supervised"
            t.rows[2].cells[2].text = "Train MLP digital twin, implement SciPy bounded batch inversion"
            t.rows[2].cells[3].text = "Trained forward surrogate & Baseline 1 logged"
            
            t.rows[3].cells[0].text = "14:30 – 15:15"
            t.rows[3].cells[1].text = "Track 2: RL Policy"
            t.rows[3].cells[2].text = "Implement continuous policy agent (act(obs, info)), tune damping & gain"
            t.rows[3].cells[3].text = "Trained RL feedback agent & Track 2 logged"
            
            # Check if there's row 4
            t.rows[4].cells[0].text = "15:15 – 16:00"
            t.rows[4].cells[1].text = "Track 3: Bayesian Opt"
            t.rows[4].cells[2].text = "Implement GP controller with Lower Confidence Bound (LCB) acquisition"
            t.rows[4].cells[3].text = "Trained GP controller & Track 3 logged"
            
            t.rows[5].cells[0].text = "16:00 – 16:30"
            t.rows[5].cells[1].text = "Live W&B Benchmark"
            t.rows[5].cells[2].text = "Execute evaluate_hackathon_benchmark across 30 seeds, sync to Leaderboard"
            t.rows[5].cells[3].text = "Live W&B run URL & official leaderboard score"
            
            # Add or update row 6 for showcase
            if len(t.rows) == 6:
                row = t.add_row()
                row.cells[0].text = "16:30 – 17:00"
                row.cells[1].text = "Showcase & Awards"
                row.cells[2].text = "Team presentations: 3-minute review of W&B dashboard, plots & trade-offs"
                row.cells[3].text = "Live W&B leaderboard review & peer discussion"
            print("Updated schedule table in Hackathon Project Guide.docx")
            
        # Check if this is the leaderboard table
        if len(t.rows) >= 4 and any("Baseline 1: Supervised MLP Inversion" in c.text for c in t.rows[1].cells):
            # Insert Track 3 at rank 1
            # Row 0: Header
            # Row 1: Track 3
            # Row 2: Baseline 1
            # Row 3: Baseline 0
            # Row 4: Track 2
            # Add a row to table
            new_row = t.add_row()
            # Shift rows down
            for r in range(len(t.rows)-1, 1, -1):
                for c in range(len(t.columns)):
                    t.rows[r].cells[c].text = t.rows[r-1].cells[c].text
            # Put Track 3 in row 1
            t.rows[1].cells[0].text = "#1"
            t.rows[1].cells[1].text = "Track 3: Bayesian Optimization Controller"
            t.rows[1].cells[2].text = "100.0%"
            t.rows[1].cells[3].text = "1.5 steps"
            t.rows[1].cells[4].text = "0.0149 mm"
            t.rows[1].cells[5].text = "0.93 A"
            t.rows[1].cells[6].text = "1,035.4 pts"
            
            # Update ranks
            t.rows[2].cells[0].text = "#2"
            t.rows[3].cells[0].text = "#3"
            t.rows[4].cells[0].text = "#4"
            print("Updated leaderboard table in Hackathon Project Guide.docx")
            
    doc.save(path)
    print("Saved Hackathon Project Guide.docx")

def update_participant_instructions():
    path = "docs/Mini-Hackathon Participant Instructions.docx"
    doc = docx.Document(path)
    
    for p in doc.paragraphs:
        if "Step 3: Complete TODO 1 by training Ridge" in p.text:
            p.text = "Step 3: Complete TODO 1 by training Ridge linear model & multi-layer MLP surrogate forward digital twin."
        if "Step 4: Solve TODO 2 implementing optimizer-based" in p.text:
            p.text = "Step 4: Solve TODO 2 by designing a closed-loop RL feedback policy agent with physics priors and adaptive damping."
        if "Step 5: Design a continuous RL feedback policy" in p.text:
            p.text = "Step 5: Solve TODO 3 by implementing a sample-efficient Bayesian Optimization controller using GaussianProcessRegressor with Lower Confidence Bound (LCB) acquisition."
            
    doc.save(path)
    print("Saved Mini-Hackathon Participant Instructions.docx")

if __name__ == "__main__":
    update_technical_preparation()
    update_hackathon_project_guide()
    update_participant_instructions()
