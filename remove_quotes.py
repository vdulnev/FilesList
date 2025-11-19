import csv

def fix_backslashes_in_csv(input_csv, output_csv):
    """
    Fix double backslashes and remove quotes from filenames in CSV file.
    """
    filenames = []
    
    print(f"Reading {input_csv}...")
    
    # Read the file directly to preserve exact content
    with open(input_csv, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header
    for line in lines[1:]:
        line = line.strip()
        if line:
            # Remove quotes if present
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            # Replace double backslashes with single backslashes
            line = line.replace('\\\\', '\\')
            filenames.append(line)
    
    print(f"Total filenames: {len(filenames)}")
    print(f"Writing to {output_csv}...")
    
    # Write without quotes and with single backslashes
    with open(output_csv, 'w', encoding='utf-8') as f:
        f.write('Filename\n')
        for filename in filenames:
            f.write(filename + '\n')
    
    print(f"Done! Fixed backslashes in {output_csv}")

if __name__ == '__main__':
    fix_backslashes_in_csv('lib.csv', 'lib.csv')

