#!/usr/bin/env python3
"""
AIKAILNOV4 Setup Script
AI-Powered Kali Linux Security System
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aikailnov4",
    version="1.0.0",
    author="AIKAILNOV4 Team",
    author_email="support@aikailnov4.com",
    description="AI-Powered Kali Linux Security System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goody81/AIKAILNOV4",
    project_urls={
        "Bug Tracker": "https://github.com/goody81/AIKAILNOV4/issues",
        "Documentation": "https://github.com/goody81/AIKAILNOV4/docs",
        "Source Code": "https://github.com/goody81/AIKAILNOV4",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aikail=src.core.aikail:main",
            "aikail-server=src.api.server:main",
            "aikail-update=scripts.update:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt"],
    },
    zip_safe=False,
    keywords=[
        "security",
        "penetration testing",
        "kali linux",
        "ai",
        "machine learning",
        "vulnerability scanner",
        "network security",
        "cybersecurity",
        "ethical hacking",
    ],
)
