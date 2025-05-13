<!-- # QuickRepo -->

<p align="center">
  <img src="assets/quickrepo.png" alt="quickrepo banner" width="40%">
</p>    

⚡ An interactive CLI tool for setting up Git repositories quickly, safely, and with a little magic.

## ✨ What It Does

QuickRepo helps you:

- Initialize a Git repository (if not already)
- Set your Git global username/email if missing
- Check for and generate SSH keys
- Add a remote origin (with smart URL handling)
- Detect if the GitHub repo already exists
- Offer sync strategies:
  - Pull changes from GitHub
  - Force-push local files
  - Compare GitHub to local before deciding
- Generate a `.gitignore` from common presets
- Make an initial commit and optionally push
- Display a project summary

All done via a clean terminal interaction — no guesswork, no accidental overwrites.

## 🛠 Installation

From the project directory:

```bash
pip install -e .
```

This creates a system-wide command:

```bash
quickrepo
```

## 📦 Usage

```bash
quickrepo           # Start interactive setup
quickrepo --dry-run # Simulate without making changes
quickrepo -h        # Show help
```

## 💡 Requirements

- Python 3.6+
- Git installed and available in your system PATH

## 📜 License

MIT — free to use, modify, and share.
