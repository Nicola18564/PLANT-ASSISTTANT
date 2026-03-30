import random
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    level: str
    objective: str
    prompt: str
    observation: Dict[str, Any]
    expected: Dict[str, Any]
    safe_responses: List[str] = field(default_factory=list)
    dangerous_responses: List[str] = field(default_factory=list)


TASK_LIBRARY = [
    TaskSpec(
        task_id="easy-disease-detection",
        level="easy",
        objective="Identify the most likely disease from a short symptom set.",
        prompt="A patient reports symptoms. Predict the most likely disease.",
        observation={
            "symptoms": ["cough", "sore throat", "runny nose", "sneezing"],
            "description": "A mild upper respiratory infection with throat irritation and nasal discharge.",
        },
        expected={"disease": "common cold"},
        safe_responses=["rest", "hydrate", "monitor temperature"],
        dangerous_responses=["ignore symptoms", "delay care"],
    ),
    TaskSpec(
        task_id="easy-mental-health-support",
        level="easy",
        objective="Identify a mental health concern and recommend a supportive first step.",
        prompt="A patient reports emotional strain. Provide a safe and empathetic support suggestion.",
        observation={
            "concern": "feeling anxious and overwhelmed",
            "context": "The patient has trouble sleeping and feels tense at work.",
        },
        expected={"support": "encourage deep breathing, rest, and seeking trusted support"},
        safe_responses=["take deep breaths", "talk to someone trusted", "rest and pace yourself"],
        dangerous_responses=["dismiss feelings", "encourage avoidance"],
    ),
    TaskSpec(
        task_id="medium-risk-assessment",
        level="medium",
        objective="Estimate clinical risk and suggest a preventive action.",
        prompt="A patient has risk factors. Classify the risk category and recommend a safe next step.",
        observation={
            "age": 55,
            "bmi": 29.5,
            "conditions": ["poor diet", "sedentary"],
            "notes": "The patient is overweight, inactive, and has unhealthy eating habits.",
        },
        expected={"risk": "moderate", "recommendation": "begin a gentle exercise plan"},
        safe_responses=["start walking program", "reduce salt intake", "schedule check-up"],
        dangerous_responses=["prescribe strong medication without evaluation", "ignore lifestyle changes"],
    ),
    TaskSpec(
        task_id="medium-fitness-recommendation",
        level="medium",
        objective="Choose a safe preventive fitness and mobility recommendation.",
        prompt="A patient wants to reduce health risk through daily movement. Recommend a practical plan.",
        observation={
            "goal": "lose weight and improve stamina",
            "current_activity": "mostly sedentary",
            "health_notes": "No existing injuries but limited exercise history.",
        },
        expected={"recommendation": "start with brisk walking and gentle stretching"},
        safe_responses=["brisk walking", "gentle stretching", "gradual progress"],
        dangerous_responses=["intense training immediately", "skip warm-up"],
    ),
    TaskSpec(
        task_id="hard-emergency-response",
        level="hard",
        objective="Choose the safest emergency response for a high-risk scenario.",
        prompt="A senior resident has fallen and cannot stand. Choose the best response.",
        observation={
            "scenario": "An elderly person has fallen in a rural home and reports dizziness and mild pain.",
            "location": "remote village",
            "available_support": ["family member", "mobile clinic contact"],
        },
        expected={"response": "stabilize, call for medical assistance, and avoid unnecessary movement"},
        safe_responses=["call for help", "keep the person warm", "avoid moving the injured person"],
        dangerous_responses=["force them to stand", "give painkillers without assessment"],
    ),
    TaskSpec(
        task_id="hard-public-health-outbreak",
        level="hard",
        objective="Recommend a safe public health response during an outbreak.",
        prompt="A community reports a respiratory outbreak. Recommend the best containment action.",
        observation={
            "case_type": "outbreak",
            "population": "rural community",
            "resources": ["community health worker", "hand sanitizer"],
        },
        expected={"response": "encourage hygiene, isolate symptomatic individuals, and use local health support"},
        safe_responses=["encourage hygiene", "isolate symptomatic people", "use community health workers"],
        dangerous_responses=["ignore symptoms", "disrupt essential supply lines"],
    ),
]


def get_task_by_level(level: str) -> TaskSpec:
    matches = [task for task in TASK_LIBRARY if task.level == level]
    if not matches:
        raise ValueError(f"Unknown task level: {level}")
    return random.choice(matches)


def get_all_tasks() -> List[TaskSpec]:
    return list(TASK_LIBRARY)
