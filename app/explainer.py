def generate_explanation(record, rule):
    return f"{record['name']} (age {record['age']}) does not meet rule: {rule['description']}"