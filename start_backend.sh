#!/bin/bash
# YinYang Backend Startup Script

cd /home/ubuntu/yinyang/backend
source venv/bin/activate
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
