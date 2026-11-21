# Flashcard Generator — Problem Statement 22

**Roll Number:** 22 · **Category:** Education & Learning

Convert study notes into concise question-and-answer flashcards for revision. The app uses a local model through Ollama, validates its JSON response, keeps cards in Streamlit session state, and exports all cards to an Excel-friendly CSV file.

## Features

- Paste notes or load a built-in photosynthesis example.
- Generate 5, 10, 15, or 20 cards from the supplied notes.
- Load three demo cards to try revision and CSV export without running a model.
- Reveal answers, navigate, restart, and track progress.
- Friendly handling for missing Ollama service/model, malformed responses, and other generation errors.

## Technology

Python, Streamlit, Ollama Python library, a local Ollama model, Pandas, JSON, and CSV.

## Project structure

```text
flashcard_generator/
├── app.py
├── requirements.txt
├── README.md
├── REPORT.md
├── VIVA.md
├── .gitignore
├── .env.example
└── utils/
    ├── __init__.py
    └── flashcard_generator.py
```

## Install and run

Python 3.10 or newer is recommended.

1. Install [Ollama](https://ollama.com/download) and make sure its local service is running.
2. In a terminal, download a model, for example:

   ```bash
   ollama pull llama3.2
   ```

   You can use another model installed in Ollama by setting `OLLAMA_MODEL` (see below).
3. Create and activate a Python virtual environment, then install app libraries:

   ```bash
   cd flashcard_generator
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

## Ollama configuration

No Gemini API key or cloud API key is needed when using the local Ollama service. The default settings are:

- `OLLAMA_HOST=http://localhost:11434`
- `OLLAMA_MODEL=llama3.2`

Set environment variables before launching Streamlit if your service or model uses different settings. PowerShell example:

```powershell
$env:OLLAMA_HOST="http://localhost:11434"
$env:OLLAMA_MODEL="qwen2.5:7b"
streamlit run app.py
```

You can also copy `.env.example` as a reference when configuring your shell. The app does not automatically load `.env` files. The selected model must already be downloaded in Ollama.

## Usage

1. Paste notes or click **Load sample notes**.
2. Choose a count and click **Generate flashcards**, or use the demo cards to explore the interface without a model call.
3. Reveal the answer, use Previous/Next, or restart the review.
4. Download the full set using **Download all flashcards as CSV**.

The prompt asks the model to use only the supplied notes. This instruction reduces unsupported content but cannot guarantee perfect accuracy; check important answers against course material.

## Example

Input: “Photosynthesis uses sunlight, carbon dioxide, and water to produce glucose and oxygen. It takes place in chloroplasts containing chlorophyll.”

Possible output:

| Question | Answer |
| --- | --- |
| Where does photosynthesis mainly take place? | In chloroplasts, which contain chlorophyll. |
| What materials are used in photosynthesis? | Sunlight, carbon dioxide, and water. |

Output wording can vary. This example illustrates the expected structure, not a claim about a particular live run.

## Screenshots to add

Capture your own running app for the main screen, loaded notes, generated question, revealed answer, and CSV download. Add them under `screenshots/` and link them here. Do not submit fabricated screenshots.

## Limitations and future scope

Generation requires the Ollama service to be running and the chosen model to be installed locally. Speed and quality depend on the model and computer resources. The model may return fewer than requested if the notes do not support enough distinct cards. Cards are kept for the current browser session and are not saved permanently. Future improvements could include file upload, subject tags, editing cards, spaced repetition, and multilingual output.

## GitHub upload

Create an empty repository on GitHub, then run these commands from this project directory (change the URL):

```bash
git init
git add .
git commit -m "Build Flashcard Generator mini project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/flashcard-generator.git
git push -u origin main
```

Before pushing, run `git status` and verify you are not committing local configuration or private data. This project has not been uploaded.
