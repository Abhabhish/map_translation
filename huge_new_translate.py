import csv
from lxml import etree
import json

my_dict = json.load(open('/home/abhishek/Downloads/svg/india-detailed/my_dict.json'))

def translate_svg_text_to_tamil(file_path, output_path):
    # Enable the huge_tree option to handle large SVG files
    parser = etree.XMLParser(resolve_entities=False, huge_tree=True)
    
    # Parse the SVG file with the custom parser
    tree = etree.parse(file_path, parser)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    
    # Open CSV file to log translations
    with open('main.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        n = 0
        for text_tag in root.xpath(".//svg:text", namespaces=namespace) + root.xpath(".//svg:tspan", namespaces=namespace):
            if text_tag.text:
                original_text = text_tag.text.strip()
                if len(original_text) > 1:
                    try:
                        # Translate text using the dictionary
                        translated_text = my_dict.get(original_text.lower(), original_text)
                    except KeyError:
                        # If translation is missing, fallback to the original text
                        translated_text = original_text

                    n += 1
                    print(n, translated_text)

                    # Update the text content with the translated text
                    text_tag.text = translated_text
                    text_tag.set("font-family", "Noto Sans Tamil")

                    # Log original and translated text to CSV
                    csv_writer.writerow([original_text, translated_text])

    # Save the translated SVG
    tree.write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

    print(f"Translated SVG saved to: {output_path}")

input_svg = "/home/abhishek/Downloads/svg/india-detailed/India-detailed-map.svg"
output_svg = "translated_tamil.svg"

translate_svg_text_to_tamil(input_svg, output_svg)
