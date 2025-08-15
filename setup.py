#!/usr/bin/env python3
"""
Setup script for LLM-Based Cybercrime Case Classification
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="llm-cybercrime-classification",
    version="1.0.0",
    author="Sanjay Singh",
    author_email="your.email@example.com",
    description="A semi-automated workflow for classifying cybercrime cases using LLM with human oversight",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Security",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cybercrime-classify=semi_automated_classification:main",
            "update-schema=update_schema_from_results:main",
            "analyze-tags=analyze_tag_distributions:main",
        ],
    },
)
