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

def parse_and_delete(directory):
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()

            boxes = []
            table_bboxes = []
            datapoint_bboxes = []
            header_bboxes = []

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
                # if class_name == 'table':
                #     table_bboxes.append(box)
                # elif class_name == 'datapoint':
                #     datapoint_bboxes.append(box)
                # elif class_name == 'header':
                #     header_bboxes.append(box)
                # else:
                boxes.append(box)

            for rbox in boxes:
                for box in boxes:
                    if percent_inside(box, rbox) >= 0.90:
                        is_inside_table = any(percent_inside(box, boxes) >= 0.90 for box in boxes)
                        is_inside_header = any(percent_inside(box, boxes) >= 0.90 for box in boxes)
                        if is_inside_table and is_inside_header:
                            # box['element'].find('name').text = 'combo_block'
                            root.remove(rbox)
                    elif class_name in ['combo_list_v', 'size_header_list', 'size_header_list_v', 'price_list_v'] :
                         root.remove(rbox)
            tree.write(os.path.join(directory, filename))

if __name__ == '__main__':
    directory = r"C:\Users\Arjun\Desktop\test\final_data_po_combo_block_and_column_nov_04"  
    parse_and_delete(directory)
