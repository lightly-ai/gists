import os

from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# Define the path to the dataset
# Dataset is folder containing images and _annotations.coco.json
# It can be an absolute path or a relative.
dataset_path = os.getenv("DATASET_PATH")

# We load the COCO dataset using the defined DATASET_PATH
# We point to the annotations json file and the input images folder.

# Defined dataset is processed here to be available for the UI application.
loader.from_coco_instance_segmentations(
    f"{dataset_path}/_annotations.coco.json",
    dataset_path,
)

# We start the UI application
loader.launch()
