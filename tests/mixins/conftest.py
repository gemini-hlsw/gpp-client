import pytest

from gpp_client.managers.base_manager import BaseManager
from gpp_client.mixins.create import CreateMixin
from gpp_client.mixins.delete import (
    DeleteBatchByProgramIdMixin,
    DeleteBatchMixin,
    DeleteByIdViaBatchMixin,
)
from gpp_client.mixins.get import GetBatchByProgramIdMixin, GetBatchMixin, GetByIdMixin
from gpp_client.mixins.restore import (
    RestoreBatchByProgramIdMixin,
    RestoreByIdViaBatchMixin,
)
from gpp_client.mixins.update import (
    UpdateBatchByProgramIdMixin,
    UpdateBatchMixin,
    UpdateByIdMixin,
    UpdateByIdViaBatchMixin,
)


# All relevant mixins for broad test coverage.
class DummyManager(
    CreateMixin,
    DeleteBatchMixin,
    DeleteByIdViaBatchMixin,
    DeleteBatchByProgramIdMixin,
    GetByIdMixin,
    GetBatchMixin,
    GetBatchByProgramIdMixin,
    RestoreByIdViaBatchMixin,
    RestoreBatchByProgramIdMixin,
    UpdateByIdMixin,
    UpdateBatchByProgramIdMixin,
    UpdateBatchMixin,
    BaseManager,
):
    default_fields = "id name"
    resource_id_field = "dummyId"
    queries = {
        "create": "mutation { create(input: {fields}) }",
        "delete_batch": "mutation { delete(input: {fields}) }",
        "delete_by_id": "mutation { deleteById(input: {fields}) }",
        "delete_batch_by_program_id": "mutation { deleteProgram(input: {fields}) }",
        "update_by_id": "mutation { updateById(input: {fields}) }",
        "get_by_id": "query { resource(id: $id) { {fields} } }",
        "get_batch": "query { resources(where: $where) { {fields} } }",
        "get_batch_by_program_id": "query { programResources(where: $where) { {fields} } }",
        "restore_by_id": "mutation { restoreById(input: {fields}) }",
        "restore_batch_by_program_id": "mutation { restoreProgram(input: {fields}) }",
        "update_batch": "mutation { updateBatch(input: {fields}) }",
        "update_batch_by_program_id": "mutation { updateProgram(input: {fields}) }",
    }


@pytest.fixture()
def manager(mocker) -> DummyManager:
    manager = DummyManager(client=mocker.MagicMock())
    return manager


# Need this one because 'update_by_id' is shared between two different mixins.
class UpdateByIdViaBatchDummyManager(
    UpdateByIdViaBatchMixin,
    BaseManager,
):
    default_fields = "id name"
    resource_id_field = "dummyId"
    queries = {
        "update_by_id": "mutation { updateById(input: {fields}) }",
    }

@pytest.fixture()
def update_by_id_via_batch_manager(mocker) -> UpdateByIdViaBatchDummyManager:
    manager = UpdateByIdViaBatchDummyManager(client=mocker.MagicMock())
    return manager
