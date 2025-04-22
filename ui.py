'''from imsdatabase import *'''
from stockdatabase import *
from projectdatabase import *
from logdatabase import*
from productdatabase import *
from userdatabase import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import font
import sqlite3
import openpyxl
from openpyxl import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import filedialog
import pandas as pd
import random
import shutil
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
wb_bill = openpyxl.load_workbook('Inventory Management System.xlsx')
sheet_bill=wb_bill["Bill Sheet"]
wb = openpyxl.load_workbook('Order Stock.xlsx')
sheet = wb["Order Stock"]
global IMS 
#ttkbotstrap config
root=ttkb.Window(themename="darkly")
root.title("Inventory Management System")
root.geometry("960x540")
root.resizable(False,False)

def login():
    def clear(event=None):
        for widget in root.winfo_children():
            widget.destroy()
    clear()
    def check():
        if check_login(username_entry.get(),password_entry.get()):
            mainscreen()
        else:
            tkmb.showerror("Error","Invalid Username or Password")

    def register():
        register_window = ttkb.Toplevel(root)
        register_window.title("Register")
        register_window.geometry("400x400")
        register_window.resizable(False,False)
        register_frame = ttkb.Frame(register_window)
        register_frame.pack(pady=30)
        username_label = ttkb.Label(register_frame,text="Username")
        username_label.grid(row=0,column=0,padx=10,pady=10)
        username_entry = ttkb.Entry(register_frame)
        username_entry.grid(row=0,column=1,padx=10,pady=10)
        password_label = ttkb.Label(register_frame,text="Password")
        password_label.grid(row=1,column=0,padx=10,pady=10)
        password_entry = ttkb.Entry(register_frame,show="*")
        password_entry.grid(row=1,column=1,padx=10,pady=10)
        email_label = ttkb.Label(register_frame,text="Email")
        email_label.grid(row=2,column=0,padx=10,pady=10)
        email_entry = ttkb.Entry(register_frame)
        email_entry.grid(row=2,column=1,padx=10,pady=10)
        phone_label = ttkb.Label(register_frame,text="Phone")
        phone_label.grid(row=3,column=0,padx=10,pady=10)
        phone_entry = ttkb.Entry(register_frame)
        phone_entry.grid(row=3,column=1,padx=10,pady=10)
        register_button = ttkb.Button(register_frame,text="Register",command=lambda:new_user(username_entry.get(),password_entry.get(),email_entry.get(),phone_entry.get(),"user"))
        register_button.grid(row=4,column=1,padx=10,pady=10)

    mainlabel = ttkb.Label(root,text="Enertect Inventory Management System",font=(DEFAULT,30))  
    mainlabel.pack(pady=50)
    loginframe = ttkb.Frame(root)
    loginframe.pack(pady=30)
    username_label = ttkb.Label(loginframe,text="Username")
    username_label.grid(row=0,column=0,padx=10,pady=10)
    username_entry = ttkb.Entry(loginframe)
    username_entry.grid(row=0,column=1,padx=10,pady=10)
    password_label = ttkb.Label(loginframe,text="Password")
    password_label.grid(row=1,column=0,padx=10,pady=10)
    password_entry = ttkb.Entry(loginframe,show="*")
    password_entry.grid(row=1,column=1,padx=10,pady=10)
    login_button = ttkb.Button(loginframe,text="Login",command=check)
    login_button.grid(row=2,column=1,padx=10,pady=10)
    register_button = ttkb.Button(loginframe,text="Register",command=register)
    register_button.grid(row=2,column=0,padx=10,pady=10)
    root.bind("<Return>",mainscreen)


