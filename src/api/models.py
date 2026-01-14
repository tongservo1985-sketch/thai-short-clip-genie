from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    original_url: str
    status: str = "pending"  # pending, processing, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Store ML analysis metadata (transcript, virality scores)
    metadata_json: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))
    
    clips: List["Clip"] = Relationship(back_populates="project")

class Clip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    start_time: float
    end_time: float
    virality_score: float
    video_path: Optional[str] = None
    status: str = "pending"
    
    project: Project = Relationship(back_populates="clips")