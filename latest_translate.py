import csv
from lxml import etree
import json

my_dict = json.load(open('/home/abhishek/Downloads/svg/my_new_dict.json'))

def translate_svg_text_to_tamil(file_path, output_path):    
    parser = etree.XMLParser(resolve_entities=False, huge_tree=True)
    
    # Parse the SVG file with the custom parser
    tree = etree.parse(file_path, parser)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    
    for text_tag in root.xpath(".//svg:text", namespaces=namespace):


        ############# GETING KEY####################
        sublist = []
        if text_tag.text and text_tag.text.strip():
            sublist.append(text_tag.text.strip())

        for tspan_tag in text_tag.xpath(".//svg:tspan", namespaces=namespace):
            if tspan_tag.text and tspan_tag.text.strip():
                sublist.append(tspan_tag.text.strip())
        key = '+'.join(sublist).lower()
        print(key)
        #################################################

        if text_tag.text and text_tag.text.strip():
            original_text = text_tag.text.strip()
            if len(original_text)>1:
                try:
                    translated_text = my_dict[key][original_text.lower()]
                except:
                    translated_text = original_text
                text_tag.text = translated_text
                text_tag.set("font-family", "Noto Sans Tamil")   

        for tspan_tag in text_tag.xpath(".//svg:tspan", namespaces=namespace):
            if tspan_tag.text and tspan_tag.text.strip():
                original_text = tspan_tag.text.strip()
                if len(original_text)>1:
                    try:
                        translated_text = my_dict[key][original_text.lower()]
                    except:
                        translated_text = original_text
                    tspan_tag.text = translated_text
                    tspan_tag.set("font-family", "Noto Sans Tamil")

    tree.write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

    print(f"Translated SVG saved to: {output_path}")

input_svg = "/home/abhishek/Downloads/svg/india-detailed/India-detailed-map.svg"
output_svg = "india-translated_tamil.svg"

translate_svg_text_to_tamil(input_svg, output_svg)
