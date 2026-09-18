import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_questions(topic="machine learning", difficulty="easy", number=5):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    prompt = f"""
Generate {number} multiple-choice quiz questions about {topic}.

Difficulty: {difficulty}

The questions are for a student learning machine learning and deep learning.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside the JSON.

Use exactly this format:

[
    {{
        "question": "Question text",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ],
        "answer": "The exact correct option",
        "topic": "{topic}",
        "difficulty": "{difficulty}",
        "explanation": "Short explanation of why the answer is correct."
    }}
]

Rules:
- Exactly 4 options per question.
- Only one correct answer.
- "answer" must exactly match one of the options.
- Make the questions factually accurate.
- Do not repeat questions.
"""

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            questions = json.loads(text)

            return questions

        except Exception as e:

            if attempt == 2:
                raise e

            time.sleep(3)