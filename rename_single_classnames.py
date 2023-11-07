import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def change_class_name(xml_folder, old_name, new_name):
    for xml_file in tqdm(os.listdir(xml_folder)):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(xml_folder, xml_file)
            
            
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for elem in root.findall('object/name'):
                if elem.text == old_name:
                    elem.text = new_name
            
            tree.write(file_path)

xml_folder = '/home/nagarjuna/Desktop/PO_PROJECT_BACKUP_DATA/po_final_dataset_oct4'  
old_name = 'quantity_list_v'  
new_name = 'size_header_list_v' 
change_class_name(xml_folder, old_name, new_name)
