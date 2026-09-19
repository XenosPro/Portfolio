import os
import time

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


class QuizQuestion(BaseModel):
    question: str = Field(description="The multiple-choice question")
    options: list[str] = Field(
        description="Exactly 4 possible answers"
    )
    answer: str = Field(
        description="The exact correct answer from the options"
    )
    topic: str
    difficulty: str
    explanation: str = Field(
        description="Short explanation of the correct answer"
    )


def generate_question(
    topic="machine learning",
    difficulty="easy",
    previous_questions=None
):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    previous_questions = previous_questions or []

    previous_text = "\n".join(
        f"- {q}" for q in previous_questions
    )

    prompt = f"""
Generate ONE multiple-choice quiz question.

Topic: {topic}
Difficulty: {difficulty}

The question is for a student learning
machine learning and deep learning.

Requirements:

- Exactly 4 options.
- Only one option is correct.
- The answer must exactly match one of the options.
- The question must be factually accurate.
- Provide a short explanation.
- Do NOT repeat any previous question.

Previous questions:
{previous_text}

Generate a NEW question.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": QuizQuestion,
                },
            )

            question = response.parsed

            if question is None:
                raise ValueError(
                    "Gemini returned no structured question."
                )

            if len(question.options) != 4:
                raise ValueError(
                    "Question does not contain exactly 4 options."
                )

            if question.answer not in question.options:
                raise ValueError(
                    "Correct answer is not one of the options."
                )

            return question.model_dump()

        except Exception as e:

            print(
                f"Gemini attempt {attempt + 1}/3 failed: "
                f"{type(e).__name__}: {e}"
            )

            if attempt < 2:
                time.sleep(2)

    raise RuntimeError(
        "Unable to generate a new question after 3 attempts."
    )