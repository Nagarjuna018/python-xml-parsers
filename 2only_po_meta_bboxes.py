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

            boxes = []
            table_bboxes = []
            # datapoint_bboxes = []
            header_bboxes = []
            all_boxes = []

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
                all_boxes.append(box)

                if class_name == 'table':
                    table_bboxes.append(box)
                elif class_name in ['combo_list_v', 'size_header_list','size_header_list_v', 'price_list_v','combo_block'] :
                    root.remove(box['element'])
                # elif class_name == 'datapoint':
                #     datapoint_bboxes.append(box)
                elif class_name == 'header':
                    header_bboxes.append(box)
                else:
                    boxes.append(box)

    
            for box in all_boxes:
                if box['element'] in root:
                    is_inside_table = any(percent_inside(box, table_bbox) >= 0.90 for table_bbox in table_bboxes)
                    is_inside_header = any(percent_inside(box, header_bbox) >= 0.90 for header_bbox in header_bboxes)
                    if is_inside_table or is_inside_header:
                        root.remove(box['element'])
            for i in all_boxes:
                if i['element'] in root:
                    if i['class_name'] in ["header", "datapoint"] :
                        root.remove(i['element'])

                        
            tree.write(os.path.join(directory, filename))

if __name__ == '__main__':
    directory = r"C:\Users\Arjun\Desktop\test\final_data_po_combo_block_and_column_nov_04"  
    parse_and_rename(directory)
