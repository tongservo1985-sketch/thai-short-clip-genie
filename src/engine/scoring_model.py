import numpy as np
from typing import List, Dict
import re

class ViralityScorer:
    """
    Calculates virality scores based on Thai linguistic patterns,
    audio intensity, and visual metrics.
    """
    def __init__(self):
        # Thai-specific viral triggers
        self.thai_hooks = [
            "แจกพิกัด", "ห้ามพลาด", "เทคนิค", "ความลับ", "สรุปให้", 
            "ล่าสุด", "ดราม่า", "วิธีทำให้", "ทำไมถึง", "ป้ายยา"
        ]
        self.slang_boosters = ["สุดๆ", "มากแม่", "ตัวแม่", "ของแทร่", "จึ้ง"]

    def calculate_linguistic_score(self, text: str) -> float:
        """
        Analyzes Thai text for viral hooks and high-engagement slang.
        """
        score = 0.0
        # Check for hooks at the start of the segment
        for hook in self.thai_hooks:
            if hook in text[:30]:  # Hook in the first few characters
                score += 0.5
        
        # Check for slang/boosters
        for slang in self.slang_boosters:
            if slang in text:
                score += 0.1
        
        # Check for question/curiosity (Thai syntax)
        if any(q in text for q in ["อย่างไร", "ไหม", "อะไร", "หรอ"]):
            score += 0.2
            
        return min(1.0, score)

    def analyze_audio_energy(self, audio_features: np.ndarray) -> float:
        """
        Calculates energy variance and peak intensity.
        """
        # Placeholder for RMS energy analysis
        mean_energy = np.mean(audio_features)
        std_energy = np.std(audio_features)
        
        # High variance usually means dynamic speaking/storytelling
        score = (mean_energy * 0.4) + (std_energy * 0.6)
        return float(np.clip(score, 0, 1))

    def get_final_score(self, 
                        transcript_segment: str, 
                        audio_intensity: float, 
                        visual_dynamic_score: float) -> float:
        """
        Combines all metrics into a final 0-100 score.
        """
        nlp_score = self.calculate_linguistic_score(transcript_segment)
        
        weighted_score = (
            (nlp_score * 0.40) +
            (audio_intensity * 0.30) +
            (visual_dynamic_score * 0.30)
        )
        
        return round(weighted_score * 100, 2)