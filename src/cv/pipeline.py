import cv2
from src.cv.detector import VideoAnalyzer
from src.cv.speaker_detection import ActiveSpeakerDetector
from src.cv.smart_cropper import SmartVerticalCropper

def process_video_to_vertical(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize CV components
    analyzer = VideoAnalyzer()
    speaker_detector = ActiveSpeakerDetector()
    cropper = SmartVerticalCropper(width, height)

    # Define output writer (9:16 ratio)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (cropper.crop_w, cropper.crop_h))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Detect faces & landmarks
        faces = analyzer.process_frame(frame)
        
        # 2. Identify who is talking
        active_face = speaker_detector.identify_speaker(faces)
        
        # 3. Calculate smooth crop window
        crop_coords = cropper.calculate_crop_window(active_face)
        
        # 4. Generate vertical frame
        vertical_frame = cropper.apply_crop(frame, crop_coords)
        
        out.write(vertical_frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    # Example usage for a Thai creator clip
    process_video_to_vertical("input_podcast.mp4", "output_short_clip.mp4")