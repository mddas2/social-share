import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from tkinter import filedialog

import threading
from dashboard.popup import PopupWindow
from utilities.api import Api
import webbrowser
import time
from utilities.os_action import getDesktop,openFolder


class DashboardGUI(Api):
    def __init__(self,user_data):
   
        super().__init__()

        master = tk.Tk()

        self.desktop_path = getDesktop()

        self.user_data = user_data
        self.master = master
        self.master.title("Dashboard")
        self.master.configure(bg="#f2f2f2")
        self.master.geometry("450x250")

        # Set window icon
        self.master.iconbitmap("images/kantipur.ico")

        self.create_widgets()
        self.selected_file = None  # Variable to store the selected file path
        self.selected_folder = None
        self.file_id = None

        self.private_signature_file = None

        self.is_websocket_connected = False
        self.websocket_obj = None
        
        # self.update_thread = threading.Thread(target=self.run_update_in_thread)
        # self.update_thread.start()

        # self.start_websocket_client_thread(self.terminal_text)# thread
        print("below code not running ")

        
        self.master.mainloop()

    def create_widgets(self):
        # Upper part - Logo and Profile section
        upper_frame = ttk.Frame(self.master, padding=10)
        upper_frame.pack(side=tk.TOP, fill=tk.X)

        # Logo
        logo_image = Image.open("images/kantipur.png")
        logo_image = logo_image.resize((50, 50), Image.BILINEAR)
        self.logo = ImageTk.PhotoImage(logo_image)

        logo_label = ttk.Label(upper_frame, image=self.logo)
        logo_label.pack(side=tk.LEFT, anchor=tk.NW)

        heading_label = ttk.Label(upper_frame, text="Kantipur Social Share", font=('Arial', 18, 'bold'))
        heading_label.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

        # Profile section
        profile_frame = ttk.Frame(upper_frame, padding=0)
        profile_frame.pack(side=tk.RIGHT, anchor=tk.NE)

        # Profile image
        profile_image = Image.open("images/username_30.png")
        profile_image = profile_image.resize((50, 50), Image.BILINEAR)
        self.profile_photo = ImageTk.PhotoImage(profile_image)
        

        profile_label = ttk.Label(profile_frame, image=self.profile_photo)
        profile_label.bind("<Enter>", lambda event: self.on_hover(event, "goto profile"))
        profile_label.bind("<Leave>", self.on_leave)
        profile_label.bind("<Button-1>", self.open_browser_for_file)
        profile_label.pack()

        # print(self.user_data)
        user_name_label = ttk.Label(profile_frame, text=self.user_data['first_name'], font=('Arial', 10, 'bold'))
        user_name_label.bind("<Button-1>", self.open_browser_for_file)
        user_name_label.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(0, 0))

        # File browser and button in the center
        center_frame = ttk.Frame(self.master, padding=20)
        center_frame.pack()


        display_frame = ttk.Frame(self.master, padding=2)
        display_frame.pack()
  

        self.file_browser = ttk.Entry(display_frame, font=('Arial', 12))
        self.file_browser.pack(side=tk.LEFT, fill=tk.X, expand=True)

        second_center_frame = ttk.Frame(self.master, padding=20)
        second_center_frame.pack()

         # Initialize the style object
        self.style = ttk.Style()

        # Set the custom style for the button
        self.style.configure('Green.TButton', foreground='black', background='white', activeforeground='white', activebackground='blue', padding=10)

        # Create the button using the custom style
        generate_button = ttk.Button(second_center_frame, text="Generate", command=lambda: self.uploadFileThread(), style='Green.TButton',)
        generate_button.pack(side=tk.LEFT, padx=10 )
 


    # def start_progress(self,percentage):
     
    #     self.progress_bar["value"] = percentage
    #     self.master.update_idletasks()  # Update the GUI immediately
   
    

    def on_close_websocket(self):
        # Set the connection image to "disconnected" when WebSocket connection is closed
        
        self.connection_label.config(image=self.disconnected_logo)
        self.connection_text_label.config(text="Disconnected to server Success")
        self.disconnect_button.config(text="connect",command=lambda:self.start_websocket_client_thread(self.terminal_text))
    
    def on_open_websocket(self):
        time.sleep(1)
        # Set the connection image to "connected" when WebSocket connection is open
        self.connection_label.config(image=self.connected_logo)
        self.connection_text_label.config(text="Connected to server Success")
        self.disconnect_button.config(text="Disconnect",command=self.disconnectWebsocket)

    def disconnectWebsocket(self):
        if self.websocket_obj and self.websocket_obj.sock:
            self.websocket_obj.close()
            self.is_websocket_connected = False
            self.on_close_websocket()

            my_thread = MyThread()
            my_thread.start()

            # Let the thread run for some time (e.g., 5 seconds)
            time.sleep(1)

            # Stop the thread gracefully
            my_thread.stop()
            my_thread.join()

            self.terminal_text.insert("1.0", f"Disconnected with server !!!\n","danger")
            self.terminal_text.tag_configure("danger", foreground="red")
            print("Thread stopped.")
            
        else:
            print("WebSocket is not connected.")         
           

    def start_websocket_client_thread(self, terminal_text):
        websocket_thread = threading.Thread(target=self.start_websocket_client, args=(terminal_text,))
        websocket_thread.start()

    def start_websocket_client(self, terminal_text):
        print(terminal_text, " initial")
        # "kitSERVER5@##@d" root password
        user_name = self.user_data['username']
        print(user_name," user data email ...")
        
        websocket_client = WebSocketClient(f"{self.websocket_api}{user_name}/", terminal_text,user_name,self)
        self.on_open_websocket()
        websocket_client.connect()
        # print("\n\n",a," websocket connected md")

    def restartWebsocket(self):
        print("restarting...")
        self.terminal_text.insert("1.0", f"Reconnecting to server... !!!\n","info")
        self.terminal_text.tag_configure("info", foreground="blue")
        self.disconnectWebsocket()
        self.start_websocket_client_thread(self.terminal_text)


    def uploadFileThread(self):
        print("this is threading ...")
        generate_thread = threading.Thread(target=self.uploadFile, args=(self.terminal_text,))
        generate_thread.start()

    def uploadFile(self, terminal_text):
        import os
        from core.signed import LocalSignPdf
      
        file_path = self.selected_file
        folder_path = self.selected_folder
        # Code execution logic here

        # for file
        if self.selected_file is not None:            
            file_id = "clientSoftware"
            root = tk.Tk()
            root.withdraw()

            popup = PopupWindow(f"Request From Server {self.user_data['username']}",self,file_id)
            self.master.wait_window(popup)
            
            code = "signature is selected ::"+self.private_signature_file+"\n"
            terminal_text.insert("1.0", code,"info")
            terminal_text.tag_configure("info", foreground="blue")
            code = file_path + " is selected \n"
            
            if "signed-by-kantipur" in file_path:
                print("it is already signed")
                messagebox.showinfo("Signed Failed", f"it is already signed !!!")
            else:
                save_or_not,pdf,pdf_id= LocalSignPdf(self.user_data,file_path,self.private_signature_file)

                if save_or_not:
                    messagebox.showinfo("Signed Successful", f"signed success.please visit signed folder !!!")
            
            # self.selected_folder = None
                    
        elif folder_path is not None:      

            file_id = "clientSoftware"
            root = tk.Tk()
            root.withdraw()

            popup = PopupWindow(f"Request From Server {self.user_data['username']}",self,file_id)
            self.master.wait_window(popup)
            
            code = "signature is selected ::"+self.private_signature_file+"\n"
            terminal_text.insert("1.0", code,"info")
            terminal_text.tag_configure("info", foreground="blue")
            code = folder_path + " is selected \n"
            
            for foldername, subfolders, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_pa = os.path.join(foldername, filename)
                    print(os.path.join(foldername, filename))
                    if "signed-by-kantipur" in filename:
                        terminal_text.insert("1.0", f"{filename} already signed!!!\n", "info")
                        terminal_text.tag_configure("info", foreground="blue")
                        continue
                    save_or_not,pdf,pdf_id= LocalSignPdf(self.user_data,file_pa,self.private_signature_file)
                    if save_or_not == True:
                        terminal_text.insert("1.0", f"{filename} signed success!!!\n","success")
                        terminal_text.tag_configure("success", foreground="green")

            messagebox.showinfo("Signed Successful", f"signed success.please visit signed folder !!!")
            openFolder(folder_path)
            
        
        else:
            terminal_text.insert("1.0", "Please select a file!\n","error")
            terminal_text.tag_configure("error", foreground="red")
            messagebox.showinfo("Error Please select a file ","Error Please select a file ...!")
            return


        terminal_text.insert("1.0", code,"info")
        terminal_text.tag_configure("info", foreground="blue")
        
        

    def run_code(self, terminal_text):
        # Execute the code and capture the output
        import sys
        from io import StringIO

        # Create a stream to redirect the output
        output_stream = StringIO()
        sys.stdout = output_stream
        print('\n')
        # Execute the code
        try:
            exec(terminal_text.get("1.0", tk.TOP), globals())
        except Exception as e:
            output = str(e)
        else:
            output = ""

        # Restore the standard output and get the captured output
        sys.stdout = sys.__stdout__
        captured_output = output_stream.getvalue()

        terminal_text.insert("1.0", captured_output + output)

    def button_clicked(self):
        print("Button clicked!")

    def insert_terminal_data(self, data):
        self.terminal_text.insert("1.0", data)

    def signedSignature(self,folder_path):
        print(" signing all pdf files inside this folder...")


    def on_hover(self,event,variable_name):
        event.widget.config(cursor="hand2")  # Change the cursor to a hand pointer on hover
        # You can add other hover effect configurations here if needed

        # Show the tooltip with the variable name
        snippet_text = variable_name
        self.show_snippet_tooltip(event, snippet_text)

    def on_leave(self,event):
        event.widget.config(cursor="")  # Reset the cursor to the default on leaving
        # You can reset other hover effect configurations here if needed


    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        self.file_browser.delete(0, tk.END)
        self.file_browser.insert(0, file_path)
        self.selected_file = file_path  # Store the selected file path
        self.selected_folder = None

    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory()  # Use askdirectory() instead of askopenfilename()
        self.file_browser.delete(0, tk.END)
        self.file_browser.insert(0, folder_path)
        self.selected_folder = folder_path  # Store the selected folder path
        self.selected_file = None

    def open_browser_for_file(self,url):
        print(url,"\n")
        webbrowser.open("http://64.227.182.105:8004/") 

    def show_snippet_tooltip(self, event, snippet_text):
        print(" income snipp text \n",snippet_text)
        tooltip_window = tk.Toplevel()
        tooltip_window.overrideredirect(True)  # Hide the window decorations
        tooltip_window.geometry(f"+{event.x_root + 5}+{event.y_root + 5}")  # Position the window near the cursor
        tooltip_window.attributes('-topmost', True)  # Display the tooltip above other windows

        # Create a Label widget to display the snippet text
        snippet_label = ttk.Label(tooltip_window, text=snippet_text, background="#ffffe0", borderwidth=1, relief="solid")
        snippet_label.pack(padx=5, pady=2)

        def close_tooltip(event):
            tooltip_window.destroy()

        # Bind the close event to destroy the tooltip when the mouse leaves the image
        event.widget.bind("<Leave>", close_tooltip)

        
# DashboardGUI({'first_name':"md","email":"admin@gmail.com",'username':"aasd"})

class MyThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print("Thread is running...")

    def stop(self):
        self._stop_event.set()
