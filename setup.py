from setuptools import setup

with open("requirements.txt", "r") as requirements_file:
    install_requires = [line.strip() for line in requirements_file]

setup(
    name="paperviz",
    version="0.1.0",
    description="Publication-ready plots, tables, layouts, and LaTeX export",
    author="Lars Quaedvlieg",
    author_email="larsquaedvlieg@outlook.com",
    packages=["paperviz"],
    install_requires=install_requires,
)
