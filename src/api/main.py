from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from typing import List
from sqlmodel import Session, create_engine, select
from src.api.models import Project, Clip
from src.workers.tasks import process_video_pipeline
import os

app = FastAPI(title="Thai Creator AI Platform API")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
engine = create_engine(DATABASE_URL)

@app.post("/projects/", response_model=Project)
async def create_project(title: str, video_file: UploadFile = File(...)):
    """
    Upload a long-form video and trigger the AI clipping pipeline.
    """
    # 1. Save File Locally/S3
    upload_path = f"./storage/uploads/{video_file.filename}"
    with open(upload_path, "wb") as buffer:
        buffer.write(await video_file.read())
    
    # 2. Create Database Record
    with Session(engine) as session:
        project = Project(title=title, original_url=upload_path)
        session.add(project)
        session.commit()
        session.refresh(project)
        
        # 3. Push to Celery Worker
        process_video_pipeline.delay(project.id)
        
        return project

@app.get("/projects/{project_id}", response_model=Project)
async def get_project_status(project_id: int):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

@app.get("/projects/{project_id}/clips", response_model=List[Clip])
async def get_project_clips(project_id: int):
    with Session(engine) as session:
        statement = select(Clip).where(Clip.project_id == project_id)
        clips = session.exec(statement).all()
        return clips

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)