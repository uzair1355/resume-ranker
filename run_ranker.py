from pathlib import Path

from src.extractor import extract_all
from src.ranker import rank_resumes

jd = Path("data/job_description.txt").read_text()
resumes = extract_all("data/resumes")

print(f"Ranking {len(resumes)} resumes\n")
print(f"{'Rank':<5}{'Score':<8}{'Quality':<9}File")
print("-" * 55)
for i, r in enumerate(rank_resumes(jd, resumes), start=1):
    print(f"{i:<5}{r['score']:<8}{r['quality']:<9}{r['filename']}")