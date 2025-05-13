#!/usr/bin/env python3

# ╔══════════════════════════════════════════════════════╗
# ║           Git Repo Setup Tool — by Rue 🧚‍♀️            ║
# ║   With Smart Repo Rescue, Help Menu & More!          ║
# ╚══════════════════════════════════════════════════════╝

import os
import subprocess
import sys
import urllib.request

# ╭──────────────────────────────╮
# │  SECTION 0: Global Flags     │
# ╰──────────────────────────────╯
DRY_RUN = "--dry-run" in sys.argv

# ╭──────────────────────────────╮
# │  SECTION 1: Help Menu        │
# ╰──────────────────────────────╯
def show_help():
    print("""
Usage: repo-setup.py [options]

Options:
  --dry-run        Simulate actions without making any changes
  --help, -h       Show this help message and exit

Description:
  This script initializes a Git repo, sets up remote origin, creates .gitignore,
  and optionally pushes to GitHub — all interactively and safely.

  Features:
    - Prompts for Git user info if missing
    - SSH key check and optional creation
    - Smart remote conflict detection with GitHub
    - Option to force push, pull, or compare changes
    - .gitignore presets for Python or Node
    - Global default branch name config
""")
    sys.exit(0)

# ╭──────────────────────────────╮
# │  SECTION 2: Banner Placeholder │
# ╰──────────────────────────────╯
def print_banner():
    banner = (
        "\033[1;36m" +
        " _____       _      _   ______                 \n"
        "|  _  |     (_)    | |  | ___ \\                \n"
        "| | | |_   _ _  ___| | _| |_/ /___ _ __   ___  \n"
        "| | | | | | | |/ __| |/ /    // _ \\ '_ \\ / _ \\ \n"
        "\\ \\/' / |_| | | (__|   <| |\\ \\  __/ |_) | (_) |\n"
        " \\_/\\_\\\\__,_|_|\\___|_|\\_\\_| \\_\\___| .__/ \\___/ \n"
        "                                  | |          \n"
        "                                  |_|          \n"
        "\033[0m"
    )
    print(banner)

# ╭──────────────────────────────╮
# │  SECTION 3: Command Runner   │
# ╰──────────────────────────────╯
def run_cmd(cmd, capture_output=False, check_success=False):
    if DRY_RUN:
        print(f"[DRY-RUN] Would run: {cmd}")
        return True if check_success else ""
    result = subprocess.run(cmd, shell=True, text=True,
                             capture_output=capture_output)
    if check_success:
        return result.returncode == 0
    if capture_output:
        return result.stdout.strip()
    return None

# ╭──────────────────────────────╮
# │  SECTION 4: Git User Config  │
# ╰──────────────────────────────╯
def check_git_global_user():
    username = run_cmd("git config --global user.name", capture_output=True)
    email = run_cmd("git config --global user.email", capture_output=True)
    return username, email

def set_git_global_user():
    print("➤ No Git username/email found. Let's set them up!")
    username = input("Enter your Git username: ").strip()
    email = input("Enter your Git email address: ").strip()
    run_cmd(f'git config --global user.name "{username}"')
    run_cmd(f'git config --global user.email "{email}"')
    print(f"✅ Git global username and email set: {username} / {email}\n")

# ╭────────────────────────────────╮
# │  SECTION 5: Default Branch Fix │
# ╰────────────────────────────────╯
def ensure_default_branch():
    current = run_cmd("git config --global init.defaultBranch", capture_output=True)
    if current != "main":
        print(f"🔧 Current global default branch is: {current or 'master (default)'}")
        fix = input("Would you like to set 'main' as your default branch globally? [y/n]: ").strip().lower()
        if fix == 'y':
            run_cmd("git config --global init.defaultBranch main")
            print("✅ Default branch updated to 'main'.\n")

# ╭──────────────────────────────╮
# │  SECTION 6: SSH Key Utility  │
# ╰──────────────────────────────╯
def check_ssh_key():
    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.isdir(ssh_dir):
        return False
    keys = [f for f in os.listdir(ssh_dir) if f.endswith(".pub")]
    return bool(keys)

def create_ssh_key():
    print("➤ No SSH key found.")
    choice = input("Would you like to create one now? [y/n]: ").lower()
    if choice == 'y':
        email = run_cmd("git config --global user.email", capture_output=True) or input("Enter email for SSH key: ")
        run_cmd(f'ssh-keygen -t ed25519 -C "{email}"')
        print("✅ SSH key generated. Don't forget to add it to GitHub!")
    else:
        print("⚠️ Skipping SSH key creation. You will need one to push via SSH.")

# ╭──────────────────────────────╮
# │  SECTION 7: Remote Handling  │
# ╰──────────────────────────────╯
def fix_remote_url(remote_input):
    if remote_input.startswith("git@github.com:"):
        return remote_input
    elif "/" in remote_input and not remote_input.startswith("http"):
        return f"git@github.com:{remote_input}"
    else:
        print("⚠️ Invalid remote format. Please enter 'username/repo.git' or full SSH URL.")
        sys.exit(1)

def repo_exists_on_github(ssh_url):
    if ssh_url.startswith("git@github.com:"):
        https_url = "https://github.com/" + ssh_url.split("git@github.com:")[1].replace(".git", "")
        try:
            with urllib.request.urlopen(https_url) as response:
                return response.status == 200
        except:
            return False
    return False

