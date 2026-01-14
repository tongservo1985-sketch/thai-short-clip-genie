variable "aws_region" {
  default = "ap-southeast-1" # Bangkok/Singapore for low latency
}

variable "gpu_instance_type" {
  default = "g4dn.xlarge" # NVIDIA T4 - Best price/performance for Whisper inference
}

variable "worker_count" {
  default = 2
}