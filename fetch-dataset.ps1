param (
    [string]$DATASET_URL,
    [string]$TARGET_FOLDER
)

# Check if both parameters are provided
if (-not $DATASET_URL -or -not $TARGET_FOLDER) {
    Write-Host "Usage: fetch-dataset.ps1 <dataset_url> <target_folder>"
    exit 1
}

# Create target directory if it doesn't exist
New-Item -ItemType Directory -Path "$TARGET_FOLDER" -Force | Out-Null

# Download and extract dataset
Invoke-WebRequest -Uri $DATASET_URL -OutFile "roboflow.zip"
Expand-Archive -Path "roboflow.zip" -DestinationPath "$TARGET_FOLDER" -Force
Remove-Item "roboflow.zip"

$DATA_YAML = "$TARGET_FOLDER\data.yaml"
if (Test-Path $DATA_YAML) {
    # Windows PowerShell equivalent of `sed`
    (Get-Content $DATA_YAML) -replace '\.\./train/images', './train/images' `
                            -replace '\.\./valid/images', './valid/images' `
                            -replace '\.\./test/images', './test/images' | Set-Content $DATA_YAML
}

Write-Host "Dataset downloaded and extracted successfully!"
