# Upscaling and Cleanup Steps

The image finally looks right — on your screen. Now what? This chapter covers getting it to full size and scrubbing the small wrongnesses before it goes anywhere public or on paper.

## Get it right at the source first

Upscaling makes pixels bigger; it does not make a picture *better*. A soft, messy image upscaled is still soft and messy, just big. Fix composition and content at generation time (Chapters 2–3), then upscale. Order of operations matters.

## What upscaling actually does

Two families of tools:

- **Plain resizers** (any image editor): interpolate pixels. Bigger, but soft.
- **AI upscalers**: trained on millions of photo pairs to *invent* plausible detail — sharpening edges, recovering skin texture, de-noising grain.

The AI kind is magic until it invents the wrong detail: new freckles that weren't there, a fence that wasn't in the photo, subtle face changes. Which raises the obvious question...

:::caution
**Faces deserve extra care.** AI upscalers can subtly change a face — a slightly different nose, smoothed expression. If the image is of a real person (your own, family), compare side-by-side with the original at 100% zoom before you print or post it. If it doesn't look like them anymore, don't ship it. See Chapter 8 for family photos.
:::

## A cleanup routine that actually works

Do these in order. Most images need only steps 1, 2, and 5.

1. **Take a break, then look at full size.** Zoom to 100% and pan around the whole image. You will spot things you missed at thumbnail size: a floating cup, a third arm on the person in the back, text that says "CAFE" and also "CAFÈ."
2. **Fix content, not pixels.** If something is genuinely wrong (six fingers, warped chair legs), go back to the tool and inpaint just that region (Chapter 3). Don't smear it with a blur brush; that looks worse, not better.
3. **Check the corners and edges.** Look for seams from outpainting, smeared borders, or leftover frame fragments. A careful crop solves about half of these.
4. **De-noise / de-artifact gently.** If the upscale added plastic-y skin or crispy halos, back off the upscale strength or re-run at 2× instead of 4×. Less is more.
5. **Crop with intent.** Decide the final aspect *after* the picture works, then crop. Save as PNG or high-quality JPEG. Name it something you'll find later: `grandma-birthday-poster-v3-final.png` beats `download(17).png`.

## Choosing upscale strength

| Your plan | Go with |
|---|---|
| Screen share, blog, social post | Often no upscale needed at all |
| 8×10 print | 2× from a decent base, then check at 100% |
| Poster (11×17+) | Generate big if the tool allows, then 2×–4×; test-print a corner first |

Don't assume "4×" is twice as good as "2×." It's usually twice as invented. Test at 2× first, and only go further if the paper size truly demands it.

## When to stop cleaning

Diminishing returns are real. Signs you're done: it reads correctly at a glance, prints pass the arm's-length test (Chapter 9), and further passes are changing things you can't name. A picture that's 95% right and *done* beats one you've polished into uncanny.

> Bottom line: generate right → inpaint wrong spots → upscale last → crop → name the file like an adult. That's the whole pipeline.
