import os
import subprocess
import shutil
from pathlib import Path
import datetime

# ── Configuration ──────────────────────────────────────────────────────────
HERMES_HOME = Path.home() / '.hermes'
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_SYNC_DIR = PROJECT_ROOT / 'data'
GITHUB_REMOTE = "https://github.com/jungwonhyo11/Hermesfor-Web.git"

def run_cmd(cmd, cwd=None):
    print(f"> Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def sync():
    print(f"--- Hermes Sync Started: {datetime.datetime.now()} ---")
    
    # 1. Ensure DATA_SYNC_DIR exists
    DATA_SYNC_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Copy critical data from ~/.hermes if it exists
    if HERMES_HOME.exists():
        print(f"Backing up data from {HERMES_HOME}...")
        # Items to sync: memories, sessions, skills, settings
        folders_to_sync = ['memories', 'webui/sessions', 'skills', 'cron']
        for folder in folders_to_sync:
            src = HERMES_HOME / folder
            dst = DATA_SYNC_DIR / folder
            if src.exists():
                print(f"  Syncing {folder}...")
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
    
    # 3. Handle Git Operations
    # Check if .git exists in PROJECT_ROOT
    if not (PROJECT_ROOT / '.git').exists():
        print("Initializing git repository...")
        run_cmd("git init", cwd=PROJECT_ROOT)
        run_cmd(f"git remote add origin {GITHUB_REMOTE}", cwd=PROJECT_ROOT)
    else:
        # Check if remote exists, update if needed
        res = run_cmd("git remote get-url origin", cwd=PROJECT_ROOT)
        if GITHUB_REMOTE not in res.stdout:
            print("Updating git remote URL...")
            run_cmd(f"git remote set-url origin {GITHUB_REMOTE}", cwd=PROJECT_ROOT)

    # 4. Git Add, Commit, Push
    print("Committing and pushing to GitHub...")
    run_cmd("git add .", cwd=PROJECT_ROOT)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_cmd(f'git commit -m "Auto-backup: {timestamp}"', cwd=PROJECT_ROOT)
    
    # Try to push (User might need to handle auth if not configured)
    print("Pushing to main branch...")
    run_cmd("git push -u origin main", cwd=PROJECT_ROOT)

    print("--- Sync Complete ---")

if __name__ == "__main__":
    sync()