def mainscreen(event=None):
    
    def clear(event=None):
        for widget in root.winfo_children():
            if widget != menubar:
                widget.destroy()
    
    def menubar():
        menubar = tk.Menu(root)
        stock_menu = tk.Menu(menubar, tearoff=0)
        stock_menu.add_command(label="New", command=lambda: add_tab("New Stock"))
        stock_menu.add_command(label="Add", command=lambda: add_tab("Add Stock"))
        stock_menu.add_command(label="Withdraw", command=lambda: add_tab("Withdraw Stock"))
        stock_menu.add_command(label="Search", command=lambda: add_tab("Search Stock"))
        stock_menu.add_command(label="Update", command=lambda: add_tab("Update Stock"))
        stock_menu.add_command(label="Delete", command=lambda: add_tab("Delete Stock"))
        menubar.add_cascade(label="Stock", menu=stock_menu)    
        product_menu = tk.Menu(menubar, tearoff=0)
        product_menu.add_command(label="New", command=lambda: add_tab("New Product"))
        product_menu.add_command(label="Edit", command=lambda: add_tab("Edit Product"))
        product_menu.add_command(label="Delete", command=lambda: add_tab("Delete Product"))
        product_menu.add_command(label="Search", command=lambda: add_tab("Search Product"))
        menubar.add_cascade(label="Product", menu=product_menu)    
        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="New", command=lambda: add_tab("New Project"))
        project_menu.add_command(label="Edit", command=lambda: add_tab("Edit Project"))
        project_menu.add_command(label="Delete", command=lambda: add_tab("Delete Project"))
        project_menu.add_command(label="Search", command=lambda: add_tab("Search Project"))
        menubar.add_cascade(label="Project", menu=project_menu)    
        users_menu = tk.Menu(menubar, tearoff=0)
        users_menu.add_command(label="Edit Role", command=lambda: add_tab("Edit Role"))
        users_menu.add_command(label="Delete", command=lambda: add_tab("Delete User"))
        users_menu.add_command(label="Search", command=lambda: add_tab("Search User"))
        users_menu.add_separator()
        users_menu.add_command(label="Logout", command=login)
        menubar.add_cascade(label="User", menu=users_menu)    
        root.config(menu=menubar)

    root.bind("<Escape>", clear)
    clear()    
    notebook = ttkb.Notebook(root)
    notebook.pack(fill="both", expand=True)
    menubar()
    
    def add_tab(tab_name):
        frame = ttkb.Frame(notebook)
        notebook.add(frame, text=tab_name)
        if tab_name == "New Stock":
            new_stock(frame,notebook)
        elif tab_name == "Add Stock":
            add_stock(frame,notebook)
        elif tab_name == "Withdraw Stock":
            withdraw_stock(frame,notebook)
        elif tab_name == "Search Stock":
            search_stock(frame,notebook)
        elif tab_name == "Update Stock":
            update_stock(frame,notebook)
        elif tab_name == "Delete Stock":
            delete_stock(frame,notebook)
        elif tab_name == "New Product":
            new_product(frame,notebook)
        elif tab_name == "Edit Product":
            edit_product(frame,notebook)
        elif tab_name == "Delete Product":
            delete_product(frame,notebook)
        elif tab_name == "Search Product":
            search_product(frame,notebook)
        elif tab_name == "New Project":
            new_project(frame,notebook)
        elif tab_name == "Edit Project":
            edit_project(frame,notebook)
        elif tab_name == "Delete Project":
            delete_project(frame,notebook)
        elif tab_name == "Search Project":
            search_project(frame,notebook)
        elif tab_name == "Edit Role":
            edit_role(frame,notebook)
        elif tab_name == "Delete User":
            delete_user(frame,notebook)
        elif tab_name == "Search User":
            search_user(frame,notebook)

