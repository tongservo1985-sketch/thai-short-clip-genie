#!/bin/bash
# Simple script to monitor GPU load on the Thai Creator Cluster
# This can be used as a custom metric for CloudWatch or Prometheus

echo "Thai Creator AI - GPU Status Dashboard"
while true
do
    clear
    nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.free --format=csv,noheader
    echo "------------------------------------------------"
    echo "Active Celery Tasks (GPU Queue):"
    celery -A api.tasks inspect active | grep "gpu_tasks"
    sleep 5
done