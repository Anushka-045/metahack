from typing import List, Dict

def extract_rules(text: str) -> List[Dict]:
    rules = []

    text = text.lower()

    if "18" in text or "age" in text:
        rules.append({
            "id": "R1",
            "description": "Employee must be at least 18 years old",
            "field": "age",
            "operator": ">=",
            "value": 18
        })

    if "salary" in text and "5000" in text:
        rules.append({
            "id": "R2",
            "description": "Salary must be at least 5000",
            "field": "salary",
            "operator": ">=",
            "value": 5000
        })

    return rules