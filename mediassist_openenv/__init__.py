"""MediAssist OpenEnv package entrypoint."""

from .core import (
    detect_disease,
    guide_patient,
    suggest_medication,
    recommend_doctor,
    predict_risk,
)
from .support import (
    mental_health_support,
    fitness_recommendations,
    monitor_health,
)
from .scenarios import (
    rural_healthcare_advice,
    accessibility_support,
    public_health_advice,
    elderly_fall_detection,
    voice_assistant_prompt,
)
from .app import run

__all__ = [
    "detect_disease",
    "guide_patient",
    "suggest_medication",
    "recommend_doctor",
    "predict_risk",
    "mental_health_support",
    "fitness_recommendations",
    "monitor_health",
    "rural_healthcare_advice",
    "accessibility_support",
    "public_health_advice",
    "elderly_fall_detection",
    "voice_assistant_prompt",
    "run",
]
