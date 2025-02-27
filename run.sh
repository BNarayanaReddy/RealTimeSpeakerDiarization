#!/bin/bash

# Exit on any error
set -e

# Install dependencies from requirements.txt (assuming it’s uploaded to Colab)
echo "Installing requirements..."
pip install -r requirements.txt
echo "Installing system audio libraries..."
sudo apt-get update && apt-get install -y libportaudio2 libasound-dev

# Get the package location dynamically
echo "Locating pyannote.audio..."
PACKAGE_LOCATION=$(pip show pyannote.audio | grep '^Location:' | cut -d ' ' -f 2)

# Check if location was found
if [ -z "$PACKAGE_LOCATION" ]; then
    echo "Error: Could not find pyannote.audio location. Is it installed?"
    exit 1
fi

# Construct the target file path
TARGET_FILE="$PACKAGE_LOCATION/pyannote/audio/models/segmentation/SSeRiouSS.py"
echo "Target file: $TARGET_FILE"

# Check if the target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "Error: $TARGET_FILE does not exist. Check package installation."
    exit 1
fi

# Check if new_network.py exists in the current directory (/content in Colab)
if [ ! -f "SSeRiouSSWithMFCC.py" ]; then
    echo "Error: SSeRiouSSWithMFCC.py not found. Please check path"
    exit 1
fi

# Backup the original file (optional)
BACKUP_FILE="$TARGET_FILE.bak"
echo "Backing up original to $BACKUP_FILE..."
cp "$TARGET_FILE" "$BACKUP_FILE"

# Overwrite SSeRiouSS.py with the contents of new_network.py
echo "Overwriting $TARGET_FILE with SSeRiouSSWithMFCC.py..."
cat SSeRiouSSWithMFCC.py > "$TARGET_FILE"

# Verify the overwrite
if [ $? -eq 0 ]; then
    echo "Successfully overwrote $TARGET_FILE"
else
    echo "Error: Failed to overwrite $TARGET_FILE"
    exit 1
fi