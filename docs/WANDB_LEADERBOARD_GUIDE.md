# W&B Leaderboard Guide

This guide explains how the live Weights & Biases (W&B) leaderboard for the
**AI Applications in Accelerators Tutorial & Mini-Hackathon** is set up and used.

- **The organizer** creates one shared W&B project that acts as the leaderboard, and a
  service account key that the launchers pass to the container.
- **Each participant** starts the environment with the provided launcher and submits runs
  under a unique hackathon team name. No invitation to the W&B team is needed.

> W&B menu labels change from time to time. If a button is not where this guide says,
> look for the equivalent action on the same page.

---

## How the pieces fit together

Three settings in the notebook configuration cell decide where a run goes and how it is labeled:

```python
WANDB_PROJECT = "ai4acc-mini-hackathon-2026"  # [DO NOT CHANGE] the leaderboard
WANDB_ENTITY = "ai4acc-mini-hackathon-2026"   # [DO NOT CHANGE] the W&B organization that owns it
TEAM_NAME = "Team_01"                         # CHANGE THIS: your unique hackathon team name
```

| Setting | What it is | Who sets it | Same for everyone? |
| --- | --- | --- | --- |
| `WANDB_ENTITY` | The W&B team (shared account) that owns the leaderboard | Organizer, preset | Yes |
| `WANDB_PROJECT` | The project inside that entity; its runs table is the leaderboard | Organizer, preset | Yes |
| `TEAM_NAME` | A label on each run naming the hackathon team that submitted it | Each hackathon team | No, unique per team |

W&B uses the word "team" for the shared account in `WANDB_ENTITY`. That is not a
hackathon team. There is **one** W&B team for the whole workshop, and every hackathon
team appears inside it as rows labeled with its `TEAM_NAME`.

Submissions are authenticated with one shared **service account key**, not with personal
keys. The key is never stored in the notebooks, the git repository or the Docker image.
It lives in a file named `wandb.apikey` that is handed out with the launchers.

The leaderboard address is:

```text
https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026
```

---

## Part A — Organizer: create the leaderboard

### A1. Create the W&B team (entity)

