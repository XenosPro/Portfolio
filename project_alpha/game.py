from llm import generate_questions


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


def get_questions(
    topic="machine learning",
    difficulty="easy",
    number=5
):
    try:
        questions = generate_questions(
            topic=topic,
            difficulty=difficulty,
            number=number
        )

        return questions

    except Exception:
        print("Gemini unavailable. Using fallback questions.")

        return FALLBACK_QUESTIONS


def check_answer(question, selected_answer):
    return selected_answer == question["answer"]

