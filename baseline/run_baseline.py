import json
from environment import MediAssistOpenEnv
from grader import Grader
from models import Action


class BaselineAgent:
    def choose_action(self, observation):
        if observation.task_level == "easy":
            return self._easy_action(observation)
        if observation.task_level == "medium":
            return self._medium_action(observation)
        if observation.task_level == "hard":
            return self._hard_action(observation)
        return Action()

    def _easy_action(self, observation):
        if observation.metadata.get("concern"):
            return Action(recommended_response="Encourage deep breathing, rest, and speaking to a trusted person.")

        symptoms = observation.metadata.get("symptoms", [])
        if "runny nose" in symptoms or "sneezing" in symptoms:
            return Action(predicted_disease="common cold")
        if "high fever" in symptoms or "body ache" in symptoms:
            return Action(predicted_disease="flu")
        return Action(predicted_disease="infection")

    def _medium_action(self, observation):
        if observation.metadata.get("goal"):
            return Action(recommended_response="Start with brisk walking and gentle stretching, gradually building up daily movement.")

        age = observation.metadata.get("age", 0)
        bmi = observation.metadata.get("bmi", 0.0)
        risk = "low"
        if age >= 55 or bmi >= 30:
            risk = "moderate"
        if age >= 65 or bmi >= 35:
            risk = "high"
        recommendation = "Recommend a gentle exercise plan and regular monitoring."
        return Action(predicted_risk=risk, recommended_response=recommendation)

    def _hard_action(self, observation):
        return Action(
            emergency_action="Call for medical assistance, keep the person still and warm, and avoid moving the injured limb."
        )


def run_baseline():
    env = MediAssistOpenEnv(seed=123)
    agent = BaselineAgent()
    results = []

    for level in ["easy", "medium", "hard"]:
        observation = env.reset(level)
        action = agent.choose_action(observation)
        next_obs, reward, done, info = env.step(action)
        results.append({
            "task_level": level,
            "action": action,
            "reward": reward.value,
            "done": done,
            "info": info,
        })
        print(f"{level.title()} task reward: {reward.value}")

    summary = {
        "total_score": round(sum(item["reward"] for item in results), 2),
        "results": results,
    }
    print("Baseline summary:", json.dumps(summary, indent=2, default=str))
    return summary


if __name__ == "__main__":
    run_baseline()
