import numpy as np
from collections import deque

class ActiveSpeakerDetector:
    """
    Analyzes lip motion over a window of frames to identify who is speaking.
    Essential for Thai talk shows or multi-person interviews.
    """
    def __init__(self, window_size=15, threshold=0.012):
        self.window_size = window_size
        self.threshold = threshold
        self.history = {} # face_id -> deque of lip distances

    def identify_speaker(self, detected_faces):
        if not detected_faces:
            return None

        active_id = -1
        max_energy = -1

        for face in detected_faces:
            if face.face_id not in self.history:
                self.history[face.face_id] = deque(maxlen=self.window_size)
            
            self.history[face.face_id].append(face.lip_distance)
            
            # Calculate 'Speech Energy' via variance in lip movement
            if len(self.history[face.face_id]) >= self.window_size:
                energy = np.var(self.history[face.face_id])
                if energy > max_energy:
                    max_energy = energy
                    active_id = face.face_id

        # Return the face metadata of the active speaker
        if max_energy > self.threshold:
            return next((f for f in detected_faces if f.face_id == active_id), detected_faces[0])
        
        # Default to first face if no one is clearly speaking
        return detected_faces[0]