import os

from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# Define the path to the dataset (folder containing annotations.json)
dataset_path = os.getenv("DATASET_PATH")

# We load the COCO dataset using the defined DATASET_PATH
# We point to the annotations json file and the input image folder.
# The image folder can be an absolute path or a relative path to the annotations.json file.

# Defined dataset is processed here to be available for the UI application and further operations.
coco_loader, dataset_id = loader.from_coco(
    f"{dataset_path}/train/_annotations.coco.json",
    input_images_folder="./"
)

loader.launch()
