from tkinter import *
from tkinter import PhotoImage, messagebox
import tasks
from tasks import add_task        # ← updated signature
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import map

def update_map(startL, endL):
    # Right side: Map
    right_frame = Frame(content_frame, bg='#C0D9F0')
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20, anchor="n")

    graph = map.draw_map(startL, endL) # Create graph of Buildings with shortest path between two points
    canvas = FigureCanvasTkAgg(graph, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def submit_task():
    # Check if all required fields are filled
    if not task_name_entry.get():
        messagebox.showwarning("Warning", "Please enter a task name.")
        return False
    if start_location_var.get() == "Select Location":
        messagebox.showwarning("Warning", "Please select a start location.")
        return False
    if end_location_var.get() == "Select Location":
        messagebox.showwarning("Warning", "Please select an end location.")
        return False
    if start_time_var_hour.get() == "Hour" or start_time_var_minute.get() == "Minute" or start_am_vs_pm.get() == "AM or PM":
        messagebox.showwarning("Warning", "Please fill all of the start time fields.")
        return False
    if end_time_var_hour.get() == "Hour" or end_time_var_minute.get() == "Minute" or end_am_vs_pm.get() == "AM or PM":
        messagebox.showwarning("Warning", "Please fill all of the end time fields.")
        return False

    name   = task_name_entry.get()
    startL = start_location_var.get()
    endL   = end_location_var.get()
    startT = start_time_var_hour.get() + ":" + start_time_var_minute.get() + " " + start_am_vs_pm.get()
    endT   = end_time_var_hour.get() + ":" + end_time_var_minute.get() + " " + end_am_vs_pm.get()

    #if endT <= startT:
       # messagebox.showwarning("Warning", "End time must be after start time.")
       # end_time_var.set("Select Time")
       # return False

    update_map(startL, endL)

    # delegate to tasks.py
    result = add_task(name, startL, endL, startT, endT)
    if result["conflicts"]:
        # list the names of conflicting tasks
        conflict_names = ", ".join(c["name"] for c in result["conflicts"])
        if messagebox.askyesno(
            "Task Overlap",
            f"New task overlaps with {conflict_names}.\nReplace them?"
        ):
            # user accepted—re‑commit with replace=True
            result = add_task(name, startL, endL, startT, endT, replace=True)
            sorted_tasks = result["scheduled"]
        else:
            # user declined—keep old schedule
            sorted_tasks = tasks.tasks
    else:
        sorted_tasks = result["scheduled"]


    messagebox.showinfo("Success", "Task submitted successfully!")

    # Create New frame with the information
    task_frame = Frame(left_frame, bg='#4E4E4E', borderwidth=5, height=100, width=400)
    task_frame.pack(pady=10, fill="both", expand=True)
    task_frame.pack_propagate(False)

    task_name = Label(task_frame, text=name, font=("Courier New", 20, "bold"), fg="white", bg="#4E4E4E", justify="left")
    task_name.pack(anchor="w", padx=10, pady=(10, 0))

    info_row = Frame(task_frame, bg="#4E4E4E")
    info_row.pack(fill="x", expand=True, padx=10, pady=(5, 10))

    locations_label = Label(info_row, 
        text=f"{startL} - {endL}", 
        font=("Courier New", 14), 
        fg="white", bg="#4E4E4E", anchor="w")
    locations_label.pack(side="left", fill="x", expand=True)

    time_label = Label(info_row, 
        text=f"{startT} - {endT}", 
        font=("Courier New", 14), 
        fg="white", bg="#4E4E4E", anchor="e")
    time_label.pack(side="right", fill="x")


    # clear inputs…
    task_name_entry.delete(0, END)
    task_desc_entry.delete(0, END)
    room_number_entry.delete(0, END)
    room_number_entry2.delete(0, END)
    start_location_var.set("Select Location")
    end_location_var.set("Select Location")
    start_time_var_hour.set("Hour")
    start_time_var_minute.set("Minute")
    end_time_var_hour.set("Hour")
    end_time_var_minute.set("Minute")
    start_am_vs_pm.set("AM or PM")
    end_am_vs_pm.set("AM or PM")


# Main Window
root = Tk()
root.title("Smart Campus Navigation and Task Scheduler")
root.geometry('1300x1300')
root.configure(background='#C0D9F0')

Label(root, text="Welcome to Path Visualizer 💫", font=("Courier New", 24, "bold"), fg="#002438", wraplength=500, justify="center", bg='#C0D9F0', pady=10).pack()

# Frame to hold left and right content
content_frame = Frame(root, bg='#C0D9F0')
content_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Left side: Form + Tasks
left_frame = Frame(content_frame, bg='#C0D9F0')
left_frame.pack(side="left", padx=10, pady=10, anchor="n")

# Main frame (Form) inside left_frame
main_frame = Frame(left_frame, bg='#4E4E4E', borderwidth=5, relief="raised", height=400, width=400)
main_frame.pack(pady=10, fill="both", expand=True)


# Task form inside main_frame
Label(main_frame, text="Task Name*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
task_name_entry = Entry(main_frame, width=30)
task_name_entry.grid(row=1, column=1, padx=10, pady=10)

Label(main_frame, text="Task Description (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
task_desc_entry = Entry(main_frame, width=30)
task_desc_entry.grid(row=2, column=1, padx=10, pady=10)

Label(main_frame, text="Start Location*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
start_location_var = StringVar(value="Select Location")
start_location_dropdown = OptionMenu(main_frame, start_location_var, 
    "Engineering & Computer Science Building", "McCarthy Hall", "Steven G. Mihaylo Hall", "Titan Student Union", "Kinesiology and Health Science Building", "Pollak Library", "Visual Arts Center", "Humanities Building")
start_location_dropdown.config(width=27)
start_location_dropdown.grid(row=3, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
room_number_entry = Entry(main_frame, width=30)
room_number_entry.grid(row=4, column=1, padx=10, pady=10)

Label(main_frame, text="End Location*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=5, column=0, padx=10, pady=10, sticky="w")
end_location_var = StringVar(value="Select Location")
end_location_dropdown = OptionMenu(main_frame, end_location_var, 
    "Engineering & Computer Science Building", "McCarthy Hall", "Steven G. Mihaylo Hall", "Titan Student Union", "Kinesiology and Health Science Building", "Pollak Library", "Visual Arts Center", "Humanities Building")
end_location_dropdown.config(width=27)
end_location_dropdown.grid(row=5, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=6, column=0, padx=10, pady=10, sticky="w")
room_number_entry2 = Entry(main_frame, width=30)
room_number_entry2.grid(row=6, column=1, padx=10, pady=10)

Label(main_frame, text="Start Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w")\
    .grid(row=7, column=0, padx=10, pady=10, sticky="w")

start_time_var_hour = StringVar(value="Hour")
start_hour_dropdown = OptionMenu(main_frame, start_time_var_hour, 
    "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")
start_hour_dropdown.config(width=4)
start_hour_dropdown.grid(row=7, column=1)

start_time_var_minute = StringVar(value="Minute")
start_minute_dropdown = OptionMenu(main_frame, start_time_var_minute, "00", "15", "30", "45")
start_minute_dropdown.config(width=4)
start_minute_dropdown.grid(row=7, column=2, padx=5, pady=10)

start_am_vs_pm = StringVar(value="AM or PM")
start_am_vs_pm_dropdown = OptionMenu(main_frame, start_am_vs_pm, "AM", "PM")
start_am_vs_pm_dropdown.config(width=6)
start_am_vs_pm_dropdown.grid(row=7, column=3)


Label(main_frame, text="End Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w")\
    .grid(row=8, column=0, padx=10, pady=10, sticky="w")

end_time_var_hour = StringVar(value="Hour")
end_hour_dropdown = OptionMenu(main_frame, end_time_var_hour, 
    "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")
end_hour_dropdown.config(width=4)
end_hour_dropdown.grid(row=8, column=1)

end_time_var_minute = StringVar(value="Minute")
end_minute_dropdown = OptionMenu(main_frame, end_time_var_minute, "00", "15", "30", "45")
end_minute_dropdown.config(width=4)
end_minute_dropdown.grid(row=8, column=2)

end_am_vs_pm = StringVar(value="AM or PM")
end_am_vs_pm_dropdown = OptionMenu(main_frame, end_am_vs_pm, "AM", "PM")
end_am_vs_pm_dropdown.config(width=6)
end_am_vs_pm_dropdown.grid(row=8, column=3)


submit_button = Button(main_frame, text="Submit Task", font=("Courier New", 14), command=submit_task)
submit_button.grid(row=9, column=0, columnspan=2, pady=20)

# map_image = PhotoImage(file="csuf_map.png")
# map_label = Label(content_frame, image=map_image, bg='#C3C3C3')
# map_label.pack(side="left", padx=20, pady=20, anchor="n")

root.mainloop()

# TODO: Reformat the way the task is displayed to have the title on a line and then seperate the rest of the information on another line
# TODO: Fix ovelap
# TODO: Check if the start time is before the end time