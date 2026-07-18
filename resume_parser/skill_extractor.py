SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "Flask",
    "Machine Learning",
    "HTML",
    "CSS",
    "JavaScript"
]

def extract_skills(text):
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills