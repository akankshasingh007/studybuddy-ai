import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_FALLBACK_MODEL = os.getenv('GEMINI_FALLBACK_MODEL', 'gemini-2.0-flash-lite')

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

PROMPTS = {
    'summary': lambda text: f"""
Summarize the following study material in clean Markdown format.

Use this exact style:

## Topic Name

- Point 1
- Point 2
- Point 3

## Next Topic Name

- Point 1
- Point 2
- Point 3

Rules:
- Put every heading on its own line.
- Put every bullet point on a new line.
- Use Markdown headings with ##.
- Use hyphen bullets only.
- Do not write all points in one paragraph.
- Keep the explanation simple for students.

Study material:
{text}
""",
    'flashcards': lambda text: f"""Create 8 flashcards from the following study material.
Format strictly as:
CARD 1
Front: [question or term]
Back: [answer or definition]

Repeat for all 8 cards.\n\n{text}""",

    'quiz': lambda text: f"""Generate 5 multiple choice questions from the following material.
Format strictly as:
Q1. [question]
A) option
B) option
C) option
D) option
Answer: [letter]

Repeat for all 5 questions.\n\n{text}""",

    'explain': lambda text: f"""Explain the key concepts in the following material in simple terms a student can easily understand. Use analogies where helpful.\n\n{text}""",

    'chat': lambda text, question: f"""You are a study assistant. Answer the student's question using ONLY the following study material as context. If the answer isn't in the material, say so.\n\nMATERIAL:\n{text}\n\nQUESTION: {question}""",
}

def run_gemini(mode, extracted_text, question=None):
    if not client:
        return "Gemini error: GEMINI_API_KEY is missing. Add it to your .env file and restart the server."

    try:
        if mode == 'chat' and question:
            prompt = PROMPTS['chat'](extracted_text, question)
        else:
            prompt = PROMPTS[mode](extracted_text)

        last_error = None
        for model in [GEMINI_MODEL, GEMINI_FALLBACK_MODEL]:
            if not model:
                continue
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text or "Gemini returned an empty response. Please try again."
            except Exception as model_error:
                last_error = model_error

        return f"Gemini error: {str(last_error)}"
    except Exception as e:
        return f"Gemini error: {str(e)}"
