---
type: concept
tags: [diffusion, generative-models, computer-vision, inference-efficiency]
created: 2026-05-24
updated: 2026-05-24
status: stub
---

# Diffusion Models

*Generative models that synthesize data by learning to reverse a gradual noising process — dominant in image/video/portrait generation, but historically slow because they require many denoising steps.*

Created from [[wiki/sources/2026-05-24-personalive-portrait-animation|PersonaLive (Li et al., 2025)]], where the operative theme is **acceleration**, not quality. Two ideas worth keeping:

- **Where the denoising budget actually goes.** Structure and motion converge in the *earliest* denoising steps; later steps only refine appearance (texture, illumination) — often redundantly. *Appearance distillation* compresses a 20+ step model to a 1–4 step schedule with little quality loss. Profile before optimizing.
- **Acceleration strategies broadly:** model quantization, sampling-step reduction, and distillation (ADD, LCM, DMD/DMD2 distill many-step models into few-step generators). PersonaLive's contribution is bringing these to real-time *streaming* portrait animation.

Connects to the [[wiki/areas/ml-research/_overview|"inference is the moat"]] framing and underpins [[wiki/concepts/real-time-avatars|real-time avatars]].

See also: [[wiki/sources/2026-05-24-personalive-portrait-animation]].
