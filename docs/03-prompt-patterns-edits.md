# Prompt Patterns for Edits

So you have an image that's 80% right. Editing is where beginners give up — usually because they rewrite the whole prompt instead of changing one thing. Here's the discipline.

## The Golden Rule of edits

**Change one thing per attempt.** One word, one setting slider, or one mask region. If the tool gives you a seed, lock the seed so the parts you like stay put. Then you can actually tell whether your change helped.

:::caution
If you rewrite the prompt completely and re-roll, the tool rebuilds the picture from scratch. Whatever you liked might survive, might not. That's not editing; that's re-generating with extra steps.
:::

## Edit tool #1: Image-to-image (img2img)

You give it a starting image plus a **strength** slider. Low strength ≈ "stay close to my image." High strength ≈ "inspired by it only."

| Goal | Start at |
|---|---|
| Slight recolor / mood nudge | 0.2 – 0.35 |
| Restyle same composition | 0.4 – 0.6 |
| New-ish take on the scene | 0.65 – 0.8 |

:::card
**Before (edit attempt)**

> Original: portrait sketch. Prompt rewrite from scratch: `a photorealistic portrait of a young woman` → new face, new hair, new background. All the parts you liked: gone.

**After (img2img, strength 0.4)**

> Same sketch as input, prompt: keep the sketch's description, add `gentle watercolor wash, warm paper texture`. Composition and likeness hold; the wash lands on top.
:::

## Edit tool #2: Inpainting (paint inside the mask)

Inpainting = "regenerate only this rectangle/brushed region." This is the correct tool for "fix the hand," "replace the sign," "put a red barn there instead." The rest of the image is untouched, which is exactly why you use it instead of re-rolling.

Pattern for the *mask prompt*: describe only what should be in the masked area, in full detail.

:::card
**Before**

> Main prompt: `a hedgehog tea party` + fix-in-same-prompt: `no hedgehog`. Tool regenerates everything; three hedgehogs become two.

**After**

> Mask the plate area, mask prompt: `a blue ceramic teacup on the table, top-down match, consistent lighting`. Only the teacup appears, everything else survives.
:::

## Edit tool #3: Outpainting (paint outside the frame)

Outpainting extends the canvas. Useful when the composition is good but the crop fights you: extend the sky, extend the road, uncrop someone's knees. Same discipline: describe the new region and the transition ("continue the grass field seamlessly").

:::card
**Before**

> Re-roll a 16:9 image as portrait to fit a phone wallpaper → different image entirely.

**After**

> Keep the 9:16 canvas, outpaint upward: `continue rocky canyon wall and hazy sky, seamless`. Now you have your wallpaper *and* your original.
:::

## Edit tool #4: Zoom-and-regenerate

No inpainting? Two workaround classics:

1. **Crop and upscale** the messed-up corner, re-feed it as a new image, and re-roll just that piece, then paste it back in any image editor. Good for faces.
2. **Crop-out trick:** if something's wrong at the edge of the frame, zoom the framing in your prompt ("tight close-up") so it never gets generated.

## Words that steer edits

- "keep everything else unchanged" (helps weaker tools a little; don't trust it fully)
- "same lighting as the rest of the scene" (helps patched regions blend)
- "consistent with the style of [X]" (helps style drift)
- Describe the *replacement*, never the removal. Tools replace inside a mask; "no plaid" in your mask prompt gives you competing plaid.

:::card
**Before**

> Mask prompt: `no text on the sign`

**After**

> Mask prompt: `plain weathered wooden sign with peeling sky-blue paint`
:::

> Bottom line: edits are surgery, not wish-granting. Small regions, small changes, lock what works. Chapter 4 is where to go when the edit leaves seams.
