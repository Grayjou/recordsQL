# recordsql Documentation

This directory contains the Sphinx documentation for recordsql.

## Building the Documentation

### Prerequisites

Make sure you have the development dependencies installed:

```bash
poetry install
```

Or if you're not using Poetry:

```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

### Building HTML Documentation

To build the HTML documentation, run:

```bash
cd docs
make html
```

Or on Windows:

```bash
cd docs
make.bat html
```

The generated HTML files will be in `_build/html/`. Open `_build/html/index.html` in your browser to view the documentation.

### Other Build Formats

Sphinx supports various output formats. To see all available formats:

```bash
make help
```

Common formats include:
- `make html` - HTML documentation
- `make latex` - LaTeX files for PDF generation
- `make text` - Plain text documentation
- `make man` - Manual pages
- `make epub` - EPUB documentation

### Cleaning Build Files

To remove generated documentation:

```bash
make clean
```

## Documentation Structure

- `conf.py` - Sphinx configuration file
- `index.rst` - Main documentation page
- `installation.rst` - Installation instructions
- `quickstart.rst` - Quick start guide
- `examples.rst` - Advanced usage examples
- `api.rst` - API reference (auto-generated from docstrings)
- `_static/` - Static files (CSS, images, etc.)
- `_templates/` - Custom templates
- `_build/` - Generated documentation (not committed to git)

## Contributing to Documentation

When adding new features or making changes to the API:

1. Update or add docstrings in the Python code
2. Update relevant `.rst` files if needed
3. Rebuild the documentation to ensure there are no errors
4. Review the generated HTML to verify your changes

## Documentation Style

We use Google-style docstrings. Example:

```python
def function_name(param1, param2):
    """Brief description of function.

    More detailed description if needed.

    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.

    Returns:
        type: Description of return value.

    Raises:
        ExceptionType: Description of when this exception is raised.

    Example:
        >>> function_name(1, 2)
        3
    """
    pass
```
