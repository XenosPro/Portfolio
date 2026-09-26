from llm import generate_question

question = generate_question(
    topic="neural networks",
    difficulty="easy",
    previous_questions=[]
)

print(question)
