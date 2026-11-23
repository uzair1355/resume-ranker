from src.extractor import extract_all

results = extract_all("data/resumes")

for r in results:
    print("=" * 60)
    print(f"File: {r['filename']}")
    print(f"Words: {r['word_count']} | Scanned? {r['is_scanned']}")
    if "error" in r:
        print(f"ERROR: {r['error']}")
    print("-" * 60)
    print(r["text"][:500])  # first 500 characters