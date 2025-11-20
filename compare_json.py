import json

def compare_json_files(file1, file2):
    """
    Compare two JSON files containing arrays of filenames.
    Shows what's in file1 but not in file2, and vice versa.
    """
    print(f"Loading {file1}...")
    with open(file1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    
    print(f"Loading {file2}...")
    with open(file2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    # Filter out excluded file types
    excluded_extensions = [
        '.jpg', '.jpeg', '.log', '.txt', '.png', '.cue',
        '.m3u', '.tif', '.bmp', '.md5', '.sfv', '.ffp',
        '.pdf', '.m3u8', '.accurip', '.inf', '.exe', '.qdat', '.diz', '.mov', '.dir', '.ons'
    ]
    
    def should_exclude_file(filename):
        """Check if filename should be excluded (case-insensitive)."""
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in excluded_extensions)
    
    print(f"Filtering out {len(excluded_extensions)} file types: {', '.join(excluded_extensions)}...")
    original_count1 = len(data1)
    original_count2 = len(data2)
    data1 = [p for p in data1 if not should_exclude_file(p)]
    data2 = [p for p in data2 if not should_exclude_file(p)]
    filtered_count1 = original_count1 - len(data1)
    filtered_count2 = original_count2 - len(data2)
    print(f"Filtered out {filtered_count1} files from {file1}")
    print(f"Filtered out {filtered_count2} files from {file2}")
    
    # Normalize paths for comparison (lowercase, standard separators)
    print("Normalizing paths for comparison...")
    import os
    
    def normalize_path(p):
        return os.path.normpath(p).lower()
        
    set1 = {normalize_path(p) for p in data1}
    set2 = {normalize_path(p) for p in data2}
    
    # Find differences
    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1
    common = set1 & set2
    
    print(f"\n{'='*80}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*80}")
    print(f"\nTotal entries in {file1} (after filtering): {len(data1)}")
    print(f"Total entries in {file2} (after filtering): {len(data2)}")
    print(f"Common entries: {len(common)}")
    print(f"Only in {file1}: {len(only_in_file1)}")
    print(f"Only in {file2}: {len(only_in_file2)}")
    
    if only_in_file1:
        print(f"\n{'='*80}")
        print(f"ENTRIES ONLY IN {file1} (missing from {file2}): {len(only_in_file1)} entries")
        print(f"{'='*80}")
        if len(only_in_file1) <= 20:
            sorted_only_1 = sorted(only_in_file1, key=str.lower)
            for i, entry in enumerate(sorted_only_1, 1):
                print(f"{i}. {entry}")
        else:
            print(f"(Too many to display, saving to file...)")
    
    if only_in_file2:
        print(f"\n{'='*80}")
        print(f"ENTRIES ONLY IN {file2} (missing from {file1}): {len(only_in_file2)} entries")
        print(f"{'='*80}")
        if len(only_in_file2) <= 20:
            sorted_only_2 = sorted(only_in_file2, key=str.lower)
            for i, entry in enumerate(sorted_only_2, 1):
                print(f"{i}. {entry}")
        else:
            print(f"(Too many to display, saving to file...)")
    
    # Save differences to files
    if only_in_file1:
        output_file = f"only_in_{file1.replace('.json', '')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in sorted(only_in_file1, key=str.lower):
                f.write(entry + '\n')
        print(f"\nSaved entries only in {file1} to: {output_file}")
    
    if only_in_file2:
        output_file = f"only_in_{file2.replace('.json', '')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in sorted(only_in_file2, key=str.lower):
                f.write(entry + '\n')
        print(f"Saved entries only in {file2} to: {output_file}")

if __name__ == '__main__':
    compare_json_files('lib.json', 'file_paths.json')
