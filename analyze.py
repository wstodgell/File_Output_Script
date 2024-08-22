import os

root_directory = r'E:\Code\scripts_and_tools\secretsUpdateScript3'

# Directories to exclude from the search (use just names for relative comparison)
excluded_dirs = [
    '__pycache__',
    'venv',
    '.git'
]

# Files to search for by name (regardless of directory)
files_to_search = [
    "scripts.js",
    "style.css",
    "index.html",
    "app.py",
    "config.json",
    "file_tools.py",
    "github_secrets_update.py",
    "terraform_secrets_update.py"
]

def print_directory_structure(root_dir, output_file):
    output_file.write(f"{root_dir}:\n")
    print(f"{root_dir}:")
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Normalize the current directory path
        norm_dirpath = os.path.normcase(os.path.normpath(dirpath))
        
        # Check if the current directory is in the excluded list
        if any(excluded_dir in norm_dirpath.split(os.sep) for excluded_dir in excluded_dirs):
            continue
        
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = '|' + '   ' * level
        line = f"{indent}+---{os.path.basename(dirpath)}"
        
        if dirpath == root_dir:
            line = f"{indent}."
        
        print(line)
        output_file.write(line + '\n')
        
        sub_indent = '|' + '   ' * (level + 1)
        for filename in filenames:
            file_line = f"{sub_indent}{filename}"
            print(file_line)
            output_file.write(file_line + '\n')

def check_files(root_dir, output_file):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Normalize current directory path
        norm_dirpath = os.path.normcase(os.path.normpath(dirpath))

        # Exclude specified directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]

        for filename in filenames:
            if filename in files_to_search:
                filepath = os.path.relpath(os.path.join(dirpath, filename), start=root_dir)
                print(f"\n{filepath}:")
                output_file.write(f"\n{filepath}:\n")
                print('"')
                output_file.write('"\n')
                with open(os.path.join(dirpath, filename), 'r') as file:
                    content = file.read()
                    print(content)
                    output_file.write(content + '\n')
                print('"')
                output_file.write('"\n')

def main():
    # Check if the directory exists
    if not os.path.isdir(root_directory):
        print(f"Error: The directory '{root_directory}' does not exist.")
        return

    # Define the path for the output file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_directory, 'output.txt')

    # Open the output file in write mode (overwrite if exists)
    with open(output_file_path, 'w') as output_file:
        # Print the directory structure
        print_directory_structure(root_directory, output_file)

        # Check and print contents of specified files
        check_files(root_directory, output_file)

    print(f"\nOutput written to {output_file_path}")

if __name__ == "__main__":
    main()
