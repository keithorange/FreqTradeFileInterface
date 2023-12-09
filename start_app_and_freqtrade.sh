#!/bin/bash

# Activate FreqTrade Virtual Environment
FREQTRADE_DIR="$HOME/Code/freqtrade"
source "$FREQTRADE_DIR/.venv/bin/activate"

# Start App (App should Launch Freqtrade, or you can launch it here)
python3 app.py
