"""Tests for process registry behavior."""

from typing import ClassVar

from cltk.core.data_types import Doc, Process
from cltk.core.process_registry import ProcessRegistry, register_process


class DummyProcess(Process):
    """Stub process for registry tests."""

    process_id: ClassVar[str] = "test.dummy"

    def run(self, input_doc: Doc) -> Doc:  # pragma: no cover - trivial passthrough
        return input_doc


@register_process
class DecoratedDummyProcess(DummyProcess):
    """Stub process registered via decorator."""

    process_id: ClassVar[str] = "test.decorated"


def test_process_registry_register_and_get() -> None:
    """Register and retrieve process classes by id."""
    ProcessRegistry.register(DummyProcess)
    assert ProcessRegistry.get_process("test.dummy") is DummyProcess
    assert "test.dummy" in ProcessRegistry.list_processes()
    assert ProcessRegistry.get_process("test.decorated") is DecoratedDummyProcess
