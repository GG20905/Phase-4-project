#To access the project in order to run it Cd into Lib then run python3 main.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.db = Database()
        self.treeview = tk.ttk.Treeview(self.root)
        self.treeview.pack()
        self.create_treeview()
        self.create_widgets()

    def create_treeview(self):
        self.treeview["columns"] = ("Name", "Age", "Grade")
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Name", anchor=tk.W, width=120)
        self.treeview.column("Age", anchor=tk.W, width=50)
        self.treeview.column("Grade", anchor=tk.W, width=50)
        self.treeview.heading("#0", text="", anchor=tk.W)
        self.treeview.heading("Name", text="Name", anchor=tk.W)
        self.treeview.heading("Age", text="Age", anchor=tk.W)
        self.treeview.heading("Grade", text="Grade", anchor=tk.W)

    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        add_button = tk.Button(button_frame, text="Add Student", command=self.add_student)
        add_button.pack(side=tk.LEFT)

        edit_button = tk.Button(button_frame, text="Edit Student", command=self.edit_student)
        edit_button.pack(side=tk.LEFT)

        delete_button = tk.Button(button_frame, text="Delete Student", command=self.delete_student)
        delete_button.pack(side=tk.LEFT)

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter student name (or press cancel to cancel):")
        
        if name is None:
            return
        
        age = simpledialog.askinteger("Add Student", "Enter student age (or press cancel to cancel):")
        
        if age is None:
            return
        
        grade = simpledialog.askinteger("Add Student", "Enter student grade (or press cancel to cancel):")
        
        if grade is None:
            return
        
        db = Database()
        
        db.add_student(name, age, grade)
        
        # Add the new student to the treeview
        self.treeview.insert("", "end", values=(name, age, grade))

    def edit_student(self):
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            name = self.treeview.item(selected_item, "values")[0]
            
            # Ask the user for new values
            new_age = simpledialog.askinteger("Edit Student", "Enter new age (or press cancel to cancel):")
            
            if new_age is None:
                return
            
            new_grade = simpledialog.askinteger("Edit Student", "Enter new grade (or press cancel to cancel):")
            
            if new_grade is None:
                return
            
            db = Database()
            
            if new_age is not None or new_grade is not None:
                db.edit_student(name, new_age, new_grade)
                
                # Update the selected student in the treeview
                self.treeview.item(selected_item, values=(name, new_age, new_grade))
        else:
            tk.messagebox.showinfo("No item selected", "Please select an item from the treeview.")

    def delete_student(self):
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            name = self.treeview.item(selected_item, "values")[0]
            
            # Ask the user to confirm deletion
            response = tk.messagebox.askokcancel("Delete Student", f"Are you sure you want to delete {name}?")
            
            if response:
                db = Database()
                db.delete_student(name)
                self.treeview.delete(selected_item)
        else:
            tk.messagebox.showinfo("No item selected", "Please select an item from the treeview.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)  # Pass the root argument to the App class
    root.mainloop()
