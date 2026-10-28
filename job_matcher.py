
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python", "java", "sql", "excel", "power bi",
    "tableau", "pandas", "numpy", "machine learning",
    "deep learning", "nlp", "data analysis",
    "data visualization", "statistics", "scikit-learn",
    "streamlit", "flask", "django", "html", "css",
    "javascript", "react", "git", "github",
    "communication", "problem solving"
]


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


def analyze_match(resume_text, job_description):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    skill_score = (
        len(matched) / len(job_skills) * 100
        if job_skills else 0
    )

    return {
        "similarity_score": round(similarity * 100, 2),
        "skill_score": round(skill_score, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing
    }
