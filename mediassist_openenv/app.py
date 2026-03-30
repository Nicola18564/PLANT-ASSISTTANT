"""Interactive MediAssist OpenEnv application."""
import os
import sys
from typing import Dict

if __name__ == "__main__" and __package__ is None:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

from mediassist_openenv.core import (
    detect_disease,
    guide_patient,
    suggest_medication,
    recommend_doctor,
    predict_risk,
)
from mediassist_openenv.scenarios import (
    rural_healthcare_advice,
    accessibility_support,
    public_health_advice,
    elderly_fall_detection,
    voice_assistant_prompt,
)
from mediassist_openenv.support import mental_health_support, fitness_recommendations, monitor_health
from mediassist_openenv.utils import format_list, parse_symptoms


def _show_menu() -> None:
    print("\n=== MediAssist OpenEnv ===")
    print("1. Symptom-based disease detection")
    print("2. Medication and guidance")
    print("3. Doctor recommendation")
    print("4. Risk prediction")
    print("5. Mental health support")
    print("6. Fitness & preventive care")
    print("7. Health monitoring")
    print("8. Rural / accessibility / public health scenarios")
    print("9. Simulated voice assistant")
    print("0. Exit")


def _prompt(text: str) -> str:
    return input(text).strip()


def run() -> None:
    while True:
        _show_menu()
        choice = _prompt("Choose an option: ")

        if choice == "0":
            print("Goodbye from MediAssist OpenEnv.")
            break

        if choice == "1":
            symptoms = _prompt("Enter symptoms separated by commas: ")
            disease = detect_disease(parse_symptoms(symptoms))
            print(f"Detected disease: {disease or 'No strong match found.'}")
        elif choice == "2":
            disease = _prompt("Enter a suspected disease name: ")
            print("Guidance:\n" + format_list(guide_patient(disease)))
            print("Medication suggestions:\n" + format_list(suggest_medication(disease)))
        elif choice == "3":
            disease = _prompt("Enter suspected disease or symptoms: ")
            location = _prompt("Enter location or region: ")
            print(recommend_doctor(disease, location))
        elif choice == "4":
            age = int(_prompt("Age: "))
            bmi = float(_prompt("BMI: "))
            conditions = _prompt("Known risk factors separated by commas: ")
            print("Risk level: " + predict_risk(age, bmi, parse_symptoms(conditions)))
        elif choice == "5":
            topic = _prompt("Enter a mental health concern (stress, anxiety, sadness): ")
            result = mental_health_support(topic)
            print(result["response"])
            print(result["resource"])
        elif choice == "6":
            goal = _prompt("Enter your fitness goal (weight loss, cardio, mobility): ")
            print("Recommendations:\n" + format_list(fitness_recommendations(goal)))
        elif choice == "7":
            vitals: Dict[str, float] = {}
            heart = _prompt("Heart rate (bpm, leave blank if unknown): ")
            if heart:
                vitals["heart_rate"] = float(heart)
            bp = _prompt("Blood pressure (systolic/diastolic, e.g. 120/80): ")
            if "/" in bp:
                systolic, diastolic = bp.split("/")
                vitals["blood_pressure"] = (float(systolic), float(diastolic))
            temp = _prompt("Temperature in °C (leave blank if unknown): ")
            if temp:
                vitals["temperature"] = float(temp)
            oxygen = _prompt("Oxygen saturation % (leave blank if unknown): ")
            if oxygen:
                vitals["oxygen_saturation"] = float(oxygen)
            print("Monitoring notes:\n" + format_list(monitor_health(vitals)))
        elif choice == "8":
            scenario = _prompt("Choose scenario type (rural, accessibility, public, fall): ")
            if scenario == "rural":
                region = _prompt("Region name: ")
                resources = _prompt("Local resources separated by commas: ")
                print(format_list(rural_healthcare_advice(region, parse_symptoms(resources))))
            elif scenario == "accessibility":
                challenge = _prompt("Describe the accessibility challenge: ")
                print(format_list(accessibility_support(challenge)))
            elif scenario == "public":
                case_type = _prompt("Public health case type (epidemic, outbreak, general): ")
                print(format_list(public_health_advice(case_type)))
            elif scenario == "fall":
                event = _prompt("Describe the fall event: ")
                print(elderly_fall_detection(event))
            else:
                print("Unknown scenario type.")
        elif choice == "9":
            text = _prompt("Speak to the assistant (type your request): ")
            print(voice_assistant_prompt(text))
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    run()