1. Log in at [wandb.ai](https://wandb.ai) with the organizer account.
2. Create a team (left sidebar or account menu → **Create a team**).
3. Give it the handle `ai4acc-mini-hackathon-2026`. It must match `WANDB_ENTITY` exactly.
4. Participants do not join the team; only the organizers need seats. Submissions come
   through the service account key created in A3.

### A2. Create the project

1. Open the team page and click **Create new project**.
2. Name it `ai4acc-mini-hackathon-2026`. It must match `WANDB_PROJECT` exactly.
3. Set the visibility to **Team**, so only team members and the shared service key can submit.

### A3. Create the service account key

A service account belongs to the W&B team, so runs logged with its key are accepted even
though the project is Team-only and participants are not members.

1. Open the team's **Team settings** page and find **Service accounts**.
2. Create a service account (for example `hackathon-submit`) and an API key for it.
3. Copy the key and note its expiry date; it must still be valid on the event day.

### A3b. Distribute the key with the launchers

1. Save the key as a single line in `dist/wandb.apikey`. The file is listed in
   `.gitignore` and `.dockerignore`, so it cannot be committed or baked into the image.
2. Run `./scripts/create_bundle.sh` (it rebuilds the image, writes the bundle and publishes the same
   commit to Docker Hub; add `--no-push` to skip publishing). It copies `wandb.apikey` into the bundle next to
   `run_hackathon_windows.bat` and `run_hackathon_mac_linux.sh`.
3. Hand out the bundle on the day (USB drive or a private download link). Do not post the
   bundle or the key publicly.

At launch, each launcher reads `wandb.apikey` from its own folder and passes it to the
container as the `WANDB_API_KEY` environment variable. The W&B library uses that variable
automatically, so the notebooks need no key and no `wandb.login()`.

Limits to be aware of:

- The key is kept out of sight, not secret from participants: anyone can open
  `wandb.apikey` or read the variable inside the container.
- Every run shows the service account as its author. `TEAM_NAME` is the only thing that
  tells hackathon teams apart.
- A Team-only project is visible to team members only. Participants see the leaderboard
  on the room display, not on their own laptops, unless the project is made Public.
- After the event, delete the service account or revoke its key. This also freezes the
  leaderboard.

### A4. Keep hackathon team names unique

W&B does not check `TEAM_NAME`. Two teams that pick the same name produce runs that
cannot be told apart on the leaderboard. Before the hackathon starts:

1. Keep a sign-up list (a shared sheet or a whiteboard) of team names and members.
2. Accept a name only if it is not already on the list.
3. Ask teams to use letters, digits and underscores only, for example `Beam_Wizards`.
   The name becomes part of the run name `<TEAM_NAME>_<agent_name>`.

### A5. Turn the runs table into a leaderboard

Every benchmark run records these summary metrics:

| Metric | Meaning |
| --- | --- |
| `challenge_score` | Official total benchmark score, 0 to 1000 points |
| `score_success`, `score_speed`, `score_precision` | The three parts of `challenge_score` |
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
5. **Group** by `team` to keep each hackathon team's submissions together.
6. Save the layout as a view and share its URL. This is the page to show on the projector.

For a cleaner page, create a **Report** inside the project with a run-set table using the
same columns and sort order, plus a bar chart of `challenge_score` by run name. Reports
update live as new runs arrive.

### A6. Test before the event

1. Run `notebooks/Single_Notebook_Beam_Orbit_Predictor_Solution.ipynb`. Four baseline
   runs should appear in the project.
2. On a second machine, start the environment with the bundled launcher and run the
   Participant notebook, to confirm that the shared key reaches the container.
3. Delete the test runs, or keep the baselines as reference rows on the leaderboard.

### A7. Reset the leaderboard

`scripts/cleanup_wandb.py` deletes runs from the leaderboard project. It reads the key from
`WANDB_API_KEY` or `dist/wandb.apikey`, lists the matching runs, and deletes nothing unless you
pass `--delete`; deleting then asks you to type the project name (skip with `--yes`).

```bash
python scripts/cleanup_wandb.py --all                         # list every run (no changes)
python scripts/cleanup_wandb.py --team-prefix MA_ --delete    # delete only the multi-agent test runs
python scripts/cleanup_wandb.py --team Team_Alpha --delete    # delete one team's runs (repeatable)
python scripts/cleanup_wandb.py --all --delete                # reset the whole leaderboard
```

Deleted runs cannot be restored. Run the script with a Python that has `wandb` installed.

---

## Part B — Participant: submit to the leaderboard

### B1. Start the environment with the launcher

Keep the files from the organizer's bundle together in one folder, including
`wandb.apikey`, and start the environment with the launcher:

- **Windows:** double-click `run_hackathon_windows.bat`.
- **macOS / Linux:** run `./run_hackathon_mac_linux.sh`.

The launcher prints `[OK] W&B leaderboard key loaded.` when it finds the key. You do not
need a W&B account or `wandb.login()` to submit.

If you start the container by hand, pass the key yourself:

```bash
docker run -it --rm -p 8888:8888 -e WANDB_API_KEY="$(cat wandb.apikey)" cspark7701/ai4acc-hackathon-2026:latest
```

### B2. Choose a unique hackathon team name

Agree on a team name with your teammates and register it with the organizer. All members
of one hackathon team use exactly the same `TEAM_NAME`, including capitalisation.

### B3. Configure the notebook

In the configuration cell, change only `TEAM_NAME`:

```python
WANDB_PROJECT = "ai4acc-mini-hackathon-2026"  # [DO NOT CHANGE]
WANDB_ENTITY = "ai4acc-mini-hackathon-2026"   # [DO NOT CHANGE]
TEAM_NAME = "Beam_Wizards"                    # your registered team name
```

### B4. Run the benchmark

Run the evaluation cells. Each agent is logged as a run named `<TEAM_NAME>_<agent_name>`,
and the notebook prints its URL:

```text
[W&B] Logged 'Beam_Wizards_Track2_RLAgent' to https://wandb.ai/ai4acc-mini-hackathon-2026/ai4acc-mini-hackathon-2026/runs/...
```

Your rank appears on the leaderboard shown on the room display.

---

## Troubleshooting

- **`[!] No W&B key found` at launch:** `wandb.apikey` is not in the same folder as the
  launcher. Copy it there and start the launcher again.
- **Permission or login error on `wandb.init`:** the container was started without the key,
  or the key has expired or been revoked. Restart with the launcher; if it persists, the
  organizer must issue a new key.
- **Runs do not appear on the leaderboard:** `WANDB_ENTITY` or `WANDB_PROJECT` was changed
  or misspelled, so the run went somewhere else. The printed run URL shows where it landed.
- **Two teams show up under one name:** both used the same `TEAM_NAME`. One team must
  rename and rerun; the organizer can delete the mislabelled runs with
  `scripts/cleanup_wandb.py --team <name> --delete`.
- **One team shows up under two names:** teammates typed `TEAM_NAME` differently. Use the
  registered spelling and rerun.
- **No network:** the harness falls back to local reporting and prints the score in the notebook.
