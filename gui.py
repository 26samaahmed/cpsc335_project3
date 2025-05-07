from tkinter import *
from tkinter import PhotoImage, messagebox
import tasks
from tasks import add_task        # ← updated signature
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csuf_map

class AutocompleteEntry(Entry):
    def __init__(self, master, complete_values, **kwargs):
        super().__init__(master, **kwargs)
        self.complete_values = complete_values
        # bind a StringVar so we can watch for edits
        self.var = self["textvariable"] = StringVar()
        self.var.trace_add("write", self._on_change)
        self.bind("<FocusIn>", self._on_change)

        # create a floating frame on the toplevel for dropdown
        self.dropdown = Frame(self.winfo_toplevel(), bd=1, relief="solid")
        # listbox inside it
        self.listbox = Listbox(self.dropdown, height=5)
        # scrollbar
        self.scrollbar = Scrollbar(self.dropdown, orient=VERTICAL,
                                   command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)

        # grid them
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.dropdown.grid_rowconfigure(0, weight=1)
        self.dropdown.grid_columnconfigure(0, weight=1)

        # selection binding
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_change(self, *args):
        typed = self.var.get().lower()
        if typed:
            matches = [v for v in self.complete_values if typed in v.lower()]
        else:
            matches = list(self.complete_values)

        # update listbox contents
        self.listbox.delete(0, END)
        for m in matches:
            self.listbox.insert(END, m)

        if matches:
            # compute coords relative to the toplevel window
            parent = self.winfo_toplevel()
            x = self.winfo_rootx() - parent.winfo_rootx()
            y = (self.winfo_rooty() - parent.winfo_rooty()
                 + self.winfo_height())
            w = self.winfo_width()
            # place dropdown in the toplevel so it floats above all frames
            self.dropdown.place(in_=parent, x=x, y=y, width=w)
            self.dropdown.lift()
        else:
            self.dropdown.place_forget()

    def _on_select(self, evt):
        sel = self.listbox.curselection()
        if sel:
            self.var.set(self.listbox.get(sel[0]))
        self.dropdown.place_forget()

