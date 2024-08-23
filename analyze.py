import os
import json

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the name of the JSON configuration file
config_file = os.path.join(script_dir, 'Configuration_SecretsUpdateScript.json')
chatGPT_blurb_file = os.path.join(script_dir, 'chatgpt.json')

def load_chatGPT(chatGPT_blurb_file):
    try:
        with open(chatGPT_blurb_file, 'r') as file:
            chatGPT_blurb = json.load(file)
        return chatGPT_blurb
    except FileNotFoundError:
        print(f"Error: The configuration file '{chatGPT_blurb_file}' does not exist.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the configuration file '{chatGPT_blurb_file}'. Please check the file's format.")
        exit(1)

# Function to read the configuration from a JSON file
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The configuration file '{config_file}' does not exist.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the configuration file '{config_file}'. Please check the file's format.")
        exit(1)

# Load the configuration
config = load_config(config_file)
chatGPT_blurb = load_chatGPT(chatGPT_blurb_file)

root_directory = config['root_directory']
excluded_dirs = config['excluded_dirs']
files_to_exclude = config['files_to_exclude']
specific_files_to_exclude = ['.gitignore', '.terraform.lock.hcl']

# Other functions and main code go here


# Check if the directory should be excluded
def is_excluded_dir(dir_name):
    return dir_name.startswith('.') or dir_name in excluded_dirs

# Check if the file is binary
def is_binary_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:  # Check for null bytes
                return True
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return True
    return False

# Check if the file should be excluded
def is_excluded_file(file_name):
    # Exclude terraform state files, lock files, and .gitignore
    return (
        file_name in files_to_exclude or 
        file_name in specific_files_to_exclude or 
        file_name.endswith('.tfstate') or 
        file_name.endswith('.tfstate.backup')
    )

def print_directory_structure(root_dir, output_file):

    output_file.write(chatGPT_blurb['blurb'] + '\n')

    output_file.write(f"{root_dir}:\n")
    print(f"{root_dir}:")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove excluded directories from dirnames to prevent os.walk from going into them
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]

        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = '|' + '   ' * level
        line = f"{indent}+---{os.path.basename(dirpath)}"

        if dirpath == root_dir:
            line = f"{indent}."

        print(line)
        output_file.write(line + '\n')

        sub_indent = '|' + '   ' * (level + 1)
        for filename in filenames:
            if not is_excluded_file(filename):
                file_line = f"{sub_indent}{filename}"
                print(file_line)
                output_file.write(file_line + '\n')

def check_files(root_dir, output_file):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove excluded directories from dirnames to prevent os.walk from going into them
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]

        for filename in filenames:
            if not is_excluded_file(filename):
                filepath = os.path.join(dirpath, filename)
                if not is_binary_file(filepath):
                    relpath = os.path.relpath(filepath, start=root_dir)
                    print(f"\n{relpath}:")
                    output_file.write(f"\n{relpath}:\n")
                    print('"')
                    output_file.write('"\n')
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            content = file.read()
                            print(content)
                            output_file.write(content + '\n')
                    except Exception as e:
                        print(f"Error reading file {filepath}: {e}")
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

        # Check and print contents of files excluding those in files_to_exclude
        check_files(root_directory, output_file)

    print(f"\nOutput written to {output_file_path}")

if __name__ == "__main__":
    main()
