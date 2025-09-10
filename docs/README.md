# Model Training Protocol Documentation

This directory contains the Sphinx documentation for the Model Training Protocol (MTP) package.

## Building the Documentation

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Building HTML Documentation

To build the HTML documentation:

```bash
# Using make (Linux/macOS)
make html

# Using make.bat (Windows)
make.bat html

# Using sphinx-build directly
sphinx-build -b html source build
```

The built documentation will be available in the `build/html` directory.

### Building Other Formats

```bash
# PDF
make latexpdf

# EPUB
make epub
```

## Documentation Structure

- `source/` - Source files for the documentation
  - `index.rst` - Main documentation index
  - `getting_started.rst` - Installation and quick start guide
  - `system_architecture.rst` - System overview and architecture
  - `tokens.rst` - Token documentation
  - `tokensets.rst` - TokenSet documentation
  - `instructions.rst` - Instruction documentation
  - `guardrails.rst` - Guardrail documentation
  - `saving_models.rst` - Model saving and deployment
  - `api_reference.rst` - API reference documentation
  - `conf.py` - Sphinx configuration

## Read the Docs Integration

This documentation is configured to work with Read the Docs. The configuration is in `.readthedocs.yml` in the project root.

## Contributing to Documentation

When adding or modifying documentation:

1. Edit the appropriate `.rst` file in the `source/` directory
2. Build the documentation locally to check for errors
3. Follow the existing documentation style and structure
4. Update the table of contents in `index.rst` if adding new pages

## Documentation Style Guide

- Use clear, concise language
- Include code examples for all major features
- Follow the existing structure and formatting
- Use proper reStructuredText syntax
- Include cross-references between related sections
