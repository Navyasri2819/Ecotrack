import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
from datetime import datetime
import matplotlib.pyplot as plt


activities = []
FILE_NAME = "eco_activities.json"


POINTS = {
    "Energy Saving": 10,
    "Recycling": 5,
    "Water Conservation": 8
}

def save_data():
    """Save activities to JSON file"""
    with open(FILE_NAME, "w") as f:
        json.dump(activities, f, indent=4)

def load_data():
    """Load activities from JSON file, convert if old format"""
    global activities
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

        
        new_data = []
        for act in data:
            if isinstance(act, str): 
                new_data.append({
                    "activity": act,
                    "category": "General",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "points": 0
                })
            else:
                new_data.append(act)
        activities = new_data
        save_data()  

    except FileNotFoundError:
        activities = []


def add_activity():
    """Add a new activity with category, timestamp, and points"""
    activity = activity_entry.get()
    category = category_var.get()
    if activity.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        points = POINTS.get(category, 1)
        entry = {"activity": activity, "category": category, "time": timestamp, "points": points}
        activities.append(entry)
        activity_entry.delete(0, tk.END)
        output_label.config(text=f"✅ Added: {activity} ({category}, +{points} pts)")
        save_data()
    else:
        messagebox.showwarning("Warning", "Please enter an activity.")

def view_activities():
    """Display all logged activities in the listbox"""
    activity_list.delete(0, tk.END)  
    if not activities:
        messagebox.showinfo("Info", "No activities logged yet.")
    else:
        for act in activities:
            activity_list.insert(
                tk.END,
                f"[{act['time']}] {act['activity']} ({act['category']}, {act['points']} pts)"
            )

def summary_report():
    """Show summary of total activities and points"""
    if not activities:
        messagebox.showinfo("Info", "No activities logged yet.")
        return

    total = len(activities)
    category_count = {}
    total_points = 0
    for act in activities:
        category_count[act['category']] = category_count.get(act['category'], 0) + 1
        total_points += act['points']

    summary_text = f"📊 Total activities: {total}\n⭐ Total points: {total_points}\n"
    for cat, count in category_count.items():
        summary_text += f"- {cat}: {count}\n"

    output_label.config(text=summary_text)

def show_graph():
    """Display a bar chart of activity categories"""
    if not activities:
        messagebox.showinfo("Info", "No data to plot.")
        return

    category_count = {}
    for act in activities:
        category_count[act['category']] = category_count.get(act['category'], 0) + 1

    plt.bar(category_count.keys(), category_count.values(), color=['green', 'blue', 'orange'])
    plt.title("EcoTrack Activities by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Activities")
    plt.show()

def export_csv():
    """Export activities to CSV file"""
    if not activities:
        messagebox.showinfo("Info", "No data to export.")
        return

    with open("eco_activities.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["activity", "category", "time", "points"])
        writer.writeheader()
        writer.writerows(activities)

    messagebox.showinfo("Success", "Data exported to eco_activities.csv")


root = tk.Tk()
root.title("EcoTrack - Daily Sustainability Logger")
root.geometry("650x600")

heading = tk.Label(root, text="EcoTrack - Daily Sustainability Logger",
                   font=("Arial", 16, "bold"), fg="green")
heading.pack(pady=10)


activity_entry = tk.Entry(root, width=40, font=("Arial", 12))
activity_entry.pack(pady=5)


category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, font=("Arial", 12))
category_dropdown['values'] = ("Energy Saving", "Recycling", "Water Conservation")
category_dropdown.current(0)
category_dropdown.pack(pady=5)


add_btn = tk.Button(root, text="Add Activity", command=add_activity,
                    font=("Arial", 12), bg="lightgreen")
add_btn.pack(pady=5)

view_btn = tk.Button(root, text="View Activities", command=view_activities,
                     font=("Arial", 12), bg="lightblue")
view_btn.pack(pady=5)

summary_btn = tk.Button(root, text="Summary Report", command=summary_report,
                        font=("Arial", 12), bg="orange")
summary_btn.pack(pady=5)

graph_btn = tk.Button(root, text="Show Graph", command=show_graph,
                      font=("Arial", 12), bg="purple", fg="white")
graph_btn.pack(pady=5)

export_btn = tk.Button(root, text="Export to CSV", command=export_csv,
                       font=("Arial", 12), bg="gray", fg="white")
export_btn.pack(pady=5)


activity_list = tk.Listbox(root, width=80, height=12, font=("Arial", 11))
activity_list.pack(pady=10)


output_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
output_label.pack(pady=5)


load_data()

root.mainloop()
