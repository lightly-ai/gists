#!/bin/bash

# Check if all parameters are provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 <dataset_url> <target_folder> <dataset_type>"
    exit 1
fi

DATASET_URL=$1
TARGET_FOLDER=$2
DATASET_TYPE=$3

# Create target directory if it doesn't exist
mkdir -p "$TARGET_FOLDER"

# Download and extract dataset
curl -L "$DATASET_URL" > roboflow.zip
unzip roboflow.zip -d "$TARGET_FOLDER"
rm roboflow.zip

# Only modify paths in data.yaml if it's a YOLO dataset
if [ "$DATASET_TYPE" = "YOLO" ]; then
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
fi
