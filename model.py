import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connecting to the database
db_connection = sqlite3.connect('school_database.db')
cursor = db_connection.cursor()

# Create the students table if it doesn't exist
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

# Function to predict promotion status
def predict_promotion(satisfaction, attendance, failed_courses, commute, disciplinary, homework, income):
    if (satisfaction > 3 and attendance > 70 and failed_courses <= 2 and
        commute <= 40 and disciplinary <= 2 and homework > 80 and
        income in ["low", "medium", "high"]):
        return "Promoted"
    else:
        return "Dropped Out"

# Function to insert data into the database
def insert_data():
    try:
        student_id = int(entry_student_id.get())
        satisfaction = float(entry_satisfaction.get())
        attendance = float(entry_attendance.get())
        failed_courses = int(entry_failed_courses.get())
        commute = int(entry_commute.get())
        disciplinary = int(entry_disciplinary.get())
        homework = float(entry_homework.get())
        family_income = income_var.get()

        # Predict promotion status
        promotion_status = predict_promotion(
            satisfaction, attendance, failed_courses, commute, disciplinary, homework, family_income
        )

        # Show notification of the prediction result
        messagebox.showinfo("Prediction Result", f"Student {student_id} is {promotion_status}.")

        # Insert into database
        cursor.execute('''
        INSERT INTO students (
            student_id, school_satisfaction, attendance_rate, failed_courses, 
            commute_time, disciplinary_incidents, homework_completion, 
            family_income, promotion_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, satisfaction, attendance, failed_courses, commute, disciplinary, homework, family_income, promotion_status))
        db_connection.commit()

        messagebox.showinfo("Success", "Student data inserted successfully!")
        clear_inputs()
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please check your entries.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists!")

# Function to retrieve data from the database and display it
def retrieve_data():
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    result_window = tk.Toplevel(window)
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

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

# Function to clear input fields
def clear_inputs():
    entry_student_id.delete(0, tk.END)
    entry_satisfaction.delete(0, tk.END)
    entry_attendance.delete(0, tk.END)
    entry_failed_courses.delete(0, tk.END)
    entry_commute.delete(0, tk.END)
    entry_disciplinary.delete(0, tk.END)
    entry_homework.delete(0, tk.END)
    income_var.set("low")

# Create GUI window
window = tk.Tk()
window.title("Student Promotion Predictor")
window.geometry("600x700")
window.configure(bg="#e6f7ff")

# Header
header = tk.Label(window, text="Student Drop out Predictor", font=("Helvetica", 20, "bold"), bg="#00509e", fg="white", pady=10)
header.pack(fill=tk.X)

# Helper function to create labels and input fields
def create_label_and_entry(label_text, entry_widget):
    tk.Label(window, text=label_text, font=("Helvetica", 12), bg="#e6f7ff").pack(pady=5)
    entry_widget.pack(pady=5)

# Labels and input fields
entry_student_id = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_satisfaction = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_attendance = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_failed_courses = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_commute = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_disciplinary = tk.Entry(window, font=("Helvetica", 12), width=30)
entry_homework = tk.Entry(window, font=("Helvetica", 12), width=30)

create_label_and_entry("Student ID:", entry_student_id)
create_label_and_entry("School Satisfaction (>3):", entry_satisfaction)
create_label_and_entry("Attendance Rate (>70):", entry_attendance)
create_label_and_entry("Failed Courses (≤2):", entry_failed_courses)
create_label_and_entry("Commute Time (≤40):", entry_commute)
create_label_and_entry("Disciplinary Cases (≤2):", entry_disciplinary)
create_label_and_entry("Homework Completion (>80):", entry_homework)

# Family Income Dropdown
tk.Label(window, text="Family Income (low, medium, high):", font=("Helvetica", 12), bg="#e6f7ff").pack(pady=5)
income_var = tk.StringVar(value="low")
income_menu = tk.OptionMenu(window, income_var, "low", "medium", "high")
income_menu.config(font=("Helvetica", 12), width=15, bg="#d9e8fc", fg="black")
income_menu.pack(pady=5)

# Buttons
btn_predict = tk.Button(window, text="PREDICT & INSERT", font=("Helvetica", 14, "bold"), bg="#00509e", fg="white", command=insert_data, width=20)
btn_predict.pack(pady=10)

btn_retrieve = tk.Button(window, text="View Database", font=("Helvetica", 14, "bold"), bg="#4682b4", fg="white", command=retrieve_data, width=20)
btn_retrieve.pack(pady=10)

btn_clear = tk.Button(window, text="Clear Inputs", font=("Helvetica", 14, "bold"), bg="#d9534f", fg="white", command=clear_inputs, width=20)
btn_clear.pack(pady=10)

# Footer
footer = tk.Label(window, text="Powered by Your Predictor Engine", font=("Helvetica", 10, "italic"), bg="#e6f7ff", fg="#00509e")
footer.pack(pady=10)

# Start GUI
window.mainloop()
