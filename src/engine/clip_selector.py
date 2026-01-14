from dataclasses import dataclass
from typing import List
from .scoring_model import ViralityScorer

@dataclass
class Segment:
    start_time: float
    end_time: float
    text: str
    audio_energy: float
    visual_score: float

@dataclass
class SelectedClip:
    start_time: float
    end_time: float
    score: float
    headline_th: str
    virality_reason: str

class ClipSelector:
    def __init__(self, min_duration=15, max_duration=60):
        self.scorer = ViralityScorer()
        self.min_duration = min_duration
        self.max_duration = max_duration

    def select_top_clips(self, segments: List[Segment], top_k: int = 5) -> List[SelectedClip]:
        """
        Groups segments into cohesive clips and ranks them.
        """
        potential_clips = []
        
        # Window-based selection logic
        for i in range(len(segments)):
            current_duration = 0
            current_text = ""
            current_audio_sum = 0
            current_visual_sum = 0
            
            for j in range(i, len(segments)):
                seg = segments[j]
                duration = seg.end_time - seg.start_time
                
                if current_duration + duration > self.max_duration:
                    break
                
                current_duration += duration
                current_text += " " + seg.text
                current_audio_sum += seg.audio_energy
                current_visual_sum += seg.visual_score
                
                if current_duration >= self.min_duration:
                    avg_audio = current_audio_sum / (j - i + 1)
                    avg_visual = current_visual_sum / (j - i + 1)
                    
                    score = self.scorer.get_final_score(
                        current_text, avg_audio, avg_visual
                    )
                    
                    potential_clips.append(SelectedClip(
                        start_time=segments[i].start_time,
                        end_time=seg.end_time,
                        score=score,
                        headline_th=self._generate_headline(current_text),
                        virality_reason=self._determine_reason(current_text, avg_audio)
                    ))

        # Filter overlaps and return top K
        sorted_clips = sorted(potential_clips, key=lambda x: x.score, reverse=True)
        return self._filter_overlapping_clips(sorted_clips)[:top_k]

    def _generate_headline(self, text: str) -> str:
        # Simplified: In production, this would call an LLM (GPT-4o or local SEA-LION)
        # to generate a catchy Thai headline.
        return f"Highlight: {text[:30]}..."

    def _determine_reason(self, text: str, audio: float) -> str:
        if audio > 0.8: return "High Energy/Excitement"
        if any(h in text for h in ["วิธี", "สอน"]): return "Educational/How-to"
        return "High Context Relevance"

    def _filter_overlapping_clips(self, clips: List[SelectedClip]) -> List[SelectedClip]:
        """
        Ensures we don't pick the same clip twice with slightly different offsets.
        """
        if not clips: return []
        unique_clips = [clips[0]]
        for c in clips[1:]:
            is_overlap = any(
                not (c.end_time < u.start_time or c.start_time > u.end_time)
                for u in unique_clips
            )
            if not is_overlap:
                unique_clips.append(c)
        return unique_clips