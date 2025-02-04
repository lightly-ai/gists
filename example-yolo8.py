import os

from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# Define the path to the dataset (folder containing data.yaml)
dataset_path = os.getenv("DATASET_PATH")

# Load YOLO dataset using data.yaml path
yolo_loader, dataset_id = loader.from_yolo(
    f"{dataset_path}/data.yaml",
    input_split="train",
)

loader.launch()