def new_stock(frame,notebook):
    def close():
        if save_stock_itemname.get() or save_stock_quantity.get() or save_stock_unit.get() or save_stock_minqty.get():
            if tkmb.askyesno("Unsaved Changes","Do u want to close without saving"):
                notebook.forget(frame)
        else:
            notebook.forget(frame)
    
    def generate_random_code():
        random_code = random.randint(100000, 999999)
        check_code = get_stock_by_id(random_code)
        if check_code:
            generate_random_code()
        else:
            save_stock_id.delete(0, tk.END)
            save_stock_id.insert(0, random_code)
    
    def generate_random_code_upload():
        random_code = random.randint(100000, 999999)
        check_code = get_stock_by_id(random_code)
        if check_code:
            generate_random_code()
        else:
            return random_code     
            
    def add_to_tree():
        if save_stock_itemname.get() and save_stock_quantity.get() and save_stock_unit.get() and save_stock_minqty.get():
            check_stock_itemname = get_stock_by_itemname(save_stock_itemname.get())
            if check_stock_itemname:
                tkmb.showerror("Error", "Item Already In Table")
            else:
                for child in stock_tree.get_children():
                    if stock_tree.item(child, 'values')[1] == save_stock_itemname.get():
                        tkmb.showerror("Error", "Item Already In Table")
                        return
            stock_tree.insert("", "end", values=(save_stock_id.get(), save_stock_itemname.get(), save_stock_quantity.get(), save_stock_unit.get(), save_stock_minqty.get()))
        else:
            tkmb.showerror("Error", "All Fields Are Required")

    def download_template():
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            shutil.copy('add_stock_template.xlsx', file_path)
            tkmb.showinfo(title="Template Downloaded", message="Edit the template and upload it to add stock.")
        else:
            tkmb.showwarning(title="Download Cancelled", message="Download operation was cancelled")
    
    def upload_stock(): 
        file_path = filedialog.askopenfilename(title="Select file", filetypes=[("Excel files", "*.xlsx")]) 
        if file_path: 
            try:
                df = pd.read_excel(file_path)
                for index, row in df.iterrows():
                    item_exists = False
                    for child in stock_tree.get_children():
                        if stock_tree.item(child, 'values')[1] == row['Item Name']:
                            item_exists = True
                            break
                    if item_exists:
                        tkmb.showerror("Error", f"Item {row['Item Name']} already exists in the stock table.")
                    else:
                        id = generate_random_code_upload()
                        itemname = row['Item Name']
                        unit = row['Unit']
                        quantity = row['Quantity']
                        minimumquantity = row['Minimum Quantity']
                        stock_tree.insert("", "end", values=(id, itemname, unit, quantity, minimumquantity))
                tkmb.showinfo("Success", "Stock added successfully.") 
            except Exception as e:
                tkmb.showerror("Error", f"Upload does not match template. Download template and try again. Error: {e}")
        else: 
            tkmb.showerror("Error", "No file selected.") 
    
    def on_row_double_click(event):
        selected_item = stock_tree.selection()[0]
        values = stock_tree.item(selected_item, "values")
        edit_window = ttkb.Toplevel(root)
        edit_window.title("Edit Stock")
        edit_window.geometry("300x300")
        edit_window.resizable(False, False)
        stock_id_label = ttkb.Label(edit_window, text="Stock ID :-")
        stock_id_label.grid(row=0, column=0, padx=10, pady=10)
        stock_id_entry = ttkb.Entry(edit_window)
        stock_id_entry.grid(row=0, column=1, padx=10, pady=10)
        stock_id_entry.insert(0, values[0])
        stock_id_entry.config(state="readonly")
        item_name_label = ttkb.Label(edit_window, text="Item Name :-")
        item_name_label.grid(row=1, column=0, padx=10, pady=10)
        item_name_entry = ttkb.Entry(edit_window)
        item_name_entry.grid(row=1, column=1, padx=10, pady=10)
        item_name_entry.insert(0, values[1])
        quantity_label = ttkb.Label(edit_window, text="Quantity :-")
        quantity_label.grid(row=2, column=0, padx=10, pady=10)
        quantity_entry = ttkb.Entry(edit_window)
        quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        quantity_entry.insert(0, values[2])
        unit_label = ttkb.Label(edit_window, text="Unit :-")
        unit_label.grid(row=3, column=0, padx=10, pady=10)
        unit_entry = ttkb.Entry(edit_window)
        unit_entry.grid(row=3, column=1, padx=10, pady=10)
        unit_entry.insert(0, values[3])
        min_qty_label = ttkb.Label(edit_window, text="Minimum Quantity :-")
        min_qty_label.grid(row=4, column=0, padx=10, pady=10)
        min_qty_entry = ttkb.Entry(edit_window)
        min_qty_entry.grid(row=4, column=1, padx=10, pady=10)
        min_qty_entry.insert(0, values[4])
        def save_changes():
            check_code = get_stock_by_id(stock_id_entry.get())
            id_exists_in_tree = any(stock_tree.item(child, 'values')[0] == stock_id_entry.get() for child in stock_tree.get_children())
            if check_code or id_exists_in_tree:
                tkmb.showerror("Error", "Id already exists, Changing to random Id.")
                id = generate_random_code_upload()
                stock_tree.item(selected_item, values=(id, item_name_entry.get(), quantity_entry.get(), unit_entry.get(), min_qty_entry.get()))
            else:
                stock_tree.item(selected_item, values=(stock_id_entry.get(), item_name_entry.get(), quantity_entry.get(), unit_entry.get(), min_qty_entry.get()))
            edit_window.destroy()
        def delete_row():
            stock_tree.delete(selected_item)
            edit_window.destroy()
        save_button = ttkb.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=5, column=0, padx=10, pady=10)
        delete_button = ttkb.Button(edit_window, text="Delete", command=delete_row)
        delete_button.grid(row=5, column=1, padx=10, pady=10)

    close_button = ttkb.Button(frame, text="X", command=close,bootstyle="danger")
    close_button.place(x=925, y=0)
    stock_id_label = ttkb.Label(frame, text="Stock ID :-")
    stock_id_label.grid(row=0, column=0, padx=10, pady=10)
    save_stock_id = ttkb.Entry(frame)
    save_stock_id.grid(row=0, column=1, padx=10, pady=10)
    generate_random_code()
    item_name_label = ttkb.Label(frame, text="Item Name :-")
    item_name_label.grid(row=1, column=0, padx=10, pady=10)
    save_stock_itemname = ttkb.Entry(frame)
    save_stock_itemname.grid(row=1, column=1, padx=10, pady=10)
    quantity_label = ttkb.Label(frame, text="Quantity :-")
    quantity_label.grid(row=2, column=0, padx=10, pady=10)
    save_stock_quantity = ttkb.Entry(frame)
    save_stock_quantity.grid(row=2, column=1, padx=10, pady=10)
    unit_label = ttkb.Label(frame, text="Unit :-")
    unit_label.grid(row=3, column=0, padx=10, pady=10)
    save_stock_unit = ttkb.Entry(frame)
    save_stock_unit.grid(row=3, column=1, padx=10, pady=10)
    min_qty_label = ttkb.Label(frame, text="Minimum Quantity :-")
    min_qty_label.grid(row=4, column=0, padx=10, pady=10)
    save_stock_minqty = ttkb.Entry(frame)
    save_stock_minqty.grid(row=4, column=1, padx=10, pady=10)
    add_stock_button = ttkb.Button(frame, text="Add",command=add_to_tree)
    add_stock_button.grid(row=5, column=1, padx=10, pady=10)
    download_template_button = ttkb.Button(frame, text="Download Template",command=download_template)
    download_template_button.grid(row=5, column=2, padx=10, pady=10)
    upload_button = ttkb.Button(frame, text="Upload Stock",command=upload_stock)
    upload_button.grid(row=5, column=3, padx=10, pady=10)
    save_stock_button = ttkb.Button(frame, text="Save",command=add_to_tree)
    save_stock_button.grid(row=5, column=4, padx=10, pady=10)
    tree_frame = ttkb.Frame(frame)
    tree_frame.grid(row=0, column=2, columnspan=3, rowspan=6, padx=10, pady=10)
    stock_tree = ttkb.Treeview(tree_frame, columns=("Stock ID", "Item Name", "Quantity", "Unit", "Minimum Quantity"))
    stock_tree.heading("#0", text="", anchor="center")
    stock_tree.heading("#1", text="Stock ID", anchor="center")
    stock_tree.heading("#2", text="Item Name", anchor="center")
    stock_tree.heading("#3", text="Quantity", anchor="center")
    stock_tree.heading("#4", text="Unit", anchor="center")
    stock_tree.heading("#5", text="Minimum Quantity", anchor="center")
    stock_tree.column("#0", width=0, stretch=tk.NO)
    stock_tree.column("#1", width=100, anchor="center")
    stock_tree.column("#2", width=150, anchor="center")
    stock_tree.column("#3", width=100, anchor="center")
    stock_tree.column("#4", width=100, anchor="center")
    stock_tree.column("#5", width=150, anchor="center")
    stock_tree.pack()
    stock_tree.bind("<Double-1>", on_row_double_click)   

