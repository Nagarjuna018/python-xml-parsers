import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

def compute_area(box):
    return (box['xmax'] - box['xmin']) * (box['ymax'] - box['ymin'])

def percent_inside(inner_box, outer_box):
    left = max(inner_box['xmin'], outer_box['xmin'])
    right = min(inner_box['xmax'], outer_box['xmax'])
    top = max(inner_box['ymin'], outer_box['ymin'])
    bottom = min(inner_box['ymax'], outer_box['ymax'])
    
    if left < right and top < bottom:
        intersection_area = compute_area({
            'xmin': left, 'ymin': top, 'xmax': right, 'ymax': bottom
        })
        return intersection_area / compute_area(inner_box)
    return 0

def parse_and_rename(directory):
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()

            # Extract all bounding boxes
            boxes = []
            table_bboxes = []
            for object in root.findall('object'):
                class_name = object.find('name').text
                bndbox = object.find('bndbox')
                box = {
                    'xmin': int(bndbox.find('xmin').text),
                    'ymin': int(bndbox.find('ymin').text),
                    'xmax': int(bndbox.find('xmax').text),
                    'ymax': int(bndbox.find('ymax').text),
                    'class_name': class_name,
                    'element': object
                }
                if class_name == 'table':
                    table_bboxes.append(box)
                else:
                    boxes.append(box)

            for table_bbox in table_bboxes:
                for box in boxes:
                    if percent_inside(box, table_bbox) >= 0.95:
                        box['element'].find('name').text = 'column'

            
            tree.write(os.path.join(directory, filename))

if __name__ == '__main__':
    directory = '/home/nagarjuna/Desktop/PO_PROJECT_2/po_final_dataset_oct_6'  
    parse_and_rename(directory)