def update_map(startL, endL):
    # Delete previous map
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create new map with the new start and end points
    graph, shortest_path_ani = csuf_map.draw_map(startL, endL) # Create graph of Buildings with shortest path between two points
    canvas = FigureCanvasTkAgg(graph, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    shortest_path_ani.event_source.start()

def render_tasks(tasks_list):
    """
    Clear out any existing task frames and render each one scrollably.
    """
    # destroy old tasks
    for w in tasks_container.winfo_children():
        w.destroy()

    for t in tasks_list:
        # a bit taller and wider for more breathing room
        tf = Frame(tasks_container, bg='#4E4E4E', borderwidth=5, height=120, width=530)
        tf.pack(pady=10, padx=10, fill="both", expand=True)
        tf.pack_propagate(False)

        # Task name
        Label(tf, text=t["name"], font=("Courier New", 20, "bold"),
              fg="white", bg="#4E4E4E", justify="left") \
          .pack(anchor="w", padx=10, pady=(10,0))

        # new: location on one line…
        Label(tf, text=f"{t['start_location']} - {t['end_location']}",
              font=("Courier New",14), fg="white", bg="#4E4E4E", anchor="w") \
          .pack(anchor="w", padx=10, pady=(5,0))
        # …and time on the next line
        Label(tf, text=f"{t['start_time']} - {t['end_time']}",
              font=("Courier New",14), fg="white", bg="#4E4E4E", anchor="w") \
          .pack(anchor="w", padx=10, pady=(0,10))

def submit_task():
    # Check if all required fields are filled
    if not task_name_entry.get():
        messagebox.showwarning("Warning", "Please enter a task name.")
        return False
    if start_location_entry.get() == "Select Location":
        messagebox.showwarning("Warning", "Please select a start location.")
        return False
    if end_location_entry.get() == "Select Location":
        messagebox.showwarning("Warning", "Please select an end location.")
        return False
    if start_time_var_hour.get() == "Hour" or start_time_var_minute.get() == "Minute" or start_am_vs_pm.get() == "AM or PM":
        messagebox.showwarning("Warning", "Please fill all of the start time fields.")
        return False
    if end_time_var_hour.get() == "Hour" or end_time_var_minute.get() == "Minute" or end_am_vs_pm.get() == "AM or PM":
        messagebox.showwarning("Warning", "Please fill all of the end time fields.")
        return False

    name   = task_name_entry.get()
    startL = start_location_entry.get()
    endL   = end_location_entry.get()
    startT = start_time_var_hour.get() + start_time_var_minute.get() + " " + start_am_vs_pm.get()
    endT   = end_time_var_hour.get() + end_time_var_minute.get() + " " + end_am_vs_pm.get()

    if startT == endT:
        messagebox.showwarning("Warning", "Start time and end time cannot be the same.")
        return False
    if startL == endL:
        messagebox.showwarning("Warning", "Start location and end location cannot be the same.")
        return False
    
    start_hour, start_minute = map(int, startT.split()[0].split(':')) 
    end_hour, end_minute = map(int, endT.split()[0].split(':'))

    # Convert 12-hour format to 24-hour format
    if start_am_vs_pm.get() == "PM" and start_hour != 12:
        start_hour += 12
    if end_am_vs_pm.get() == "PM" and end_hour != 12:
        end_hour += 12
    if start_am_vs_pm.get() == "AM" and start_hour == 12:
        start_hour = 0
    if end_am_vs_pm.get() == "AM" and end_hour == 12:
        end_hour = 0

    # Check if start time is before end time
    if (start_hour > end_hour) or (start_hour == end_hour and start_minute >= end_minute):
        messagebox.showwarning("Warning", "Start time must be before end time.")
        return False

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
            # user declined—do not add this task
            messagebox.showinfo("Task Skipped", "Task was not added to the schedule.")
            return
    else:
        sorted_tasks = result["scheduled"]

    # re‐draw the list from scratch
    render_tasks(sorted_tasks)

    messagebox.showinfo("Success", "Task submitted successfully!")

    # clear inputs…
    task_name_entry.delete(0, END)
    task_desc_entry.delete(0, END)
    room_number_entry.delete(0, END)
    room_number_entry2.delete(0, END)
    start_location_entry.delete(0, END)
    end_location_entry.delete(0, END)
    start_time_var_hour.set("Hour")
    start_time_var_minute.set("Minute")
    end_time_var_hour.set("Hour")
    end_time_var_minute.set("Minute")
    start_am_vs_pm.set("AM or PM")
    end_am_vs_pm.set("AM or PM")

    # --- reset autocomplete state so the dropdown will reappear next time ---
    start_location_entry.var.set("")  
    end_location_entry.var.set("")    
    start_location_entry.dropdown.place_forget()
    end_location_entry.dropdown.place_forget()


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
main_frame = Frame(left_frame, bg='#4E4E4E', borderwidth=5, relief="raised")
main_frame.pack(pady=10, fill="both", expand=True)


# Task form inside main_frame
Label(main_frame, text="Task Name*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
task_name_entry = Entry(main_frame, width=30)
task_name_entry.grid(row=1, column=1, padx=10, pady=10)

Label(main_frame, text="Task Description (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
task_desc_entry = Entry(main_frame, width=30)
task_desc_entry.grid(row=2, column=1, padx=10, pady=10)

building_names = list(csuf_map.string_to_enum.keys())
Label(main_frame, text="Start Location*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
start_location_entry = AutocompleteEntry(main_frame, complete_values=building_names, width=29)
start_location_entry.grid(row=3, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
room_number_entry = Entry(main_frame, width=30)
room_number_entry.grid(row=4, column=1, padx=10, pady=10)

Label(main_frame, text="End Location*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=5, column=0, padx=10, pady=10, sticky="w")
end_location_entry = AutocompleteEntry(main_frame, complete_values=building_names, width=29)
end_location_entry.grid(row=5, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w").grid(row=6, column=0, padx=10, pady=10, sticky="w")
room_number_entry2 = Entry(main_frame, width=30)
room_number_entry2.grid(row=6, column=1, padx=10, pady=10)

Label(main_frame, text="Start Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w")\
    .grid(row=7, column=0, padx=10, pady=10, sticky="w")

hour_list = ["12:", "01:", "02:", "03:", "04:", "05:", "06:", "07:", "08:", "09:", "10:", "11:"]
minute_list = ["00", "15", "30", "45"]
start_time_frame = Frame(main_frame)
start_time_frame.grid(row=7, column=1, columnspan=3, sticky="w", padx=15)

start_time_var_hour = StringVar(value="Hour")
start_hour_dropdown = OptionMenu(start_time_frame, start_time_var_hour, *hour_list)
start_hour_dropdown.config(width=3)
start_hour_dropdown.pack(side="left", padx=5)

start_time_var_minute = StringVar(value="Minute")
start_minute_dropdown = OptionMenu(start_time_frame, start_time_var_minute, *minute_list)
start_minute_dropdown.config(width=4)
start_minute_dropdown.pack(side="left", padx=5)

start_am_vs_pm = StringVar(value="AM or PM")
start_am_vs_pm_dropdown = OptionMenu(start_time_frame, start_am_vs_pm, "AM", "PM")
start_am_vs_pm_dropdown.config(width=6)
start_am_vs_pm_dropdown.pack(side="left", padx=5)


Label(main_frame, text="End Time*", font=("Courier New", 14), bg='#4E4E4E', fg="white", anchor="w")\
    .grid(row=8, column=0, padx=10, pady=10, sticky="w")

end_time_frame = Frame(main_frame)
end_time_frame.grid(row=8, column=1, columnspan=3, sticky="w", padx=15)

end_time_var_hour = StringVar(value="Hour")
end_hour_dropdown = OptionMenu(end_time_frame, end_time_var_hour, *hour_list)
end_hour_dropdown.config(width=3)
end_hour_dropdown.pack(side="left", padx=5)

end_time_var_minute = StringVar(value="Minute")
end_minute_dropdown = OptionMenu(end_time_frame, end_time_var_minute, *minute_list)
end_minute_dropdown.config(width=4)
end_minute_dropdown.pack(side="left", padx=5)

end_am_vs_pm = StringVar(value="AM or PM")
end_am_vs_pm_dropdown = OptionMenu(end_time_frame, end_am_vs_pm, "AM", "PM")
end_am_vs_pm_dropdown.config(width=6)
end_am_vs_pm_dropdown.pack(side="left", padx=5)


submit_button = Button(main_frame, text="Submit Task", font=("Courier New", 14), command=submit_task)
submit_button.grid(row=9, column=0, columnspan=2, pady=20)

main_frame.pack(pady=10, fill="both", expand=True)

# --- BEGIN SCROLLABLE TASK LIST SETUP ---
# create a larger canvas + scrollbar inside left_frame, below main_frame
tasks_canvas = Canvas(
    left_frame,
    bg='#C0D9F0',
    highlightthickness=0,
    width=500,    # make it wider
    height=600,   # and taller
)
scrollbar_tasks = Scrollbar(left_frame, orient="vertical", command=tasks_canvas.yview)
tasks_canvas.configure(yscrollcommand=scrollbar_tasks.set)

# layout
tasks_canvas.pack(side="left", fill="both", expand=True, pady=(0,10))
scrollbar_tasks.pack(side="right", fill="y", pady=(0,10))

# frame inside canvas where task frames will go
tasks_container = Frame(tasks_canvas, bg='#C0D9F0')
tasks_canvas.create_window((0,0), window=tasks_container, anchor="nw")

# update scrollregion when container changes size
def _on_tasks_resize(event):
    tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all"))

tasks_container.bind("<Configure>", _on_tasks_resize)
# --- END SCROLLABLE TASK LIST SETUP ---

# map_image = PhotoImage(file="csuf_map.png")
# map_label = Label(content_frame, image=map_image, bg='#C3C3C3')
# map_label.pack(side="left", padx=20, pady=20, anchor="n")

# Right side: Map (Show empty map before paths are created)
right_frame = Frame(content_frame, bg='#C0D9F0')
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20, anchor="n")

graph, shortest_path = csuf_map.draw_map() # Create graph of Buildings with shortest path between two points
canvas = FigureCanvasTkAgg(graph, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()

# TODO: Fix ovelap
# TODO: Check if the start time is before the end time