import os
import re

# Function to count lines in a file
def count_lines_in_file(file_path, file_type):
    code_lines = 0
    comment_lines = 0
    blank_lines = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()

            if not stripped_line:
                blank_lines += 1  # Blank line
            elif file_type == 'py':
                if stripped_line.startswith('#'):
                    comment_lines += 1  # Comment line in Python
                else:
                    code_lines += 1  # Code line
            elif file_type in ['html', 'js', 'css']:
                if stripped_line.startswith('<!--') or stripped_line.startswith('/*') or stripped_line.startswith('//'):
                    comment_lines += 1  # Comment line in HTML/JS/CSS
                else:
                    code_lines += 1  # Code line
            else:
                code_lines += 1  # For other files

    return code_lines, comment_lines, blank_lines

# Function to process a directory and its files
def count_lines_of_code(directory, extensions):
    results = {ext: {'code': 0, 'comments': 0, 'blank': 0, 'total': 0} for ext in extensions}

    # Ignored hidden folders
    ignored_folders = ['.git', '.venv', '_pycache_']

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignored_folders]  # Exclude hidden folders
        for file in files:
            ext = file.split('.')[-1]
            if ext in extensions:
                file_path = os.path.join(root, file)
                code, comments, blank = count_lines_in_file(file_path, ext)
                results[ext]['code'] += code
                results[ext]['comments'] += comments
                results[ext]['blank'] += blank
                results[ext]['total'] += (code + comments + blank)

    return results

# Function to print the results
def print_results(results):
    grand_total = {'code': 0, 'comments': 0, 'blank': 0, 'total': 0}
    for ext, counts in results.items():
        print(f"\nFile Type: {ext.upper()}")
        print(f"  Total lines: {counts['total']}")
        print(f"  Code lines: {counts['code']}")
        print(f"  Comment lines: {counts['comments']}")
        print(f"  Blank lines: {counts['blank']}")
        grand_total['code'] += counts['code']
        grand_total['comments'] += counts['comments']
        grand_total['blank'] += counts['blank']
        grand_total['total'] += counts['total']
    
    print(f"\nGrand Total:")
    print(f"  Total lines: {grand_total['total']}")
    print(f"  Code lines: {grand_total['code']}")
    print(f"  Comment lines: {grand_total['comments']}")
    print(f"  Blank lines: {grand_total['blank']}")

if __name__ == "__main__":
    project_directory = "."  # Current directory
    extensions = ['py', 'html', 'css', 'js']  # Specify the file types you want to analyze
    results = count_lines_of_code(project_directory, extensions)
    print_results(results)