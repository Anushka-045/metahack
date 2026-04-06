def detect_conflicts(rules):
    conflicts = []

    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            r1, r2 = rules[i], rules[j]

            if r1["field"] == r2["field"]:
                if r1["operator"] != r2["operator"] or r1["value"] != r2["value"]:
                    conflicts.append({
                        "rule1": r1,
                        "rule2": r2,
                        "reason": "Conflicting conditions on same field"
                    })

    return conflicts