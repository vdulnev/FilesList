import os
import json
import argparse
from pathlib import Path

def search_files(directory, output_file):
    """
    Recursively searches for files in the given directory and saves their absolute paths to a JSON file.
    """
    directory_path = Path(directory).resolve()
    
    if not directory_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not directory_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return

    print(f"Searching in: {directory_path}")
    print(f"Outputting to: {output_file}")

    try:
        # First pass: collect all directories
        directories = []
        for root, _, files in os.walk(directory_path):
            if files:  # Only include directories that have files
                directories.append(root)
        
        # Sort directories
        directories.sort()
        
        # Second pass: process each directory and collect file paths
        file_paths = []
        
        for directory in directories:
            # Get files in this directory only (not subdirectories)
            try:
                files = sorted([f for f in os.listdir(directory) 
                               if os.path.isfile(os.path.join(directory, f))])
                
                for file in files:
                    full_path = os.path.join(directory, file)
                    print(f"Found: {full_path}")
                    file_paths.append(full_path)
                    
            except PermissionError:
                print(f"Warning: Permission denied for directory '{directory}'")
                continue
        
        # Write to JSON file
        with open(output_file, mode='w', encoding='utf-8') as jsonfile:
            json.dump(file_paths, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"Successfully saved {len(file_paths)} file paths to '{output_file}'.")

    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Recursively search a folder and save full paths of files to a JSON file.")
    parser.add_argument("directory", nargs='?', default=".", help="The directory to search recursively (default: current directory).")
    parser.add_argument("-o", "--output", default="file_paths.json", help="The output JSON file name (default: file_paths.json).")

    args = parser.parse_args()

    search_files(args.directory, args.output)

if __name__ == "__main__":
    main()
