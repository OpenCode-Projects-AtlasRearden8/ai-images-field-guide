# Glossary

Plain-English definitions for the words this guide (and every other guide) throws around. Alphabetical.

## Artifact

A visible glitch in an image: smeared edges, plastic skin, halos around objects, warped geometry. Artifacts are usually reasons to re-roll or inpaint, not reasons to accept.

## Aspect ratio

The shape of the canvas, width to height (1:1 square, 16:9 widescreen, 9:16 phone). Set it *before* generating; it shapes the whole composition.

## Bleed

Extra image that extends past the paper's trim line (~3 mm) so commercial cutting never leaves a white edge. Chapter 9.

## CMYK / RGB

The two ways color is made: ink (Cyan-Magenta-Yellow-Black) and light (Red-Green-Blue). Screens use RGB; printers use CMYK; a perfect match between them is impossible, so test-print (Chapter 9).

## Commercial use

Using an image for business: selling it, using it to promote a business, printing it on products you sell. Always check your tool's terms before any commercial use (Chapter 6).

## Diffusion model

The most common kind of image AI. It starts with random noise and removes it step by step until your description remains. That's why the same prompt + different seed gives different pictures.

## DPI (dots per inch)

Print resolution. Paper wants ~300 pixels per inch of printed size; 8×10 needs 2400×3000 pixels. Chapter 9 has the table.

## Inpainting

Regenerating *only* a masked region of an image ("fix just the hand"). The right tool for targeted edits. Chapter 3.

## Img2img (image-to-image)

Generating from a starting image + a strength slider instead of from text alone. Low strength preserves more of your input. Chapter 3.

## Mask

The area you paint to tell an inpainting tool "work here, nowhere else." The prompt you pair with a mask describes only what should be *inside* it.

## Negative prompt

A field for things you *don't* want: `blurry, watermark, extra fingers`. A brake, not a steering wheel (Chapter 2).

## Outpainting

Extending the image beyond its current borders ("add more sky"). Great for rescuing a good composition trapped in the wrong crop. Chapter 3.

## Prompt

The text you write describing what you want. A *description*, not a wish — the pattern is in Chapter 2.

## Re-roll

Generating again. The bread and butter of the whole hobby: expect 3–10 attempts for a decent simple image (Chapter 5).

## Seed

The random number a generation starts from. Same prompt + same seed = (nearly) same image. Lock it when you're editing so your changes are the only thing moving.

## Strength (in img2img)

How far the tool is allowed to wander from your input image (0 = no change, 1 = ignores it). Chapter 3's table has starting points.

## Upscaling

Making an image bigger. Plain resizing just interpolates; AI upscalers invent plausible detail — great, until they invent *wrong* detail. Chapter 4.

## Variation

Same prompt, new roll (or a tool button that makes near-copies with small changes). A gentler way to explore than full re-rolls.

## Watermark

A visible mark showing who made/owns an image. Respect everyone's: don't remove others', don't remove your tool's stamp (it marks rights limits), don't fake one. Chapter 6.
