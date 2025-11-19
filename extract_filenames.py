import xml.etree.ElementTree as ET
import csv

def extract_filenames_to_csv(xml_file, csv_file):
    """
    Extract filename fields from lib.xml and write to CSV file, sorted alphabetically.
    """
    filenames = []
    
    print(f"Processing {xml_file}...")
    
    # Use iterparse for memory-efficient processing of large XML files
    context = ET.iterparse(xml_file, events=('start', 'end'))
    context = iter(context)
    
    item_count = 0
    
    for event, elem in context:
        if event == 'end' and elem.tag == 'Item':
            # Look for the Filename field within this Item
            for field in elem.findall('Field'):
                if field.get('Name') == 'Filename':
                    filename = field.text
                    if filename:
                        filenames.append(filename)
                    break
            
            item_count += 1
            if item_count % 10000 == 0:
                print(f"Processed {item_count} items, found {len(filenames)} filenames...")
            
            # Clear the element to free memory
            elem.clear()
    
    print(f"\nTotal items processed: {item_count}")
    print(f"Total filenames found: {len(filenames)}")
    print("Sorting filenames alphabetically...")
    
    # Sort filenames alphabetically (case-insensitive)
    filenames.sort(key=str.lower)
    
    print(f"Writing to {csv_file}...")
    
    # Write to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename'])  # Header
        for filename in filenames:
            writer.writerow([filename])
    
    print(f"Done! {len(filenames)} filenames written to {csv_file}")

if __name__ == '__main__':
    extract_filenames_to_csv('lib.xml', 'lib.csv')
