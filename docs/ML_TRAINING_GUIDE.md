# ML Training Guide: Mastering Thai Creator Nuances

## Overview
Standard ASR models struggle with "Thanglish" (Thai + English) and colloquial particles (e.g., นะครับ, อะ, คือแบบ). Our fine-tuning strategy focuses on these linguistic quirks to ensure 98%+ accuracy for Thai creators.

## Data Strategy
1. **Linguistic Normalization:** We use `PyThaiNLP` to handle zero-width space characters and vowel ordering before feeding text to Whisper's tokenizer.
2. **Synthetic Thanglish:** We augment the training set by programmatically replacing Thai technical terms with English equivalents commonly used by tech/lifestyle creators.
3. **Tone Consistency:** Thai is a tonal language. Our preprocessing ensures that the pitch info is preserved during feature extraction.

## Evaluation Metrics
- **CER (Character Error Rate):** Primary metric for Thai due to lack of word boundaries.
- **WER (Word Error Rate):** Secondary metric using `pythainlp.tokenize` as the reference tokenizer.
- **Viral Recall:** Custom metric measuring how many "High-Engagement" moments (defined by TikTok/Reels metadata) were correctly identified as hooks.

## Natural Segmentation (Line Breaking)
Thai text doesn't have spaces. To make captions "Viral-Ready":
- Use `crfcut` for semantic-aware breaks.
- Limit each line to 18-25 characters for readability on mobile screens.
- Avoid breaking in the middle of a Thai "SARA" (vowel) or tone mark.