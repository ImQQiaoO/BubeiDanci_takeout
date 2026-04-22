import sys
from pathlib import Path


def get_app_base_dir() -> Path:
    """Return runtime base dir: exe folder when frozen, project root in source mode."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def resolve_resource_path(*parts: str) -> Path:
    return get_app_base_dir().joinpath(*parts)


def resolve_output_path(file_name: str) -> Path:
    return get_app_base_dir().joinpath(file_name)
