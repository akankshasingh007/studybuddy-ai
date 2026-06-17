def get_prompt(mode, content):

    prompts = {

        "summary": f"""
Create concise study notes.

{content}
""",

        "revision": f"""
Create exam revision notes.

Include:

- key concepts
- formulas
- important definitions
- likely questions

{content}
""",

        "studyplan": f"""
Create a 7-day study plan
based on this material.

{content}
""",

        "flashcards": f"""
Create flashcards from:

{content}
""",

        "quiz": f"""
Create MCQ quiz from:

{content}
"""
    }

    return prompts.get(
        mode,
        content
    )