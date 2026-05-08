# Voice Assistant

A clean, modular Python voice assistant scaffold with:
- Speech-to-text using `SpeechRecognition`
- Text-to-speech using `gTTS`
- Ollama API integration with `gemma3:1b`
- Intent detection and fuzzy fallback
- Name extraction and configurable settings

## Setup

1. Open a terminal in this folder:
   ```powershell
   cd d:\fire-house\week-5\may-7
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Copy the environment example:
   ```powershell
   copy .env.example .env
   ```

5. Edit `.env` if needed, then run:
   ```powershell
   python main.py
   ```

## Structure

- `main.py` — main application workflow
- `speech/` — speech recognition
- `tts/` — text-to-speech
- `llm/` — Ollama client
- `intent/` — intent classifier, name extractor, fuzzy matcher
- `utils/` — helper utilities
- `config/` — settings and config
- `audio/` — temporary audio output

## Notes

- `audio/` stores generated MP3 files
- `.env` is ignored by git
- Use local Ollama API URL in `.env`
