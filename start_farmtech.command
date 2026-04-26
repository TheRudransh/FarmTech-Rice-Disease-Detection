#!/bin/bash

# Start Flask API
source /Users/rudranshgarg/FarmTech/.venv311/bin/activate
python /Users/rudranshgarg/FarmTech/app.py &

# Wait for Flask to load
sleep 8

# Start website server
cd /Users/rudranshgarg/FarmTech/build-a-professional-rice-leaf-disease
python3 -m http.server 8000 &

# Open Safari automatically
sleep 2
open -a Safari http://localhost:8000

echo "FarmTech is running!"