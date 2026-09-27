# Knowledge Graph Construction Mini Project

This mini project extracts entities and relations from the Knowledge Graphs project-group case study using Python and spaCy.

## Input text

> Berners-Lee was born in London on 8 June 1955. Berners-Lee worked as an independent contractor at CERN from June to December 1980. While in Geneva, he proposed a project based on the concept of hypertext, to facilitate sharing and updating information among researchers.

## Approach

The project uses two complementary approaches:

1. **Named Entity Recognition (NER):** spaCy's `en_core_web_sm` model identifies entities such as people, organizations, locations, and dates.
2. **Pattern-based relation extraction:** transparent rules are used for the relations in this short case study. This keeps the output reproducible and makes it clear how each relation was obtained.

The final structured result is saved to `outputs.json`.

## Setup

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Run the extractor:

```bash
python extract_kg.py
```

This creates/updates `outputs.json`.

## Example relations

The extracted relations include:

- `(Berners-Lee, born_in, London)`
- `(Berners-Lee, birth_date, 8 June 1955)`
- `(Berners-Lee, worked_at, CERN)`
- `(Berners-Lee, was_in, Geneva)`
- `(Berners-Lee, proposed, project)`
- `(project, based_on, concept of hypertext)`

## Notes

Relation extraction is more difficult than NER because spaCy's standard English model does not provide a general-purpose relation-extraction component. For this small case study, explicit patterns are used so that the extraction logic is easy to inspect. For a larger dataset, this could be extended with a trained relation-extraction model, dependency parsing, or an LLM-based extraction pipeline.
