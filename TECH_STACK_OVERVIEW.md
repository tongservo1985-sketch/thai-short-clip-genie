# Technical Stack: Thai Viral AI Platform

## Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS + Shadcn UI
- **State Management:** TanStack Query (React Query)
- **Video Player:** Remotion (for programmatic video rendering and preview)

## Backend & AI Pipeline
- **API Engine:** Python (FastAPI) - Preferred for AI/ML integration.
- **Task Queue:** Celery + Redis (Handling heavy video processing).
- **Database:** PostgreSQL (Supabase) for metadata; Vector DB (Pinecone) for semantic search within videos.
- **Storage:** AWS S3 or Cloudflare R2 for video assets.

## AI Models
- **STT:** OpenAI Whisper v3 (Self-hosted on RunPod/Lambda Labs for Thai fine-tuning).
- **Segmentation:** PyThaiNLP for Thai-specific tokenization.
- **Intelligence:** LLM (GPT-4o/Claude) via API for hook detection and caption summarization.

## Infrastructure
- **CI/CD:** GitHub Actions.
- **Deployment:** Vercel (Frontend), Railway or AWS EC2 (Backend).
- **GPU Workers:** Auto-scaling nodes for FFmpeg and Whisper inference.