import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def change_class_names(xml_folder, name_mapping):
    for xml_file in tqdm(os.listdir(xml_folder)):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(xml_folder, xml_file)
            
            
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            
            for elem in root.findall('object/name'):
                if elem.text in name_mapping:
                    elem.text = name_mapping[elem.text]
            
            
            tree.write(file_path)

xml_folder = 'path_to_your_xml_files'  
name_mapping = {
    'old_class_name1': 'new_class_name1',
    'old_class_name2': 'new_class_name2',
    
}

change_class_names(xml_folder, name_mapping)
