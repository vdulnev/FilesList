import os
import csv
import argparse
from pathlib import Path

def search_files(directory, output_file):
    """
    Recursively searches for files in the given directory and saves their absolute paths to a CSV file.
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
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['File Path'])  # Header

            file_count = 0
            for root, _, files in os.walk(directory_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    writer.writerow([full_path])
                    file_count += 1
            
            print(f"Successfully saved {file_count} file paths to '{output_file}'.")

    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Recursively search a folder and save full paths of files to a CSV file.")
    parser.add_argument("directory", help="The directory to search recursively.")
    parser.add_argument("-o", "--output", default="file_paths.csv", help="The output CSV file name (default: file_paths.csv).")

    args = parser.parse_args()

    search_files(args.directory, args.output)

if __name__ == "__main__":
    main()
