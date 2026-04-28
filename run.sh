#!/bin/bash
echo "Installing backend dependencies..."
cd backend && pip install -r requirements.txt

echo "Installing playwright browsers..."
playwright install chromium

echo "Training biased model if needed..."
python train_model.py 2>/dev/null || echo "model already exists"

echo "Starting FastAPI on port 8000..."
uvicorn app:app --host 0.0.0.0 --port 8000 &

echo "Installing frontend dependencies..."
cd ../frontend && npm install firebase chart.js react-chartjs-2 && npm install

echo "Starting Next.js on port 3000..."
npm run dev
