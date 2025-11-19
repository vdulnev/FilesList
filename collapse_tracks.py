import csv

def collapse_iso_tracks(input_csv, output_csv):
    """
    Collapse ISO/SACD track entries (filename;1, filename;2, etc.) into single base filename.
    """
    filenames = []
    seen = set()
    
    print(f"Reading {input_csv}...")
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if row:
                filename = row[0]
                
                # Check if filename has semicolon followed by number (ISO/SACD track)
                if ';' in filename:
                    # Extract base filename (everything before the semicolon)
                    base_filename = filename.rsplit(';', 1)[0]
                    
                    # Only add if we haven't seen this base filename before
                    if base_filename not in seen:
                        filenames.append(base_filename)
                        seen.add(base_filename)
                else:
                    # Regular filename, add as-is
                    filenames.append(filename)
    
    print(f"Original entries: {len(filenames) + len(seen)}")
    print(f"After collapsing: {len(filenames)}")
    print(f"Collapsed {len(seen)} ISO/SACD multi-track files")
    
    print("Sorting alphabetically...")
    filenames.sort(key=str.lower)
    
    print(f"Writing to {output_csv}...")
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename'])  # Header
        for filename in filenames:
            writer.writerow([filename])
    
    print(f"Done! {len(filenames)} unique filenames written to {output_csv}")

if __name__ == '__main__':
    collapse_iso_tracks('lib.csv', 'lib.csv')