# ╭──────────────────────────────╮
# │  SECTION 8: .gitignore Gen   │
# ╰──────────────────────────────╯
def create_gitignore():
    presets = {
        "python": [
            "*.pyc", "__pycache__/", ".venv/", "env/", "build/", "dist/", "*.egg-info/"
        ],
        "node": [
            "node_modules/", "dist/", "*.log", "npm-debug.log*", ".env"
        ]
    }
    choice = input("➤ Create .gitignore? Choose [python/node/custom/skip]: ").lower()
    if choice == "skip":
        return
    lines = []
    if choice in presets:
        lines = presets[choice]
    else:
        print("Enter custom ignore patterns (one per line, blank line to finish):")
        while True:
            line = input("> ").strip()
            if not line:
                break
            lines.append(line)
    with open(".gitignore", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("✅ .gitignore created.\n")

# ╭──────────────────────────────╮
# │  SECTION 9: Summary Display  │
# ╰──────────────────────────────╯
def show_summary(username, email, remote_url):
    print("\n📜 Project Summary:")
    print(f"  - Working Dir: {os.getcwd()}")
    print(f"  - Git User: {username}")
    print(f"  - Email: {email}")
    print(f"  - Remote: {remote_url or 'Not set'}")
    print(f"  - Dry Run: {'Yes' if DRY_RUN else 'No'}")
    print("✨ All done. May your commits be mighty!\n")

# ╭──────────────────────────────╮
# │  SECTION 10: Main Logic      │
# ╰──────────────────────────────╯
def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()

    print_banner()
    print(f"📁 You are currently in:\n    {os.getcwd()}\n")

    if os.getcwd() in [os.path.expanduser("~"), "/"]:
        print("⚠️ This may not be a good project directory.")
        if input("Are you sure you want to continue? [y/n]: ").lower() != 'y':
            sys.exit(1)

    ensure_default_branch()

    username, email = check_git_global_user()
    if not username or not email:
        set_git_global_user()
        username, email = check_git_global_user()
    else:
        print(f"➤ Git user already set: {username} / {email}\n")

    if not check_ssh_key():
        create_ssh_key()
    else:
        print("➤ SSH key found.\n")

    if not os.path.isdir(".git"):
        init = input("➤ No Git repo found. Initialize new Git repo here? [y/n]: ").lower()
        if init != 'y':
            print("❌ Exiting.")
            sys.exit(0)
        run_cmd("git init")
        print("✅ Initialized new Git repository.\n")

    remote_input = input("➤ Enter SSH path (e.g., username/repo.git): ").strip()
    ssh_url = fix_remote_url(remote_input)

    if repo_exists_on_github(ssh_url):
        print(f"⚠️ That repo already exists on GitHub:\n   {ssh_url}")
        confirm = input("Are you trying to link this folder to that repo? [y/n]: ").lower()
        if confirm != 'y':
            print("❌ Aborting to avoid accidental overwrite.")
            sys.exit(1)

        compare_choice = input("Do you want to compare local files to what's on GitHub? [y/n]: ").lower()
        if compare_choice == 'y':
            tmp_path = "/tmp/quickrepo-temp-clone"
            run_cmd(f"rm -rf {tmp_path}")
            run_cmd(f"git clone {ssh_url} {tmp_path}")
            run_cmd(f"diff -rq {tmp_path} .")
            print("📎 Above are file differences between local and GitHub.\n")

        sync_choice = input("Choose sync option:\n"
                            "  [1] Pull changes from GitHub (rebase)\n"
                            "  [2] Overwrite GitHub with local (force push)\n"
                            "  [3] Cancel setup\n"
                            "→ ").strip()

        if sync_choice == '1':
            run_cmd(f"git remote add origin {ssh_url}")
            run_cmd("git pull origin main --rebase")
            print("✅ Synced with GitHub.")
        elif sync_choice == '2':
            run_cmd(f"git remote add origin {ssh_url}")
            run_cmd("git add .")
            run_cmd("git commit -m 'Force sync to GitHub'")
            run_cmd("git branch -M main")
            run_cmd("git push --force origin main")
            print("🔥 Force-pushed local files to GitHub.")
        else:
            print("❌ Aborted by user.")
            sys.exit(1)
    else:
        run_cmd(f"git remote add origin {ssh_url}")
        print(f"✅ Remote origin set: {ssh_url}\n")

    create_gitignore()

    run_cmd("git add .")
    print("✅ Staged all files.\n")

    commit_message = input("➤ Enter a commit message: ").strip() or "Initial commit"
    run_cmd(f'git commit -m "{commit_message}"')
    print(f"✅ Commit made: {commit_message}\n")

    run_cmd("git branch -M main")

    if input("➤ Push to GitHub now? [y/n]: ").lower() == 'y':
        success = run_cmd("git push -u origin main", check_success=True)
        if success:
            print("✅ Pushed to GitHub!\n")
        else:
            print("❌ Push failed.\n💡 Try:\n    git pull --rebase origin main\n")
    else:
        print("⚠️ Push skipped.\n")

    show_summary(username, email, ssh_url)

# ╭─────────────────────────────╮
# │  ENTRY POINT FOR EXECUTION │
# ╰─────────────────────────────╯
if __name__ == "__main__":
    main()

