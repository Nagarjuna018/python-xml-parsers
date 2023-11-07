import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

def is_inside(inner_box, outer_box):
    return (inner_box['xmin'] >= outer_box['xmin'] and
            inner_box['ymin'] >= outer_box['ymin'] and
            inner_box['xmax'] <= outer_box['xmax'] and
            inner_box['ymax'] <= outer_box['ymax'])

def parse_and_rename(directory):
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory, filename))
            root = tree.getroot()
            
            table_bbox = None
            for object in root.findall('object'):
                class_name = object.find('name').text
                if class_name == 'table':
                    bndbox = object.find('bndbox')
                    table_bbox = {
                        'xmin': int(bndbox.find('xmin').text),
                        'ymin': int(bndbox.find('ymin').text),
                        'xmax': int(bndbox.find('xmax').text),
                        'ymax': int(bndbox.find('ymax').text),
                    }

            if table_bbox:
                for object in root.findall('object'):
                    class_name = object.find('name').text
                    bndbox = object.find('bndbox')
                    box = {
                        'xmin': int(bndbox.find('xmin').text),
                        'ymin': int(bndbox.find('ymin').text),
                        'xmax': int(bndbox.find('xmax').text),
                        'ymax': int(bndbox.find('ymax').text),
                    }
                    if class_name in 'tabledatapoint':
                        continue
                    elif is_inside(box, table_bbox) :  # Additional condition to prevent renaming of datapoint
                        object.find('name').text = 'column'
        
            tree.write(os.path.join(directory, filename))

if __name__ == '__main__':
    directory = '/home/nagarjuna/Desktop/PO_PROJECT_2/po_final_dataset_oct_6'  
    parse_and_rename(directory)
