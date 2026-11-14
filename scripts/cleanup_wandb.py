#!/usr/bin/env python3
"""
scripts/cleanup_wandb.py
Reset the W&B leaderboard by deleting runs from the hackathon project.

The script lists matching runs by default and deletes nothing. Deleting requires
--delete and a typed confirmation (or --yes for non-interactive use).

Examples:
    # List every run on the leaderboard (no changes)
    python scripts/cleanup_wandb.py --all

    # Delete only the multi-agent test runs (team names starting with MA_)
    python scripts/cleanup_wandb.py --team-prefix MA_ --delete

    # Delete one team's runs
    python scripts/cleanup_wandb.py --team Team_Alpha --delete

    # Reset the whole leaderboard without a prompt (e.g. in a script)
    python scripts/cleanup_wandb.py --all --delete --yes

The API key is taken from the WANDB_API_KEY environment variable, or else from
dist/wandb.apikey in the repository root (or the file given with --key-file).
"""
import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENTITY = "ai4acc-mini-hackathon-2026"
DEFAULT_PROJECT = "ai4acc-mini-hackathon-2026"
DEFAULT_KEY_FILE = REPO_ROOT / "dist" / "wandb.apikey"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List or delete runs on the hackathon W&B leaderboard (lists only, unless --delete is given).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--entity", default=DEFAULT_ENTITY, help=f"W&B entity (default: {DEFAULT_ENTITY})")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help=f"W&B project (default: {DEFAULT_PROJECT})")
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY_FILE,
                        help="API key file used when WANDB_API_KEY is not set (default: dist/wandb.apikey)")

    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--all", action="store_true", help="Select every run in the project")
    select.add_argument("--team-prefix", metavar="PREFIX",
                        help="Select runs whose team name starts with PREFIX (e.g. MA_)")
    select.add_argument("--team", metavar="NAME", action="append",
                        help="Select runs of this exact team name (repeatable)")

    parser.add_argument("--delete", action="store_true", help="Delete the selected runs (default: list only)")
    parser.add_argument("--yes", action="store_true", help="Skip the confirmation prompt when deleting")
    return parser.parse_args()


def load_api_key(key_file: Path) -> None:
    """Make sure WANDB_API_KEY is set, without ever printing the key."""
    if os.environ.get("WANDB_API_KEY"):
        return
    if not key_file.is_file():
        sys.exit(f"Error: WANDB_API_KEY is not set and the key file {key_file} does not exist.")
    key = key_file.read_text().strip()
    if not key:
        sys.exit(f"Error: the key file {key_file} is empty.")
    os.environ["WANDB_API_KEY"] = key


def team_of(run) -> str:
    """Team name as logged by evaluate_hackathon_benchmark (config 'team'), or '' if missing."""
    return str(run.config.get("team", "") or "")


def select_runs(runs, args: argparse.Namespace) -> list:
    if args.all:
        return list(runs)
    if args.team_prefix:
        return [r for r in runs if team_of(r).startswith(args.team_prefix)]
    wanted = set(args.team)
    return [r for r in runs if team_of(r) in wanted]


def print_table(selected: list) -> None:
    print(f"{'Run ID':<10} {'Team':<28} {'Run name':<52} {'Score':>9}  {'State':<9} Created")
    print("-" * 132)
    for r in selected:
        score = r.summary.get("challenge_score")
        score_txt = f"{score:9.3f}" if isinstance(score, (int, float)) else f"{'-':>9}"
        print(f"{r.id:<10} {team_of(r)[:28]:<28} {r.name[:52]:<52} {score_txt}  {r.state:<9} {r.created_at}")


def confirm(path: str, count: int) -> bool:
    print(f"\nThis permanently deletes {count} run(s) from {path}. Deleted runs cannot be restored.")
    try:
        answer = input(f"Type the project name '{path.split('/')[-1]}' to confirm: ")
    except EOFError:
        return False
    return answer.strip() == path.split("/")[-1]


def main() -> int:
    args = parse_args()
    load_api_key(args.key_file)

    import wandb  # imported after the key is set so the API picks it up

    path = f"{args.entity}/{args.project}"
    try:
        runs = wandb.Api(timeout=60).runs(path)
        all_runs = list(runs)
    except Exception as exc:  # network, auth or missing project
        print(f"Error: could not list runs in {path}: {exc}", file=sys.stderr)
        return 1

    selected = select_runs(all_runs, args)
    print(f"Project {path}: {len(all_runs)} run(s) in total, {len(selected)} selected.\n")
    if not selected:
        return 0
    print_table(selected)

    if not args.delete:
        print("\nNothing was deleted (list only). Add --delete to delete the selected runs.")
        return 0

    if not args.yes and not confirm(path, len(selected)):
        print("Aborted; nothing was deleted.")
        return 1

    deleted, failed = 0, 0
    for r in selected:
        try:
            r.delete()
            deleted += 1
            print(f"Deleted {r.id} ({r.name})")
        except Exception as exc:
            failed += 1
            print(f"Failed to delete {r.id} ({r.name}): {exc}", file=sys.stderr)

    print(f"\nDeleted {deleted} of {len(selected)} selected run(s); {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
