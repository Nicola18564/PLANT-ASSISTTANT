import random
from typing import Dict, Optional

from models import Action, Observation, Reward, TaskLevel
from tasks import TaskSpec, get_task_by_level, get_all_tasks


class MediAssistOpenEnv:
    def __init__(self, seed: Optional[int] = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.current_task: Optional[TaskSpec] = None
        self.current_observation: Optional[Observation] = None
        self.done = False
        self.steps = 0

    def reset(self, task_level: Optional[TaskLevel] = None) -> Observation:
        if task_level is None:
            task_level = self.rng.choice(["easy", "medium", "hard"])
        self.current_task = get_task_by_level(task_level)
        self.current_observation = Observation(
            task_id=self.current_task.task_id,
            task_level=self.current_task.level,
            prompt=self.current_task.prompt,
            metadata=self.current_task.observation,
        )
        self.done = False
        self.steps = 0
        return self.current_observation

    def step(self, action: Action):
        if self.current_task is None or self.current_observation is None:
            raise RuntimeError("Environment must be reset before calling step().")
        if self.done:
            raise RuntimeError("Episode already completed. Call reset() to start a new task.")

        self.steps += 1
        reward_value, info = self.evaluate_action(self.current_task, action)
        reward = Reward(value=reward_value)
        self.done = True
        observation = Observation(
            task_id=self.current_task.task_id,
            task_level=self.current_task.level,
            prompt=self.current_task.prompt,
            metadata={
                **self.current_task.observation,
                "agent_action": action,
                "evaluation": info,
            },
        )
        self.current_observation = observation
        return observation, reward, self.done, info

    def state(self) -> Dict[str, Optional[object]]:
        return {
            "task_id": self.current_task.task_id if self.current_task else None,
            "task_level": self.current_task.level if self.current_task else None,
            "done": self.done,
            "steps": self.steps,
            "seed": self.seed,
        }

    @staticmethod
    def evaluate_action(task: TaskSpec, action: Action):
        info = {"task_id": task.task_id, "level": task.level}
        if task.level == "easy":
            return MediAssistOpenEnv._score_easy(task, action, info)
        if task.level == "medium":
            return MediAssistOpenEnv._score_medium(task, action, info)
        if task.level == "hard":
            return MediAssistOpenEnv._score_hard(task, action, info)
        raise ValueError(f"Unsupported task level: {task.level}")

    @staticmethod
    def _score_easy(task: TaskSpec, action: Action, info: Dict[str, object]):
        if "disease" in task.expected:
            predicted = (action.predicted_disease or "").strip().lower()
            expected = task.expected["disease"].lower()
            if not predicted:
                info["reason"] = "No disease prediction provided."
                return -0.5, info
            if predicted == expected:
                info["reason"] = "Correct disease prediction."
                return 1.0, info
            if expected in predicted or predicted in expected:
                info["reason"] = "Partial disease match."
                return 0.4, info
            if any(word in predicted for word in ["infection", "cold", "flu"]):
                info["reason"] = "Incorrect but related disease class."
                return 0.2, info
            info["reason"] = "Incorrect or dangerous disease prediction."
            return -0.5, info

        if "support" in task.expected:
            recommendation = (action.recommended_response or "").strip().lower()
            if not recommendation:
                info["reason"] = "No mental health support suggestion provided."
                return -0.3, info
            if any(word in recommendation for word in ["breathe", "support", "rest", "talk", "share"]):
                info["reason"] = "Safe mental health support suggested."
                return 0.8, info
            info["reason"] = "Support suggestion is not aligned with safe mental health guidance."
            return 0.0, info

        info["reason"] = "Unsupported easy task expected output."
        return 0.0, info

    @staticmethod
    def _score_medium(task: TaskSpec, action: Action, info: Dict[str, object]):
        score = 0.0
        recommendation = (action.recommended_response or "").strip().lower()
        safe_keywords = ["exercise", "reduce", "monitor", "check", "hydrate", "stretch", "walk"]

        if "risk" in task.expected:
            predicted_risk = (action.predicted_risk or "").strip().lower()
            expected_risk = task.expected["risk"].lower()
            if predicted_risk == expected_risk:
                score += 0.6
                info["risk_match"] = True
            elif predicted_risk in ["low", "moderate", "high"]:
                score += 0.2
                info["risk_match"] = False
            else:
                score -= 0.2
                info["risk_match"] = False

        if recommendation:
            if any(word in recommendation for word in safe_keywords):
                score += 0.4
                info["recommendation_quality"] = "safe"
            else:
                score -= 0.3
                info["recommendation_quality"] = "unsafe"
        else:
            info["recommendation_quality"] = "missing"
            score -= 0.2

        if score > 1.0:
            score = 1.0
        if score < -1.0:
            score = -1.0
        info["reason"] = "Medium task evaluation completed."
        return round(score, 2), info

    @staticmethod
    def _score_hard(task: TaskSpec, action: Action, info: Dict[str, object]):
        response = (action.emergency_action or "").strip().lower()
        if not response:
            info["reason"] = "No emergency action provided."
            return -1.0, info
        safe_matches = sum(1 for keyword in task.safe_responses if keyword in response)
        dangerous_matches = sum(1 for keyword in task.dangerous_responses if keyword in response)
        if dangerous_matches > 0:
            info["reason"] = "Dangerous emergency response detected."
            return -1.0, info
        if safe_matches >= 2:
            info["reason"] = "Strong safe emergency response."
            return 1.0, info
        if safe_matches == 1:
            info["reason"] = "Partially safe emergency response."
            return 0.3, info
        info["reason"] = "Response missing safe emergency procedures."
        return 0.0, info
