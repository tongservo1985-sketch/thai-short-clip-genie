# Virality Scoring Algorithm (VSA) Documentation

Our proprietary VSA focuses on four pillars specifically tuned for the Thai digital landscape:

## 1. The "Hook" Density (Weight: 40%)
In Thai social media, the first 3 seconds are critical. We look for:
- **Thai Call-to-Action (CTA):** Keywords like "แจกพิกัด", "สรุปให้", "ห้ามพลาด".
- **Emotional Spikes:** Detecting high-intensity Thai particles (e.g., "นะเนี่ย", "สุดๆ", "ว้าย").
- **Question-Answer Loops:** Identifying segments that start with a "Why" or "How" in Thai.

## 2. Audio Dynamics & Energy (Weight: 25%)
- **Speech Rate:** 140-160 Thai words per minute is optimal for engagement.
- **Volume Variance:** Significant shifts in volume often indicate excitement or a punchline.
- **Background Music/Laughter:** Detection of "555" (laughter) or audience reaction.

## 3. Semantic Coherence (Weight: 20%)
- Ensures the clip is a complete "thought."
- Uses Thai Sentence Segmentation to avoid cutting mid-sentence.
- Checks for a clear Subject-Action-Result flow.

## 4. Visual Retention Potential (Weight: 15%)
- **Active Motion:** Frequency of scene changes or movement.
- **Face Prominence:** How well the speaker's face is framed (linked to the CV Detector module).

## Scoring Formula
`ViralScore = (HookScore * 0.4) + (AudioEnergy * 0.25) + (Coherence * 0.2) + (VisualDynamics * 0.15)`