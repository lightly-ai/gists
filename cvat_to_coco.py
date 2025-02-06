import xml.etree.ElementTree as ET
import json
from datetime import datetime
import os
from pathlib import Path

def cvat_to_coco(xml_path, image_dir, output_path):
    """
    Convert CVAT XML annotations to COCO format
    Args:
        xml_path: Path to CVAT XML file
        image_dir: Directory containing the images
        output_path: Path to save the COCO JSON file
    """
    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize COCO format dictionary
    coco_format = {
        "info": {
            "description": "Converted from CVAT",
            "url": "",
            "version": "1.0",
            "year": datetime.now().year,
            "contributor": "",
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Get categories from labels
    categories = {}
    category_id = 1
    for label in root.findall(".//label"):
        label_name = label.find("name").text
        categories[label_name] = category_id
        coco_format["categories"].append({
            "id": category_id,
            "name": label_name,
            "supercategory": "none"
        })
        category_id += 1

    # Process images and annotations
    annotation_id = 1
    for image in root.findall(".//image"):
        # Image info
        image_id = int(image.get("id"))
        width = int(image.get("width"))
        height = int(image.get("height"))
        filename = image.get("name")

        # Add image to COCO format
        coco_format["images"].append({
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": filename,
            "license": 0,
            "flickr_url": "",
            "coco_url": "",
            "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        })

        # Process annotations for this image
        for box in image.findall(".//box"):
            label = box.get("label")
            category_id = categories[label]
            
            # Get coordinates
            xtl = float(box.get("xtl"))
            ytl = float(box.get("ytl"))
            xbr = float(box.get("xbr"))
            ybr = float(box.get("ybr"))
            
            # Calculate COCO format values
            width = xbr - xtl
            height = ybr - ytl
            
            # Add annotation to COCO format
            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xtl, ytl, width, height],
                "area": width * height,
                "segmentation": [],
                "iscrowd": 0
            })
            annotation_id += 1

    # Save to JSON file
    with open(output_path, 'w') as f:
        json.dump(coco_format, f, indent=2)

    print(f"Conversion completed. COCO format annotations saved to {output_path}")
    print(f"Total images: {len(coco_format['images'])}")
    print(f"Total annotations: {len(coco_format['annotations'])}")
    print(f"Total categories: {len(coco_format['categories'])}")

def verify_images(coco_path, image_dir):
    """
    Verify that all images referenced in COCO file exist in image directory
    """
    with open(coco_path, 'r') as f:
        coco_data = json.load(f)
    
    image_dir = Path(image_dir)
    missing_images = []
    
    for img in coco_data['images']:
        if not (image_dir / img['file_name']).exists():
            missing_images.append(img['file_name'])
    
    if missing_images:
        print("Warning: Following images are missing:")
        for img in missing_images:
            print(f"  - {img}")
    else:
        print("All images verified successfully!")

def main():
    # Get parameters from environment variables
    xml_path = os.getenv('CVAT_XML_PATH')
    image_dir = os.getenv('IMAGE_DIR')
    output_path = os.getenv('OUTPUT_PATH')
    
    # Check if required parameters are present
    missing_params = []
    if not xml_path:
        missing_params.append('CVAT_XML_PATH')
    if not image_dir:
        missing_params.append('IMAGE_DIR')
    if not output_path:
        missing_params.append('OUTPUT_PATH')
    
    if missing_params:
        print("Error: Missing required environment variables:")
        for param in missing_params:
            print(f"  - {param}")
        return
    
    # Convert annotations
    cvat_to_coco(xml_path, image_dir, output_path)
    
    # Verify images
    verify_images(output_path, image_dir)

if __name__ == "__main__":
    main()