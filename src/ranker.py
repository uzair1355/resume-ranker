"""TF-IDF + cosine similarity baseline ranker."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocess import preprocess


def rank_resumes(job_description: str, resumes: list[dict]) -> list[dict]:
    """Score each resume against the job description, sorted best first."""
    jd_clean = preprocess(job_description)
    resume_clean = [preprocess(r["text"]) for r in resumes]

    # Fit on JD + resumes together so they share one vocabulary
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([jd_clean] + resume_clean)

    # Row 0 is the JD; compare it to every resume row
    scores = cosine_similarity(matrix[0:1], matrix[1:])[0]

    ranked = [
        {
            "filename": r["filename"],
            "score": round(float(s) * 100, 1),
            "quality": r["quality"],
        }
        for r, s in zip(resumes, scores)
    ]
    return sorted(ranked, key=lambda x: x["score"], reverse=True)