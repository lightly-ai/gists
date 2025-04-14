# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the yaml file describing the dataset
# and the input images subfolder.
# We use train subfolder.
loader.from_yolo(
    data_yaml_path="dataset/data.yaml",
    input_split="train",
)

# We start the UI application on port 8001
loader.launch()
