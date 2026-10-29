
import re

def calculate_ats_score(resume_text, job_description):
    resume = resume_text.lower()
    job = job_description.lower()

    keywords = set(re.findall(r"\b[a-zA-Z][a-zA-Z+#.]*\b", job))

    stop_words = {
        "the", "and", "for", "with", "you", "your",
        "are", "our", "this", "that", "will", "have",
        "from", "into", "who", "what", "their", "they",
        "job", "role", "work", "using", "about", "candidate"
    }

    keywords = {
        word for word in keywords
        if len(word) > 1 and word not in stop_words
    }

    if not keywords:
        return 0, [], []

    matched = sorted(
        word for word in keywords if word in resume
    )

    missing = sorted(
        word for word in keywords if word not in resume
    )

    score = round(len(matched) / len(keywords) * 100, 2)

    return score, matched, missing
