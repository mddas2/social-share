import zipfile
import os
from tqdm import tqdm  # Import tqdm

def extract_archive_with_progress():
    archive_path = 'main.zip'
    extract_dir = 'C:/dsc-extracted'
    with zipfile.ZipFile(archive_path, 'r') as zipf:
        total_files = len(zipf.namelist())
        with tqdm(total=total_files, desc='Extracting') as pbar:
            for file_info in zipf.infolist():
                zipf.extract(file_info, extract_dir)
                pbar.update(1)  # Update the progress bar
