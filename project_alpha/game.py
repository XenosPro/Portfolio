from llm import generate_question


# Backup questions used if Gemini is temporarily unavailable
FALLBACK_QUESTIONS = [
    {
        "question": "Which model is commonly used for binary classification?",
        "options": [
            "Linear Regression",
            "Logistic Regression",
            "K-Means",
            "PCA"
        ],
        "answer": "Logistic Regression",
        "topic": "machine learning",
        "difficulty": "easy",
        "explanation": "Logistic Regression is commonly used for binary classification problems."
    },
    {
        "question": "What does overfitting mean?",
        "options": [
            "The model performs badly on training data",
            "The model memorizes training data and performs poorly on new data",
            "The model has too few parameters",
            "The dataset contains no labels"
        ],
        "answer": "The model memorizes training data and performs poorly on new data",
        "topic": "machine learning",
        "difficulty": "easy",
        "explanation": "Overfitting happens when a model learns the training data too closely and fails to generalize to unseen data."
    }
]


def get_question(
    topic="machine learning",
    difficulty="easy",
    previous_questions=None
):
    try:
        return generate_question(
            topic=topic,
            difficulty=difficulty,
            previous_questions=previous_questions
        )

    except Exception as e:
        print(f"Gemini unavailable: {e}")
        print("Using fallback question.")

        previous_questions = previous_questions or []

        for question in FALLBACK_QUESTIONS:
            if question["question"] not in previous_questions:
                return question

        # If all fallback questions were used, restart the fallback bank
        return FALLBACK_QUESTIONS[0]


def check_answer(question, selected_answer):
    return selected_answer == question["answer"]