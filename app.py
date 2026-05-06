import asyncio
import base64
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from google import genai
from google.genai import types
from hume import AsyncHumeClient
from hume.tts import PostedUtterance, PostedUtteranceVoiceWithName
from hume.empathic_voice.chat.audio.audio_utilities import play_audio

# Load .env from project root
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUME_API_KEY = os.getenv("HUME_API_KEY")

if not HUME_API_KEY:
    raise EnvironmentError("HUME_API_KEY not found in .env")


# ── LLM backends ──────────────────────────────────────────────────────────────

def generate_with_gemini(character_prompt: str, user_message: str) -> str:
    if not GEMINI_API_KEY:
        raise EnvironmentError("GEMINI_API_KEY not found in .env")
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=character_prompt),
        contents=user_message,
    )
    return response.text


def generate_with_claude(character_prompt: str, user_message: str) -> str:
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError("ANTHROPIC_API_KEY not found in .env")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=character_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text


def generate_text(model_choice: str, character_prompt: str, user_message: str) -> str:
    if model_choice == "gemini":
        return generate_with_gemini(character_prompt, user_message)
    elif model_choice == "claude":
        return generate_with_claude(character_prompt, user_message)
    else:
        raise ValueError(f"Unknown model: {model_choice}")


# ── Hume TTS ──────────────────────────────────────────────────────────────────

async def speak(text: str):
    hume = AsyncHumeClient(api_key=HUME_API_KEY)
    result = await hume.tts.synthesize_json(
        utterances=[
            PostedUtterance(
                text=text,
                voice=PostedUtteranceVoiceWithName(name="Ava Song", provider="HUME_AI"),
            )
        ]
    )
    audio_data = base64.b64decode(result.generations[0].audio)
    await play_audio(audio_data)


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("\n=== Gemini + Hume TTS Playground ===\n")

    # Model selection
    print("Select a model:")
    print("  1. Gemini (gemini-2.5-flash)")
    print("  2. Claude (claude-haiku-4-5)")
    model_input = input("\nEnter 1 or 2 [default: 1]: ").strip()
    model_choice = "claude" if model_input == "2" else "gemini"
    print(f"\nUsing: {model_choice}\n")

    # Character prompt
    character_prompt = input("Character prompt (who should the AI play?): ").strip()
    if not character_prompt:
        character_prompt = "You are a helpful assistant."

    print()

    while True:
        user_message = input("Your message (or 'quit' to exit): ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            break
        if not user_message:
            continue

        print("\nGenerating response...")
        text = generate_text(model_choice, character_prompt, user_message)

        print(f"\n{model_choice.capitalize()}: {text}\n")

        # print("Speaking...\n")
        # await speak(text)


if __name__ == "__main__":
    asyncio.run(main())
