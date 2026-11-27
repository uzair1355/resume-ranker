"""NLP preprocessing: clean text -> lemmatized tokens."""

import re

import spacy

# Only tokenizer, tagger and lemmatizer are needed, so disable heavy parts for speed
_nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

_EMAIL = re.compile(r"\S+@\S+")
_URL = re.compile(r"(https?://\S+|www\.\S+|github\.com/\S+|linkedin\.com/\S+)")
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def remove_contact_info(text: str) -> str:
    """Emails, links and phone numbers carry no skill information."""
    text = _EMAIL.sub(" ", text)
    text = _URL.sub(" ", text)
    text = _PHONE.sub(" ", text)
    return text


def preprocess(text: str) -> str:
    """Lowercase, remove contact info and stop words, lemmatize."""
    text = remove_contact_info(text)
    doc = _nlp(text.lower())
    tokens = [
        tok.lemma_
        for tok in doc
        if tok.is_alpha and not tok.is_stop and len(tok.lemma_) > 1
    ]
    return " ".join(tokens)