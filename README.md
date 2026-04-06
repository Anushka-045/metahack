# 🛡️ Compliance Monitor — OpenEnv Environment

**Team:** RunTimers | Gargi Monga · Anushka Pandey  
**Hackathon:** Meta × Scaler OpenEnv Round 1  
**Deadline:** 8 April 2026, 11:59 PM IST

---

## Overview

Companies store compliance rules in PDF documents that are rarely read until violations occur. This environment simulates a **real-world AI compliance monitoring agent** that:

- Scans company records (employees, contracts, transactions)
- Detects policy violations against structured compliance rules
- Assigns severity (Low / Medium / High / Critical)
- Generates plain-English violation explanations
- Suggests specific remediation actions
- Flags contradictions between policy rules

**Domain:** Enterprise Legal/Compliance — directly applicable to any data-driven organization managing regulatory risk.

---

## Environment Design

### Action Space (6 actions)

| Action | Parameters | Description |
|--------|-----------|-------------|
| `check_record` | `record_id` | Inspect a record and identify applicable rules |
| `flag_violation` | `record_id`, `rule_id`, `reason` | Flag a record as violating a rule (+0.4 reward if correct) |
| `assign_severity` | `violation_id`, `severity` | Set Low/Medium/High/Critical (+0.2 if correct) |
| `generate_explanation` | `violation_id`, `explanation` | Plain-English violation reason (+0.2 based on quality) |
| `suggest_fix` | `violation_id`, `fix` | Actionable remediation step (+0.2 based on quality) |
| `resolve_conflict` | `rule_id_a`, `rule_id_b`, `resolution` | Resolve contradicting rules (+0.3 if known conflict) |

### Observation Space

```json
{
  "records": [...],            // company records in scope
  "rules": [...],              // active compliance rules
  "violations": [...],         // flagged violations (with severity, explanation, fix)
  "conflicts": [...],          // identified rule conflicts
  "checked_record_ids": [...], // records already inspected
  "episode_step": 0,
  "max_steps": 60,
  "done": false,
  "total_reward": 0.0,
  "task_id": "task_medium"
}
```

### Reward Function

```
R = detection(+0.4) + severity(+0.2) + explanation(+0.2) + fix(+0.2)
  - false_positive_penalty(-0.1 per FP)
  + conflict_resolution(+0.3 per known conflict resolved)
```

- **Shaped reward** — agent gets signal at every sub-action, not just at episode end
- **Partial credit** — adjacent severity level earns 0.1 instead of 0.2
- **Quality scoring** — explanations and fixes are scored on actionability and relevance

---

## Tasks

### Task 1 — Easy: Single Record vs Single Rule
- 1 employee record, 1 rule
- Binary score: 0.0 or 1.0
- Max 10 steps
- Tests: basic violation detection

### Task 2 — Medium: Multi-Record Multi-Rule
- 10 records, 5 rules
- Partial credit scoring
- Max 60 steps
- Tests: scanning, prioritization, severity assignment

### Task 3 — Hard: Full DB + Conflicting Policies
- 30+ records (employees, contracts, transactions), 12 rules (including 2 contradicting)
- Weighted scoring: detection(35%) + severity(25%) + explanation(20%) + fix(10%) + conflict(10%)
- Max 200 steps
- Genuinely challenges frontier models: requires multi-hop reasoning, policy interpretation, conflict resolution

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/reset` | Start new episode. Body: `{"task_id": "task_easy", "seed": 42}` |
| `POST` | `/step` | Take action. Body: `{"action": {...}}` |
| `GET` | `/state` | Get current environment state |
| `GET` | `/tasks` | List available tasks |
| `GET` | `/health` | Health check |

---

## Setup & Running

### Local

```bash
pip install -r requirements.txt
python server.py
# Server runs on http://localhost:7860
```

### Docker

```bash
docker build -t compliance-monitor .
docker run -p 7860:7860 compliance-monitor
```

### Inference (baseline agent)

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-hf-or-openai-key"
export ENV_URL="http://localhost:7860"

python inference.py
```

The inference script:
- Runs all 3 tasks sequentially
- Falls back to deterministic heuristic if LLM is unavailable
- Emits structured `[START]` / `[STEP]` / `[END]` JSON logs to stdout
- Completes in < 5 minutes on a 2vCPU / 8GB machine

---

## Pre-Submission Checklist

- [x] HF Space deploys and responds to `/reset` with HTTP 200
- [x] `openenv.yaml` present with full spec
- [x] Typed Pydantic models for all observations and actions
- [x] `step()` / `reset()` / `state()` endpoints implemented
- [x] 3 tasks with graders producing scores in 0.0–1.0
- [x] Graders are deterministic and reproducible
- [x] Reward function provides shaped (non-sparse) signal
- [x] `inference.py` in root directory, uses OpenAI Client
- [x] `[START]` / `[STEP]` / `[END]` log format implemented
- [x] `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN` env vars used
- [x] Dockerfile builds and runs
- [x] Runtime < 20 min on 2vCPU / 8GB

---

## Contact

help_openenvhackathon@scaler.com