def add_stock(frame,notebook):
    stock_label = ttkb.Label(frame, text="Item Name")
    stock_label.grid(row=0, column=0, padx=10, pady=10)
    stock_entry = ttkb.Entry(frame)
    stock_entry.grid(row=0, column=1, padx=10, pady=10)
    stock_quantity_label = ttkb.Label(frame, text="Quantity")
    stock_quantity_label.grid(row=1, column=0, padx=10, pady=10)
    stock_quantity_entry = ttkb.Entry(frame)
    stock_quantity_entry.grid(row=1, column=1, padx=10, pady=10)
    add_button = ttkb.Button(frame, text="Add")
    add_button.grid(row=2, column=1, padx=10, pady=10)
    tree_frame = ttkb.Frame(frame)
    tree_frame.grid(row=0, column=3, rowspan=3, padx=10, pady=10)
    stock_tree = ttkb.Treeview(tree_frame, columns=("Item Name", "Quantity"))
    stock_tree.heading("#0", text="ID", anchor="center")
    stock_tree.heading("#1", text="Item Name", anchor="center")
    stock_tree.heading("#2", text="Quantity", anchor="center")
    stock_tree.column("#0", width=50, anchor="center")
    stock_tree.column("#1", width=150, anchor="center")
    stock_tree.column("#2", width=100, anchor="center")
    stock_tree.pack()

