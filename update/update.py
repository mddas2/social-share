from utilities.api import Api
from .os_action import open_browser_for_file,delete_folder,rename_folder
from tkinter import messagebox
import requests
import os
from .extract_zip import extract_archive_with_progress

class Update(Api):
    def __init__(self):
        super().__init__()

    def getLatestVersion(self):
        response_version = requests.get(self.get_current_version)
        
        respopnse_status = response_version.status_code
        if respopnse_status == 200:
            return response_version.text
        else:
            return "0.0.0"
        

    def checkForUpdate(self):
        update_format = "major.minor.bug" #"1.2.2"

        old_version = self.version
        current_version = self.getLatestVersion()

        print("current version::",old_version)
        print("Latest vesion::",current_version)

        old_version_split = old_version.split(".")
        current_version_split = current_version.split(".")

        if int(current_version_split[0]) > int(old_version_split[0]):
            print("major update")
            return True
        elif int(old_version_split[0]) == int(current_version_split[0]) and int(current_version_split[1]) > int(old_version_split[1]):
            print("minor new feature addedd")
            return True
        elif int(current_version_split[0]) == int(old_version_split[0]) and int(current_version_split[1]) == int(old_version_split[1]) and int(current_version_split[2]) > int(old_version_split[2]):
            print("bug fixed addedd")
            return True
        else:
            print("You are running latest Version..")
            return False
        

    def download_and_install(self,start_progress):
        # return True
        if self.checkForUpdate():
            messagebox.showinfo("Latest Version Found!!!","Please install latest version.")
            # open_browser_for_file(self.software_download)
            print("latest version successfully Installed..")
            import time
          
            time.sleep(0.1)
            url = "http://127.0.0.1:8001/media/latest_version/kantipur_dsc_"+str(self.getLatestVersion())+".zip"
            filename = "main.zip"  # You can specify the desired filename here
            response = requests.get(url)
            total_size = int(response.headers.get('content-length', 0))

            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    start_time = time.time()  # Record the start time
                    chunk_size = 5120  # Size of each chunk
                    downloaded_size = 0  # Initialize the downloaded size
                    for data in response.iter_content(chunk_size=chunk_size):
                        downloaded_size += len(data)
                        file.write(data)
                        percent_complete = (downloaded_size / total_size) * 100
                        # print(f"Downloaded: {percent_complete:.2f}%")
                        start_progress(int(percent_complete)) #display progress bar
                    end_time = time.time()  # Record the end time

                download_time = end_time - start_time  # Calculate the download time in seconds
                file_size = os.path.getsize(filename)  # Get the size of the downloaded file in bytes
                download_speed = file_size / download_time  # Calculate the download speed in bytes per second

                print(f"Downloaded {filename} successfully.")
                print(f"Download speed: {download_speed:.2f} bytes/s")
            else:
                print(f"Failed to download. Status code: {response.status_code}")
                return False
                
            return True
        else:
            return False
    
    def checkInstall(self):
        extract_archive_with_progress()
        delete_folder()
        rename_folder()
        print("all are uptodated, nothing to do.")
        pass

    def main(self,start_progress):
        total = 6000
        # for i in range(total):
        #     percent_complete = (i/total)*100
        #     # print(percent_complete)
        #     start_progress(percent_complete) #display progress bar
        return True
        # if self.download_and_install(start_progress):            
        #     self.checkInstall()
        #     return False
        # else:
        #     return True
 