"""Health support and monitoring helpers."""
from typing import Dict, List

MENTAL_HEALTH_TEMPLATES: Dict[str, Dict[str, str]] = {
    "stress": {
        "response": "It sounds like you're under stress. Take a short break, breathe deeply, and focus on one task at a time.",
        "resource": "Try simple breathing exercises or speak with a counselor if stress persists.",
    },
    "anxiety": {
        "response": "If anxiety is making it hard to stay calm, notice your surroundings and ground yourself with five slow breaths.",
        "resource": "Contact a trusted friend, family member, or mental health line for support.",
    },
    "sadness": {
        "response": "Sadness is valid. Reach out to someone you trust, and consider small steps like a short walk or journaling.",
        "resource": "If feelings last more than a few days, seek professional mental health support.",
    },
}

FITNESS_PLANS: Dict[str, List[str]] = {
    "weight loss": [
        "Begin with 20 minutes of brisk walking daily.",
        "Add two strength movements such as bodyweight squats and push-ups.",
        "Keep a balanced plate with vegetables, lean protein, and whole grains.",
    ],
    "cardio": [
        "Start with low-impact activities like walking or cycling.",
        "Increase duration gradually by 5 minutes each week.",
        "Stay hydrated and listen to your body.",
    ],
    "mobility": [
        "Perform gentle stretches for shoulders, hips, and knees.",
        "Practice seated balance and ankle mobility exercises.",
        "Take regular movement breaks throughout the day.",
    ],
}


def mental_health_support(topic: str) -> Dict[str, str]:
    key = topic.strip().lower()
    return MENTAL_HEALTH_TEMPLATES.get(
        key,
        {
            "response": "I am here to listen. Try to describe how you feel and take one small step toward self-care.",
            "resource": "Reach out to a trusted person or professional if you need more support.",
        },
    )


def fitness_recommendations(goal: str) -> List[str]:
    key = goal.strip().lower()
    return FITNESS_PLANS.get(
        key,
        [
            "Aim for at least 20 minutes of movement daily.",
            "Choose activities you enjoy and can keep doing.",
            "Balance exercise with nutritious meals and rest.",
        ],
    )


def monitor_health(vitals: Dict[str, float]) -> List[str]:
    alerts = []
    heart_rate = vitals.get("heart_rate")
    blood_pressure = vitals.get("blood_pressure")
    temperature = vitals.get("temperature")
    oxygen = vitals.get("oxygen_saturation")

    if heart_rate is not None:
        if heart_rate < 50:
            alerts.append("Heart rate is low. Consider rest and evaluate symptoms.")
        elif heart_rate > 100:
            alerts.append("Heart rate is elevated. Hydrate and rest; seek care if it stays high.")

    if blood_pressure is not None:
        systolic, diastolic = blood_pressure
        if systolic > 140 or diastolic > 90:
            alerts.append("Blood pressure appears elevated. Use relaxation and consult a provider.")
        elif systolic < 90 or diastolic < 60:
            alerts.append("Blood pressure is low. Sit safely and drink fluids.")

    if temperature is not None:
        if temperature >= 38.0:
            alerts.append("Fever detected. Monitor temperature and reduce exposure.")
        elif temperature < 35.5:
            alerts.append("Body temperature is low. Keep warm.")

    if oxygen is not None and oxygen < 95:
        alerts.append("Oxygen saturation is below normal. Seek urgent care if breathing difficulty occurs.")

    return alerts or ["All monitored values are within a typical range. Continue healthy habits."]
