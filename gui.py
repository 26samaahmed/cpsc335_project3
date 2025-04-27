from tkinter import *
from tkinter import PhotoImage

# Add a button to submit the task
def submit_task():
    task_name = task_name_entry.get()
    task_desc = task_desc_entry.get()
    start_location = start_location_var.get()
    end_location = end_location_var.get()
    room_number = room_number_entry.get()
    start_time = start_time_var.get()
    end_time = end_time_var.get()

    print(f"Task Name: {task_name}, Description: {task_desc}, Start Location: {start_location}, End Location: {end_location}, Room Number: {room_number}, Start Time: {start_time}, End Time: {end_time}")

root = Tk()
root.title("Smart Campus Navigation and Task Scheduler")
root.geometry('1300x800')
root.configure(background='#C3C3C3')

Label(root, text="Welcome to Path Visualizer", font=("Courier New", 24, "bold"), fg="#002438", wraplength=500, justify="center", bg='#C3C3C3', pady=10).pack()

# New frame to hold both form and image side-by-side
content_frame = Frame(root, bg='#C3C3C3')
content_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Left side: Main frame for form
main_frame = Frame(content_frame, bg='#4E4E4E', borderwidth=5, relief="raised", height=300, width=400)
main_frame.pack(side="left", padx=20, pady=20, anchor="n")
main_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

# Label(main_frame, text="Your Tasks", font=("Courier New", 24, "bold"), fg="white", bg='#4E4E4E').grid(row=0, column=0, columnspan=2)

Label(main_frame, text="Task Name", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=1, column=0, padx=10, pady=10)
task_name_entry = Entry(main_frame, width=30)
task_name_entry.grid(row=1, column=1, padx=10, pady=10)

Label(main_frame, text="Task Description (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=2, column=0, padx=10, pady=10)
task_desc_entry = Entry(main_frame, width=30)
task_desc_entry.grid(row=2, column=1, padx=10, pady=10)

Label(main_frame, text="Start Location", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=3, column=0, padx=10, pady=10)
start_location_var = StringVar(value="Select Location")
start_location_dropdown = OptionMenu(main_frame, start_location_var, "Location 1", "Location 2", "Location 3")
start_location_dropdown.grid(row=3, column=1, padx=10, pady=10)

Label(main_frame, text="End Location", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=5, column=0, padx=10, pady=10)
end_location_var = StringVar(value="Select Location")
end_location_dropdown = OptionMenu(main_frame, end_location_var, "Location 1", "Location 2", "Location 3")
end_location_dropdown.grid(row=5, column=1, padx=10, pady=10)

Label(main_frame, text="Room Number (optional)", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=4, column=0, padx=10, pady=10)
room_number_entry = Entry(main_frame, width=30)
room_number_entry.grid(row=4, column=1, padx=10, pady=10)

Label(main_frame, text="Start Time", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=6, column=0, padx=10, pady=10)
start_time_var = StringVar(value="Select Time")
start_time_dropdown = OptionMenu(main_frame, start_time_var, "08:00 AM", "09:00 AM", "10:00 AM")
start_time_dropdown.grid(row=6, column=1, padx=10, pady=10)

Label(main_frame, text="End Time", font=("Courier New", 14), bg='#4E4E4E', fg="white").grid(row=7, column=0, padx=10, pady=10)
end_time_var = StringVar(value="Select Time")
end_time_dropdown = OptionMenu(main_frame, end_time_var, "09:00 AM", "10:00 AM", "11:00 AM")
end_time_dropdown.grid(row=7, column=1, padx=10, pady=10)

submit_button = Button(main_frame, text="Submit Task", font=("Courier New", 14), command=submit_task)
submit_button.grid(row=8, column=0, columnspan=2, pady=20)

# Right side: Map image
map_image = PhotoImage(file="csuf_map.png")
map_label = Label(content_frame, image=map_image, bg='#C3C3C3')
map_label.pack(side="left", padx=20, pady=20, anchor="n")


root.mainloop()
