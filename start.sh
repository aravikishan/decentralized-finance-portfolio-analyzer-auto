#!/bin/bash
set -e
echo "Starting Decentralized Finance Portfolio Analyzer..."
uvicorn app:app --host 0.0.0.0 --port 9024 --workers 1
