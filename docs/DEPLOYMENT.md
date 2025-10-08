# Documentation Deployment Guide

This guide explains how to build and deploy the Model Train Protocol documentation using GitHub Actions and Read the Docs.

## Overview

The documentation is built using Sphinx and can be deployed in multiple ways:

1. **Read the Docs** - Automatic builds when you push to main
2. **GitHub Pages** - Hosted directly from GitHub
3. **Manual builds** - For local development and testing

The documentation is currently deployed on Read the Docs

## Setup Instructions

### 1. Read the Docs Setup (Recommended)

1. **Connect your repository to Read the Docs:**
   - Go to [readthedocs.org](https://readthedocs.org)
   - Sign in with your GitHub account
   - Click "Import a Project"
   - Select your repository: `databiomes/modeltrainprotocol`
   - Configure the project settings:
     - **Name**: `model-train-protocol`
     - **Repository**: `https://github.com/databiomes/modeltrainprotocol`
     - **Default branch**: `main`
     - **Documentation type**: Sphinx
     - **Configuration file**: `.readthedocs.yml`

2. **Configure build settings:**
   - The `.readthedocs.yml` file is already configured
   - Read the Docs will automatically build when you push to main
   - Your docs will be available at: `https://model-train-protocol.readthedocs.io/`

3. **Enable automatic builds:**
   - In your Read the Docs project settings, enable "Build pull requests"
   - This will build docs for PRs to help catch documentation issues early

### 2. GitHub Pages Setup (Alternative)

If you prefer to host docs on GitHub Pages:

1. **Enable GitHub Pages:**
   - Go to your repository settings
   - Navigate to "Pages" section
   - Select "GitHub Actions" as the source

2. **Use the docs-branch workflow:**
   - The `.github/workflows/docs-branch.yml` workflow will build docs to a `docs-branch`
   - Configure GitHub Pages to serve from the `docs-branch`

3. **Your docs will be available at:**
   - `https://databiomes.github.io/modeltrainprotocol/`

## Workflow Files

### `.github/workflows/docs.yml`
- **Purpose**: Main documentation workflow
- **Triggers**: Push to main/develop, PRs
- **Features**:
  - Builds and tests documentation
  - Deploys to GitHub Pages (if enabled)
  - Provides guidance for Read the Docs integration

### `.github/workflows/docs-branch.yml`
- **Purpose**: Alternative deployment to separate branch
- **Triggers**: Push to main/develop, manual dispatch
- **Features**:
  - Builds docs and pushes to `docs-branch`
  - Useful for GitHub Pages or custom hosting

## Local Development

### Building Documentation Locally

```bash
# Install dependencies
pip install -r docs/requirements.txt
pip install -e .

# Build documentation
cd docs
make html

# View the built docs
open build/html/index.html
```

### Testing Documentation

```bash
# Check for broken links and errors
cd docs
make linkcheck

# Build in different formats
make pdf
make epub
```

## Configuration Files

### `.readthedocs.yml`
- Configures Read the Docs build environment
- Specifies Python version, dependencies, and build commands
- Includes build settings for consistent builds

### `docs/source/conf.py`
- Sphinx configuration
- Defines project metadata, extensions, and theme
- Configures autodoc for API documentation

### `docs/requirements.txt`
- Documentation-specific dependencies
- Includes Sphinx, theme, and extensions

## Troubleshooting

### Common Issues

1. **Import errors in autodoc:**
   - Ensure your package is installed in development mode: `pip install -e .`
   - Check that all dependencies are listed in `pyproject.toml`

2. **Build failures on Read the Docs:**
   - Check the build logs in your Read the Docs dashboard
   - Ensure `.readthedocs.yml` is properly configured
   - Verify that all dependencies are in `docs/requirements.txt`

3. **GitHub Pages not updating:**
   - Check that GitHub Pages is enabled in repository settings
   - Verify the workflow has the correct permissions
   - Ensure the workflow is running on the correct branch

### Getting Help

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review [Read the Docs documentation](https://docs.readthedocs.io/)
- Look at [GitHub Actions documentation](https://docs.github.com/en/actions)

## Best Practices

1. **Keep documentation up to date:**
   - Update docs when you change code
   - Use the PR workflow to catch doc issues early

2. **Test locally first:**
   - Always build docs locally before pushing
   - Check for broken links and formatting issues

3. **Use meaningful commit messages:**
   - Include "docs:" prefix for documentation changes
   - Reference issues or PRs when relevant

4. **Monitor build status:**
   - Check Read the Docs build status regularly
   - Fix build failures promptly

