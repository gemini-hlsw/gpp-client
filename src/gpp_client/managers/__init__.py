from .call_for_proposals import CallForProposalsManager
from .configuration_request import ConfigurationRequestManager
from .group import GroupManager
from .observation import ObservationManager
from .program import ProgramManager
from .program_note import ProgramNoteManager
from .site_status import SiteStatusManager
from .target import TargetManager

__all__ = [
    "ProgramNoteManager",
    "TargetManager",
    "ProgramManager",
    "CallForProposalsManager",
    "ObservationManager",
    "SiteStatusManager",
    "GroupManager",
    "ConfigurationRequestManager",
]
