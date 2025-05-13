#!/usr/bin/env python3

# setup.py — QuickRepo CLI Installer
import os
import sys
from setuptools import setup

def intro_message():
    print("""
📦 QuickRepo CLI Installer

This script sets up your `quickrepo.py` as a system-wide command using:

    pip install -e .

Once installed, you'll be able to run:

    quickrepo             → Launch the tool
    quickrepo --dry-run   → Simulate everything
    quickrepo -h          → Show help

🧚 This is a local, editable install — any changes to your source file apply instantly.
""")

def confirm_or_exit():
    proceed = input("✨ Ready to install QuickRepo as a CLI tool? [y/n]: ").strip().lower()
    if proceed != 'y':
        print("❌ Installation cancelled.")
        sys.exit(0)

def auto_install():
    if input("Would you like me to run `pip install -e .` for you now? [y/n]: ").lower() == 'y':
        os.system("pip install -e .")
        print("✅ Installed. Try running: quickrepo")
    else:
        print("\n💡 You can install manually anytime with:\n    pip install -e .\n")

# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    intro_message()
    confirm_or_exit()

    setup(
        name="quickrepo",
        version="0.1",
        py_modules=["quickrepo"],
        entry_points={
            "console_scripts": [
                "quickrepo = quickrepo:main",
            ],
        },
        author="Aaron (with Rue 🧚)",
        description="Interactive Git repo initializer with smart sync and .gitignore presets",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Environment :: Console",
        ],
        python_requires=">=3.6",
    )

    auto_install()

