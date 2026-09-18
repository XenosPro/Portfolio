from llm import generate_questions

questions = generate_questions(
    topic="neural networks",
    difficulty="easy",
    number=3
)

print(questions)