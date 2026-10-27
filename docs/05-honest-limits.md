# Honest Limits: Hands and Text

You deserve the truth: today's image tools are dazzling and broken at the same time. Knowing *where* they break is what separates people who ship from people who give up. Here are the known weak spots, so you stop blaming yourself.

## Hands and fingers

Hands are the classic tell. Why: hands have many small parts in many configurations, appear tiny in training images, and images often contain *some* hands, so the model hedges. Expect extra fingers, fused fingers, and wrist pretzels regularly.

**Workarounds that actually help:**

- Hide them. Gloves, pockets, crossed arms, holding a big object. Not a failure — a composition choice.
- Fewer hands in frame: profile shots, subjects interacting with a surface.
- Inpaint just the hand (Chapter 3) instead of re-rolling the whole image.
- Upscale the hand region, fix it, paste it back (the crop-and-regenerate trick).
- Accept that some rolls will be discarded. Pros throw away more images than you think.

## Text in images

AI tools are dramatically better at text than two years ago, and still unreliable. Problems: misspellings that *look* right at a glance ("CAFE" / "CAFÉ"), gibberish on small signage, text that shifts when you change anything else.

**Workarounds:**

- Ask for **no text at all**, then add text in a normal graphics app. Ten minutes of editing beats ten re-rolls.
- Keep any necessary text to one or two short words, and treat every render as a draft to proofread *zoomed in*.
- For signs and book covers: generate the art, typeset the words yourself. This is the pro workflow, not a consolation prize.

## Other known weak spots (know before you go)

- **Crowds:** distant faces get smeary or duplicated.
- **Mirrors and reflections:** the reflection often disagrees with reality.
- **Glasses and straws:** frames/straws routinely merge with the face.
- **Furniture logic:** chairs with legs that don't meet the floor, stairs that go nowhere.
- **Counting:** "three apples" gets you *some* apples.
- **Extremes of realism:** an image can be 97% convincing and wrong in one spot that your brain can't un-see once noticed.

:::caution
**The uncanny trust problem:** images *look* authoritative even when wrong. If an AI image will inform anyone — a map, a diagram, a "how it works" illustration for real-world facts — verify the substance yourself, and say in the caption that it's an AI illustration. Chapter 7 has more on labeling.
:::

## The re-roll math (so you stop feeling bad)

A good rule of thumb: expect to generate **3 to 10 attempts** for a decent simple image, and **10+ attempts plus edits** for anything with people, props, or text. If your tenth attempt is still broken, don't conclude you're bad at this. Change tactics: simplify the prompt, inpaint the offender, or crop it out entirely.

> Realistic expectations are the beginner's superpower. If you know text will fail, you plan for it and never lose an afternoon to it.
