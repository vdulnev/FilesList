import unittest
import os
import csv
import tempfile
import shutil
from pathlib import Path
from file_searcher import search_files


class TestFileSearcher(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary directory structure for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, 'output.csv')
        
        # Create test directory structure
        # /test_dir
        #   /a_folder
        #     - file2.txt
        #     - file1.txt
        #   /b_folder
        #     - file3.txt
        #   /c_folder
        #     /nested
        #       - file4.txt
        #   - root_file.txt
        
        os.makedirs(os.path.join(self.test_dir, 'a_folder'))
        os.makedirs(os.path.join(self.test_dir, 'b_folder'))
        os.makedirs(os.path.join(self.test_dir, 'c_folder', 'nested'))
        
        # Create test files
        Path(os.path.join(self.test_dir, 'a_folder', 'file2.txt')).touch()
        Path(os.path.join(self.test_dir, 'a_folder', 'file1.txt')).touch()
        Path(os.path.join(self.test_dir, 'b_folder', 'file3.txt')).touch()
        Path(os.path.join(self.test_dir, 'c_folder', 'nested', 'file4.txt')).touch()
        Path(os.path.join(self.test_dir, 'root_file.txt')).touch()
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_basic_search(self):
        """Test that all files are found"""
        search_files(self.test_dir, self.output_file)
        
        # Read the CSV
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Check header
        self.assertEqual(rows[0], ['File Path'])
        
        # Check that we have 6 files (5 test files + output.csv itself, excluding header)
        self.assertEqual(len(rows) - 1, 6)
    
    def test_files_sorted_within_folders(self):
        """Test that files are sorted alphabetically within each folder"""
        search_files(self.test_dir, self.output_file)
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)[1:]  # Skip header
        
        file_paths = [row[0] for row in rows]
        
        # Check that file1.txt comes before file2.txt in a_folder
        a_folder_files = [p for p in file_paths if 'a_folder' in p]
        self.assertEqual(len(a_folder_files), 2)
        self.assertTrue(a_folder_files[0].endswith('file1.txt'))
        self.assertTrue(a_folder_files[1].endswith('file2.txt'))
    
    def test_folders_sorted_alphabetically(self):
        """Test that folders are processed in alphabetical order"""
        search_files(self.test_dir, self.output_file)
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)[1:]  # Skip header
        
        file_paths = [row[0] for row in rows]
        
        # Extract folder names from paths
        folders_order = []
        for path in file_paths:
            rel_path = os.path.relpath(path, self.test_dir)
            folder = os.path.dirname(rel_path)
            if folder and folder not in folders_order:
                folders_order.append(folder)
        
        # Check that folders appear in sorted order
        self.assertEqual(folders_order, sorted(folders_order))
    
    def test_nested_directories(self):
        """Test that nested directories are handled correctly"""
        search_files(self.test_dir, self.output_file)
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)[1:]  # Skip header
        
        file_paths = [row[0] for row in rows]
        
        # Check that nested file is found
        nested_files = [p for p in file_paths if 'file4.txt' in p]
        self.assertEqual(len(nested_files), 1)
        self.assertIn('c_folder', nested_files[0])
        self.assertIn('nested', nested_files[0])
    
    def test_output_file_created(self):
        """Test that output CSV file is created"""
        self.assertFalse(os.path.exists(self.output_file))
        search_files(self.test_dir, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
    
    def test_csv_format(self):
        """Test that output is valid CSV format"""
        search_files(self.test_dir, self.output_file)
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Each row should have exactly one column
        for row in rows:
            self.assertEqual(len(row), 1)
    
    def test_absolute_paths(self):
        """Test that all paths in output are absolute"""
        search_files(self.test_dir, self.output_file)
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)[1:]  # Skip header
        
        for row in rows:
            path = row[0]
            self.assertTrue(os.path.isabs(path), f"Path {path} is not absolute")
    
    def test_nonexistent_directory(self):
        """Test handling of non-existent directory"""
        fake_dir = '/this/does/not/exist'
        search_files(fake_dir, self.output_file)
        
        # Should not create output file for non-existent directory
        self.assertFalse(os.path.exists(self.output_file))
    
    def test_empty_directory(self):
        """Test handling of empty directory"""
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir)
        
        output = os.path.join(self.test_dir, 'empty_output.csv')
        search_files(empty_dir, output)
        
        with open(output, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Should only have header
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ['File Path'])


if __name__ == '__main__':
    unittest.main()
