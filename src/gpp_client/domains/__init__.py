"""
This module defines the domain classes for the GPP client. Each domain class
encapsulatess specific areas of functionality related to GPP, such as handling
observations, targets, programs,and workflow states. These domain classes provide
high-level methods that internally use the client's GraphQL and REST clients to
interact with the GPP API, abstracting away the details of making requests and handling
responses.
"""

from .atom import AtomDomain
from .attachment import AttachmentDomain
from .goats import GOATSDomain
from .observation import ObservationDomain
from .program import ProgramDomain
from .scheduler import SchedulerDomain
from .site_status import SiteStatusDomain
from .target import TargetDomain
from .workflow_state import WorkflowStateDomain

__all__ = [
    "AtomDomain",
    "TargetDomain",
    "WorkflowStateDomain",
    "GOATSDomain",
    "ObservationDomain",
    "ProgramDomain",
    "SchedulerDomain",
    "SiteStatusDomain",
    "AttachmentDomain",
]
