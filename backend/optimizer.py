import random
import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class OptimizationStrategyResult:
	text: str
	techniques: List[str]


def set_seed(seed: int) -> None:
	"""Set random seed for deterministic runs."""
	random.seed(seed)


def apply_template(base: str, use_case: str) -> OptimizationStrategyResult:
	templates = {
		"email": "Write a professional email with subject and greeting. {prompt}",
		"summary": "Summarize the following in 5 bullets with key takeaways: {prompt}",
		"code": "Provide a code solution with explanation and tests: {prompt}",
		"extraction": "Extract structured fields from the text: {prompt}",
	}
	template = templates.get(use_case.lower(), "{prompt}")
	return OptimizationStrategyResult(
		text=template.format(prompt=base),
		techniques=["Template"]
	)


def apply_regex_transforms(base: str) -> OptimizationStrategyResult:
	text = base
	text = re.sub(r"\s+", " ", text).strip()
	text = re.sub(r"(?i)please\s+", "", text)
	techniques = ["Regex cleanup"]
	return OptimizationStrategyResult(text=text, techniques=techniques)


def apply_qa_guided_rewrite(base: str) -> OptimizationStrategyResult:
	questions = [
		"What is the desired output format?",
		"What constraints or limits apply?",
		"Who is the target audience?",
	]
	text = base + "\n\nAnswer these before responding:\n" + "\n".join(
		f"- {q}" for q in questions
	)
	return OptimizationStrategyResult(text=text, techniques=["QA guided"])


def apply_evolutionary(base: str, creativity: float) -> OptimizationStrategyResult:
	mutations = [
		"Be specific and include concrete examples.",
		"Structure your response with clear sections.",
		"You are an expert in this field.",
		"Think step by step and explain your reasoning.",
		"Keep the response under 500 words.",
	]
	if random.random() < creativity:
		mutation = random.choice(mutations)
		return OptimizationStrategyResult(
			text=f"{base} {mutation}",
			techniques=["Evolutionary"]
		)
	return OptimizationStrategyResult(text=base, techniques=["Evolutionary"])


def apply_reinforcement(base: str, creativity: float) -> OptimizationStrategyResult:
	rewrites = [
		"Use clear, unambiguous language.",
		"Break this task into sub-tasks.",
		"Do NOT include filler words or vague statements.",
	]
	if random.random() < creativity:
		rewrite = random.choice(rewrites)
		return OptimizationStrategyResult(
			text=f"{base} {rewrite}",
			techniques=["Reinforcement"]
		)
	return OptimizationStrategyResult(text=base, techniques=["Reinforcement"])


def optimize_prompt(
	base: str,
	strategy: str,
	use_case: str,
	creativity: float,
) -> OptimizationStrategyResult:
	techniques: List[str] = []
	text = base

	if use_case:
		template_result = apply_template(text, use_case)
		text = template_result.text
		techniques.extend(template_result.techniques)

	regex_result = apply_regex_transforms(text)
	text = regex_result.text
	techniques.extend(regex_result.techniques)

	if strategy in ["evolutionary", "hybrid"]:
		evo = apply_evolutionary(text, creativity)
		text = evo.text
		techniques.extend(evo.techniques)

	if strategy in ["reinforcement", "hybrid"]:
		reinf = apply_reinforcement(text, creativity)
		text = reinf.text
		techniques.extend(reinf.techniques)

	if strategy in ["qa", "hybrid"]:
		qa = apply_qa_guided_rewrite(text)
		text = qa.text
		techniques.extend(qa.techniques)

	return OptimizationStrategyResult(text=text, techniques=techniques)


def score_length(text: str) -> int:
	length = len(text)
	if length < 50:
		return 40
	if length < 200:
		return 70
	if length < 500:
		return 85
	return 60


def score_tone(text: str) -> int:
	score = 60
	if any(word in text.lower() for word in ["please", "kindly", "thanks"]):
		score += 10
	if any(word in text.lower() for word in ["urgent", "asap"]):
		score -= 8
	return min(95, max(30, score))


def score_formality(text: str) -> int:
	score = 55
	if any(word in text.lower() for word in ["therefore", "however", "furthermore"]):
		score += 15
	if any(word in text.lower() for word in ["gonna", "wanna", "btw"]):
		score -= 10
	return min(95, max(30, score))


def score_bias(text: str) -> int:
	score = 70
	if any(word in text.lower() for word in ["always", "never", "everyone", "no one"]):
		score -= 10
	return min(95, max(20, score))


def score_fluency(text: str) -> int:
	score = 60
	if re.search(r"\b(and and|the the|to to)\b", text.lower()):
		score -= 10
	return min(95, max(30, score))


def score_hallucination_risk(text: str) -> int:
	score = 70
	if any(word in text.lower() for word in ["guaranteed", "always correct", "100%"]):
		score -= 15
	return min(95, max(20, score))


def compute_additional_scores(text: str) -> Dict[str, int]:
	return {
		"length": score_length(text),
		"tone": score_tone(text),
		"formality": score_formality(text),
		"bias": score_bias(text),
		"fluency": score_fluency(text),
		"hallucination_risk": score_hallucination_risk(text),
	}
