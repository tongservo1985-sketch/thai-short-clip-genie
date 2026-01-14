import pythainlp
from pythainlp.tokenize import word_tokenize, sent_tokenize
from pythainlp.util import normalize

class ThaiNaturalSegmenter:
    """
    Handles the nuances of Thai language which has no spaces between words.
    Crucial for generating readable captions for short-form video.
    """
    
    def __init__(self, engine="crfcut"):
        self.engine = engine

    def clean_text(self, text: str) -> str:
        # Standardize Thai characters and remove redundant vowels
        return normalize(text)

    def segment_for_captions(self, text: str, max_chars: int = 40) -> list:
        """
        Segments long Thai ASR output into natural phrases suitable for subtitles.
        Uses CRF-based segmentation for better context awareness.
        """
        text = self.clean_text(text)
        words = word_tokenize(text, engine=self.engine)
        
        phrases = []
        current_phrase = ""
        
        for word in words:
            if len(current_phrase) + len(word) <= max_chars:
                current_phrase += word
            else:
                phrases.append(current_phrase.strip())
                current_phrase = word
        
        if current_phrase:
            phrases.append(current_phrase.strip())
            
        return phrases

    def detect_slang_and_thanglish(self, text: str):
        """
        Identify code-switching (Thai-English) to ensure the NLU
        correctly weights viral potential of 'Trendy' language.
        """
        words = word_tokenize(text)
        english_words = [w for w in words if pythainlp.util.isthai(w) is False and w.isalnum()]
        return {
            "thanglish_count": len(english_words),
            "detected_keywords": english_words
        }

# Example Usage
if __name__ == "__main__":
    segmenter = ThaiNaturalSegmenter()
    raw_transcript = "วันนี้เราจะมาสอนทำอาหารไทยที่อร่อยที่สุดในโลกแบบง่ายๆสไตล์เด็กหอ"
    print(segmenter.segment_for_captions(raw_transcript, max_chars=20))