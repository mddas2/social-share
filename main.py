from update.update import Update
import sys
import tkinter as tk
from tkinter import ttk,messagebox
import time

import tkinter as tk
from tkinter import ttk
import time

def start_progress(percentage):
    # print(percentage)
    progress_var.set(percentage)
    progress.update()
    # progress_var.set(0)

# Create the main window
root = tk.Tk()
root.title("Updating...")
root.iconbitmap("images/kantipur.ico")
# root.geometry("655x560")  # Set the initial geometry of the window

# Create a progress bar
progress_var = tk.IntVar()
progress = ttk.Progressbar(root, variable=progress_var, maximum=100,length=400)
progress.pack(pady=20)

def run_update_in_thread():
    update_class_obj = Update()
    action = update_class_obj.main(start_progress)
    if action == False:
        sys.exit()
    else:
        root.destroy()
        from login import login

# Create a button to start progress simulation
start_button = tk.Button(root, text="Check Update", command=run_update_in_thread)
start_button.pack()

# Start the main event loop
root.mainloop()


