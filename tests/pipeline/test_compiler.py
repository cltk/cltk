"""Tests for compiling declarative pipeline specs."""

from cltk.pipeline.compiler import compile_pipeline
from cltk.pipeline.specs import PipelineSpec, StepSpec


def test_compile_pipeline_respects_enabled_and_order() -> None:
    """Compile steps in order and skip disabled entries."""
    spec = PipelineSpec(
        language="lati1261",
        steps=[
            StepSpec(id="normalize"),
            StepSpec(id="sentence_split", enabled=False),
            StepSpec(
                id="morphosyntax.genai",
                config={"prompt_profile": "latin_ud_strict"},
            ),
        ],
    )
    pipeline = compile_pipeline(spec)
    assert pipeline.processes is not None
    names = [proc.__class__.__name__ for proc in pipeline.processes]
    assert names == ["NormalizeProcess", "GenAIMorphosyntaxProcess"]
    assert pipeline.processes[1].prompt_profile == "latin_ud_strict"
    assert pipeline.processes[1].glottolog_id == "lati1261"
    assert pipeline.spec is not None
    assert len(pipeline.spec.steps or []) == 3
