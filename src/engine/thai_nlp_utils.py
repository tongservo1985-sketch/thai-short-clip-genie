import re

def clean_thai_text(text: str) -> str:
    """
    Removes redundant Thai characters and normalizes spaces for better analysis.
    """
    # Remove excessive spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Basic normalization for Thai tone marks and vowels
    # (Implementation details for character normalization)
    return text

def detect_emotional_particles(text: str) -> float:
    """
    Detects Thai particles that indicate high emotional engagement.
    """
    particles = ["นะเนี่ย", "เลยทีเดียว", "จุงเลอ", "ชิหาย", "มากก"]
    count = sum(1 for p in particles if p in text)
    return min(1.0, count * 0.2)