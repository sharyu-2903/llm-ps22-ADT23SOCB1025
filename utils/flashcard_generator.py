"""Ollama integration and safe parsing for flashcard generation."""

import json
import os
import re
from typing import Any


class FlashcardError(Exception):
    """A user-safe error raised while generating flashcards."""


MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

FLASHCARD_SCHEMA = {
    "type": "object",
    "properties": {
        "flashcards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                },
                "required": ["question", "answer"],
            },
        }
    },
    "required": ["flashcards"],
}


def build_prompt(notes: str, number_of_cards: int) -> str:
    """Create the constrained prompt used by the local model."""
    return f"""Act as an educational flashcard generator. Read the study notes carefully and identify their important concepts, definitions, facts, and relationships.

Create up to {number_of_cards} useful, non-repetitive flashcards. Each question must be clear, independent, and understandable without another card. Each answer must be accurate, informative, and concise. Cover the most important material fairly. Use only information explicitly stated in the supplied notes or a faithful paraphrase of it; do not use outside knowledge or fill gaps. A term merely being named does not support asking for its definition, function, cause, or effect unless the notes explain that information. If the notes do not support {number_of_cards} distinct question-and-answer pairs, return fewer cards rather than inventing content.

Return valid JSON only, with no Markdown or surrounding explanation, using this exact structure:
{{"flashcards":[{{"question":"...","answer":"..."}}]}}

Study notes:
<study_notes>
{notes}
</study_notes>"""


def _extract_json(text: str) -> Any:
    """Parse plain JSON or a JSON object wrapped in a Markdown code fence."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as first_error:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                pass
        raise FlashcardError("Ollama returned a response that could not be read as flashcard JSON. Please try again.") from first_error


def validate_flashcards(payload: Any, requested_count: int) -> list[dict[str, str]]:
    """Validate the expected object and normalize usable card text."""
    if not isinstance(payload, dict) or not isinstance(payload.get("flashcards"), list):
        raise FlashcardError("The model response did not contain a flashcards list. Please try again.")
    cards: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in payload["flashcards"]:
        if not isinstance(item, dict):
            continue
        question = item.get("question")
        answer = item.get("answer")
        if not isinstance(question, str) or not isinstance(answer, str):
            continue
        question, answer = question.strip(), answer.strip()
        if not question or not answer:
            continue
        key = re.sub(r"\W+", " ", question.casefold()).strip()
        if key in seen:
            continue
        seen.add(key)
        cards.append({"question": question, "answer": answer})
        if len(cards) >= requested_count:
            break
    if not cards:
        raise FlashcardError("No complete question-and-answer cards were found in the model response. Please try again.")
    return cards


def generate_flashcards(notes: str, number_of_cards: int) -> list[dict[str, str]]:
    """Call the local Ollama service and return validated flashcards."""
    if not notes or len(notes.strip()) < 40:
        raise FlashcardError("Please provide at least a few detailed sentences of notes.")
    if number_of_cards not in (5, 10, 15, 20):
        raise FlashcardError("Choose 5, 10, 15, or 20 flashcards.")

    try:
        import ollama
    except ImportError as exc:
        raise FlashcardError("The Ollama Python library is not installed. Run: pip install -r requirements.txt") from exc

    try:
        client = ollama.Client(host=OLLAMA_HOST)
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": build_prompt(notes, number_of_cards)}],
            format=FLASHCARD_SCHEMA,
            options={"temperature": 0},
            stream=False,
        )
        response_text = response.message.content
        if not response_text:
            raise FlashcardError("Ollama returned an empty response. Try again with clearer notes.")
        return validate_flashcards(_extract_json(response_text), number_of_cards)
    except FlashcardError:
        raise
    except Exception as exc:
        message = str(exc).lower()
        if "model" in message and ("not found" in message or "pull" in message):
            raise FlashcardError(
                f"Ollama model '{MODEL_NAME}' is not installed. Run 'ollama pull {MODEL_NAME}' in a terminal, or set OLLAMA_MODEL to an installed model."
            ) from exc
        if (
            "connection refused" in message
            or "connecterror" in message
            or "failed to connect" in message
            or ("connection" in message and "failed" in message)
        ):
            raise FlashcardError("Could not connect to Ollama. Start the Ollama app or service, then try again.") from exc
        raise FlashcardError("Ollama could not generate the flashcards. Check that the service and selected model are available, then try again.") from exc
