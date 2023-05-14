import os

def recreate_project_structure(file_path):
    with open(file_path, 'r') as input_file:
        lines = input_file.readlines()

    root_dir = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0])
    os.makedirs(root_dir, exist_ok=True)

    # Remove trailing newlines and separator
    lines = [line.rstrip('\n') for line in lines if line.strip() != '---']

    # Create directories and files
    current_dir = root_dir
    current_content = []
    for line in lines:
        if line.startswith('# File:'):
            # Create the previous file with its content
            if current_content:
                file_path = os.path.join(current_dir, file_name)
                with open(file_path, 'w') as file:
                    file.write('\n'.join(current_content))
                current_content = []

            file_path = line[8:].strip()
            dir_name = os.path.dirname(file_path)

            # Create directories if necessary
            if dir_name:
                current_dir = os.path.join(root_dir, dir_name)
                os.makedirs(current_dir, exist_ok=True)

            # Get the file name
            file_name = os.path.basename(file_path)
        else:
            # Collect the content of the current file
            current_content.append(line)

    # Create the last file with its content
    if current_content:
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'w') as file:
            file.write('\n'.join(current_content))

# Entry point
if __name__ == '__main__':
    file_path = input("Enter the path to the text file: ")
    recreate_project_structure(file_path)
    print("Project structure successfully recreated.")
