# from lxml import etree

# def get_words(file_path):
    
#     tree = etree.parse(file_path)
#     root = tree.getroot()
#     namespace = {"svg": "http://www.w3.org/2000/svg"}
    
#     for text_tag in root.xpath(".//svg:text", namespaces=namespace) + root.xpath(".//svg:tspan", namespaces=namespace):
#         if text_tag.text:
#             original_text = text_tag.text.strip()
#             if len(original_text)>1:          
#                 with open('en-words.txt','a') as f:
#                     f.write(original_text+'\n')

# input_svg = "/home/abhishek/Downloads/svg/chennai/example.svg"            # Replace with the path to your SVG file

# get_words(input_svg)


import json
from lxml import etree
import csv

def get_words_as_json(file_path, output_json_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    
    all_texts = []
    
    # Iterate over all <text> elements
    for text_tag in root.xpath(".//svg:text", namespaces=namespace):
        sublist = []  # Create a new sublist for each <text> element
        
        # Check for direct text inside <text> tag
        if text_tag.text and text_tag.text.strip():
            sublist.append(text_tag.text.strip())
        
        # Check for <tspan> elements inside <text>
        for tspan_tag in text_tag.xpath(".//svg:tspan", namespaces=namespace):
            if tspan_tag.text and tspan_tag.text.strip():
                sublist.append(tspan_tag.text.strip())
        
        # Add sublist to the main list if it has any words
        if sublist:
            all_texts.append(sublist)
    
    # Write the list to a JSON file
    with open(output_json_path, 'w',encoding='utf-8') as json_file:
        json.dump(all_texts, json_file, indent=4,ensure_ascii=False)

    with open('en-words.csv','w',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(all_texts)

# Input and output file paths
input_svg = "/home/abhishek/Downloads/svg/india-detailed/India-detailed-map-1.svg"  # Replace with your SVG file path
output_json = "en-words.json"  # Replace with your desired JSON output path

get_words_as_json(input_svg, output_json)

print(f"Words have been extracted and saved to {output_json}.")
