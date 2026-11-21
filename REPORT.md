# Procedure Report: Flashcard Generator

**Problem Statement:** 22  
**Roll Number:** 22  
**Category:** Education & Learning

> Replace bracketed placeholders with your own details and observations. Confirm every implementation and testing statement against your actual run before submission.

## 1. Problem statement

Students often need to revise large amounts of study material in limited time. Reading notes repeatedly can make it difficult to identify key ideas and check understanding. This project provides a web application that converts student-provided notes into question-and-answer flashcards for revision.

## 2. Objective

The objective is to build a simple GenAI application that accepts study notes, requests concise flashcards grounded in those notes, presents them interactively, and exports the complete set as CSV.

## 3. Tools and technologies

Python handles application logic. Streamlit provides the user interface and session state. The Ollama Python library connects to a local Ollama service and downloaded language model. JSON provides a structured model response, Pandas organizes cards as rows and columns, and CSV provides a portable download format.

## 4. Procedure followed

1. **Project setup:** Created `app.py`, a `utils` package, dependency list, configuration examples, and documentation.
2. **Library installation:** Install dependencies with `python -m pip install -r requirements.txt` in a virtual environment. **[Record the Python version and installation result from your machine.]**
3. **Ollama setup:** Install Ollama, start its local service, and download a model such as `llama3.2` with `ollama pull llama3.2`. Configure `OLLAMA_HOST` or `OLLAMA_MODEL` only if using non-default settings. No Gemini API key is used.
4. **Prompt engineering:** The prompt defines the educational role, exact card count target, clarity and non-duplication criteria, concise answers, source-only grounding, and a fixed JSON shape. It tells the model to return fewer cards rather than invent content if the notes are insufficient.
5. **Python implementation:** A utility module constructs the prompt, calls the local Ollama model with a JSON schema, parses the response, filters incomplete or repeated questions, and maps common errors to understandable messages.
6. **Streamlit interface:** The app provides a notes box, sample and clear actions, count selector, generation button, one-card-at-a-time revision, answer reveal, navigation, restart, progress, and CSV download. A small built-in demo set allows the revision and export interface to be explored without an API call.
7. **Testing:** In this environment, the dependencies installed successfully in the project virtual environment (`streamlit` 1.67.0, `pandas` 3.1.1, `ollama` 0.6.3). Source compilation and imports passed. Streamlit started and its health endpoint returned `ok`. The default `llama3.2` model was downloaded, and the application's `generate_flashcards` function returned five non-empty, validated cards from sample notes. Additional checks passed for malformed JSON, short-note validation, duplicate/incomplete card filtering, UTF-8 CSV headers and rows, and Streamlit demo-card loading, answer reveal, next-card navigation, restart, and CSV download control. **Please still inspect the visual layout and click the CSV download in your browser before reporting your own final results.**

## 5. Final prompt used by the application

```text
Act as an educational flashcard generator. Read the study notes carefully and identify their important concepts, definitions, facts, and relationships.

Create up to {number_of_cards} useful, non-repetitive flashcards. Each question must be clear, independent, and understandable without another card. Each answer must be accurate, informative, and concise. Cover the most important material fairly. Use only information explicitly stated in the supplied notes or a faithful paraphrase of it; do not use outside knowledge or fill gaps. A term merely being named does not support asking for its definition, function, cause, or effect unless the notes explain that information. If the notes do not support {number_of_cards} distinct question-and-answer pairs, return fewer cards rather than inventing content.

Return valid JSON only, with no Markdown or surrounding explanation, using this exact structure:
{"flashcards":[{"question":"...","answer":"..."}]}

Study notes:
<study_notes>
{notes}
</study_notes>
```

In the actual request, `{number_of_cards}` and `{notes}` are replaced with the selected count and the user's notes.

## 6. Results and sample output

The app displays one question at a time and hides its answer until the user selects **Reveal answer**. The local generation check returned five cards. One actual result was: **Question:** “What is the process by which green plants make food?” **Answer:** “Photosynthesis.” The exact wording depends on the selected local model. **[Capture and attach screenshots of your own app run, including answer reveal and CSV export.]**

## 7. Challenges and solutions

Potential integration challenges are variable model response formatting, a stopped local service, and a model that has not been downloaded. The implementation requests structured JSON, validates the returned structure, accepts JSON wrapped in a code fence as a fallback, and shows brief messages for common errors. **[Add challenges you actually encountered; remove this paragraph if you did not encounter them.]**

## 8. Conclusion

The project demonstrates a small educational use of a large language model running locally with Ollama. It connects a text input interface to the model, validates structured output, supports interactive revision, and provides a CSV export. Students should verify generated content against their original notes.

## 9. Future improvement

Possible additions include uploading PDF or text notes, allowing students to edit cards, adding spaced-repetition scheduling, and supporting more languages. These are future ideas and are not included in the current implementation.

## Personal completion checklist

- **Student name:** [Fill in]
- **Course / class / institution:** [Fill in]
- **Date of practical:** [Fill in]
- **Python version and machine used:** [Fill in]
- **Actual test results:** [Fill in]
- **Screenshots:** [Insert your own screenshots]
