# IRIS GUI Concepts

Visual identity ideas for the IRIS interface. The goal: something that feels alive,
reactive, and has personality — not just a camera feed with text.

---

## 1. The Eye (literal IRIS)
An animated eye that IS the camera feed. The iris is the live video, surrounded by
a stylized sclera and pupil overlay. The pupil dilates when IRIS is "thinking" or
sees something interesting. Blinks slowly when idle. When listening, the iris
vibrates subtly with the audio waveform. Most on-brand option given the name.

---

## 2. Ball of Energy
A pulsing orb — glowing plasma or energy field that breathes and reacts to state.
- **Idle**: slow blue pulse, like a heartbeat
- **Listening**: ripples outward from center with mic input amplitude
- **Thinking**: faster chaotic swirl, warmer color (amber/white)
- **Speaking**: rhythmic pulses matching TTS output waveform
Built with OpenCV radial gradients + noise functions or a particle system.

---

## 3. Face / Avatar
A minimal, expressive face — not cartoonish, more like a sleek robot face.
Two dots for eyes, a subtle mouth line. Reacts emotionally to context:
- Curious tilt when asking a question
- Eyes widen when capturing a frame
- Slight "smile" when responding warmly
- Eyes narrow/scan when analyzing an image
Think: *2001 HAL 9000* meets *Portal GLaDOS* but friendlier.

---

## 4. Tamagotchi / Creature
A little creature that lives on screen alongside the camera feed. Has moods,
gets "hungry" for input when idle too long, visibly excited when you show it
something new. Could evolve or change appearance over time based on usage.
Personality grows with the relationship. High attachment potential.

---

## 5. Radar / Sonar Sweep
A circular radar screen — dark background, green sweep arm rotating continuously.
Detected objects from YOLO appear as blips with labels at their angular positions.
When IRIS speaks, the sweep pulses. Feels tactical and sci-fi.
The camera feed lives in the center circle.

---

## 6. Neural Constellation
A star map of nodes and edges — like a neural network or constellation diagram.
Nodes light up and connect as IRIS processes: audio nodes, vision nodes, language
nodes firing in sequence. Each conversation turn leaves a faint trail.
Beautiful when idle, mesmerizing when active. Very "brain" coded.

---

## 7. Liquid Mercury / Blob
A fluid simulation that morphs based on state — calm and still when idle,
turbulent when processing, stretches toward the camera feed when capturing.
Could split into two blobs for stereo audio, merge when thinking.
Implemented with metaballs or shader-style distance fields in OpenCV/pygame.

---

## 8. Waveform Creature
The audio waveform IS the creature. When silent: a flat sleeping line with
a slow breathing undulation. When you speak: it erupts into a dynamic waveform
that wraps into shapes — a circle, a figure, a spiral. When IRIS speaks back:
a different color waveform responds in real time.

---

## 9. Holographic HUD
Sci-fi heads-up display laid over the camera feed. Scan lines, corner brackets,
reticles that track detected faces/objects. Data readouts in the corners
(battery, FPS, last transcription, confidence scores).
Feels like Iron Man's HUD or a drone targeting system.
Most useful for seeing detection data; least "personality."

---

## 10. Crystal / Gem
A rotating 3D low-poly gem (dodecahedron or icosahedron) that glows from within.
Color shifts with mood/state — cool blue for idle, gold for listening,
white-hot for processing, soft green for speaking.
Faces of the gem subtly display the camera feed as a texture.
Elegant and abstract — feels like an artifact, not software.

---

## 11. Black Hole / Void
A swirling dark vortex with a bright accretion ring. The camera feed
is "pulled into" the center. Particles orbit the ring and get
absorbed when IRIS processes input, then eject outward when it responds.
Dramatic, mysterious, high contrast. Fits IRIS as something that
*consumes* information and transforms it.

---

## 12. Vinyl Record / Soundwave Disk
A spinning record where the grooves visualize audio amplitude in real time —
zoomed in, the grooves are actually the waveform. The label in the center
shows the camera feed or current status. Slows when thinking, fast when speaking.
Warm, tactile aesthetic — analog meets AI.

---

## Hybrid Idea: Reactive Eye + HUD
The eye (concept 1) as the core identity, with a minimal HUD ring around it
showing status, battery, and object detection labels. Best of both worlds —
personality from the eye, utility from the data overlay.

---

## Implementation Notes
- **OpenCV + numpy**: good for overlays, waveforms, radar, HUD elements
- **pygame**: better for fluid simulations, particle systems, smooth animation
- **pyglet / moderngl**: if you want actual shaders for the orb/crystal/black hole
- All concepts can live alongside the camera feed or replace it when not in use

