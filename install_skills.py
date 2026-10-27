"""Download the Elephant and Goldfish skills and install them into this project.

Run from the project root:
  python install_skills.py                  # Antigravity (agy): .agents/skills/
  python install_skills.py --agent claude   # Claude Code: .claude/skills/
  python install_skills.py --agent both
Installs into this project folder only, never globally. Works on macOS, Linux and Windows. Needs git. Source:
https://github.com/techpeerPat/elephant-goldfish-skills
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/techpeerPat/elephant-goldfish-skills.git"
SKILLS = ["elephant-grow", "elephant-teach", "goldfish-understand", "goldfish-critic",
          "goldfish-ready", "implement-design", "adversary-review"]
ap = argparse.ArgumentParser()
ap.add_argument("--agent", choices=["agy", "claude", "both"], default="agy")
args = ap.parse_args()
root = Path(__file__).parent
dests = []
if args.agent in ("agy", "both"):
    dests.append(root / ".agents" / "skills")
if args.agent in ("claude", "both"):
    dests.append(root / ".claude" / "skills")

if shutil.which("git") is None:
    sys.exit("git is not installed. Install git, then run this again.")

with tempfile.TemporaryDirectory() as tmp:
    clone = Path(tmp) / "egs"
    result = subprocess.run(["git", "clone", "--depth", "1", REPO, str(clone)])
    if result.returncode != 0:
        sys.exit("Clone failed. Check your network connection and try again.")
    src = clone / ".agents" / "skills"
    if not src.is_dir():
        sys.exit("Unexpected repo layout: .agents/skills not found.")
    for name in SKILLS:
        if not (src / name).is_dir():
            sys.exit(f"Skill folder missing in the repo: {name}")
    for dest in dests:
        dest.mkdir(parents=True, exist_ok=True)
        for name in SKILLS:
            shutil.copytree(src / name, dest / name, dirs_exist_ok=True)

print(f"Installed {len(SKILLS)} skills into: " + ", ".join(str(d) for d in dests))
for name in SKILLS:
    print(f"  /{name}")
print("Start your agent from this folder and type /ele to see them.")
