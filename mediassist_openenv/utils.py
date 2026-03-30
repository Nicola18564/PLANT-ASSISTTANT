"""Utility helpers for MediAssist OpenEnv."""
from typing import List


def normalize_text(text: str) -> str:
    return text.strip().lower()


def parse_symptoms(text: str) -> List[str]:
    separators = [",", ";", " and ", " / ", "|"]
    cleaned = text.lower()
    for sep in separators:
        cleaned = cleaned.replace(sep, "|")
    return [segment.strip() for segment in cleaned.split("|") if segment.strip()]


def format_list(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
