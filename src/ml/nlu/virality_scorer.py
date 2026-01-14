import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class ThaiViralScorer:
    """
    A transformer-based model (Fine-tuned WangchanBERTa) to predict
    if a segment of a transcript has high viral potential (The 'Hook').
    """
    def __init__(self, model_path="airesearch/wangchanberta-base-att-spm-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        # In production, this would be a fine-tuned head for regression/classification
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=1)
        self.model.eval()

    def score_segment(self, text: str) -> float:
        """
        Predicts a 'Viral Score' from 0.0 to 1.0.
        Factors: Emotion, Action Verbs, Thai Slang, Hook Phrasing.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Apply sigmoid to get 0-1 range
            score = torch.sigmoid(outputs.logits).item()
            
        return score

    def find_viral_hooks(self, segments: list, top_k: int = 3):
        """
        Ranks segments and returns the best 'Hooks' for auto-clipping.
        """
        scored_segments = []
        for seg in segments:
            score = self.score_segment(seg['text'])
            scored_segments.append({**seg, "viral_score": score})
            
        # Sort by highest score
        ranked = sorted(scored_segments, key=lambda x: x['viral_score'], reverse=True)
        return ranked[:top_k]

# segment data structure example
# [{'start': 0.0, 'end': 5.0, 'text': 'สวัสดีครับทุกคน วันนี้ผมมีเคล็ดลับลับมาบอก'}, ...]