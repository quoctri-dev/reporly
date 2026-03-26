"""Reporly Templates — NoVa default style."""
from .styles import Template, TEMPLATES


def get_template(name: str = "nova") -> Template:
    """Get NoVa template (single default)."""
    return TEMPLATES["nova"]


__all__ = ["get_template", "Template", "TEMPLATES"]
