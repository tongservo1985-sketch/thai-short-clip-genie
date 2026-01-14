import ffmpeg
import os
import logging

logger = logging.getLogger(__name__)

class VideoTranscoder:
    """
    Handles FFmpeg operations for converting horizontal long-form content 
    to vertical (9:16) viral clips.
    """
    
    @staticmethod
    def create_viral_clip(input_path: str, output_path: str, start: float, duration: float, crop_x: int = 0):
        """
        Extracts a segment and applies a 9:16 vertical crop centered on the 
        active speaker (coordinates provided by the CV Service).
        """
        try:
            # target resolution: 1080x1920 (Vertical)
            stream = ffmpeg.input(input_path, ss=start, t=duration)
            
            # 1. Scale to height 1920 first while maintaining aspect ratio
            # 2. Crop the center (or speaker-focused X) to 1080 width
            # 3. Ensure hardware acceleration if available (h264_nvenc)
            
            video = (
                stream.video
                .filter('scale', -1, 1920)
                .filter('crop', 1080, 1920, crop_x, 0)
            )
            
            audio = stream.audio
            
            output = ffmpeg.output(
                video, audio, 
                output_path, 
                vcodec='libx264', 
                acodec='aac', 
                strict='experimental',
                preset='fast',
                crf=23
            )
            
            output.run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            return True
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            return False