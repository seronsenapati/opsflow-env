def grade(task, action):
    score = 0.0

    if task["type"] == "address_fix":
        response = action["decision"].get("fixed_address", "").lower()
        for word in task["keywords"]:
            if word in response:
                score += 1 / len(task["keywords"])

    elif task["type"] == "prioritization":
        response = action["decision"].get("order_sequence", [])
        if response == task["expected"]:
            score = 1.0
        elif set(response) == set(task["expected"]):
            score = 0.5

    elif task["type"] == "driver_assignment":
        data = task["observation"]["data"]

        assigned = action["decision"].get("assigned_orders", 0)
        urgent_handled = action["decision"].get("urgent_handled", False)

        efficiency = assigned / data["orders"]

        # reward structure
        score += efficiency * 0.6  # delivery efficiency
        if urgent_handled:
            score += 0.3  # priority handling

        # penalty for wasting drivers
        if assigned > data["drivers"]:
            score -= 0.2

        score = max(0, score)

    return {"score": round(score, 2)}
