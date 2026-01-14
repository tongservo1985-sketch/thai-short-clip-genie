# Developer Setup & Scaling Instructions

## How to add a new AI Model
1. Define a new task in `backend/app/worker/tasks.py`.
2. Add the `gpu_` prefix to ensure it routes to the GPU queue.
3. Update the `docker-compose.yml` to include the necessary NVIDIA drivers/environment.

## Thai Language Edge Case Handling
Our pipeline uses `PyThaiNLP` in the `cpu_identify_hooks` stage to ensure that even if the STT model fails to segment Thai words correctly (due to no spaces in Thai script), the post-processing engine can correctly identify keywords for the viral scoring algorithm.

## Performance Targets
- **Transcription Latency:** < 1 min for a 10-min video.
- **Rendering Throughput:** 50 concurrent clips per GPU cluster.
- **Thai STT Accuracy:** Target 95%+ WER (Word Error Rate) for colloquial Thai.