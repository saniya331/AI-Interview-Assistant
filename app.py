from resume_parser.parser import extract_text
from ai_engine.evaluator import evaluate_all_answers
from ai_engine.gemini_generator import generate_questions
from resume_parser.skill_extractor import extract_skills
from flask import Flask, render_template, request
from google.api_core.exceptions import ResourceExhausted
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

question_list = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global question_list

    resume = request.files.get("resume")
    job_role = request.form.get("job_role", "").strip()

    if not resume or resume.filename == "":
        return "Please select a resume file."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    resume_text = extract_text(filepath)
    skills = extract_skills(resume_text)

    try:
        questions = generate_questions(
            skills,
            resume_text,
            job_role
        )
    except ResourceExhausted:
        return """
        Gemini free quota is exhausted. Please wait a while and try again.
        """

    if not questions:
        return "Question generation failed. Please check your Gemini API key and try again."

    question_list = [
        question.strip()
        for question in questions.split("\n")
        if question.strip()
    ]

    return render_template(
        "interview.html",
        questions=question_list
    )


@app.route("/evaluate", methods=["POST"])
def evaluate():
    if not question_list:
        return "No interview questions found. Please upload your resume again."

    answers = []

    for i in range(len(question_list)):
        answer = request.form.get(f"answer{i + 1}", "").strip()
        answers.append(answer)

    try:
        evaluation_result = evaluate_all_answers(
            question_list,
            answers
        )
    except ResourceExhausted:
        return """
        Gemini free quota is exhausted. Please wait a while and try again.
        """


    evaluation_result = re.sub(r'\n{3,}', '\n\n', evaluation_result)

    return render_template(
        "result.html",
        evaluation_result=evaluation_result
    )


if __name__ == "__main__":
    app.run(debug=True)