import os
import re
import xml.etree.ElementTree as ET
from tqdm import tqdm

def remove_suffix_from_class_names(xml_folder):
    # Regular expression to match class names with underscores followed by numbers
    pattern = re.compile(r'_(\d+)$')

    for xml_file in tqdm(os.listdir(xml_folder)):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(xml_folder, xml_file)
            
            # Parse XML
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Check and modify class names
            for elem in root.findall('object/name'):
                # Use re.sub() to replace the matched pattern with an empty string
                elem.text = pattern.sub('', elem.text)
            
            # Save the changes back to the XML file
            tree.write(file_path)

xml_folder = '/home/nagarjuna/Desktop/PO_PROJECT_BACKUP_DATA/po_final_dataset_oct4'  # Replace with the path to your XML files

remove_suffix_from_class_names(xml_folder)
