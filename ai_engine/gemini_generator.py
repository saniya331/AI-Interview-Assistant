import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_questions(skills, resume_text, job_role):
    prompt = f"""
You are a technical interviewer.

Create exactly 10 concise interview questions using the candidate's resume and target job role.

Target Job Role:
{job_role}

Candidate Skills:
{', '.join(skills)}

Resume:
{resume_text}

Rules:
- Each question must be one sentence only.
- Ask only one concept per question.
- Use simple and clear interview language.
- Prioritize resume skills relevant to the target job role.
- Do not ask advanced topics absent from both the resume and job role.
- Return only a numbered list from 1 to 10.
- Do not add headings, explanations, answers, or extra text.
"""

    response = model.generate_content(prompt)

    return response.text