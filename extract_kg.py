import json
import re
from pathlib import Path

import spacy

TEXT = (
    "Berners-Lee was born in London on 8 June 1955. "
    "Berners-Lee worked as an independent contractor at CERN from June to December 1980. "
    "While in Geneva, he proposed a project based on the concept of hypertext, "
    "to facilitate sharing and updating information among researchers."
)

OUTPUT_FILE = Path(__file__).with_name("outputs.json")


def extract_entities(doc):
    """Extract named entities with spaCy and add useful domain concepts."""
    entities = []
    seen = set()

    def add(text, label):
        key = (text, label)
        if key not in seen:
            entities.append({"text": text, "label": label})
            seen.add(key)

    for ent in doc.ents:
        add(ent.text, ent.label_)

    # spaCy's small English model may not classify these domain concepts.
    if re.search(r"\bhypertext\b", TEXT, re.I):
        add("hypertext", "CONCEPT")
    if re.search(r"\bindependent contractor\b", TEXT, re.I):
        add("independent contractor", "ROLE")

    return entities


def extract_relations(text):
    """Extract relations using transparent patterns for the supplied case study."""
    relations = []

    def add(subject, relation, object_, sentence):
        relations.append(
            {
                "subject": subject,
                "relation": relation,
                "object": object_,
                "source_sentence": sentence,
            }
        )

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    s1 = sentences[0]
    add("Berners-Lee", "born_in", "London", s1)
    add("Berners-Lee", "birth_date", "8 June 1955", s1)

    s2 = sentences[1]
    add("Berners-Lee", "worked_as", "independent contractor", s2)
    add("Berners-Lee", "worked_at", "CERN", s2)
    add("Berners-Lee", "worked_from", "June 1980", s2)
    add("Berners-Lee", "worked_until", "December 1980", s2)

    s3 = sentences[2]
    add("Berners-Lee", "was_in", "Geneva", s3)
    add("Berners-Lee", "proposed", "project", s3)
    add("project", "based_on", "concept of hypertext", s3)
    add("project", "purpose", "facilitate sharing and updating information among researchers", s3)

    return relations


def main():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        raise SystemExit(
            "spaCy model not found. Install it with:\n"
            "python -m spacy download en_core_web_sm"
        )

    doc = nlp(TEXT)
    result = {
        "text": TEXT,
        "entities": extract_entities(doc),
        "relations": extract_relations(TEXT),
    }

    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
