import typer

from ...managers.call_for_proposals import CallForProposalsManager
from ..utils import async_cli_method

call_for_proposals = typer.Typer(help="Manage Calls for Proposals")


def print_get_all_results(result: dict):
    cfps = result["callsForProposals"]
    for cfp in cfps.get("matches", []):
        typer.echo(f"- {cfp['id']}: {cfp.get('title', 'Untitled')} ({cfp['semester']})")


# Register command dynamically
async_cli_method(
    app=call_for_proposals,
    manager_class=CallForProposalsManager,
    manager_attr="call_for_proposals",
    method_name="get_all",
    handle_result=print_get_all_results,
)
