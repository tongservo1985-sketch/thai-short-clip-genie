import cv2
import numpy as np

class SmartVerticalCropper:
    """
    Calculates the 9:16 crop window and applies temporal smoothing 
    to prevent jerky camera movements.
    """
    def __init__(self, width, height, smoothing_factor=0.15):
        self.canvas_w = width
        self.canvas_h = height
        self.target_aspect = 9 / 16
        self.smoothing = smoothing_factor
        
        # Calculate crop width based on original height for 9:16
        self.crop_w = int(self.canvas_h * self.target_aspect)
        self.crop_h = self.canvas_h
        
        # Initialize center at middle of video
        self.current_center_x = self.canvas_w // 2

    def calculate_crop_window(self, active_speaker_face):
        if active_speaker_face:
            # Target center is the x-midpoint of the speaker's face
            x, y, w, h = active_speaker_face.bbox
            target_x = x + (w // 2)
        else:
            target_x = self.canvas_w // 2

        # Apply Linear Interpolation (Lerp) for smoothing
        self.current_center_x = (
            (1 - self.smoothing) * self.current_center_x + 
            self.smoothing * target_x
        )

        # Boundary constraints
        left = int(self.current_center_x - (self.crop_w // 2))
        right = left + self.crop_w

        if left < 0:
            left = 0
            right = self.crop_w
        if right > self.canvas_w:
            right = self.canvas_w
            left = right - self.crop_w

        return left, 0, right, self.crop_h

    def apply_crop(self, frame, crop_coords):
        x1, y1, x2, y2 = crop_coords
        return frame[y1:y2, x1:x2]