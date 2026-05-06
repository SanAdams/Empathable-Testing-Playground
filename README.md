# Gemini + Hume TTS Playground

A simple interactive playground to experiment with how system prompts affect Gemini's text generation, with Hume TTS reading the responses aloud.

## Setup

1. Clone the repo and enter the directory:
   ```bash
   git clone <your-repo-url>
   cd gemini-hume-playground
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   - Get a Gemini API key at https://aistudio.google.com/apikey
   - Get a Hume API key at https://platform.hume.ai

## Usage

```bash
.venv/Scripts/python.exe app.py
```

When prompted:
- Enter a **character prompt** describing who Gemini should play (e.g. `a grumpy pirate`, `a Shakespearean scholar`, `a cheerful customer service rep`)
- Then type messages to that character and hear the responses spoken aloud
- Type `quit` to exit
