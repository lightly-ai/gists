import os

from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the annotations json file and the input images folder.
# Defined dataset is processed here to be available for the UI application.
loader.from_coco_instance_segmentations(
    "dataset/_annotations.coco.json",
    "dataset/train",
)

# We start the UI application
loader.launch()
