# System Architecture: Thai Creator AI Video Pipeline

## 1. High-Level Design
The system follows a **Producer-Consumer** pattern using a distributed task queue.

- **API Layer (FastAPI):** Handles user uploads, metadata management, and job status polling.
- **Message Broker (Redis/RabbitMQ):** Orchestrates tasks between the API and Workers.
- **Worker Tier (Celery/Python):**
    - **CPU Workers:** Task orchestration, metadata parsing, and simple FFmpeg operations.
    - **GPU Workers:** Dedicated nodes for Whisper-v3 (Thai STT), CLIP (Visual Analysis), and LLM-based viral scoring.
- **Storage (S3-Compatible):** MinIO or AWS S3 for raw and processed video chunks.

## 2. GPU Queue Strategy
To maximize ROI on expensive GPU instances, we implement:
- **Priority Queuing:** 'Real-time' vs 'Batch' processing.
- **Dynamic Scaling:** Using KEDA (Kubernetes Event-driven Autoscaling) to spin up GPU nodes based on the number of pending tasks in the `gpu_transcription` queue.
- **Resource Locking:** Ensuring only one Whisper model is loaded per GPU memory (VRAM) to prevent OOM (Out of Memory) errors.

## 3. Data Flow
1. User uploads video -> API stores metadata -> Trigger `PROCESS_VIDEO` task.
2. Worker 1 (CPU) -> Extracts audio -> Saves to S3.
3. Worker 2 (GPU) -> Fetches audio -> Runs Fine-tuned Whisper (Thai) -> Generates JSON Transcript.
4. Worker 3 (LLM/GPU) -> Analyzes transcript + Social Trends -> Identifies "Viral Hooks" (Start/End timestamps).
5. Worker 4 (CPU/FFmpeg) -> Slices video based on hooks -> Adds Thai Captions -> Final Render.