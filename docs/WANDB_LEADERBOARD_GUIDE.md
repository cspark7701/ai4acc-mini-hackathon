# W&B Leaderboard Setup Guide (Organizers)

This guide shows how to create the live Weights & Biases (W&B) leaderboard for the
**AI Applications in Accelerators Tutorial & Mini-Hackathon**.

In W&B a leaderboard is a shared **project** whose runs table is sorted by a metric.
The official project name is:

```text
ai4acc-mini-hackathon-2026
```

> W&B menu labels change from time to time. If a button is not where this guide says,
> look for the equivalent action on the same page.

---

## 1. Choose where the project lives

All participants must log to the same *entity* (a W&B team or user account).
If they do not, each participant's runs go to a private copy of the project under
their own account and never appear on the shared leaderboard.

| Option | How | When to use |
| --- | --- | --- |
| **Team (recommended)** | Create a team on [wandb.ai](https://wandb.ai) and invite every participant by email or invite link. | You know the participants in advance and your plan has enough seats. Check the seat limit of your plan first. |
| **Open project** | Create the project under the organizer's own account and set its visibility to **Open**. | No team is available. Anyone with a W&B account can then submit runs, including people outside the workshop. |

The name of the team (or the organizer's username for an open project) is the
`WANDB_ENTITY` value used below.

## 2. Create the project

1. Open the team page (or your profile page) on wandb.ai.
2. Click **Create new project**.
3. Name it `ai4acc-mini-hackathon-2026`.
4. Set the visibility: **Team** for a team project, **Open** for an open project.

W&B also creates the project automatically on the first run logged to it, but
creating it beforehand lets you set the visibility before anyone submits.

## 3. Point the notebooks at the project

The project name is already preset in the notebooks, `README.md`,
`scripts/update_notebooks.py` and `src/benchmark.py`. Only the entity must be filled in.
In the configuration cell of both notebooks:

```python
WANDB_PROJECT = "ai4acc-mini-hackathon-2026"  # Official project name for live leaderboard
WANDB_ENTITY = "<your-team-or-username>"      # Entity chosen in step 1
TEAM_NAME = "Team_01"                         # Assigned team name
```

`WANDB_ENTITY` ships as `None`. With `None`, W&B uses each participant's default
entity, which is their personal account. Set the real entity in the notebooks (and in
`scripts/update_notebooks.py`, which regenerates them) before distributing the
notebooks or building the Docker image.

## 4. Turn the runs table into a leaderboard

Every benchmark run is named `<TEAM_NAME>_<agent_name>` and records these summary metrics:

| Metric | Meaning |
| --- | --- |
| `challenge_score` | Official total benchmark score |
| `success_rate_pct` | Percentage of the 30 seeds reaching RMS < 0.03 mm |
| `mean_steps` | Average steps to convergence |
| `mean_final_rms_mm` | Average residual orbit error |
| `mean_current_norm_A` | Average corrector current norm |
| `mean_latency_ms` | Mean policy compute time per seed |

Each run also stores `team` and `agent` in its config and a `seed_breakdown_table`
with the per-seed results.

1. Open the project and switch to the **Runs** table.
2. Click **Columns**. Show the six metrics above plus `team` and `agent`, and hide the rest.
3. Pin `challenge_score` so it stays visible.
4. Click the `challenge_score` column header and choose **Sort descending**.
5. Optionally **Group** by `team` to keep each team's submissions together.
6. Save the layout as a view and share its URL. This is the page to show on the projector.

### Optional: a report page

For a cleaner public page, create a **Report** inside the project and add:

- a run-set table with the same columns and sort order, and
- a bar chart of `challenge_score` by run name.

Reports update live as new runs arrive.

## 5. Test before the event

1. Run `notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb` with the final
   `WANDB_PROJECT` and `WANDB_ENTITY` values. Four baseline runs should appear in the project.
2. Submit one run from a second W&B account to confirm that participants have write access.
3. Delete the test runs, or keep the baselines as reference rows on the leaderboard.

## Troubleshooting

- **Runs do not appear on the leaderboard:** `WANDB_ENTITY` is `None` or misspelled, so the
  run went to the participant's personal account. The run URL printed by the benchmark
  (`[W&B] Logged ... to https://wandb.ai/<entity>/<project>/...`) shows where it landed.
- **Permission error on `wandb.init`:** the participant is not a member of the team, or the
  project is not open. Invite them or change the project visibility.
- **No network:** the harness falls back to local reporting and prints the score in the notebook.
