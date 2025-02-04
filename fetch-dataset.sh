#!/bin/bash

# Check if both parameters are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <dataset_url> <target_folder>"
    exit 1
fi

DATASET_URL=$1
TARGET_FOLDER=$2

# Create target directory if it doesn't exist
mkdir -p "$TARGET_FOLDER"

# Download and extract dataset
curl -L "$DATASET_URL" > roboflow.zip
unzip roboflow.zip -d "$TARGET_FOLDER"
rm roboflow.zip

# Detect OS and use appropriate sed syntax
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's|../train/images|./train/images|g' "$TARGET_FOLDER/data.yaml"
    sed -i '' 's|../valid/images|./valid/images|g' "$TARGET_FOLDER/data.yaml"
    sed -i '' 's|../test/images|./test/images|g' "$TARGET_FOLDER/data.yaml"
else
    # Linux and others
    sed -i 's|../train/images|./train/images|g' "$TARGET_FOLDER/data.yaml"
    sed -i 's|../valid/images|./valid/images|g' "$TARGET_FOLDER/data.yaml"
    sed -i 's|../test/images|./test/images|g' "$TARGET_FOLDER/data.yaml"
fi
