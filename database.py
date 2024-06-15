import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                name TEXT,
                age INTEGER,
                grade INTEGER
            )
        ''')
        self.conn.commit()

    def add_student(self, name, age, grade):
        query = 'INSERT INTO students VALUES (?, ?, ?)'
        self.cursor.execute(query, (name, age, grade))
        self.conn.commit()

    def edit_student(self, name, age, grade):
        query = 'UPDATE students SET age = ?, grade = ? WHERE name = ?'
        self.cursor.execute(query, (age, grade, name))
        self.conn.commit()

    def delete_student(self, name):
        query = 'DELETE FROM students WHERE name = ?'
        self.cursor.execute(query, (name,))
        self.conn.commit()

    def search_students(self, search_term):
        query = 'SELECT * FROM students WHERE name LIKE ?'
        self.cursor.execute(query, ('%' + search_term + '%',))
        return self.cursor.fetchall()

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Database")
        self.root.geometry("500x300")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.treeview = ttk.Treeview(frame, columns=("Name", "Age", "Grade"), show="headings")
        self.treeview.column("Name", anchor="w")
        self.treeview.column("Age", anchor="w")
        self.treeview.column("Grade", anchor="w")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Age", text="Age")
        self.treeview.heading("Grade", text="Grade")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        add_button = tk.Button(self.root, text="Add Student", command=self.add_student)
        add_button.pack(fill=tk.X)

        edit_button = tk.Button(self.root, text="Edit Student", command=self.edit_student)
        edit_button.pack(fill=tk.X)

        delete_button = tk.Button(self.root, text="Delete Student", command=self.delete_student)
        delete_button.pack(fill=tk.X)

        search_button = tk.Button(self.root, text="Search Students", command=self.search_students)
        search_button.pack(fill=tk.X)

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter student name:")
        age = simpledialog.askinteger("Add Student", "Enter student age:")
        grade = simpledialog.askinteger("Add Student", "Enter student grade:")
        
        if name and age and grade:
            db = Database()
            db.add_student(name, age, grade)
            
            # Insert the new student into the treeview
            self.treeview.insert("", "end", values=(name, age, grade))

    def edit_student(self):
        selected_item = self.treeview.selection()[0]
        
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

    def delete_student(self):
        selected_item = self.treeview.selection()[0]
        
        # Ask the user to confirm deletion
        response = tk.messagebox.askokcancel("Delete Student", f"Are you sure you want to delete {self.treeview.item(selected_item, 'values')[0]}?")
        
        if response:
            name = self.treeview.item(selected_item, "values")[0]
            db = Database()
            db.delete_student(name)
            self.treeview.delete(selected_item)

    def search_students(self):
        # Search for students by name
        search_term = simpledialog.askstring("Search Students", "Enter search term:")
        
        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())
        
        if search_term is None:
            return
        
        db = Database()
         
        results = db.search_students(search_term)
         
        for row in results:
            self.treeview.insert("", "end", values=row)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
