import os
import subprocess
import webbrowser
import shutil

def getDesktop():
    if os.name == "posix":
        # Unix-based systems (macOS, Linux)
        desktop_path = os.path.expanduser("~/Desktop")
    elif os.name == "nt":
        # Windows system
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        # Other/unknown system
        desktop_path = None

    if desktop_path:
        print("Desktop Path:", desktop_path)
    else:
        print("Unable to determine desktop path for this system.")
    return desktop_path

def openFolder(path):
    subprocess.Popen(['explorer', path])

def open_browser_for_file(url):
    print(url,"\n")
    webbrowser.open(url) 

def delete_folder():
    folder_path = "C:/dsc"
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the folder: {e}")

def rename_folder():
    old_path = "C:/dsc-extracted"
    new_name = "C:/dsc"
    # Get the directory path and parent directory
    directory, _ = os.path.split(old_path)
    
    # Create the new path by combining the parent directory and the new folder name
    new_path = os.path.join(directory, new_name)
    
    # Rename the folder
    os.rename(old_path, new_path)