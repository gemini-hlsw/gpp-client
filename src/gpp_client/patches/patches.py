__all__ = [
    "patch_base_operations_graphql_field__format_variable_name",
    "patch_base_operations_graphql_field_get_formatted_variables",
]

from typing import Any, Set

from ..api.base_operation import GraphQLField


def patch_base_operations_graphql_field__format_variable_name() -> None:
    """
    This method is taken directly from the original generated code in `api`,
    with the duplicate name logic commented out. This change ensures that GraphQL
    variables like `includeDeleted` are preserved with stable names across nested
    resources (e.g., when querying `program` from within `target`).

    The original implementation aggressively renamed variables to avoid duplicates,
    which inadvertently dropped shared variables or renamed them inconsistently-
    breaking propagation in nested structures. This patch ensures consistent naming
    by avoiding unnecessary renaming, allowing shared variables to work as expected.
    We are not aware of any issues caused by this patch.

    This is not in use right now, a relic of a patch before the real issue was
    discovered. Holding onto this until further testing concludes this is not needed.
    """

    def _format_variable_name(
        self, idx: int, var_name: str, used_names: Set[str]
    ) -> str:
        """Generates a unique variable name by appending an index and,
        if necessary, an additional counter to avoid duplicates."""
        base_name = f"{var_name}_{idx}"
        unique_name = base_name
        # counter = 1

        # Ensure the generated name is unique
        # while unique_name in used_names:
        #     unique_name = f"{base_name}_{counter}"
        #     counter += 1

        # Add the unique name to the set of used names
        used_names.add(unique_name)

        return unique_name

    GraphQLField._format_variable_name = _format_variable_name


def patch_base_operations_graphql_field_get_formatted_variables() -> None:
    """
    The generated client missed variables that were declared deep inside the
    field tree. It only kept the variables that belonged to each direct child
    node. If a nested field, for example program(includeDeleted) inside
    targets, added its own variable, the query referenced that variable but the
    accompanying variables payload did not include a value. The server then
    returned an error saying the variable was undefined.

    This patch replaces the method with one that walks through every level of
    the field tree, gathers the variables from every sub-field and inline
    fragment, and returns them in a single flat dictionary. With every value
    now present in the payload, the undefined-variable error is resolved.
    """

    def get_formatted_variables(self) -> dict[str, dict[str, Any]]:
        """
        Recursively collect all variables under this field.

        Returns
        -------
        dict[str, dict[str, Any]]
            The formatted variables.
        """
        formatted_variables = self.formatted_variables.copy()

        # Collect from direct sub‑fields.
        for subfield in self._subfields:
            formatted_variables.update(subfield.get_formatted_variables())

        # Collect from inline fragments.
        for subfields in self._inline_fragments.values():
            for subfield in subfields:
                formatted_variables.update(subfield.get_formatted_variables())

        return formatted_variables

    GraphQLField.get_formatted_variables = get_formatted_variables
