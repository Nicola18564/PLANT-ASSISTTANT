import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from baseline.run_baseline import run_baseline


def handler(request):
    summary = run_baseline()

    # Convert Action objects to plain JSON-serializable dictionaries
    for item in summary.get("results", []):
        action = item.get("action")
        if action is not None:
            item["action"] = {
                "predicted_disease": getattr(action, "predicted_disease", None),
                "predicted_risk": getattr(action, "predicted_risk", None),
                "recommended_response": getattr(action, "recommended_response", None),
                "emergency_action": getattr(action, "emergency_action", None),
            }

    return {"success": True, "summary": summary}
