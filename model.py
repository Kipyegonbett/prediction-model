import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connecting to the  database
db_connection = sqlite3.connect('school_database.db')
cursor = db_connection.cursor()

# Creating the students table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    school_satisfaction FLOAT,
    attendance_rate FLOAT,
    failed_courses INTEGER,
    commute_time INTEGER,
    disciplinary_incidents INTEGER,
    homework_completion FLOAT,
    family_income TEXT,
    promotion_status TEXT
);
''')
db_connection.commit()

# Function to retrieve and display data
def view_data():
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    result_window = tk.Toplevel(root)
    result_window.title("Database Records")
    result_window.geometry("800x400")
    
    tree = ttk.Treeview(result_window, columns=("ID", "Satisfaction", "Attendance", "Failed Courses", 
                                                "Commute Time", "Disciplinary", "Homework", "Income", "Status"), show="headings")
    tree.heading("ID", text="Student ID")
    tree.heading("Satisfaction", text="School Satisfaction")
    tree.heading("Attendance", text="Attendance Rate")
    tree.heading("Failed Courses", text="Failed Courses")
    tree.heading("Commute Time", text="Commute Time")
    tree.heading("Disciplinary", text="Disciplinary Cases")
    tree.heading("Homework", text="Homework Completion")
    tree.heading("Income", text="Family Income")
    tree.heading("Status", text="Promotion Status")
    
    for col in ("ID", "Satisfaction", "Attendance", "Failed Courses", "Commute Time", 
                "Disciplinary", "Homework", "Income", "Status"):
        tree.column(col, width=100)
    
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.pack(fill=tk.BOTH, expand=True)

# Function to delete data
def delete_data():
    try:
        student_id = int(entry_delete_id.get())
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        db_connection.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully!")
        else:
            messagebox.showwarning("Warning", f"No student found with ID {student_id}.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter a valid Student ID.")

# Main window
root = tk.Tk()
root.title("Database Viewer")
root.geometry("400x300")
root.configure(bg="#f0f8ff")

# View Data Button
btn_view = tk.Button(root, text="View Data", font=("Helvetica", 14, "bold"), bg="#4682b4", fg="white", command=view_data)
btn_view.pack(pady=20)

# Delete Data Input and Button
label_delete = tk.Label(root, text="Enter Student ID to Delete:", font=("Helvetica", 12), bg="#f0f8ff")
label_delete.pack(pady=5)

entry_delete_id = tk.Entry(root, font=("Helvetica", 12), width=20)
entry_delete_id.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Record", font=("Helvetica", 14, "bold"), bg="#d9534f", fg="white", command=delete_data)
btn_delete.pack(pady=10)

# Footer
footer = tk.Label(root, text="Managed By The Whiskers", font=("Helvetica", 10, "italic"), bg="#f0f8ff", fg="#4682b4")
footer.pack(pady=20)

# interface
root.mainloop()
