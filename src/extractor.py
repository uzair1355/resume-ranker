"""Extract and clean text from resume PDFs."""

import re
from pathlib import Path

import pdfplumber



def extract_text_from_pdf(pdf_path: str) -> str:
    """Return the raw text of every page in a PDF, joined together."""
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
             text = page.extract_text(x_tolerance=1.5)
             if text:  # scanned/image-only pages return None
                pages_text.append(text)
    return "\n".join(pages_text)




def text_quality(text: str) -> float:
    """Fraction of tokens that look like normal words (0 to 1). Low = likely OCR garbage."""
    tokens = text.split()
    if not tokens:
        return 0.0
    good = sum(1 for t in tokens if t.strip(".,;:()-'\"/&").isalpha())
    return round(good / len(tokens), 2)




def clean_text(text: str) -> str:
    """Normalize raw extracted text so later NLP steps get consistent input."""
    # Convert "smart" punctuation to plain ASCII before the non-ASCII strip
    replacements = {
        "\u2019": "'", "\u2018": "'",    # curly single quotes
        "\u201c": '"', "\u201d": '"',    # curly double quotes
        "\u2013": "-", "\u2014": "-",    # en/em dashes
        "\u00a0": " ",                   # non-breaking space
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Rejoin words split across lines with a hyphen: "develop-\nment" -> "development"
    text = re.sub(r"-\n(\w)", r"\1", text)
    # Replace bullet characters and other symbols with a space
    text = re.sub(r"[•●▪■◦○►✓�]", " ", text)
    # Remove non-printable / non-ASCII junk but keep common punctuation
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    # Collapse multiple spaces/tabs into one
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse 3+ newlines into a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip spaces around each line
    text = "\n".join(line.strip() for line in text.splitlines())
    return text.strip()



def extract_resume(pdf_path: str) -> dict:
    """Full pipeline for one resume: extract, clean, and report quality."""
    raw = extract_text_from_pdf(pdf_path)
    cleaned = clean_text(raw)
    return {
        "filename": Path(pdf_path).name,
        "text": cleaned,
        "word_count": len(cleaned.split()),
        "is_scanned": len(cleaned.split()) < 30,  # almost no text -> likely an image PDF
         "quality": text_quality(cleaned),
    }




def extract_all(folder: str) -> list[dict]:
    """Run the pipeline on every PDF in a folder."""
    results = []
    for pdf_file in sorted(Path(folder).glob("*.pdf")):
        try:
            results.append(extract_resume(str(pdf_file)))
        except Exception as e:  # one bad file shouldn't crash the whole batch
            results.append({"filename": pdf_file.name, "text": "", "word_count": 0,
                            "is_scanned": False, "error": str(e)})
    return results