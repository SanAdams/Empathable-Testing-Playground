# What Changed and Why

This document explains the updates made to `app.py` for someone unfamiliar with the Hume and Google Gemini libraries.

---

## Background: What the app does

The app lets you define a character (via a system prompt), then have a conversation with that character. Google Gemini generates the text responses, and Hume TTS reads them aloud using an expressive AI voice.

---

## The two libraries involved

### Google Gemini (`google-genai`)
Gemini is Google's large language model. You send it a **system instruction** (who it should be) and a **user message** (what you're saying), and it returns a text response.

The key concept here is the **system prompt** — it shapes the character's personality, knowledge, and behavior for the entire conversation. For example:

> *"You are Eleanor, a high school principal from Vermont. You are anxious and research-oriented..."*

Everything Gemini says will be filtered through that lens.

### Hume TTS (`hume`)
Hume is a text-to-speech API that goes beyond robotic narration. It reads the **emotional content** of the text and adjusts the voice delivery accordingly — speaking faster when the text is anxious, slower when something is heavy or emotional. This means the character's personality comes through not just in the words, but in how they're spoken.

---

## What changed in this update

### 1. Switched from full audio to streaming

**Before:** The app called `synthesize_json`, which waited for Hume to generate the entire audio file before playing anything.

**After:** The app now calls `synthesize_json_streaming`, which returns audio in small **chunks** as they are generated. Each chunk is a short segment of the full response.

This is the foundation that makes interruption possible — instead of one big audio file, we have a list of pieces we can stop at any point.

---

### 2. Added interruptible playback

During playback, the app now checks for a keypress **before playing each chunk**. If a key is detected, playback stops immediately and the remaining unplayed chunks are saved in memory.

This means if Eleanor is mid-sentence and you press a key, she stops — but the rest of what she was going to say is not lost.

---

### 3. Added a 5-second interrupt window

When playback is interrupted, a prompt appears:

```
[Interrupted]
You (5s to respond, or wait to resume):
```

You have 5 seconds to type a message. Two things can happen:

- **You type something** → your message is sent to Gemini, a new response is generated, and Eleanor responds to what you said. The interrupted speech is discarded.
- **You say nothing (or wait 5 seconds)** → Eleanor resumes speaking from exactly where she left off.

---

### 4. Resume from interruption point

The unplayed audio chunks are kept in a variable called `pending_chunks`. If you choose not to respond, those chunks are played in order — so Eleanor picks up mid-thought rather than restarting her full response from the beginning.

---

## Flow diagram

```
Start
  │
  ▼
Enter character prompt
  │
  ▼
Enter your message
  │
  ▼
Gemini generates response text
  │
  ▼
Hume fetches audio as chunks
  │
  ▼
Play chunks one by one ──── keypress detected?
  │                                  │
  │ No                               │ Yes
  │                                  ▼
  │                         Show 5-second prompt
  │                                  │
  │                    ┌─────────────┴─────────────┐
  │                    │ typed message              │ no input / timeout
  │                    ▼                            ▼
  │             New Gemini response          Resume remaining chunks
  │
  ▼
Back to "Enter your message"
```

---

## What hasn't changed

- The character prompt is still entered once at the start and applies to the whole session
- Gemini still generates all text (Hume only handles speech)
- The voice used is "Ava Song" from Hume's voice library
- API keys are still loaded from the `.env` file
