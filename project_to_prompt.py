import os
import shutil

def clean_temp_directory(temp_dir):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def process_directory(root_dir, output_file):
    temp_dir = os.path.join(root_dir, '.temp')
    clean_temp_directory(temp_dir)

    os.makedirs(temp_dir)

    excluded_files = ['package-lock.json', '.env']
    excluded_dirs = ['node_modules', 'dist']

    for root, dirs, files in os.walk(root_dir):
        # Exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Exclude excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            temp_file_path = os.path.join(temp_dir, rel_path)

            # Skip excluded files
            if any(excluded_file in rel_path for excluded_file in excluded_files):
                continue

            try:
                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                shutil.copy(file_path, temp_file_path)
            except PermissionError:
                print(f"Permission denied: {file_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")

    with open(output_file, 'w') as output:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, temp_dir)
                output.write(f'# File: {rel_path}\n')
                with open(file_path, 'r') as input_file:
                    output.write(input_file.read())
                output.write('\n---\n')

    clean_temp_directory(temp_dir)

    # Add explanation section at the end
    with open(output_file, 'a') as output:
        output.write('\n---\n')
        output.write('File Generation Details:\n')
        output.write('- The generated file contains the contents of each file within the specified root directory.\n')
        output.write('- Each file is preceded by a comment line indicating its path.\n')
        output.write('- Files and directories excluded from the output:\n')
        for excluded_dir in excluded_dirs:
            output.write(f'  - Directory: {excluded_dir}\n')
        for excluded_file in excluded_files:
            output.write(f'  - File: {excluded_file}\n')

    print(f'File "{output_file}" generated successfully.')

if __name__ == '__main__':
    root_dir = input("Enter the root directory: ")
    output_file = input("Enter the output file name: ")

    process_directory(root_dir, output_file)
