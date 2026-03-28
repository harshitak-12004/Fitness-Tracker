import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("fitness.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS fitness (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    steps INTEGER,
    calories INTEGER,
    workout TEXT,
    duration INTEGER
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------

def add_data():
    date = datetime.now().strftime("%Y-%m-%d")
    steps = steps_entry.get()
    calories = calories_entry.get()
    workout = workout_entry.get()
    duration = duration_entry.get()

    if steps == "" or calories == "" or workout == "" or duration == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("INSERT INTO fitness (date, steps, calories, workout, duration) VALUES (?, ?, ?, ?, ?)",
                   (date, steps, calories, workout, duration))
    conn.commit()

    messagebox.showinfo("Success", "Data Added Successfully!")
    clear_fields()
    show_data()

def clear_fields():
    steps_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    workout_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

def show_data():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM fitness")
    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | Steps: {row[2]} | Calories: {row[3]} | {row[4]} ({row[5]} min)")

def delete_data():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select item to delete")
        return

    item = listbox.get(selected[0])
    record_id = item.split("|")[0].strip()

    cursor.execute("DELETE FROM fitness WHERE id=?", (record_id,))
    conn.commit()

    messagebox.showinfo("Deleted", "Entry deleted")
    show_data()

def show_graph():
    cursor.execute("SELECT date, steps, calories FROM fitness")
    data = cursor.fetchall()

    if not data:
        messagebox.showerror("Error", "No data available")
        return

    dates = [row[0] for row in data]
    steps = [row[1] for row in data]
    calories = [row[2] for row in data]

    plt.figure()
    plt.plot(dates, steps, marker='o', label="Steps")
    plt.plot(dates, calories, marker='o', label="Calories")

    plt.title("Fitness Progress")
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# ---------------- UI ----------------

root = tk.Tk()
root.title("🏋 Fitness Tracker App")
root.geometry("500x600")

title = tk.Label(root, text="Fitness Tracker", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Input Fields
tk.Label(root, text="Steps").pack()
steps_entry = tk.Entry(root)
steps_entry.pack()

tk.Label(root, text="Calories Burned").pack()
calories_entry = tk.Entry(root)
calories_entry.pack()

tk.Label(root, text="Workout Type").pack()
workout_entry = tk.Entry(root)
workout_entry.pack()

tk.Label(root, text="Duration (minutes)").pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

# Buttons
tk.Button(root, text="Add Data", command=add_data, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_data, bg="red", fg="white").pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph, bg="blue", fg="white").pack(pady=5)

# Listbox (Dashboard)
listbox = tk.Listbox(root, width=70, height=15)
listbox.pack(pady=10)

show_data()

root.mainloop()