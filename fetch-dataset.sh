#!/bin/bash

# Check if required parameters are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <dataset_url> <target_folder> [dataset_type]"
    echo "       dataset_type is optional and defaults to YOLO"
    exit 1
fi

DATASET_URL=$1
TARGET_FOLDER=$2
# Set default dataset type to YOLO if not provided
DATASET_TYPE=${3:-YOLO}

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
