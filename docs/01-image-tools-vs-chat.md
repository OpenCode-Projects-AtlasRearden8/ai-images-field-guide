# How Image Tools Differ From Chat

If you've used a chat assistant, you already have expectations, and some of them will work against you here. An image tool is a different animal. Here's what actually changes.

## Chat AIs and image AIs do different jobs

A chat AI predicts text. It can reason, ask follow-up questions, write a recipe, and correct itself mid-conversation. An image AI (usually a "diffusion model") turns your words into pixels by denoising static into a picture that matches your description. That's why it can paint a gorgeous dragon and still get confused if you ask it to count the dragon's toes.

| | Chat AI | Image AI |
|---|---|---|
| Output | Text back and forth | Pictures (one per attempt) |
| Memory | Rich conversation history | Usually thin: your prompt, a seed, settings |
| Asking questions | It can answer back | It cannot ask back. It just renders |
| Self-correction | "Actually, let me redo that..." | You must re-roll and re-prompt |
| Instructions | Nuance: "except Mondays" works | Every word shifts the whole image |
| Best for | Thinking, writing, planning | Making visuals |

## Five things that surprise chat people

### 1. It cannot ask you to clarify

In chat, if you say "plan my weekend," it asks "indoor or outdoor?" An image tool never asks. If your prompt is ambiguous, it doesn't negotiate — it picks one meaning, silently, and bakes it into pixels. Ambiguity is your job to remove.

:::caution
**Why this matters:** vague prompts aren't "chances" — they're hidden decisions the tool is making *for* you. "A dinner party" could mean a formal banquet, a backyard barbecue, or a rainy kitchen with three chairs. The tool default is almost never your intention.
:::

### 2. There's no conversation, only iterations

You don't have a back-and-forth. You have attempts. Each attempt = a prompt + settings + a roll of the dice. Two sessions of work looks like: ask, look, adjust one thing, ask again, look. Think "taking photos with an old film camera" more than "texting a friend."

### 3. Every word changes *everything*

In chat, one extra sentence usually changes one answer. In images, a single word reshuffles the whole composition. "Dog in a field, sunny" and "Dog in a field, sunny, golden hour" are different pictures, not the same picture with softer light. This is why Chapter 2 teaches the one-change-at-a-time rule.

### 4. Chat-image hybrids are a middle ground

Some tools now put an image generator inside a chat (so you can say "no, the cat on the left") — but underneath, it's still generating fresh images, and the chat wrapper can only nudge it. It still can't truly "fix point X" the way a human artist who redraws one pixel region can. That's what *inpainting* is for (Chapter 3).

### 5. Where you are matters

Some tools run in your browser on someone else's servers (fast, no install, your prompt leaves your machine). Some run **locally** on your own computer or a home server (free per image, slower setup, nothing leaves your device). If privacy matters — and it does for family photos, see Chapter 8 — that difference is a real safety feature, not a spec sheet detail.

## Words you'll meet on the way

These are all in the Glossary (Chapter 11) if you want the full list.

- **Prompt** — the text you write to describe what you want.
- **Seed** — the random starting point; same prompt + same seed = (nearly) same picture.
- **Re-roll** — generate again. What you'll do most.

> Bottom line: treat an image tool like a camera-and-darkroom in a box, not like a chat buddy. Describe scenes, make attempts, keep the good ones.
