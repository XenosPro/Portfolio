def calculate_xp(correct, difficulty):
    if not correct:
        return 0

    if difficulty == "easy":
        return 10
    elif difficulty == "medium":
        return 20
    elif difficulty == "hard":
        return 30

    return 0
