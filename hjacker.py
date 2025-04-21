import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Establish connection to SQLite database
conn = sqlite3.connect('attendance_system.db')
cursor = conn.cursor()

# Create tables if they don't exist
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')

    conn.commit()

# Function to add a student
def add_student(name, roll_no):
    try:
        cursor.execute('''
            INSERT INTO students (name, roll_no)
            VALUES (?, ?)
        ''', (name, roll_no))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")

# Function to mark attendance
def mark_attendance(roll_no, status):
    try:
        # Get student ID using roll number
        cursor.execute('''
            SELECT student_id FROM students WHERE roll_no = ?
        ''', (roll_no,))
        student = cursor.fetchone()

        if student:
            student_id = student[0]
            date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
            ''', (student_id, date, status))
            conn.commit()
            messagebox.showinfo("Success", f"Attendance for {roll_no} marked as {status}!")
        else:
            messagebox.showerror("Error", "Student not found!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to view attendance
def view_attendance(roll_no):
    cursor.execute('''
        SELECT student_id FROM students WHERE roll_no = ?
    ''', (roll_no,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]
        cursor.execute('''
            SELECT date, status FROM attendance
            WHERE student_id = ? ORDER BY date DESC
        ''', (student_id,))
        records = cursor.fetchall()

        if records:
            record_text = f"\nAttendance records for {roll_no}:\n"
            for record in records:
                record_text += f"Date: {record[0]}, Status: {record[1]}\n"
            messagebox.showinfo("Attendance Records", record_text)
        else:
            messagebox.showinfo("No Records", f"No attendance records found for {roll_no}.")
    else:
        messagebox.showerror("Error", "Student not found!")

# GUI Application using Tkinter
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Management System")
        self.root.geometry("500x400")

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Add Student Section
        self.add_student_label = tk.Label(self.root, text="Add Student", font=("Arial", 14))
        self.add_student_label.pack(pady=10)

        self.student_name_label = tk.Label(self.root, text="Name:")
        self.student_name_label.pack()
        self.student_name_entry = tk.Entry(self.root, width=40)
        self.student_name_entry.pack(pady=5)

        self.student_roll_no_label = tk.Label(self.root, text="Roll Number:")
        self.student_roll_no_label.pack()
        self.student_roll_no_entry = tk.Entry(self.root, width=40)
        self.student_roll_no_entry.pack(pady=5)

        self.add_student_button = tk.Button(self.root, text="Add Student", command=self.add_student)
        self.add_student_button.pack(pady=10)

        # Mark Attendance Section
        self.mark_attendance_label = tk.Label(self.root, text="Mark Attendance", font=("Arial", 14))
        self.mark_attendance_label.pack(pady=10)

        self.attendance_roll_no_label = tk.Label(self.root, text="Roll Number:")
        self.attendance_roll_no_label.pack()
        self.attendance_roll_no_entry = tk.Entry(self.root, width=40)
        self.attendance_roll_no_entry.pack(pady=5)

        self.attendance_status_label = tk.Label(self.root, text="Status (Present/Absent):")
        self.attendance_status_label.pack()
        self.attendance_status_entry = tk.Entry(self.root, width=40)
        self.attendance_status_entry.pack(pady=5)

        self.mark_attendance_button = tk.Button(self.root, text="Mark Attendance", command=self.mark_attendance)
        self.mark_attendance_button.pack(pady=10)

        # View Attendance Section
        self.view_attendance_label = tk.Label(self.root, text="View Attendance", font=("Arial", 14))
        self.view_attendance_label.pack(pady=10)

        self.view_roll_no_label = tk.Label(self.root, text="Enter Roll Number:")
        self.view_roll_no_label.pack()
        self.view_roll_no_entry = tk.Entry(self.root, width=40)
        self.view_roll_no_entry.pack(pady=5)

        self.view_attendance_button = tk.Button(self.root, text="View Attendance", command=self.view_attendance)
        self.view_attendance_button.pack(pady=10)

    def add_student(self):
        name = self.student_name_entry.get()
        roll_no = self.student_roll_no_entry.get()
        if name and roll_no:
            add_student(name, roll_no)
        else:
            messagebox.showerror("Error", "Please fill out all fields.")

    def mark_attendance(self):
        roll_no = self.attendance_roll_no_entry.get()
        status = self.attendance_status_entry.get()
        if roll_no and status:
            mark_attendance(roll_no, status)
        else:
            messagebox.showerror("Error", "Please fill out all fields.")

    def view_attendance(self):
        roll_no = self.view_roll_no_entry.get()
        if roll_no:
            view_attendance(roll_no)
        else:
            messagebox.showerror("Error", "Please enter a roll number.")

# Create database tables and launch the Tkinter application
create_tables()

# Create the main window and start the Tkinter application
root = tk.Tk()
app = AttendanceApp(root)
root.mainloop()

# Close the database connection when the application is closed
conn.close()
