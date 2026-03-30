"""Scenario-based support for rural, accessibility, public health, and emergency cases."""
from typing import Dict, List


def rural_healthcare_advice(region: str, resources: List[str]) -> List[str]:
    advice = [
        f"For rural area {region}, use available community health workers and mobile clinics when possible.",
        "Prioritize clean water, safe nutrition, and basic first aid supplies.",
        "Record symptoms and share them with the nearest health provider or telehealth service.",
    ]
    if resources:
        advice.append(f"Use these local resources: {', '.join(resources)}.")
    return advice


def accessibility_support(challenge: str) -> List[str]:
    challenge = challenge.strip().lower()
    if "vision" in challenge:
        return [
            "Use large-print or audio health advisories.",
            "Choose simplified instructions with clear verbal cues.",
        ]
    if "hearing" in challenge:
        return [
            "Provide text-based alerts and captioned video guidance.",
            "Use vibration or visual signals for urgent reminders.",
        ]
    return [
        "Use accessible formats, simple language, and caregiver support.",
        "Prioritize safe routes to care and assistive devices where available.",
    ]


def public_health_advice(case_type: str) -> List[str]:
    case_type = case_type.strip().lower()
    if "epidemic" in case_type or "outbreak" in case_type:
        return [
            "Encourage hand hygiene, mask use, and physical distancing.",
            "Report symptoms early and isolate if infection is suspected.",
            "Stay informed through trusted health authorities.",
        ]
    return [
        "Track local health alerts and follow public guidance.",
        "Support vaccination and community prevention measures.",
    ]


def elderly_fall_detection(event: str) -> str:
    if "fall" in event.lower():
        return (
            "Detected a fall event. Check for injury, help the person sit or lie safely, "
            "and call for medical assistance if needed."
        )
    return "No fall event detected. Continue monitoring mobility and balance support."


def voice_assistant_prompt(text_input: str) -> str:
    return (
        f"[Voice Assistant] Received: '{text_input}'. \n"
        "Simulated response: I can help with symptoms, guidance, medication ideas, "
        "doctor recommendations, and health monitoring. Please describe your situation."
    )
