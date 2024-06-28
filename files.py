import os

def list_files_in_directory(directory_path):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            print(file_path)

# Example usage:
# Replace 'your_directory_path' with the path of the directory you want to scan
directory_path = r'C:/Users/xcrss/OneDrive - Universidad Tecnológica de Panamá/C 2/C/Code/Samsung/Proyecto_Tokyo/Tokyo_repo/csv'
list_files_in_directory(directory_path)
