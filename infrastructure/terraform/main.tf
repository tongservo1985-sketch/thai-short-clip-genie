provider "aws" {
  region = var.aws_region
}

# GPU Optimized Security Group
resource "aws_security_group" "gpu_worker_sg" {
  name        = "thai-creator-gpu-sg"
  description = "Allow internal traffic for Celery/Redis"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # In production, restrict to VPN
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Spot Instance Request for GPU Workers (Cost Saving)
resource "aws_spot_instance_request" "gpu_worker" {
  count         = var.worker_count
  ami           = "ami-064562725417529ad" # Deep Learning OSS Nvidia Driver AMI
  instance_type = var.gpu_instance_type
  key_name      = "thai-creator-key"

  vpc_security_group_ids = [aws_security_group.gpu_worker_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Installing NVIDIA Container Toolkit..."
              distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
              curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
              curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
              sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
              sudo systemctl restart docker
              EOF

  tags = {
    Name = "Thai-Creator-Worker-GPU"
    Role = "Video-Processing"
  }
}