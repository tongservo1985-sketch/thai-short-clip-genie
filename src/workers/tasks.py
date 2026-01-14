from celery import Celery
import os
from src.services.transcoder import VideoTranscoder
from src.api.models import Project, Clip
from sqlmodel import Session, create_engine, select

# Initialize Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("video_tasks", broker=REDIS_URL, backend=REDIS_URL)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
engine = create_engine(DATABASE_URL)

@celery_app.task(name="process_video_pipeline")
def process_video_pipeline(project_id: int):
    """
    The main orchestration task:
    1. Extract Audio -> STT (Whisper)
    2. Analyze Virality (NLP Agent)
    3. Detect Speakers (CV Service)
    4. Transcode Clips (FFmpeg)
    """
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project: return
        
        project.status = "processing"
        session.add(project)
        session.commit()

        # Step 1: Simulated Call to ML STT (Linguistic Dominance Phase)
        # transcript = whisper_service.transcribe(project.original_url)
        
        # Step 2: Identify Viral Segments (Agent Logic)
        # segments = virality_agent.get_top_segments(transcript)
        
        # Placeholder segments for implementation demo
        mock_segments = [
            {"start": 10.5, "end": 40.5, "score": 0.95, "speaker_center_x": 420},
        ]
        
        for seg in mock_segments:
            clip = Clip(
                project_id=project.id,
                start_time=seg['start'],
                end_time=seg['end'],
                virality_score=seg['score'],
                status="processing"
            )
            session.add(clip)
            session.commit()
            
            # Step 3: Transcode to 9:16
            output_filename = f"clip_{clip.id}.mp4"
            success = VideoTranscoder.create_viral_clip(
                input_path=project.original_url,
                output_path=f"./storage/clips/{output_filename}",
                start=seg['start'],
                duration=seg['end'] - seg['start'],
                crop_x=seg['speaker_center_x']
            )
            
            if success:
                clip.video_path = output_filename
                clip.status = "completed"
            else:
                clip.status = "failed"
            
            session.add(clip)
            session.commit()
            
        project.status = "completed"
        session.add(project)
        session.commit()