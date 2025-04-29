from tkinter import *
from tkinter import PhotoImage, messagebox
import tasks
from tasks import add_task        # ← updated signature

def submit_task():
    name   = task_name_entry.get()
    startL = start_location_var.get()
    endL   = end_location_var.get()
    startT = start_time_var.get()
    endT   = end_time_var.get()

    # delegate to tasks.py
    result = add_task(name, startL, endL, startT, endT)
    if result["conflicts"]:
        # list the names of conflicting tasks
        conflict_names = ", ".join(c["name"] for c in result["conflicts"])
        if messagebox.askyesno(
            "Task Overlap",
            f"New task overlaps with: {conflict_names}.\nReplace them?"
        ):
            # user accepted—re‑commit with replace=True
            result = add_task(name, startL, endL, startT, endT, replace=True)
            sorted_tasks = result["scheduled"]
        else:
            # user declined—keep old schedule
            sorted_tasks = tasks.tasks
    else:
        sorted_tasks = result["scheduled"]

    # redraw the task list from sorted_tasks
    task_list.config(state="normal")
    task_list.delete("1.0", END)
    for task in sorted_tasks:
        task_list.insert("end", task["name"], "bold")
        task_list.insert("end",
            f" | {task['start_location']} ➔ {task['end_location']} | "
            f"{task['start_time']} - {task['end_time']}\n"
        )
    task_list.config(state="disabled")

    # clear inputs…
    task_name_entry.delete(0, END)
    task_desc_entry.delete(0, END)
    room_number_entry.delete(0, END)
    room_number_entry2.delete(0, END)
    start_location_var.set("Select Location")
    end_location_var.set("Select Location")
    start_time_var.set("Select Time")
    end_time_var.set("Select Time")


# Main Window
root = Tk()
root.title("Smart Campus Navigation and Task Scheduler")
root.geometry('1300x800')
root.configure(background='#C0D9F0')

Label(root, text="Welcome to Path Visualizer 💫", font=("Courier New", 24, "bold"), fg="#002438", wraplength=500, justify="center", bg='#C0D9F0', pady=10).pack()

# Frame to hold left and right content
content_frame = Frame(root, bg='#C0D9F0')
content_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Left side: Form + Tasks
left_frame = Frame(content_frame, bg='#C0D9F0')
left_frame.pack(side="left", padx=20, pady=20, anchor="n")

# Main frame (Form) inside left_frame
main_frame = Frame(left_frame, bg='#4E4E4E', borderwidth=5, relief="raised", height=400, width=400)
main_frame.pack(pady=10, fill="both", expand=True)
main_frame.pack_propagate(False)

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
    "College Park", "Pollak Library", "Engineering Building", "Humanities Building", 
    "Computer Science Building", "Visual Arts Center", "Steven G. Mihaylo Hall", 
    "McCarthy Hall", "University Hall", "Titan Student Union", 
    "Kinesiology and Health Science Building", "Langsdorf Hall", 
    "Gordon Hall", "Dan Black Hall")
start_location_dropdown.config(width=27)
start_location_dropdown.grid(row=3, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
room_number_entry = Entry(main_frame, width=30)
room_number_entry.grid(row=4, column=1, padx=10, pady=10)

Label(main_frame, text="End Location*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=5, column=0, padx=10, pady=10, sticky="w")
end_location_var = StringVar(value="Select Location")
end_location_dropdown = OptionMenu(main_frame, end_location_var, 
    "College Park", "Pollak Library", "Engineering Building", "Humanities Building", 
    "Computer Science Building", "Visual Arts Center", "Steven G. Mihaylo Hall", 
    "McCarthy Hall", "University Hall", "Titan Student Union", 
    "Kinesiology and Health Science Building", "Langsdorf Hall", 
    "Gordon Hall", "Dan Black Hall")
end_location_dropdown.config(width=27)
end_location_dropdown.grid(row=5, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=6, column=0, padx=10, pady=10, sticky="w")
room_number_entry2 = Entry(main_frame, width=30)
room_number_entry2.grid(row=6, column=1, padx=10, pady=10)

Label(main_frame, text="Start Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=7, column=0, padx=10, pady=10, sticky="w")
start_time_var = StringVar(value="Select Time")
start_time_dropdown = OptionMenu(main_frame, start_time_var, 
    "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM",
    "06:00 PM", "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM",
    "11:00 PM", "12:00 AM", "01:00 AM", "02:00 AM", "03:00 AM",
    "04:00 AM", "05:00 AM", "06:00 AM", "07:00 AM")
start_time_dropdown.config(width=27)
start_time_dropdown.grid(row=7, column=1, padx=10, pady=10)

Label(main_frame, text="End Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=8, column=0, padx=10, pady=10, sticky="w")
end_time_var = StringVar(value="Select Time")
end_time_dropdown = OptionMenu(main_frame, end_time_var, 
    "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM",
    "06:00 PM", "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM",
    "11:00 PM", "12:00 AM", "01:00 AM", "02:00 AM", "03:00 AM",
    "04:00 AM", "05:00 AM", "06:00 AM", "07:00 AM")
end_time_dropdown.config(width=27)
end_time_dropdown.grid(row=8, column=1, padx=10, pady=10)

submit_button = Button(main_frame, text="Submit Task", font=("Courier New", 14), command=submit_task)
submit_button.grid(row=9, column=0, columnspan=2, pady=20)

task_frame = Frame(left_frame, bg='#4E4E4E', borderwidth=5, relief="raised", height=300, width=400)
task_frame.pack(pady=10, fill="both", expand=True)
task_frame.pack_propagate(False)

#task_list_label = Label(task_frame, text="Your Tasks", font=("Courier New", 20, "bold"), fg="white", bg='#4E4E4E', pady=10)
#task_list_label.pack()
#task_list = Listbox(task_frame, width=60, height=10, font=("Courier New", 14), bg='#4E4E4E', border=0, fg="white")
#task_list.pack(pady=10)

task_list_label = Label(task_frame, text="Your Tasks", font=("Courier New", 20, "bold"), fg="white", bg="#4E4E4E", pady=10)
task_list_label.pack()

task_list = Text(task_frame, width=60, height=10, font=("Courier New", 14), bg="#4E4E4E", fg="white", wrap="word", border=0, bd=0, highlightthickness=0)
task_list.tag_configure("bold", font=("Courier New", 14, "bold"))
task_list.pack(pady=10)
task_list.config(state="disabled")

map_image = PhotoImage(file="csuf_map.png")
map_label = Label(content_frame, image=map_image, bg='#C3C3C3')
map_label.pack(side="left", padx=20, pady=20, anchor="n")


root.mainloop()

# TODO: Check if all required filled have been filled
# TODO: Check that end time is after start time, and give a warning if not
# TODO: Reformat the way the task is displayed to have the title on a line and then seperate the rest of the information on another line
