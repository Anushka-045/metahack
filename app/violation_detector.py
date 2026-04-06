def check_violation(record, rule):
    field = rule["field"]
    operator = rule["operator"]
    value = rule["value"]

    record_value = record.get(field)

    if operator == ">=":
        return record_value >= value
    elif operator == "<=":
        return record_value <= value
    elif operator == ">":
        return record_value > value
    elif operator == "<":
        return record_value < value
    elif operator == "==":
        return record_value == value
    else:
        return False