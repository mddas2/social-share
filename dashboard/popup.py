import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
from dashboard.database import Model

class PopupWindow(tk.Toplevel):
    def __init__(self, message,socket_obj,id):
        super().__init__()
        self.Model = Model()

        self.file_id = id
        self.socket_obj = socket_obj

        self.title(message)
        self.geometry("400x300")  # Increase the size of the popup window

        # Apply a specific theme to the popup window
        style = ttk.Style(self)
        style.theme_use("clam")  # Change to the desired theme name

        # Create a table-like list using Treeview
        self.table_list = ttk.Treeview(self, column=("Name",), show="headings")
        style.configure("Treeview", cellspan=lambda col: "center")
        self.table_list.heading("Name", text="Name")
       

        self.table_list.pack(expand=True, fill=tk.BOTH)

        # Create a button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Create a file upload button
        button_delete = ttk.Button(button_frame, text="Delete", command=self.button_delete)
        button_delete.pack(side=tk.LEFT, padx=10) 

        upload_button = ttk.Button(button_frame, text="Upload File", command=self.uploadFile)
        upload_button.pack(side=tk.LEFT)

        # Create a submit button
        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit)
        submit_button.pack(side=tk.LEFT, padx=10)

        self.selected_data = None
        self.fetchData()

    def fetchData(self):
        rows = self.Model.selectAll()
        # Clear existing items in the table list
        self.table_list.delete(*self.table_list.get_children())

        # Insert fetched data into the table list
    
        for row in rows:
            print(row[0]," id")
            name = row[1]
            name =  name.split('/')
            name = name[-1]
            if len(row) >= 2:  # Check if the row has at least three columns
                self.table_list.insert("", tk.END, values=(name),
                                       tags=(row[0],))  # Assuming column order: id, name, size
            else:
                print("Invalid row:", row)

        # conn.close()  # Close the connection

    def uploadFile(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.Model.create(file_path,"100kb")
            # Fetch data from the database and update the table list
            self.fetchData()

    def submit(self):
        selected_item = self.table_list.selection()
        if selected_item:
            item_tags = self.table_list.item(selected_item)['tags']
            if item_tags:
                row_id = item_tags[0]
                self.selected_data = row_id
                print("Submit button clicked")
                row = self.Model.getById(self.selected_data)
                signature_path = row[0][1]
                
                print(self.file_id,":: file id popup to blend somewhere \n")
                if self.file_id == "clientSoftware":
                    print("Selected signature file:", signature_path," send to dashboard.py obj")
                    self.socket_obj.private_signature_file = signature_path
                    self.destroy()
                    
                    #in this case self means dashboard.py obj
                else:
                    print("Selected data (ID):", self.selected_data," and File id:" ,self.file_id)                
                    self.socket_obj.send_signature(signature_path,self.file_id)
                    #in this case self means socket obj
                    self.destroy()
            else:
                print("No data selected.")
        else:
            print("No item selected.")


    def deleteRow(self, row_id):
        # Check if the item exists in the table list
        item_exists = False
        for item in self.table_list.get_children():
            if self.table_list.item(item)['tags'][0] == row_id:
                item_exists = True
                break
        
        if item_exists:
            obj = self.Model.delete(row_id)
            # Delete the row from the table list
            self.table_list.delete(item)

        else:
            print("Item not found in the table list:", row_id)

    def button_delete(self):
        selected_item = self.table_list.selection()
        if selected_item:
            item_tags = self.table_list.item(selected_item)['tags']
            if item_tags:
                row_id = item_tags[0]
                self.selected_data = row_id
                print("Submit button clicked")
                print("Selected data (ID):", self.selected_data)
                self.deleteRow(self.selected_data)
            else:
                print("No data selected.")
        else:
            print("No item selected.")
    

