# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the annotations json file and the input images folder.
# Defined dataset is processed here to be available for the UI application.
loader.from_coco_instance_segmentations(
    annotations_json_path="dataset/_annotations.coco.json",
    input_images_folder="dataset/train",
)

# We start the UI application on port 8001
loader.launch()
