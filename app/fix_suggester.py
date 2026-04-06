def suggest_fix(rule):
    if rule["field"] == "age":
        return "Ensure employee meets minimum legal working age requirement"
    return f"Adjust {rule['field']} to meet rule condition"