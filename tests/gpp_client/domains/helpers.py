"""
Helper functions for domain tests.
"""

__all__ = ["_yield_events"]


async def _yield_events(events):
    """
    Yield test events.
    """
    for event in events:
        yield event
