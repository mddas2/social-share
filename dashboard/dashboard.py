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
        self.news_url.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.news_url.bind('<KeyRelease>', lambda event: self.FetchPortalData(event))

        self.count = ttk.Entry(display_frame, font=('Arial', 12),width=6)
        self.count.pack(side=tk.RIGHT, fill=tk.X ,expand=True)
        
        second_center_frame = ttk.Frame(self.master, padding=15)
        second_center_frame.pack()

         # Initialize the style object
        self.style = ttk.Style()

        # Set the custom style for the button
        self.style.configure('Green.TButton', foreground='black', background='white', activeforeground='white', activebackground='blue', padding=10)

        # Create the button using the custom style
        generate_button = ttk.Button(second_center_frame, text="Share", command=lambda: self.UrlGenerate(), style='Green.TButton',)
        generate_button.pack(side=tk.LEFT, padx=10 )

        fetch_display = ttk.Frame(self.master, padding=2)
        fetch_display.pack()

        self.portal_name = ttk.Label(fetch_display, text="Kantipur Infotech Sharing System", font=('Arial', 13, 'bold'),foreground='blue')
        self.portal_name.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

        seperator = ttk.Label(fetch_display, text=":", font=('Arial', 13, 'bold'),foreground='black')
        seperator.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

        portal_name = ttk.Label(fetch_display, text="count", font=('Arial', 13, 'bold'),foreground='green')
        portal_name.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=(10, 5))

    def FetchPortalData(self,event):
        url = self.news_url.get()
        portal_name,is_ok = get_site_name_with_requests(url)
        self.portal_name.configure(text=portal_name)

        if is_ok:
            get_total_shares = self.get_total_shares(url)
            self.count.configure(text = get_total_shares)
        
    def CountEvent(self,event):
        url = self.news_url.get()
        portal_name = get_site_name_with_requests(url)
        self.portal_name.configure(text=portal_name)
   
    def UrlGenerate(self):
        user_input = self.news_url.get()
        generate_thread = threading.Thread(target=self.ShareAction, args=(user_input,self.count.get()))
        generate_thread.start()

    def get_total_shares(self,url):
        # obj = SocialShare(url)
        return 10
        # return obj.getLiveTotalShare()
    
    def ShareAction(self, url,count):
        number = count.strip()
        number = int(number)
 
        obj = SocialShare(url)
        obj.IncreaseCountShare(number)
        obj.exit()

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

