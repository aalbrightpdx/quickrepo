from setuptools import setup

setup(
    name="quickrepo",
    version="0.1",
    py_modules=["quickrepo"],
    entry_points={
        "console_scripts": [
            "quickrepo = quickrepo:main",
        ],
    },
    install_requires=[],
    author="Aaron and Rue 🧚‍♀️",
    description="Smart Git repo setup tool with SSH checks, .gitignore presets, and GitHub sync",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
)

