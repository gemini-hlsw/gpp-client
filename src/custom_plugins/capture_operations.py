__all__ = ["CAPTURE_KEY", "CaptureOperationsPlugin"]

from ariadne_codegen.plugins.base import Plugin

from graphql import ExecutableDefinitionNode

CAPTURE_KEY = "captured_operations"
"""Key under ``[tool.gpp-client]`` of the list that receives each operation."""


class CaptureOperationsPlugin(Plugin):
    def generate_operation_str(
        self, operation_str: str, operation_definition: ExecutableDefinitionNode
    ) -> str:
        """
        Hand the build each operation exactly as the generated client embeds it.

        Parameters
        ----------
        operation_str : str
            The operation and the fragments it uses.
        operation_definition : ExecutableDefinitionNode
            The operation.

        Returns
        -------
        str
            ``operation_str``, unchanged.
        """
        sink = self.config_dict.get("tool", {}).get("gpp-client", {}).get(CAPTURE_KEY)
        if sink is not None:
            sink.append(operation_str)
        return operation_str
