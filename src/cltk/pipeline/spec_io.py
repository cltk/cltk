"""I/O helpers for pipeline specifications."""

from pathlib import Path
from typing import Any

from cltk.core.cltk_logger import logger
from cltk.pipeline.presets import get_preset, list_presets
from cltk.pipeline.specs import PipelineSpec, StepSpec

try:  # Python 3.11+
    import tomllib as _toml
except Exception:  # pragma: no cover - fallback for older runtimes
    import tomli as _toml  # type: ignore[import-not-found,no-redef]


def load_pipeline_spec(path: str | Path) -> PipelineSpec:
    """Load a TOML pipeline spec from disk."""
    spec_path = Path(path)
    data = _toml.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Pipeline TOML must decode to a table.")

    step_table = data.get("step") or {}
    step_entries = (
        _flatten_step_table(step_table) if isinstance(step_table, dict) else {}
    )

    overrides_table = data.get("step_overrides") or {}
    overrides = (
        _flatten_step_table(overrides_table)
        if isinstance(overrides_table, dict)
        else {}
    )

    steps_order = data.get("steps")
    preset_name = data.get("preset")
    language = data.get("language")
    meta = data.get("meta") or {}

    base_steps: list[StepSpec] = []
    base_configs: dict[str, dict[str, Any]] = {}
    base_enabled: dict[str, bool] = {}

    if steps_order is None:
        if not preset_name:
            presets = ", ".join(list_presets())
            raise ValueError(
                f"Missing steps list. Provide 'steps' or a 'preset'. Available presets: {presets}"
            )
        preset = get_preset(preset_name)
        base_steps = preset.steps or []
        base_configs = {step.id: dict(step.config) for step in base_steps}
        base_enabled = {step.id: step.enabled for step in base_steps}
        if language is None:
            language = preset.language
    else:
        if not isinstance(steps_order, list) or not all(
            isinstance(step, str) for step in steps_order
        ):
            raise ValueError("'steps' must be a list of process_id strings.")

    ordered_ids: list[str] = (
        [step.id for step in base_steps] if steps_order is None else list(steps_order)
    )

    extras = [step_id for step_id in step_entries if step_id not in ordered_ids]
    if extras and steps_order is None:
        logger.info("Appending un-ordered steps from [step.*]: %s", ", ".join(extras))
        ordered_ids.extend(sorted(extras))

    merged_overrides = {
        step_id: dict(cfg)
        for step_id, cfg in overrides.items()
        if isinstance(cfg, dict)
    }

    steps: list[StepSpec] = []
    for step_id in ordered_ids:
        config: dict[str, Any] = {}
        enabled = base_enabled.get(step_id, True)
        if step_id in base_configs:
            config.update(base_configs[step_id])
        entry = step_entries.get(step_id, {})
        if entry:
            entry = dict(entry)
            enabled = bool(entry.pop("enabled", enabled))
            config.update(entry)
        if step_id in merged_overrides:
            config.update(merged_overrides[step_id])
        steps.append(StepSpec(id=step_id, enabled=enabled, config=config))

    return PipelineSpec(
        preset=preset_name,
        language=language,
        steps=steps,
        step_overrides=merged_overrides,
        meta=meta if isinstance(meta, dict) else {},
    )


def _flatten_step_table(table: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Flatten nested [step.*] tables into dot-joined keys."""
    flattened: dict[str, dict[str, Any]] = {}

    def _is_leaf(node: dict[str, Any]) -> bool:
        """Return True when the node maps directly to a step config."""
        if "enabled" in node or "config" in node:
            return True
        return any(not isinstance(value, dict) for value in node.values())

    def _walk(prefix: str, node: dict[str, Any]) -> None:
        """Walk nested step tables and accumulate flattened entries."""
        for key, value in node.items():
            if not isinstance(value, dict):
                continue
            if "." in key:
                full_key = f"{prefix}.{key}" if prefix else key
                flattened[full_key] = value
                continue
            full_key = f"{prefix}.{key}" if prefix else key
            if _is_leaf(value):
                flattened[full_key] = value
            else:
                _walk(full_key, value)

    if table:
        _walk("", table)
    return flattened
