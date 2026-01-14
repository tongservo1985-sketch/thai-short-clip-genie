import cv2
import mediapipe as mp
import numpy as np
from dataclasses import dataclass

@dataclass
class FaceMetadata:
    bbox: tuple  # (x, y, w, h)
    landmarks: any
    face_id: int
    lip_distance: float = 0.0

class VideoAnalyzer:
    """
    Uses MediaPipe to detect faces and extract landmarks for active speaker analysis.
    """
    def __init__(self, min_detection_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=4,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence
        )

    def get_lip_distance(self, landmarks, img_height, img_width):
        """Calculates normalized distance between upper and lower lips."""
        # MediaPipe indices for inner lips
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]
        
        dist = np.sqrt((upper_lip.x - lower_lip.x)**2 + (upper_lip.y - lower_lip.y)**2)
        return dist

    def process_frame(self, frame):
        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        faces = []
        
        if results.multi_face_landmarks:
            for idx, landmarks in enumerate(results.multi_face_landmarks):
                ih, iw, _ = frame.shape
                
                # Calculate Bounding Box
                x_coords = [lm.x for lm in landmarks.landmark]
                y_coords = [lm.y for lm in landmarks.landmark]
                
                xmin, xmax = min(x_coords) * iw, max(x_coords) * iw
                ymin, ymax = min(y_coords) * ih, max(y_coords) * ih
                
                lip_dist = self.get_lip_distance(landmarks.landmark, ih, iw)
                
                faces.append(FaceMetadata(
                    bbox=(int(xmin), int(ymin), int(xmax - xmin), int(ymax - ymin)),
                    landmarks=landmarks,
                    face_id=idx,
                    lip_distance=lip_dist
                ))
        return faces