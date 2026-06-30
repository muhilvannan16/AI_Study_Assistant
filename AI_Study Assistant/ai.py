import os
from groq import Groq

# -------------------------------
# AI Client
# -------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Change this line if you want to use another Groq model later.
MODEL = "llama-3.3-70b-versatile"


# -------------------------------
# Main AI Function
# -------------------------------

def ask_ai(prompt):

    try:

        completion = client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role":"system",
                    "content":
                    "You are an AI Study Assistant for high school students. "
                    "Explain topics in simple language. "
                    "Never use Markdown (**,#,*,`). "
                    "Use plain text with short paragraphs and numbered lists."
                },

                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )

        answer = completion.choices[0].message.content

        answer = answer.replace("**", "")
        answer = answer.replace("* ", "• ")
        answer = answer.replace("#", "")

        answer = "\n".join(
            line.rstrip()
            for line in answer.splitlines()
        )
        
        return answer

    except Exception as error:

        return f"Error:\n\n{error}"


# -------------------------------
# Summarize Notes
# -------------------------------

def summarize_note(note):

    prompt = f"""
Summarize the following study note.

Keep it short.

Use bullet points.

Study Note:

{note}
"""

    return ask_ai(prompt)


# -------------------------------
# Flashcard Generator
# -------------------------------

def generate_flashcards(note):

    prompt = f"""
Create flashcards from the following note.

Format:

Question:
...

Answer:
...

Create 5 flashcards.

Note:

{note}
"""

    return ask_ai(prompt)


# -------------------------------
# Quiz Generator
# -------------------------------

def generate_quiz(note):

    prompt = f"""
Create a multiple choice quiz.

Use this note.

Create 5 questions.

Each question should have

A
B
C
D

Then give the correct answer.

Note:

{note}
"""

    return ask_ai(prompt)


# -------------------------------
# Study Planner
# -------------------------------

def create_study_plan(subject, days):

    prompt = f"""
Create a study plan.

Subject:
{subject}

Days until exam:
{days}

Create a day-by-day study schedule.
"""

    return ask_ai(prompt)