def withdraw_stock(frame,notebook):
    stock_label = ttkb.Label(frame,text="Stock")
    stock_label.grid(row=0,column=0,padx=10,pady=10)
    stock_entry = ttkb.Entry(frame)
    stock_entry.grid(row=0,column=1,padx=10,pady=10)
    stock_quantity_label = ttkb.Label(frame,text="Quantity")
    stock_quantity_label.grid(row=1,column=0,padx=10,pady=10)
    stock_quantity_entry = ttkb.Entry(frame)
    stock_quantity_entry.grid(row=1,column=1,padx=10,pady=10)
    add_button = ttkb.Button(frame,text="Add")
    add_button.grid(row=2,column=1,padx=10,pady=10)

def search_stock(frame,notebook):
    stock_label = ttkb.Label(frame,text="Stock")
    stock_label.grid(row=0,column=0,padx=10,pady=10)
    stock_entry = ttkb.Entry(frame)
    stock_entry.grid(row=0,column=1,padx=10,pady=10)
    search_button = ttkb.Button(frame,text="Search")
    search_button.grid(row=1,column=1,padx=10,pady=10)

def update_stock(frame,notebook):
    stock_label = ttkb.Label(frame,text="Stock")
    stock_label.grid(row=0,column=0,padx=10,pady=10)
    stock_entry = ttkb.Entry(frame)
    stock_entry.grid(row=0,column=1,padx=10,pady=10)
    stock_quantity_label = ttkb.Label(frame,text="Quantity")
    stock_quantity_label.grid(row=1,column=0,padx=10,pady=10)
    stock_quantity_entry = ttkb.Entry(frame)
    stock_quantity_entry.grid(row=1,column=1,padx=10,pady=10)
    update_button = ttkb.Button(frame,text="Update")
    update_button.grid(row=2,column=1,padx=10,pady=10)

def delete_stock(frame,notebook):
    stock_label = ttkb.Label(frame,text="Stock")
    stock_label.grid(row=0,column=0,padx=10,pady=10)
    stock_entry = ttkb.Entry(frame)
    stock_entry.grid(row=0,column=1,padx=10,pady=10)
    delete_button = ttkb.Button(frame,text="Delete")
    delete_button.grid(row=1,column=1,padx=10,pady=10)
    
def new_product(frame,notebook):
    product_label = ttkb.Label(frame,text="Product")
    product_label.grid(row=0,column=0,padx=10,pady=10)
    product_entry = ttkb.Entry(frame)
    product_entry.grid(row=0,column=1,padx=10,pady=10)
    product_description_label = ttkb.Label(frame,text="Description")
    product_description_label.grid(row=1,column=0,padx=10,pady=10)
    product_description_entry = ttkb.Entry(frame)
    product_description_entry.grid(row=1,column=1,padx=10,pady=10)
    add_button = ttkb.Button(frame,text="Add")
    add_button.grid(row=2,column=1,padx=10,pady=10)

def edit_product(frame,notebook):
    product_label = ttkb.Label(frame,text="Product")
    product_label.grid(row=0,column=0,padx=10,pady=10)
    product_entry = ttkb.Entry(frame)
    product_entry.grid(row=0,column=1,padx=10,pady=10)
    product_description_label = ttkb.Label(frame,text="Description")
    product_description_label.grid(row=1,column=0,padx=10,pady=10)
    product_description_entry = ttkb.Entry(frame)
    product_description_entry.grid(row=1,column=1,padx=10,pady=10)
    update_button = ttkb.Button(frame,text="Update")
    update_button.grid(row=2,column=1,padx=10,pady=10)

