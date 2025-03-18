import json
from lxml import etree
import csv

def get_words_as_json(file_path, output_json_path):
    parser = etree.XMLParser(huge_tree=True)  # Enable huge_tree to handle large files
    tree = etree.parse(file_path, parser=parser)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    
    all_texts = []
    
    # Iterate over all <text> elements
    for text_tag in root.xpath(".//svg:text", namespaces=namespace):
        sublist = []

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

    # Write the list to a CSV file
    with open('en-words.csv', 'w',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(all_texts)

# Input and output file paths
input_svg = "/home/abhishek/Downloads/svg/india-detailed/India-detailed-map.svg"
output_json = "en-words.json"

get_words_as_json(input_svg, output_json)

print(f"Words have been extracted and saved to {output_json}.")
