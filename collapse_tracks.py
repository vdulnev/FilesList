import json

def collapse_iso_tracks(input_json, output_json):
    """
    Collapse ISO/SACD track entries (filename;1, filename;2, etc.) into single base filename.
    """
    filenames = []
    seen = set()
    
    print(f"Reading {input_json}...")
    
    with open(input_json, 'r', encoding='utf-8') as f:
        all_filenames = json.load(f)
        
        for filename in all_filenames:
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
    
    print(f"Writing to {output_json}...")
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(filenames, f, ensure_ascii=False, indent=2)
    
    print(f"Done! {len(filenames)} unique filenames written to {output_json}")

if __name__ == '__main__':
    collapse_iso_tracks('lib.json', 'lib.json')
