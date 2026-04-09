"""
Commands for the GPP CLI.
"""

from .attachment import attachment_app
from .goats import goats_app
from .observation import observation_app
from .program import program_app
from .scheduler import scheduler_app
from .site_status import site_status_app
from .target import target_app
from .workflow_state import workflow_state_app

__all__ = [
    "observation_app",
    "program_app",
    "attachment_app",
    "target_app",
    "workflow_state_app",
    "site_status_app",
    "goats_app",
    "scheduler_app",
]
