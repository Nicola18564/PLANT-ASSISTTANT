from typing import Dict, List

from environment import MediAssistOpenEnv
from models import Action, Observation, Reward


class Grader:
    def __init__(self, env: MediAssistOpenEnv):
        self.env = env

    def grade_action(self, task_level: str, action: Action) -> Dict[str, object]:
        observation = self.env.reset(task_level)
        _, reward, done, info = self.env.step(action)
        return {
            "task_id": observation.task_id,
            "task_level": observation.task_level,
            "reward": reward.value,
            "done": done,
            "info": info,
        }

    def grade_sequence(self, actions: List[Action]) -> Dict[str, object]:
        results = []
        for level, action in zip(["easy", "medium", "hard"], actions):
            results.append(self.grade_action(level, action))
        total = sum(item["reward"] for item in results)
        return {"results": results, "total_score": round(total, 2)}


def grade_task_set(actions: List[Action]) -> Dict[str, object]:
    env = MediAssistOpenEnv()
    grader = Grader(env)
    return grader.grade_sequence(actions)
