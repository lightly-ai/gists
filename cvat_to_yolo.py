import xml.etree.ElementTree as ET
import os
from pathlib import Path
import shutil
from typing import Dict, Tuple
import yaml

class CVATtoYOLO:
    def __init__(self, xml_path: str, image_dir: str, output_dir: str):
        """
        Initialize converter
        Args:
            xml_path: Path to CVAT XML file
            image_dir: Directory containing source images
            output_dir: Directory to save YOLO format dataset
        """
        self.xml_path = Path(xml_path)
        self.image_dir = Path(image_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'images').mkdir(exist_ok=True)
        (self.output_dir / 'labels').mkdir(exist_ok=True)
        
        # Parse XML
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        
        # Get categories
        self.categories = self._get_categories()
        
    def _get_categories(self) -> Dict[str, int]:
        """Extract categories from XML and assign YOLO indices"""
        categories = {}
        for idx, label in enumerate(self.root.findall(".//label/name")):
            categories[label.text] = idx
        return categories
    
    def _convert_bbox(self, bbox: Tuple[float, float, float, float], img_width: int, img_height: int) -> Tuple[float, float, float, float]:
        """
        Convert CVAT bbox (x1, y1, x2, y2) to YOLO format (x_center, y_center, width, height)
        All values normalized to [0, 1]
        """
        x1, y1, x2, y2 = bbox
        
        # Calculate width and height
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height
        
        # Calculate center coordinates
        x_center = (x1 + (x2 - x1) / 2) / img_width
        y_center = (y1 + (y2 - y1) / 2) / img_height
        
        return x_center, y_center, width, height
    
    def create_yaml(self):
        """Create YAML file for dataset configuration"""
        yaml_content = {
            'path': str(self.output_dir.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'names': {idx: name for name, idx in self.categories.items()}
        }
        
        with open(self.output_dir / 'dataset.yaml', 'w') as f:
            yaml.dump(yaml_content, f, sort_keys=False)
    
    def convert(self, split_ratio: Tuple[float, float, float] = (0.8, 0.1, 0.1)):
        """
        Convert annotations and organize dataset
        Args:
            split_ratio: Ratio for train/val/test split (default: 0.8/0.1/0.1)
        """
        # Create split directories
        for split in ['train', 'val', 'test']:
            (self.output_dir / 'images' / split).mkdir(exist_ok=True)
            (self.output_dir / 'labels' / split).mkdir(exist_ok=True)
        
        # Get all images
        images = list(self.root.findall(".//image"))
        total_images = len(images)
        
        # Calculate split indices
        train_idx = int(total_images * split_ratio[0])
        val_idx = train_idx + int(total_images * split_ratio[1])
        
        # Process each image
        for idx, image in enumerate(images):
            # Determine split
            if idx < train_idx:
                split = 'train'
            elif idx < val_idx:
                split = 'val'
            else:
                split = 'test'
            
            # Get image info
            img_filename = image.get('name')
            img_width = float(image.get('width'))
            img_height = float(image.get('height'))
            
            # Copy image to appropriate split directory
            src_path = self.image_dir / img_filename
            dst_path = self.output_dir / 'images' / split / img_filename
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
            else:
                print(f"Warning: Image not found: {src_path}")
                continue
            
            # Create YOLO annotation file
            label_filename = dst_path.stem + '.txt'
            label_path = self.output_dir / 'labels' / split / label_filename
            
            with open(label_path, 'w') as f:
                # Process each bounding box
                for box in image.findall('.//box'):
                    label = box.get('label')
                    class_idx = self.categories[label]
                    
                    # Get coordinates
                    x1 = float(box.get('xtl'))
                    y1 = float(box.get('ytl'))
                    x2 = float(box.get('xbr'))
                    y2 = float(box.get('ybr'))
                    
                    # Convert to YOLO format
                    x_center, y_center, width, height = self._convert_bbox(
                        (x1, y1, x2, y2), img_width, img_height
                    )
                    
                    # Write to file
                    f.write(f"{class_idx} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        # Create YAML configuration file
        self.create_yaml()
        
        print(f"Conversion completed. Dataset saved to {self.output_dir}")
        print(f"Total images processed: {total_images}")
        print(f"Categories: {self.categories}")

def main():
    # Read from environment variables
    xml_path = os.getenv('CVAT_XML_PATH')
    image_dir = os.getenv('IMAGE_DIR')
    output_dir = os.getenv('OUTPUT_DIR')
    
    # Check if any required parameters are missing
    missing_params = []
    if not xml_path:
        missing_params.append('CVAT_XML_PATH')
    if not image_dir:
        missing_params.append('IMAGE_DIR')
    if not output_dir:
        missing_params.append('OUTPUT_DIR')
    
    if missing_params:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_params)}\n"
            f"Please set the following environment variables:\n"
            f"- CVAT_XML_PATH: Path to CVAT XML file\n"
            f"- IMAGE_DIR: Directory containing source images\n"
            f"- OUTPUT_DIR: Directory to save YOLO format dataset"
        )
    
    converter = CVATtoYOLO(xml_path, image_dir, output_dir)
    converter.convert()

if __name__ == "__main__":
    main()