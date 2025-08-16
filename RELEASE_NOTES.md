# Release Notes - v1.0.0

## What's New

This is the first public release of the LLM-Based Cybercrime Case Classification system, designed to be easily distributable and user-friendly.

## Features

### Core Functionality
- **Semi-automated classification** using Claude (Anthropic) LLM
- **Three-stage iterative workflow** for schema refinement
- **Human oversight integration** for quality assurance
- **Automatic schema updates** based on classification results
- **Comprehensive tag distribution analysis**

### User Experience Improvements
- **One-click installation** scripts for Unix and Windows
- **Clear documentation** with step-by-step instructions
- **Demo script** for testing with sample data
- **Configuration examples** for customization
- **Progress tracking** and resume capability

## Installation Options

### Quick Start (Recommended)
```bash
# Unix/Linux/macOS
./install.sh

# Windows
install.bat
```

### Manual Installation
```bash
git clone https://github.com/sanjaysingh13/llm_based_categorization_of_cyber_cases.git
cd llm_based_categorization_of_cyber_cases
python3.12 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
```

## System Requirements

- **Python**: 3.12 or higher
- **Memory**: 8GB+ RAM recommended for large datasets
- **Storage**: 2GB+ free space
- **Network**: Stable internet connection for API calls
- **API Key**: Anthropic Claude API key

## What's Included

### Core Scripts
- `semi_automated_classification.py` - Main classification workflow
- `update_schema_from_results.py` - Schema enhancement automation
- `analyze_tag_distributions.py` - Tag distribution analysis

### Configuration & Setup
- `requirements.txt` - Python dependencies
- `setup.py` - Package installation
- `config.example.py` - Configuration template
- `.env` template - API key configuration

### Documentation
- `README.md` - Quick start guide
- `INSTRUCTIONS.md` - Detailed workflow documentation
- `RELEASE_NOTES.md` - This file

### Installation Scripts
- `install.sh` - Unix/Linux/macOS setup
- `install.bat` - Windows setup
- `demo.py` - System demonstration

## Workflow Overview

1. **Stage 1**: Initial classification (100 cases) - ~$5-6
2. **Stage 2**: Manual review and schema update
3. **Stage 3**: Validation (500 cases) - ~$25-30
4. **Stage 4**: Final schema refinement
5. **Stage 5**: Full processing (remaining cases) - ~$80-85
6. **Stage 6**: Tag distribution analysis

## Cost Estimate

- **Total Dataset**: ~$110-120
- **Demo (3 cases)**: ~$0.05-0.10
- **Stage 1**: ~$5-6
- **Stage 2**: ~$25-30
- **Stage 3**: ~$80-85

## Getting Help

1. **Start with demo**: Run `python demo.py` to test the system
2. **Check README.md**: Quick start guide and workflow overview
3. **Review INSTRUCTIONS.md**: Detailed technical documentation
4. **Examine examples**: Look at existing output files for reference

## Future Enhancements

- Web-based interface for easier interaction
- Batch processing optimization for very large datasets
- Additional LLM provider support

## Support

For issues and questions:
1. Check the documentation files
2. Review existing output files for examples
3. Ensure all dependencies are properly installed
4. Verify API key configuration

---

**Version**: 1.0.0  
**Release Date**: December 2024  
**Compatibility**: Python 3.12+, Cross-platform
