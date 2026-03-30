from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

TaskLevel = Literal["easy", "medium", "hard"]


@dataclass(frozen=True)
class Observation:
    task_id: str
    task_level: TaskLevel
    prompt: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class Action:
    predicted_disease: Optional[str] = None
    predicted_risk: Optional[str] = None
    recommended_response: Optional[str] = None
    emergency_action: Optional[str] = None


@dataclass(frozen=True)
class Reward:
    value: float


@dataclass(frozen=True)
class StepResult:
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any]
