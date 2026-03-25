"""Reporly Templates — report styling system."""
from .styles import Template, TEMPLATES

TEMPLATE_NAMES = list(TEMPLATES.keys())


def get_template(name: str = "minimal") -> Template:
    """Get template by name. Falls back to 'minimal' if not found."""
    return TEMPLATES.get(name, TEMPLATES["minimal"])


__all__ = ["get_template", "Template", "TEMPLATE_NAMES"]
