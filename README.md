# MediAssist OpenEnv

MediAssist OpenEnv is a Gym-style AI training environment for healthcare decision support. It is designed for the Meta OpenEnv hackathon and focuses on agent training rather than a user-facing application.

## Problem Statement

AI agents should learn to support real-world healthcare decision tasks without internet access or external APIs.
This environment simulates:
- symptom-based disease detection
- clinical risk prediction and safe prevention advice
- emergency response planning for elderly or rural scenarios

## Environment Design

The environment implements the required OpenEnv API:
- `reset()` → initial `Observation`
- `step(action)` → `(observation, reward, done, info)`
- `state()` → current state snapshot

## Observation / Action / Reward Models

Typed models are defined in `models.py`:
- `Observation`: task metadata and input context
- `Action`: structured agent decision outputs
- `Reward`: graded numeric score

## Tasks

This project includes three tasks:
- `easy`: disease detection from symptoms
- `medium`: risk assessment and preventive recommendation
- `hard`: emergency response for a vulnerable scenario

Each task includes a clear objective, expected output, and programmatic grading.

## Reward Logic

Reward shaping is implemented to support graded progress:
- correct answers receive high reward
- partially correct answers receive intermediate reward
- dangerous or missing actions are penalized

## Files

- `environment.py`: core environment implementation
- `models.py`: typed observation/action/reward definitions
- `tasks.py`: task catalog and expected outputs
- `grader.py`: programmatic grader for agent actions
- `baseline/run_baseline.py`: reproducible baseline agent
- `openenv.yaml`: environment manifest for Meta OpenEnv
- `Dockerfile`: container configuration
- `requirements.txt`: dependency list

## Running Locally

```powershell
python -m baseline.run_baseline
```

## Build and Run in Docker

```bash
docker build -t mediassist-openenv .
docker run --rm mediassist-openenv
```

## Notes

This repository is structured as a true AI environment for agent training, not a chatbot or UI app. It is intended to satisfy Meta OpenEnv hackathon requirements for task-based grading, reward shaping, and container deployment.
