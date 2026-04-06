"""
Pre-submission validation script.
Runs all checks locally before pushing to HF Spaces.
"""
import sys, os, json, subprocess, importlib
sys.path.insert(0, os.path.dirname(__file__))

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "
results = []

def check(name, fn):
    try:
        ok, msg = fn()
        icon = PASS if ok else FAIL
        print(f"{icon} {name}: {msg}")
        results.append((name, ok, msg))
    except Exception as e:
        print(f"{FAIL} {name}: EXCEPTION — {e}")
        results.append((name, False, str(e)))

# 1. openenv.yaml present and parseable
def check_yaml():
    import yaml
    with open("openenv.yaml") as f:
        data = yaml.safe_load(f)
    required = ["name","version","tasks","reward","api"]
    missing = [k for k in required if k not in data]
    if missing:
        return False, f"Missing keys: {missing}"
    tasks = data["tasks"]
    if len(tasks) < 3:
        return False, f"Only {len(tasks)} tasks, need 3+"
    return True, f"{len(tasks)} tasks, all required keys present"

check("openenv.yaml valid", check_yaml)

# 2. Models importable
def check_models():
    from models import (EnvState, ComplianceRule, Violation,
                        StepResult, ResetRequest, TaskInfo)
    return True, "All typed models importable"
check("Pydantic models", check_models)

# 3. Environment reset/step/state
def check_env():
    from environment import ComplianceEnvironment
    env = ComplianceEnvironment()
    r = env.reset("task_easy")
    assert "observation" in r
    obs = r["observation"]
    assert len(obs["records"]) >= 1
    assert len(obs["rules"]) >= 1
    assert obs["done"] == False

    step_r = env.step({"action": "flag_violation", "record_id": "EMP001",
                        "rule_id": "RULE001", "reason": "No background check"})
    assert "reward" in step_r
    assert step_r["reward"] == 0.4

    state = env.state()
    assert "violations" in state
    assert len(state["violations"]) == 1
    return True, "reset/step/state all working, reward=0.4 verified"
check("Environment core (reset/step/state)", check_env)

# 4. All tasks
def check_tasks():
    from environment import ComplianceEnvironment, TASK_CONFIGS
    env = ComplianceEnvironment()
    for tid in ["task_easy","task_medium","task_hard"]:
        r = env.reset(tid)
        assert r["observation"]["task_id"] == tid
    return True, "All 3 tasks initialize correctly"
check("All 3 tasks", check_tasks)

# 5. Graders
def check_graders():
    from graders.task1_grader import grade as g1
    from graders.task2_grader import grade as g2
    from graders.task3_grader import grade as g3

    assert g1({"violations": [{"record_id":"EMP001","rule_id":"RULE001"}]}) == 1.0
    assert g1({"violations": []}) == 0.0

    perfect2 = {"violations": [
        {"record_id":"EMP001","rule_id":"RULE001","severity":"Critical"},
        {"record_id":"EMP001","rule_id":"RULE002","severity":"High"},
        {"record_id":"EMP010","rule_id":"RULE003","severity":"Critical"},
        {"record_id":"EMP005","rule_id":"RULE004","severity":"Medium"},
    ]}
    s2 = g2(perfect2)
    assert s2 == 1.0, f"Task2 perfect score should be 1.0, got {s2}"

    assert g2({"violations":[]}) == 0.0

    # Task 3: check scores in range
    s3 = g3({"violations": [{"record_id":"EMP001","rule_id":"RULE001","severity":"Critical",
              "explanation":"EMP001 violates the background check policy requirement.",
              "fix":"Conduct a background check for EMP001 immediately."}], "conflicts": []})
    assert 0.0 <= s3 <= 1.0, f"Score out of range: {s3}"
    return True, f"All graders pass, scores in [0,1]. Task2 perfect={s2}, Task3 sample={s3:.3f}"

check("Graders (all 3)", check_graders)

# 6. Inference.py exists and has required elements
def check_inference():
    with open("inference.py") as f:
        src = f.read()
    required = ["[START]","[STEP]","[END]","API_BASE_URL","MODEL_NAME","HF_TOKEN","OpenAI"]
    missing = [k for k in required if k not in src]
    if missing:
        return False, f"Missing from inference.py: {missing}"
    return True, "inference.py has all required elements"
check("inference.py structure", check_inference)

# 7. Dockerfile exists
def check_dockerfile():
    with open("Dockerfile") as f:
        src = f.read()
    checks = ["FROM python","EXPOSE 7860","CMD"]
    missing = [c for c in checks if c not in src]
    if missing:
        return False, f"Dockerfile missing: {missing}"
    return True, "Dockerfile structure valid"
check("Dockerfile", check_dockerfile)

# 8. Reward is shaped (not sparse)
def check_reward_shaped():
    from environment import ComplianceEnvironment
    env = ComplianceEnvironment()
    env.reset("task_hard")
    rewards = []
    for action in [
        {"action": "flag_violation", "record_id": "EMP001", "rule_id": "RULE001", "reason": "test"},
        {"action": "assign_severity", "violation_id": None, "severity": "Critical"},
    ]:
        if action["action"] == "assign_severity":
            state = env.state()
            vids = [v["id"] for v in state["violations"]]
            if vids:
                action["violation_id"] = vids[0]
        r = env.step(action)
        rewards.append(r["reward"])
    unique_rewards = len(set(rewards))
    if unique_rewards < 2:
        return False, f"Reward not shaped — all rewards identical: {rewards}"
    return True, f"Reward is shaped, observed values: {rewards}"
check("Reward function is shaped", check_reward_shaped)

# ─── Summary ───────────────────────────────────────────────────────────────
print("\n" + "="*55)
passed = sum(1 for _,ok,_ in results if ok)
total  = len(results)
print(f"VALIDATION RESULT: {passed}/{total} checks passed")
if passed == total:
    print("🎉 ALL CHECKS PASSED — ready to submit!")
else:
    print("Fix the failing checks before submitting.")
    for name, ok, msg in results:
        if not ok:
            print(f"  {FAIL} {name}: {msg}")
sys.exit(0 if passed == total else 1)
