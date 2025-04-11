from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the yaml file describing the dataset
# and the input images subfolder.
# We use train subfolder.
loader.from_yolo(
    "example-datase/data.yaml",
    "train",
)

# We start the UI application
loader.launch()
