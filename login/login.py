import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from tkinter import font
from login import auth


class LoginGUI:
    def __init__(self, master):

        self.master = master
        self.master.title("Login")
        self.master.configure(bg="#f2f2f2")
        self.master.geometry("550x550")

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12), background="#f2f2f2")
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))

        # Load custom font for the header label
        font_path = os.path.join("fonts", "Roboto-Bold.ttf")
        self.custom_font = font.Font(family="Roboto", size=20, weight="bold")
        self.master.option_add("*TLabel.font", self.custom_font)

        # Create header label with updated style
        header_label = ttk.Label(
            self.master,
            text="Kantipur Infotech Sharing System",
            font=self.custom_font,
            background="#f2f2f2",
            foreground="#333333"  # Custom header text color
        )
        header_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Load and resize the logo image
        logo_image = Image.open("images/kantipur.png")
        logo_image = logo_image.resize((125, 125), Image.BILINEAR)
        self.logo_image = ImageTk.PhotoImage(logo_image)

        logo_label = ttk.Label(self.master, image=self.logo_image, background="#f2f2f2")
        logo_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.frame = ttk.Frame(self.master, padding=20)
        self.frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Load and resize the username and password images
        username_image = Image.open("images/username_30.png")
        username_image = username_image.resize((24, 24), Image.BILINEAR)
        self.username_image = ImageTk.PhotoImage(username_image)

        password_image = Image.open("images/password_30.png")
        password_image = password_image.resize((24, 24), Image.BILINEAR)
        self.password_image = ImageTk.PhotoImage(password_image)

        self.username_label = ttk.Label(self.frame, image=self.username_image, background="#f2f2f2")
        self.username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.username_entry = ttk.Entry(self.frame, font=('Arial', 12))
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.username_entry.insert(0, "Enter username")

        self.password_label = ttk.Label(self.frame, image=self.password_image, background="#f2f2f2")
        self.password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.password_entry = ttk.Entry(self.frame, show="*", font=('Arial', 12))
        self.password_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        self.password_entry.insert(0, "Enter password")

        self.login_button = tk.Button(
            self.frame,
            text="Login",
            command=self.login,
            font=('Arial', 12, 'bold'),
            bg="#4CAF50",
            fg="white",
            activebackground="#45A049",
            activeforeground="white"
        )
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.username_entry.bind("<FocusIn>", self.clear_entry)
        self.username_entry.bind("<FocusOut>", self.restore_entry)
        self.password_entry.bind("<FocusIn>", self.clear_entry)
        self.password_entry.bind("<FocusOut>", self.restore_entry)

        self.username_entry.focus()

        # Custom style for the login button
        self.style.configure(
            "Custom.TButton",
            font=('Arial', 12),
            background="#4CAF50",
            foreground="white",
            padding=10,
            width=15
        )

    def clear_entry(self, event):
        entry = event.widget
        if entry.get() == "Enter username" or entry.get() == "Enter password":
            entry.delete(0, tk.END)

    def restore_entry(self, event):
        entry = event.widget
        if entry.get() == "":
            if entry == self.username_entry:
                entry.insert(0, "Enter username")
            else:
                entry.insert(0, "Enter password")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_obj = auth.Login(username,password)
        login = login_obj.login()
        # Check if the username and password are correct
        if login['status'] == True:
            name = login['data']['first_name']
            print(login['data'],"...login data")
            # messagebox.showinfo("Login Successful", f"Welcome, {name}!")
            self.open_dashboard(login['data'])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def open_dashboard(self,user_data):
        self.master.destroy()  # Close the login window
        from dashboard.dashboard import DashboardGUI 

        DashboardGUI(user_data)  # Create an instance of the DashboardGUI class


# Create the main window
window = tk.Tk()
window.title("Login")
window.configure(bg="#f2f2f2")
window.geometry("600x600")

# Set window icon
window.iconbitmap("images/kantipur.ico")

# Create an instance of the LoginGUI class
login_gui = LoginGUI(window)

# Run the main window's event loop
window.mainloop()
