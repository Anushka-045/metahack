from fastapi import FastAPI
from app.pdf_ingest import extract_text
from app.rule_extractor import extract_rules
from app.violation_detector import check_violation
from app.data_loader import load_data
from app.severity import assign_severity
from app.explainer import generate_explanation
from app.fix_suggester import suggest_fix
from app.conflict_detector import detect_conflicts
from app.trend_tracker import log_score, get_trend

app = FastAPI()
from app.database import init_db

@app.on_event("startup")
def startup_event():
    init_db()
@app.get("/")
def home():
    return {"message": "Compliance AI Running"}

@app.get("/analyze")
def analyze():
    rules = [
        {
            "id": "R1",
            "description": "Employee must be at least 18 years old",
            "field": "age",
            "operator": ">=",
            "value": 18
        }
    ]

    records = load_data()

    violations = []

    for record in records:
        for rule in rules:
            if not check_violation(record, rule):
                
                severity = assign_severity(rule)
                explanation = generate_explanation(record, rule)
                fix = suggest_fix(rule)

                violations.append({
                    "record": record,
                    "rule": rule,
                    "severity": severity,
                    "explanation": explanation,
                    "fix": fix
                })

    conflicts = detect_conflicts(rules)

    # compliance score
    total = len(records)
    failed = len(violations)
    score = ((total - failed) / total) * 100 if total > 0 else 100

    log_score(score)
    trend = get_trend()

    return {
        "rules": rules,
        "violations": violations,
        "conflicts": conflicts,
        "compliance_score": round(score, 2),
        "trend": trend
    }