import json

def collapse_iso_tracks_text(input_txt, output_txt):
    """
    Collapse ISO/SACD track entries (filename;1, filename;2, etc.) in a text file into single base filename.
    """
    filenames = []
    seen = set()
    original_count = 0
    collapsed_count = 0
    
    print(f"Reading {input_txt}...")
    
    with open(input_txt, 'r', encoding='utf-8') as f:
        for line in f:
            filename = line.strip()
            if not filename:
                continue
            
            original_count += 1
            
            # Check if filename has semicolon followed by ONLY a number at the end (ISO/SACD track)
            # Pattern: filename;123 (where 123 is digits only, nothing after)
            if ';' in filename:
                parts = filename.rsplit(';', 1)
                if len(parts) == 2:
                    base_filename = parts[0]
                    suffix = parts[1]
                    # Only collapse if suffix is digits only (ISO/SACD track number)
                    if suffix.isdigit():
                        # Only add if we haven't seen this base filename before
                        if base_filename not in seen:
                            filenames.append(base_filename)
                            seen.add(base_filename)
                        else:
                            collapsed_count += 1
                    else:
                        # Semicolon but not followed by just digits - treat as regular filename
                        filenames.append(filename)
                else:
                    # Multiple semicolons or other issue - treat as regular filename
                    filenames.append(filename)
            else:
                # Regular filename, add as-is
                filenames.append(filename)
    
    print(f"Original entries: {original_count}")
    print(f"After collapsing: {len(filenames)}")
    print(f"Collapsed {collapsed_count} ISO/SACD track entries")
    
    print("Sorting alphabetically...")
    filenames.sort(key=str.lower)
    
    print(f"Writing to {output_txt}...")
    
    with open(output_txt, 'w', encoding='utf-8') as f:
        for filename in filenames:
            f.write(filename + '\n')
    
    print(f"Done! {len(filenames)} unique filenames written to {output_txt}")

def collapse_iso_tracks(input_json, output_json):
    """
    Collapse ISO/SACD track entries (filename;1, filename;2, etc.) into single base filename.
    """
    filenames = []
    seen = set()
    original_count = 0
    collapsed_count = 0
    
    print(f"Reading {input_json}...")
    
    with open(input_json, 'r', encoding='utf-8') as f:
        all_filenames = json.load(f)
        
        for filename in all_filenames:
            original_count += 1
            
            # Check if filename has semicolon followed by ONLY a number at the end (ISO/SACD track)
            # Pattern: filename;123 (where 123 is digits only, nothing after)
            if ';' in filename:
                parts = filename.rsplit(';', 1)
                if len(parts) == 2:
                    base_filename = parts[0]
                    suffix = parts[1]
                    # Only collapse if suffix is digits only (ISO/SACD track number)
                    if suffix.isdigit():
                        # Only add if we haven't seen this base filename before
                        if base_filename not in seen:
                            filenames.append(base_filename)
                            seen.add(base_filename)
                        else:
                            collapsed_count += 1
                    else:
                        # Semicolon but not followed by just digits - treat as regular filename
                        filenames.append(filename)
                else:
                    # Multiple semicolons or other issue - treat as regular filename
                    filenames.append(filename)
            else:
                # Regular filename, add as-is
                filenames.append(filename)
    
    print(f"Original entries: {original_count}")
    print(f"After collapsing: {len(filenames)}")
    print(f"Collapsed {collapsed_count} ISO/SACD track entries")
    
    print("Sorting alphabetically...")
    filenames.sort(key=str.lower)
    
    print(f"Writing to {output_json}...")
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(filenames, f, ensure_ascii=False, indent=2)
    
    print(f"Done! {len(filenames)} unique filenames written to {output_json}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file
        
        if input_file.endswith('.json'):
            collapse_iso_tracks(input_file, output_file)
        else:
            collapse_iso_tracks_text(input_file, output_file)
    else:
        # Default: process lib.json
        collapse_iso_tracks('lib.json', 'lib.json')
