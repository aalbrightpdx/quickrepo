from setuptools import setup

setup(
    name="quickrepo",
    version="0.1",
    py_modules=["quickrepo"],  # assumes quickrepo.py exists in this dir
    entry_points={
        "console_scripts": [
            "quickrepo = quickrepo:main",  # links 'quickrepo' command to main() in quickrepo.py
        ],
    },
    author="aalbrightpdx",
    description="Interactive Git repo initializer with smart sync and .gitignore presets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
)

