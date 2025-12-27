"""Compiler for declarative pipeline specs."""

from __future__ import annotations

from typing import Any

from cltk.core.data_types import Pipeline
from cltk.core.process_registry import ProcessRegistry
from cltk.pipeline.presets import get_preset
from cltk.pipeline.specs import PipelineSpec, StepSpec


def compile_processes(spec: PipelineSpec) -> list[Any]:
    """Compile a PipelineSpec into an ordered list of Process instances."""
    steps = _resolve_steps(spec)
    processes: list[Any] = []
    for step in steps:
        if not step.enabled:
            continue
        process_cls = ProcessRegistry.get_process(step.id)
        config = dict(step.config)
        if spec.language and "glottolog_id" not in config:
            config["glottolog_id"] = spec.language
        if spec.step_overrides and step.id in spec.step_overrides:
            config.update(spec.step_overrides[step.id])
        processes.append(process_cls(**config))
    return processes


def compile_pipeline(spec: PipelineSpec) -> Pipeline:
    """Compile a PipelineSpec into a Pipeline instance."""
    steps = _resolve_steps(spec)
    compiled = Pipeline(
        processes=compile_processes(spec),
        glottolog_id=spec.language,
        spec=PipelineSpec(
            preset=spec.preset,
            language=spec.language,
            steps=steps,
            step_overrides=spec.step_overrides,
            meta=spec.meta,
        ),
    )
    return compiled


def _resolve_steps(spec: PipelineSpec) -> list[StepSpec]:
    """Return ordered steps, falling back to the preset if needed."""
    if spec.steps:
        return list(spec.steps)
    if spec.preset:
        preset = get_preset(spec.preset)
        return list(preset.steps or [])
    raise ValueError("PipelineSpec must define steps or a preset.")
