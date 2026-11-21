# Viva Preparation: Flashcard Generator

1. **What is Generative AI?**  
   It is AI that creates new content, such as text, images, or code, based on patterns learned from data.

2. **What is an LLM?**  
   A Large Language Model is an AI model trained to understand and generate language.

3. **What is Ollama?**  
   Ollama is software that runs language models on a computer and provides a local service applications can call.

4. **What is prompt engineering?**  
   It is writing clear instructions and context so an AI model is more likely to produce the desired result.

5. **How does this application work?**  
   The student enters notes, Python builds a prompt, the app sends it to Ollama, validates the returned JSON cards, and Streamlit displays and exports them.

6. **What is an API?**  
   An API is a defined way for one program to request a service or data from another program.

7. **Why did you use Python?**  
   Python has readable syntax and libraries for web apps, data handling, and AI services.

8. **Why did you use Streamlit?**  
   Streamlit lets us build an interactive Python web interface without writing a separate frontend.

9. **Why is JSON used?**  
   JSON represents structured data in a format that is easy for the model and Python to exchange and validate.

10. **Why is Pandas used?**  
    Pandas converts the list of cards into a table with Question and Answer columns for CSV export.

11. **What is CSV?**  
    CSV is a plain-text table format that many spreadsheet applications can open.

12. **How are flashcards generated?**  
   The app sends the notes and instructions to the selected model through the local Ollama service, then checks the JSON response for usable question-answer pairs.

13. **Does this project need a Gemini API key?**  
    No. It connects to Ollama on the local computer, so it does not send a Gemini key or require a Gemini account key.

14. **What is session state?**  
    Streamlit session state stores values, such as generated cards and the current card number, across interactions in a user's session.

15. **How does the application handle errors?**  
    It checks for empty or short notes and missing keys, validates the response, and shows friendly messages for malformed output, rate limits, and connection problems.

16. **What does “grounded in the notes” mean here?**  
    The prompt asks the Ollama model to base cards only on supplied notes. This reduces unsupported content but cannot guarantee perfect accuracy, so users should verify answers.

17. **What are the limitations?**  
    Ollama and a model must be installed locally, and generation speed depends on the computer. Results depend on the notes and model response, and cards are not saved permanently.

18. **What is the future scope?**  
    Possible improvements include file uploads, card editing, spaced repetition, and additional languages.

19. **What is `OLLAMA_MODEL`?**  
    It is the environment variable that selects which downloaded Ollama model the app should use, such as `llama3.2`.
