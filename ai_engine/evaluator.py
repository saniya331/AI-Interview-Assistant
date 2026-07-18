import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_all_answers(questions, answers):
    formatted_answers = ""

    for index, (question, answer) in enumerate(zip(questions, answers), start=1):
        formatted_answers += f"""
Question {index}: {question}
Candidate Answer: {answer if answer else "No answer provided"}

"""

    prompt = f"""
You are an experienced technical interviewer.

Evaluate all candidate answers.

IMPORTANT:
- Return ONLY HTML.
- Do NOT return Markdown.
- Do NOT use **, #, ---, or ```html.
- Do NOT return <html>, <head>, <body>, <script>, or <style>.
- Return compact HTML with NO unnecessary blank lines or indentation.

For each question, use EXACTLY this structure:

<div class="question-result">
<h3>Question 1</h3>
<p class="score">Score: X/10</p>
<p><strong>Feedback:</strong> One short and specific improvement suggestion.</p>
<p><strong>Sample Answer:</strong> A concise interview-ready answer in 2–4 sentences.</p>
</div>

After all questions, include:

<h2>Total Score: X/100</h2>

<h3>Strengths</h3>
<ul>
<li>Point 1</li>
<li>Point 2</li>
<li>Point 3</li>
</ul>

<h3>Improvement Areas</h3>
<ul>
<li>Point 1</li>
<li>Point 2</li>
<li>Point 3</li>
</ul>

Rules:
- Score each question out of 10.
- Keep feedback short.
- Keep sample answers concise.
- Keep the total response under 700 words.
- Return valid HTML only.

Candidate Responses:

{formatted_answers}
"""

    response = model.generate_content(prompt)

    html = response.text

    # Remove markdown code blocks if Gemini adds them
    html = html.replace("```html", "")
    html = html.replace("```", "")

    # Remove markdown formatting
    html = html.replace("**", "")
    html = html.replace("---", "")

    # Remove unnecessary whitespace between HTML tags
    html = re.sub(r'>\s+<', '><', html)

    # Remove extra blank lines
    html = re.sub(r'\n\s*\n+', '\n', html)

    return html.strip()