def assign_severity(rule):
    if "age" in rule["field"]:
        return "High"
    if "salary" in rule["field"]:
        return "Medium"
    return "Low"