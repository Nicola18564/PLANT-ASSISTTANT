"""Core disease detection and clinical support utilities."""
from typing import Dict, List, Optional

DISEASE_MODELS: Dict[str, Dict[str, object]] = {
    "common cold": {
        "symptoms": {"cough", "sore throat", "runny nose", "sneezing", "mild fever"},
        "medications": ["rest", "hydration", "paracetamol", "cough syrup"],
        "specialty": "general physician",
        "guidance": [
            "Stay hydrated and rest.",
            "Use warm salt-water gargle for sore throat.",
            "Monitor temperature and avoid close contact.",
        ],
    },
    "flu": {
        "symptoms": {"high fever", "body ache", "headache", "fatigue", "cough"},
        "medications": ["antiviral care", "acetaminophen", "rest", "flu liquids"],
        "specialty": "general physician",
        "guidance": [
            "Take fever-reducing medicine as needed.",
            "Rest and keep warm.",
            "Seek medical care if breathing becomes difficult.",
        ],
    },
    "diabetes": {
        "symptoms": {"excessive thirst", "frequent urination", "fatigue", "blurred vision"},
        "medications": ["blood sugar monitoring", "metformin", "dietary changes"],
        "specialty": "endocrinologist",
        "guidance": [
            "Track blood sugar regularly.",
            "Follow a low-sugar diet.",
            "Exercise consistently and consult an endocrinologist.",
        ],
    },
    "hypertension": {
        "symptoms": {"headache", "dizziness", "chest discomfort", "fatigue"},
        "medications": ["blood pressure monitoring", "lifestyle modification", "anti-hypertensives"],
        "specialty": "cardiologist",
        "guidance": [
            "Reduce salt intake.",
            "Exercise gently and monitor blood pressure.",
            "Follow up with a cardiologist if values remain high.",
        ],
    },
    "dehydration": {
        "symptoms": {"dry mouth", "thirst", "dark urine", "dizziness", "weakness"},
        "medications": ["oral rehydration", "electrolyte drinks", "rest"],
        "specialty": "general physician",
        "guidance": [
            "Drink oral rehydration solutions.",
            "Avoid caffeine and alcohol.",
            "Rest until symptoms improve.",
        ],
    },
}

RISK_FACTORS = {
    "smoking": 1.2,
    "poor_diet": 1.3,
    "sedentary": 1.2,
    "family_history": 1.4,
    "high_bmi": 1.3,
}


def detect_disease(symptoms: List[str]) -> Optional[str]:
    normalized = {symptom.strip().lower() for symptom in symptoms if symptom}
    best_match = None
    best_score = 0

    for disease, model in DISEASE_MODELS.items():
        signature = model["symptoms"]
        score = len(normalized & signature)
        if score > best_score:
            best_score = score
            best_match = disease

    if best_score == 0:
        return None
    return best_match


def guide_patient(disease: str) -> List[str]:
    disease = disease.lower()
    model = DISEASE_MODELS.get(disease)
    return model["guidance"] if model else ["Please consult a healthcare professional for a personalized plan."]


def suggest_medication(disease: str) -> List[str]:
    disease = disease.lower()
    model = DISEASE_MODELS.get(disease)
    return model["medications"] if model else ["No standard suggestion available. Seek professional care."]


def recommend_doctor(disease: str, location: str = "local") -> str:
    disease = disease.lower()
    model = DISEASE_MODELS.get(disease)
    specialty = model["specialty"] if model else "general physician"
    return f"Recommended specialist: {specialty}. Search for nearby clinics or telehealth services in {location}."


def predict_risk(age: int, bmi: float, conditions: List[str]) -> str:
    score = 0.0
    if age >= 60:
        score += 1.5
    elif age >= 45:
        score += 1.1

    if bmi >= 30:
        score += RISK_FACTORS["high_bmi"]
    elif bmi >= 25:
        score += 1.1

    normalized = {item.strip().lower() for item in conditions}
    for factor, multiplier in RISK_FACTORS.items():
        if factor in normalized:
            score += multiplier

    if score < 2.5:
        return "Low risk"
    if score < 4.5:
        return "Moderate risk"
    return "High risk"
