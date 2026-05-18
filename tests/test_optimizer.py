import random

from backend.optimizer import (
    apply_regex_transforms,
    compute_additional_scores,
    optimize_prompt,
    set_seed,
)
from backend.main import score_clarity, score_specificity, generate_variation


def test_score_functions_ranges():
    text = "This is a clear and specific prompt with example 123."
    assert 30 <= score_clarity(text) <= 98
    assert 25 <= score_specificity(text) <= 97


def test_regex_transform_cleanup():
    result = apply_regex_transforms("please   do   this")
    assert "  " not in result.text
    assert not result.text.lower().startswith("please")


def test_optimize_prompt_uses_template():
    result = optimize_prompt("Analyze data", "evolutionary", "summary", 0.0)
    assert "Summarize" in result.text


def test_deterministic_seed():
    set_seed(42)
    first = generate_variation("Base", "evolutionary", "summary", 1.0, 1)
    set_seed(42)
    second = generate_variation("Base", "evolutionary", "summary", 1.0, 1)
    assert first.text == second.text


def test_additional_scores_keys():
    scores = compute_additional_scores("Simple prompt")
    assert set(scores.keys()) == {
        "length",
        "tone",
        "formality",
        "bias",
        "fluency",
        "hallucination_risk",
    }