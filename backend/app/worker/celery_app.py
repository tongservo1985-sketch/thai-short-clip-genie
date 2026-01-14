from celery import Celery
import os

# Initialize Celery to handle distributed video processing
celery_app = Celery(
    "video_processor",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Bangkok",
    enable_utc=True,
    # Separate queues for CPU and GPU tasks
    task_routes={
        "app.worker.tasks.gpu_*": {"queue": "gpu_tasks"},
        "app.worker.tasks.cpu_*": {"queue": "cpu_tasks"},
    },
    # Prevent a single worker from hogging too many tasks
    worker_prefetch_multiplier=1
)