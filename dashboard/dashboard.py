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
from utilities.scrap import get_site_name_with_requests
from utilities.action import SocialShare

class DashboardGUI(Api):
    def __init__(self,user_data):
   
        super().__init__()

        master = tk.Tk()

        self.desktop_path = getDesktop()

        self.user_data = user_data
        self.master = master
        self.master.title("Dashboard")
        self.master.configure(bg="#f2f2f2")
        self.master.geometry("550x300")

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
        
        self.social_share_obj = None
        self.total_share_count = '0'
        self.ok_url = ''
        self.is_share = True
        self.url_count_datasets = {}

        # self.portal_name_count_number = 0

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

        heading_label = ttk.Label(upper_frame, text="Kantipur Infotech Sharing System", font=('Arial', 18, 'bold'))
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
  

        self.news_url = ttk.Entry(display_frame, font=('Arial', 12),width=30)
        #self.news_url.insert(0, 'https://newspolar.com/archives/226068')  # Set the initial value
        self.news_url.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # self.news_url.insert(0, "Enter url")

        self.news_url.bind('<KeyRelease>', lambda event: self.FetchPortalData(event))

        self.count = ttk.Entry(display_frame, font=('Arial', 12),width=6)
        self.count.pack(side=tk.RIGHT, fill=tk.X ,expand=True)

        self.count.bind('<KeyRelease>', lambda event: self.CountEvent(event))
        # self.count.insert(0, "number")

        second_center_frame = ttk.Frame(self.master, padding=15)
        second_center_frame.pack()

         # Initialize the style object
        self.style = ttk.Style()

        # Set the custom style for the button
        self.style.configure('Green.TButton', foreground='black', background='white', activeforeground='white', activebackground='blue', padding=10)

        # Create the button using the custom style
        self.generate_button = ttk.Button(second_center_frame, text="Share", command=lambda: self.UrlGenerate(), style='Green.TButton',state='disabled')
        self.generate_button.pack(side=tk.LEFT, padx=6 )

        self.progress_bar = ttk.Progressbar(second_center_frame, mode='indeterminate', length=100)

        fetch_display = ttk.Frame(self.master, padding=2)
        fetch_display.pack()

        self.portal_name = ttk.Label(fetch_display, text="Kantipur Infotech Sharing System", font=('Arial', 13, 'bold'),foreground='blue')
        self.portal_name.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

        seperator = ttk.Label(fetch_display, text=":", font=('Arial', 13, 'bold'),foreground='black')
        seperator.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

        self.portal_name_count = ttk.Label(fetch_display, text="count", font=('Arial', 13, 'bold'),foreground='green')
        self.portal_name_count.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))
        
    def threadFetchPortalData(self,event):
        generate_thread = threading.Thread(target=self.FetchPortalData, args=(event))
        generate_thread.start()

    def FetchPortalData(self,event):
        url = self.news_url.get()
        url = url.strip()
        is_ok = False
        if url != self.ok_url:
            portal_name,is_ok = get_site_name_with_requests(url)
            self.portal_name.configure(text=portal_name)
        
        if is_ok and self.is_share == True:
            self.url_count_datasets[url] = 0
            self.start_busy()
            self.ok_url = url.strip()
            generate_thread = threading.Thread(target=self.get_total_shares, args=(url,))
            generate_thread.start()
        else:
            print("not ok")
            # self.generate_button['state'] = 'disabled'
            # self.social_share_obj = None
        
    def CountEvent(self,event):
        total_share_count = str(self.total_share_count) + '+' + self.count.get()
        self.portal_name_count.configure(text = total_share_count)

    def get_total_shares(self,url):
        obj = SocialShare(url)
        self.social_share_obj = obj
        total_share= obj.getLiveTotalShare()
        try:
            total_share = int(total_share)
        except:
            total_share = 0

        # print(total_share, " total live shares" )
        self.total_share_count = total_share
        self.portal_name_count.configure(text = total_share)
        self.stop_busy()

    def UrlGenerate(self):
        self.start_busy()
        self.is_share = False
        user_input = self.news_url.get()
        print(user_input, " clicking  ...")
        generate_thread = threading.Thread(target=self.ShareAction, args=(user_input,self.count.get()))
        generate_thread.start()
    
    def ShareAction(self, url,count):
        try:
            number = count.strip()
            number = int(number)
        except:
            number = 10

        obj = self.social_share_obj
        # print("obj:" , obj)
        obj.IncreaseCountShare(number)
        self.stop_busy()
        # obj.exit()
        self.is_share = True

        self.url_count_datasets[url] = self.url_count_datasets[url] + number
        total = self.url_count_datasets[url]  + int(self.total_share_count)

        self.portal_name_count.configure(text=str(total))


    def button_clicked(self):
        print("Button clicked!")

    def on_hover(self,event,variable_name):
        event.widget.config(cursor="hand2")  # Change the cursor to a hand pointer on hover
        # You can add other hover effect configurations here if needed

        # Show the tooltip with the variable name
        snippet_text = variable_name
        self.show_snippet_tooltip(event, snippet_text)

    def on_leave(self,event):
        event.widget.config(cursor="")  # Reset the cursor to the default on leaving
        # You can reset other hover effect configurations here if needed


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

    def start_busy(self):
        # Disable the button
        self.generate_button['state'] = 'disabled'

        # Place the progress bar next to the button
        self.progress_bar.place(in_=self.generate_button, relx=1.05, rely=-0.1, anchor='ne')

        # Start the progress bar animation in a separate thread
        threading.Thread(target=self.animate_progress_bar).start()

        # Simulate some time-consuming task (replace this with your actual task)

        # Stop the progress bar and enable the button after the task is done


    def animate_progress_bar(self):
        # Start the progress bar animation
        self.progress_bar.start()

    def stop_busy(self):
        # Stop the progress bar animation
        self.progress_bar.stop()

        # Enable the button
        self.generate_button['state'] = 'normal'

        # Remove the progress bar
        self.progress_bar.place_forget()