def delete_product(frame,notebook):
    product_label = ttkb.Label(frame,text="Product")
    product_label.grid(row=0,column=0,padx=10,pady=10)
    product_entry = ttkb.Entry(frame)
    product_entry.grid(row=0,column=1,padx=10,pady=10)
    delete_button = ttkb.Button(frame,text="Delete")
    delete_button.grid(row=1,column=1,padx=10,pady=10)

def search_product(frame,notebook):
    product_label = ttkb.Label(frame,text="Product")
    product_label.grid(row=0,column=0,padx=10,pady=10)
    product_entry = ttkb.Entry(frame)
    product_entry.grid(row=0,column=1,padx=10,pady=10)
    search_button = ttkb.Button(frame,text="Search")
    search_button.grid(row=1,column=1,padx=10,pady=10)

def new_project(frame,notebook):
    project_label = ttkb.Label(frame,text="Project")
    project_label.grid(row=0,column=0,padx=10,pady=10)
    project_entry = ttkb.Entry(frame)
    project_entry.grid(row=0,column=1,padx=10,pady=10)
    project_description_label = ttkb.Label(frame,text="Description")
    project_description_label.grid(row=1,column=0,padx=10,pady=10)
    project_description_entry = ttkb.Entry(frame)
    project_description_entry.grid(row=1,column=1,padx=10,pady=10)
    add_button = ttkb.Button(frame,text="Add")
    add_button.grid(row=2,column=1,padx=10,pady=10)

def edit_project(frame,notebook):
    project_label = ttkb.Label(frame,text="Project")
    project_label.grid(row=0,column=0,padx=10,pady=10)
    project_entry = ttkb.Entry(frame)
    project_entry.grid(row=0,column=1,padx=10,pady=10)
    project_description_label = ttkb.Label(frame,text="Description")
    project_description_label.grid(row=1,column=0,padx=10,pady=10)
    project_description_entry = ttkb.Entry(frame)
    project_description_entry.grid(row=1,column=1,padx=10,pady=10)
    update_button = ttkb.Button(frame,text="Update")
    update_button.grid(row=2,column=1,padx=10,pady=10)

def delete_project(frame,notebook):
    project_label = ttkb.Label(frame,text="Project")
    project_label.grid(row=0,column=0,padx=10,pady=10)
    project_entry = ttkb.Entry(frame)
    project_entry.grid(row=0,column=1,padx=10,pady=10)
    delete_button = ttkb.Button(frame,text="Delete")
    delete_button.grid(row=1,column=1,padx=10,pady=10)

def search_project(frame,notebook):
    project_label = ttkb.Label(frame,text="Project")
    project_label.grid(row=0,column=0,padx=10,pady=10)
    project_entry = ttkb.Entry(frame)
    project_entry.grid(row=0,column=1,padx=10,pady=10)
    search_button = ttkb.Button(frame,text="Search")
    search_button.grid(row=1,column=1,padx=10,pady=10)

def edit_role(frame,notebook):
    user_label = ttkb.Label(frame,text="User")
    user_label.grid(row=0,column=0,padx=10,pady=10)
    user_entry = ttkb.Entry(frame)
    user_entry.grid(row=0,column=1,padx=10,pady=10)
    role_label = ttkb.Label(frame,text="Role")
    role_label.grid(row=1,column=0,padx=10,pady=10)
    role_entry = ttkb.Entry(frame)
    role_entry.grid(row=1,column=1,padx=10,pady=10)
    update_button = ttkb.Button(frame,text="Update")
    update_button.grid(row=2,column=1,padx=10,pady=10)

def delete_user(frame,notebook):
    user_label = ttkb.Label(frame,text="User")
    user_label.grid(row=0,column=0,padx=10,pady=10)
    user_entry = ttkb.Entry(frame)
    user_entry.grid(row=0,column=1,padx=10,pady=10)
    delete_button = ttkb.Button(frame,text="Delete")
    delete_button.grid(row=1,column=1,padx=10,pady=10)

def search_user(frame,notebook):
    user_label = ttkb.Label(frame,text="User")
    user_label.grid(row=0,column=0,padx=10,pady=10)
    user_entry = ttkb.Entry(frame)
    user_entry.grid(row=0,column=1,padx=10,pady=10)
    search_button = ttkb.Button(frame,text="Search")
    search_button.grid(row=1,column=1,padx=10,pady=10)

login()
root.mainloop()
