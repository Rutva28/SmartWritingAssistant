
import json
from pathlib import Path

import spacy
from spacy import displacy

# Smart Reading & Writing Assistant
# Stage 2A: POS Tagging and Dependency Parsing

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "en_core_web_sm"


def load_nlp_model():
    """Load spaCy's English language model."""
    try:
        return spacy.load(MODEL_NAME)
    except OSError as error:
        raise RuntimeError(
            "English model not found. Run:\n"
            "python -m spacy download en_core_web_sm"
        ) from error


def process_sentence(text, nlp):
    """Return POS tags, dependencies, entities, and a parse tree."""
    doc = nlp(text)

    sentences = []

    for sentence in doc.sents:
        tokens = []

        for token in sentence:
            if token.is_space:
                continue

            tokens.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dependency": token.dep_,
                "head": token.head.text,
            })

        sentences.append({
            "sentence": sentence.text,
            "tokens": tokens,
        })

    entities = [
        {
            "text": entity.text,
            "label": entity.label_,
            "description": spacy.explain(entity.label_) or entity.label_,
        }
        for entity in doc.ents
    ]

    # Save an HTML visualization of dependency relations.
    html = displacy.render(
        doc,
        style="dep",
        page=True,
        options={"compact": True, "distance": 100},
    )

    html_path = OUTPUT_DIR / "dependency_parse.html"
    html_path.write_text(html, encoding="utf-8")

    result = {
        "text": text,
        "sentences": sentences,
        "entities": entities,
        "dependency_visualization": str(html_path),
    }

    json_path = OUTPUT_DIR / "syntax_results.json"
    json_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return result


def print_results(result):
    print("\n" + "=" * 65)
    print("SMART READING & WRITING ASSISTANT")
    print("STAGE 2A: SYNTACTIC PROCESSING")
    print("=" * 65)

    print("\nInput text:")
    print(result["text"])

    for number, sentence in enumerate(result["sentences"], start=1):
        print(f"\nSentence {number}: {sentence['sentence']}")
        print("-" * 65)
        print(f"{'WORD':<18}{'POS':<12}{'TAG':<12}{'DEPENDENCY':<18}HEAD")
        print("-" * 65)

        for token in sentence["tokens"]:
            print(
                f"{token['text']:<18}"
                f"{token['pos']:<12}"
                f"{token['tag']:<12}"
                f"{token['dependency']:<18}"
                f"{token['head']}"
            )

    print("\nNamed entities:")
    if result["entities"]:
        for entity in result["entities"]:
            print(f"- {entity['text']}: {entity['description']}")
    else:
        print("- No named entities detected.")

    print("\nDependency visualization saved to:")
    print(result["dependency_visualization"])
    print("\nStructured JSON saved to:")
    print(OUTPUT_DIR / "syntax_results.json")


def main():
    nlp = load_nlp_model()

    sample = (
        "The student reads the book. "
        "Rutva studies computer engineering at Ahmedabad."
    )

    result = process_sentence(sample, nlp)
    print_results(result)


if __name__ == "__main__":
    main()
