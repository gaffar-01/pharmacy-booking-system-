import tkinter
from tkinter import messagebox
import backend
from tkcalendar import Calendar
import datetime



window = tkinter.Tk()
window.title("Moin's Chemist Booking System")
window.geometry("800x500")
window.configure(bg="#DBCECE")

frame = tkinter.Frame(bg="#DBCECE")

try:
    logo_photo = tkinter.PhotoImage(file="moins.png")
    logo_label = tkinter.Label(frame, image=logo_photo, bg="#4F7302")
    logo_label.image = logo_photo
    logo_label.grid(row=0, column=2, rowspan=6, padx=30, pady=20, sticky="ne")
except:
    print("Could not load image. Make sure the file path is correct.")

login_label = tkinter.Label(
    frame, 
    text="Welcome to the Pharmacy Portal",
    bg="#DBCECE",
    fg="#0B0B0B",
    font=("Arial", 22, "bold")
)

email_label = tkinter.Label(
    frame,
    text="Email:",
    bg="#DBCECE",
    fg="#0B0B0B",
    font=("Arial", 12)
)
email_entry = tkinter.Entry(
    frame,
    font=("Arial", 11),
    width=35,
    bd=2,
    relief="solid"
)

password_label = tkinter.Label(
    frame,
    text="Password:",
    bg="#DBCECE",
    fg="#0B0B0B",
    font=("Arial", 12)
)
password_entry = tkinter.Entry(
    frame,
    show="*",
    font=("Arial", 11),
    width=35,
    bd=2,
    relief="solid"
)

def handle_login():
    email = email_entry.get()
    password = password_entry.get()
    
    if not email or not password:
        messagebox.showwarning("Input Error", "Please enter both email and password")  #warning box if not all fields are answered
        return
    
    user = backend.login(email, password) # calls login function in backend 
    
    if user: #if login function returns true 
        user_id, name, role = user
        if role == 'Patient':
            window.destroy()
            open_patient_dashboard(user_id, name)
        else:
            window.destroy()
            open_staff_dashboard(user_id,name)
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")
        password_entry.delete(0, tkinter.END)

def open_register():
    #window creation for open register 
    register_win = tkinter.Toplevel(window)
    register_win.title("Create Account - Moin's Chemist")
    register_win.geometry("600x450")
    register_win.configure(bg="#DBCECE")
    
    reg_frame = tkinter.Frame(register_win, bg="#DBCECE")
    reg_frame.pack(expand=True, fill="both", padx=30, pady=30)
    
    try:
        logo_photo = tkinter.PhotoImage(file="moins.png") #logo added to window 
        logo_label = tkinter.Label(reg_frame, image=logo_photo, bg="#4F7302")
        logo_label.image = logo_photo
        logo_label.place(x=420, y=10, width=150, height=150)
    except:
        pass
    
    tkinter.Label(
        reg_frame, 
        text="Register New Account", 
        font=("Arial", 18, "bold"), 
        bg="#DBCECE",
        fg="#0B0B0B"
    ).grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="w", padx=20)
    
    tkinter.Label(reg_frame, text="Name:", bg="#DBCECE", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    name_entry = tkinter.Entry(reg_frame, font=("Arial", 10), width=25, bd=2, relief="solid")
    name_entry.grid(row=1, column=1, pady=8, sticky="w")
    
    tkinter.Label(reg_frame, text="Email:", bg="#DBCECE", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    reg_email_entry = tkinter.Entry(reg_frame, font=("Arial", 10), width=25, bd=2, relief="solid")
    reg_email_entry.grid(row=2, column=1, pady=8, sticky="w")
    
    tkinter.Label(reg_frame, text="Password:", bg="#DBCECE", font=("Arial", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=8)
    reg_pass_entry = tkinter.Entry(reg_frame, show="*", font=("Arial", 10), width=25, bd=2, relief="solid")
    reg_pass_entry.grid(row=3, column=1, pady=8, sticky="w")

    tkinter.Label(
        reg_frame, 
        text="Security Question:", 
        bg="#DBCECE", 
        font=("Arial", 11, "bold")
    ).grid(row=4, column=0, columnspan=2, pady=(15, 5))
    
    tkinter.Label(
        reg_frame,
        text="Favourite Teacher? ",  # security question
        bg="#DBCECE",
        font=("Arial", 10, "italic"),
        fg="#555555"
    ).grid(row=5, column=0, columnspan=2, pady=(0, 10))
    
    tkinter.Label(reg_frame, text="Answer:", bg="#DBCECE", font=("Arial", 11)).grid(row=6, column=0, sticky="e", padx=10, pady=8)
    reg_ans_entry = tkinter.Entry(reg_frame, font=("Arial", 10), width=25, bd=2, relief="solid")
    reg_ans_entry.grid(row=6, column=1, pady=8, sticky="w")
    
    def handle_register():
        #get all fields entered 
        name = name_entry.get() 
        email = reg_email_entry.get()
        password = reg_pass_entry.get()
        answer = reg_ans_entry.get()
        role = "Patient" #any account created here are patients 
        
        success, message = backend.create_account(email, password, name, role,answer) # calls ffunction in backend 
        
        if success:
            messagebox.showinfo("Success", message) # if function return true 
            register_win.destroy()
        else:
            messagebox.showerror("Error", message) #if function returns false 
    
    register_btn = tkinter.Button(
        reg_frame, 
        text="REGISTER", 
        bg="#0C6D99", 
        fg="white", 
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        command=handle_register #calls handle register function when user presses register 
    )
    register_btn.grid(row=9, column=2, columnspan=2, pady=(25, 0))
    
    back_btn = tkinter.Button(
        register_win, 
        text="BACK", 
        bg="#A4C639", 
        fg="white", 
        font=("Arial", 10, "bold"),
        width=12,
        height=2,
        bd=0,
        cursor="hand2",
        command=register_win.destroy
    )
    back_btn.place(x=30, y=380)

def open_forgot_password():
    #tkinter window creation 
    forgot_win = tkinter.Toplevel(window)
    forgot_win.title("Reset Password - Moin's Chemist")
    forgot_win.geometry("800x400")
    forgot_win.configure(bg="#DBCECE")
    
    forgot_frame = tkinter.Frame(forgot_win, bg="#DBCECE")
    forgot_frame.pack(expand=True, pady=30) #frame used to align labels 
    
    #all labels needed on reset password window
    tkinter.Label(
        forgot_frame,
        text="Reset Password",
        font=("Arial", 18, "bold"),
        bg="#DBCECE",
        fg="#0B0B0B"
    ).grid(row=0, column=0, columnspan=2, pady=(0, 30))
    
    tkinter.Label(
        forgot_frame,
        text="Email:",
        bg="#DBCECE",
        font=("Arial", 11)
    ).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    
    email_entry = tkinter.Entry(
        forgot_frame,
        font=("Arial", 10),
        width=25,
        bd=2,
        relief="solid"
    )
    email_entry.grid(row=1, column=1, pady=10, sticky="w")
    
    tkinter.Label(
        forgot_frame,
        text="New Password:",
        bg="#DBCECE",
        font=("Arial", 11)
    ).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    
    new_pass_entry = tkinter.Entry(
        forgot_frame,
        show="*",
        font=("Arial", 10),
        width=25,
        bd=2,
        relief="solid"
    )
    new_pass_entry.grid(row=2, column=1, pady=10, sticky="w")
    
    tkinter.Label(
        forgot_frame,
        text="Confirm Password:",
        bg="#DBCECE",
        font=("Arial", 11)
    ).grid(row=3, column=0, sticky="e", padx=10, pady=10)
    
    confirm_pass_entry = tkinter.Entry(
        forgot_frame,
        show="*",
        font=("Arial", 10),
        width=25,
        bd=2,
        relief="solid"
    )
    confirm_pass_entry.grid(row=3, column=1, pady=10, sticky="w")
      # Security Question Display
    tkinter.Label(
        forgot_frame,
        text="Security Question:",
        bg="#DBCECE",
        font=("Arial", 11, "bold")
    ).grid(row=4, column=0, columnspan=2, pady=(15, 5))
    
    tkinter.Label(
        forgot_frame,
        text="Favourite Teacher?",
        bg="#DBCECE",
        font=("Arial", 10, "italic"),
        fg="#555555"
    ).grid(row=5, column=0, columnspan=2, pady=(0, 10))
    
    # Security Answer
    tkinter.Label(forgot_frame, text="Answer:", bg="#DBCECE", font=("Arial", 11)).grid(row=6, column=0, sticky="e", padx=10, pady=10)
    answer_entry = tkinter.Entry(forgot_frame, font=("Arial", 10), width=25, bd=2, relief="solid")
    answer_entry.grid(row=6, column=1, pady=10, sticky="w")
    
    
    def handle_reset():
        email = email_entry.get()
        new_password = new_pass_entry.get()
        confirm_password = confirm_pass_entry.get()
        answer = answer_entry.get()
        
        if not email or not new_password or not confirm_password or not answer:
            messagebox.showwarning("Input Error", "Please fill in all fields") #check if all fields are utilised 
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match") #both passwords have to match
            return
        
        success, message = backend.forgot_password(email, new_password,answer) #calls forgot_password function in backend file - output of function is a tuple 
        
        if success: #boolean
            messagebox.showinfo("Success", message)
            forgot_win.destroy() #close forget window screen 
        else:
            messagebox.showerror("Error", message)
    
    tkinter.Button(
        forgot_frame,
        text="RESET PASSWORD",
        bg="#0C6D99",
        fg="white",
        font=("Arial", 10, "bold"),
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=handle_reset # calls haandle reset function above once user presses forgot password button 
    ).grid(row=7, column=0, columnspan=2, pady=(20, 0))
    
    tkinter.Button(
        forgot_win,
        text="BACK",
        bg="#A4C639",
        fg="white",
        font=("Arial", 10, "bold"),
        width=12,
        height=2,
        bd=0,
        cursor="hand2",
        command=forgot_win.destroy
    ).place(x=30, y=330)

def open_book_appointment(user_id):
    #book appointment window creation
    book_win = tkinter.Toplevel()
    book_win.title("Book Appointment")
    book_win.geometry("500x500")
    book_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        book_win,
        text="Book Appointment",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    tkinter.Label(
        book_win,
        text="Select Date:",
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=10)
    
    cal = Calendar(
        book_win,
        selectmode='day', #allow the user to choose a day 
        date_pattern='yyyy-mm-dd',
        mindate=datetime.date.today() #tkcalender function to get relevant date 
    )
    cal.pack(pady=10)
    
    def next_step():
        selected_date = cal.get_date() #gets user input 
        book_win.destroy() #destroys window leading to the show service function below 
        show_service_and_time_selection(user_id, selected_date)
    
    tkinter.Button(
        book_win,
        text="CONTINUE",
        bg="#0C6D99",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        command=next_step #runs next step when continue button pressed 
    ).pack(pady=20)

def show_service_and_time_selection(user_id, selected_date):
    #window creation
    slot_win = tkinter.Toplevel()
    slot_win.title("Select Service and Time")
    slot_win.geometry("450x450")
    slot_win.configure(bg="#DBCECE")
    #shows selected date 
    tkinter.Label(
        slot_win,
        text=f"Date: {selected_date}",
        font=("Arial", 14, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    #label to show select service
    tkinter.Label(
        slot_win,
        text="Select Service:",
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=5)
    
    services = backend.get_services() #calls function in backend to get all available services from database
    service_var = tkinter.StringVar() #stores the selected service in a variable 
    
    service_menu = tkinter.ttk.Combobox(
        slot_win,
        textvariable=service_var,
        state="readonly",#can only select,not change 
        width=25
    )
    
    service_names = [] #1d array for service name
    service_ids = [] # 1d array for service id 
    
    for service in services:
        service_id = service[0] #get service id 
        service_name = service[1] #get service name 
        service_names.append(service_name) #adds to array
        service_ids.append(service_id)#adds tp array 
    
    service_menu['values'] = service_names #content of menu contains service name so user can choose 
    service_menu.pack(pady=10)
    if service_names:
        service_menu.current(0) #automatically on first service
    
    tkinter.Label(
        slot_win,
        text="Select Time:",
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=15)
    
    time_var = tkinter.StringVar() #stores time in variable 
    time_menu = tkinter.ttk.Combobox(
        slot_win,
        textvariable=time_var,
        state="readonly", #only can select
        width=25
    )
    
    available_times = backend.get_available_slots(selected_date) #gets slot from database 
    time_menu['values'] = available_times # menu for all available times
    time_menu.pack(pady=10)
    if available_times:
        time_menu.current(0) #automatically first time if nothing selected 
    
    def book_now():
        #gets user selection for time and service
        selected_service = service_var.get() 
        selected_time = time_var.get()
        #all fields must be used 
        if not selected_service or not selected_time:
            messagebox.showwarning("Error", "Please select service and time")
            return
        
        service_index = service_names.index(selected_service)
        service_id = service_ids[service_index]
        
        #calls backend funcion to append data to database 
        success, message = backend.book_appointment(user_id, service_id, selected_date, selected_time) 
        
        if success:
            messagebox.showinfo("Success", message)
            slot_win.destroy() #closes slot window
        else:
            messagebox.showerror("Error", message)
    
    tkinter.Button(
        slot_win,
        text="CONFIRM BOOKING",
        bg="#A4C639",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        command=book_now #calls book now function when button pressed 
    ).pack(pady=30)

def open_patient_dashboard(user_id,name):
    backend.attended_appointments() #updates status of appointments 
    #window creation for patient dash 
    dashboard_win = tkinter.Tk()
    dashboard_win.title("Patient Dashboard")
    dashboard_win.geometry("700x450")
    dashboard_win.configure(bg="#E8E8E8")
    
    tkinter.Label( #title
        dashboard_win,
        text="Patient Dashboard", 
        font=("Arial", 16, "bold"),
        bg="#E8E8E8",
        fg="#003366"
    ).pack(anchor="nw", padx=20, pady=20)
    
    try:
        logo_photo = tkinter.PhotoImage(file="moins.png") #logo
        logo_label = tkinter.Label(dashboard_win, image=logo_photo, bg="#4F7302")
        logo_label.image = logo_photo
        logo_label.place(x=520, y=60, width=130, height=130)
    except:
        pass
    
    tkinter.Label(
        dashboard_win,
        text="Welcome Patient",
        font=("Arial", 18, "bold"),
        bg="#E8E8E8",
        fg="#000000"
    ).place(x=260, y=80)
    
    tkinter.Label(
        dashboard_win,
        text="View Services",
        font=("Arial", 10, "underline"),
        bg="#E8E8E8",
        fg="#000000",
        cursor="hand2"
    ).place(x=280, y=120)
    
    button_frame = tkinter.Frame(dashboard_win, bg="white", relief="solid", bd=2)
    button_frame.place(x=205, y=155, width=215, height=280)
    
    tkinter.Button(
        button_frame,
        text="Book Appointment",
        bg="#6B8E23",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: open_book_appointment(user_id) # calls function once user interacts with book appointment button
    ).pack(pady=(20, 8))
    
    tkinter.Button(
        button_frame,
        text="View Upcoming",
        bg="#DC143C",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: view_upcoming_appointments(user_id) # calls function once user interacts with view upcoming button
    ).pack(pady=8)
    
    tkinter.Button(
        button_frame,
        text="Cancel Appointment",
        bg="#00CED1",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: cancel_appointment(user_id) # calls function once user interacts with cancel appointment button
    ).pack(pady=8)
    
    tkinter.Button(
        button_frame,
        text="View History",
        bg="#8B7BB8",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: view_previous_appointments(user_id) # calls function once user interacts with view appointment history button
    ).pack(pady=8)
    
    tkinter.Button(
        dashboard_win,
        text="LOG OUT",
        bg="#9ACD32",
        fg="black",
        font=("Arial", 10, "bold"),
        width=10,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: logout(dashboard_win) #closes window 
    ).place(x=70, y=420)
    
    dashboard_win.mainloop()

def open_staff_dashboard(user_id, name):
    #window creation 
    staff_win = tkinter.Tk()
    staff_win.title("Admin Dashboard")
    staff_win.geometry("700x550")
    staff_win.configure(bg="#E8E8E8")
    
    tkinter.Label(
        staff_win,
        text="Admin Dashboard",#title 
        font=("Arial", 16, "bold"),
        bg="#E8E8E8",
        fg="#003366"
    ).pack(anchor="nw", padx=20, pady=20)
    
    try:
        logo_photo = tkinter.PhotoImage(file="moins.png")
        logo_label = tkinter.Label(staff_win, image=logo_photo, bg="#4F7302")#logo
        logo_label.image = logo_photo
        logo_label.place(x=520, y=60, width=130, height=130)
    except:
        pass
    
    tkinter.Label(
        staff_win,
        text="Welcome Admin",#title
        font=("Arial", 18, "bold"),
        bg="#E8E8E8",
        fg="#000000"
    ).place(x=260, y=80)
    
    tkinter.Label(
        staff_win,
        text="View Services",#title
        font=("Arial", 10, "underline"),
        bg="#E8E8E8",
        fg="#000000",
        cursor="hand2",
    ).place(x=280, y=120)
    
    button_frame = tkinter.Frame(staff_win, bg="white", relief="solid", bd=2)
    button_frame.place(x=205, y=155, width=215, height=320)
    
    tkinter.Button(
        button_frame,
        text="View Appointments",
        bg="#6B8E23",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=view_all_appointments_staff #runs when button is pressed
    ).pack(pady=(20, 8))
    
    tkinter.Button(
        button_frame,
        text="Add Service",
        bg="#DC143C",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=add_service_window #runs when button is pressed
    ).pack(pady=8)
    
    tkinter.Button(
        button_frame,
        text="Remove Service",
        bg="#00CED1",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=remove_service_window #runs when button is pressed
    ).pack(pady=8)
    
    tkinter.Button(
        button_frame,
        text="Cancel Appointment",
        bg="#FF8C00",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        command=cancel_appointment_staff_window #runs when button is pressed
    ).pack(pady=8)

       
    tkinter.Button(
        button_frame,
        text="Add Staff Account",
        bg="#8B4789",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        command=staff_account_creation_window
    ).pack(pady=(8,15))
    
    
    tkinter.Button(
        staff_win,
        text="LOG OUT",
        bg="#9ACD32",
        fg="black",
        font=("Arial", 10, "bold"),
        width=10,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: logout(staff_win) #runs when button is pressed
    ).place(x=70, y=370)
    
    staff_win.mainloop()


def view_all_services():
    services = backend.get_services()
    
    view_win = tkinter.Toplevel()
    view_win.title("All Services")
    view_win.geometry("500x400")
    view_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        view_win,
        text="All Services",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    if not services:
        tkinter.Label(
            view_win,
            text="No services available",
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
    else:
        for service in services:
            service_id = service[0]
            service_name = service[1]
            
            tkinter.Label(
                view_win,
                text=f"ID: {service_id}  |  Service: {service_name}",
                font=("Arial", 10),
                bg="#DBCECE"
            ).pack(pady=5)


def view_all_appointments_staff():
    appointments = backend.all_appointments() #function gets all appoitnments with 'booked status'
    #window creation
    view_win = tkinter.Toplevel()
    view_win.title("All Appointments")
    view_win.geometry("700x500")
    view_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        view_win,
        text="All Appointments", #title 
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    if not appointments:
        tkinter.Label(
            view_win,
            text="No appointments found",#returns this when no appointments are 'booked'
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
    else:
        for appointment in appointments:
            appointment_id = appointment[0] #found at index 0 in 1D array 
            patient_name = appointment[1] #found at index 1 in 1D array 
            service_name = appointment[2] #found at index 2 in 1D array 
            date = appointment[3] #found at index 3 in 1D array 
            time = appointment[4] #found at index 4 in 1D array 
            
            tkinter.Label(
                view_win,
                text=f"ID: {appointment_id} | Patient: {patient_name} | Service: {service_name} | Date: {date} | Time: {time}",
                #shown on interface if appointment found
                font=("Arial", 9),
                bg="#DBCECE"
            ).pack(pady=3)


def add_service_window():
    #window creation
    add_win = tkinter.Toplevel()
    add_win.title("Add Service")
    add_win.geometry("400x250")
    add_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        add_win,
        text="Add New Service", #title
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    tkinter.Label(
        add_win,
        text="Service Name:", #label
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=5)
    
    service_entry = tkinter.Entry(add_win, font=("Arial", 11), width=30)
    service_entry.pack(pady=10)
    
    def add_now():
        service_name = service_entry.get() #gets name entered by staff user
        if not service_name:
            messagebox.showwarning("Error", "Please enter service name") #if left empty, output this 
            return
        
        success, message = backend.add_service(service_name)
        if success:#sucess = true or false 
            messagebox.showinfo("Success", message) #if true 
            add_win.destroy()
        else:
            messagebox.showerror("Error", message) #if false 
    
    tkinter.Button(
        add_win,
        text="ADD SERVICE",
        bg="#0C6D99",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        command=add_now
    ).pack(pady=20)


def remove_service_window():
    #window creation
    remove_win = tkinter.Toplevel()
    remove_win.title("Remove Service")
    remove_win.geometry("400x300")
    remove_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        remove_win,
        text="Remove Service", #title 
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    services = backend.get_services() #gets services from table in database 
    
    if not services:
        tkinter.Label(
            remove_win,
            text="No services to remove", #if no services, output this 
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
        return
    
    tkinter.Label(
        remove_win,
        text="Select Service to Remove:", #title 
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=10)
    
    service_var = tkinter.StringVar()
    service_menu = tkinter.ttk.Combobox( #provides menu for user
        remove_win,
        textvariable=service_var,
        state="readonly", #user can only select, not change 
        width=30
    )
    
    service_dict = {} #maps service display name to ids 
    service_names = [] #holds services name for menu 
    
    for service in services:
        service_id = service[0] #id found at index 0 
        service_name = service[1] # id found at index 1 
        display_name = f"{service_name} (ID: {service_id})"
        service_names.append(display_name) #menu content 
        service_dict[display_name] = service_id
    
    service_menu['values'] = service_names #menu values = services names 
    service_menu.pack(pady=10)
    if service_names:
        service_menu.current(0) #if there is 1 or more services, current is first value 
    
    def remove_now():
        selected = service_var.get() #selected service to remove 
        if not selected:
            messagebox.showwarning("Error", "Please select a service") #nothing selected 
            return
        
        service_id = service_dict[selected] #gets service id 
        
        success, message = backend.delete_service(service_id) #passes id into delete service function
        if success:
            messagebox.showinfo("Success", message) #success = true 
            remove_win.destroy() #closes window 
        else:
            messagebox.showerror("Error", message) #success = false 
    
    tkinter.Button(
        remove_win,
        text="REMOVE SERVICE",
        bg="#DC143C",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        command=remove_now #when button is pressed
    ).pack(pady=20)

def cancel_appointment_staff_window():
    #window creation
    cancel_win = tkinter.Toplevel()
    cancel_win.title("Cancel Appointment")
    cancel_win.geometry("400x250")
    cancel_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        cancel_win,
        text="Cancel Appointment", #title 
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    tkinter.Label(
        cancel_win,
        text="Appointment ID:", #title 
        font=("Arial", 11),
        bg="#DBCECE"
    ).pack(pady=5)
    
    appointment_id_entry = tkinter.Entry(cancel_win, font=("Arial", 11), width=30) #allows user to enter app id 
    appointment_id_entry.pack(pady=10)
    
    def cancel_now():
        appointment_id = appointment_id_entry.get() #gets user entry
        if not appointment_id:
            messagebox.showwarning("Error", "Please enter appointment ID") #if nothing entered
            return
        
        success, message = backend.staff_cancel(appointment_id) #passes user entry into this function
        if success: 
            messagebox.showinfo("Success", message) #success = true 
            cancel_win.destroy() #close window 
        else:
            messagebox.showerror("Error", message) #success = false 
    
    tkinter.Button(
        cancel_win,
        text="CANCEL APPOINTMENT",
        bg="#FF8C00",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18,
        height=2,
        command=cancel_now #runs when button pressed 
    ).pack(pady=20)


def view_upcoming_appointments(user_id):
    appointments = backend.upcoming_appointments(user_id) #calls upcoming appointments function in backend 
    #tkinter window creation 
    view_win = tkinter.Toplevel()
    view_win.title("Upcoming Appointments")
    view_win.geometry("600x400")
    view_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        view_win,
        text="Upcoming Appointments",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    if not appointments:
        tkinter.Label(
            view_win,
            text="No upcoming appointments",#if appointments variable is empty - print no upcoming 
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
    else:
        for appointment in appointments:
            date = appointment[3] #date in index 3 
            time = appointment[4] #time in index 4 
            
            frame = tkinter.Frame(view_win, bg="white", relief="solid", bd=1)
            frame.pack(pady=5, padx=20, fill="x")
            
            tkinter.Label(
                frame,
                text=f"Date: {date}  |  Time: {time}", #date and time as a label 
                font=("Arial", 10),
                bg="white"
            ).pack(side="left", padx=10, pady=10)

def cancel_appointment(user_id):
    appointments = backend.upcoming_appointments(user_id) #calls upcoming appointments function in backend 
    #tkinter window creation 
    view_win = tkinter.Toplevel()
    view_win.title("Upcoming Appointments")
    view_win.geometry("600x400")
    view_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        view_win,
        text="Upcoming Appointments",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    if not appointments:
        tkinter.Label(
            view_win,
            text="No upcoming appointments",#if appointments variable is empty - print no upcoming 
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
    else:
        for appointment in appointments:
            appointment_id = appointment[0]
            date = appointment[3] #date in index 3 
            time = appointment[4] #time in index 4 
            
            frame = tkinter.Frame(view_win, bg="white", relief="solid", bd=1)
            frame.pack(pady=5, padx=20, fill="x")
            
            tkinter.Label(
                frame,
                text=f"Date: {date}  |  Time: {time}", #date and time as a label 
                font=("Arial", 10),
                bg="white"
            ).pack(side="left", padx=10, pady=10)
            
            tkinter.Button( 
                frame, 
                text="CANCEL", 
                bg="red", 
                fg="white", 
                font=("Arial", 9), 
                command=lambda aid=appointment_id: cancel_and_refresh(aid, view_win, user_id) 
            ).pack(side="right", padx=10) 

                   
def cancel_and_refresh(appointment_id, window, user_id):
    success, message = backend.cancel_appointment(appointment_id)
    if success:
        messagebox.showinfo("Success", message)
        window.destroy()
        view_upcoming_appointments(user_id)
    else:
        messagebox.showerror("Error", message)

def view_previous_appointments(user_id):
    appointments = backend.previous_appointments(user_id) #runs the bfunction from backend to get all appointments from database 
    #tkinter window creation
    view_win = tkinter.Toplevel()
    view_win.title("Previous Appointments")
    view_win.geometry("600x400")
    view_win.configure(bg="#DBCECE")
    
    tkinter.Label(
        view_win,
        text="Previous Appointments",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    if not appointments:#if no appointments previously 
        tkinter.Label(
            view_win,
            text="No previous appointments",#output
            font=("Arial", 11),
            bg="#DBCECE"
        ).pack(pady=20)
    else:
        for appointment in appointments:
            date = appointment[3] #date in appointment index 3 
            time = appointment[4] #time in appointment index 4 
            status = appointment[5]#status in appointment index 5 
            
            tkinter.Label(
                view_win,
                text=f"Date: {date}  |  Time: {time}  |  Status: {status}", #layout on interface in the form of a label
                font=("Arial", 10),
                bg="#DBCECE"
            ).pack(pady=5)
def staff_account_creation_window():
    #tkinter window creation 
    staff_account_win = tkinter.Toplevel()
    staff_account_win.title("Upcoming Appointments")
    staff_account_win.geometry("600x400")
    staff_account_win.configure(bg="#DBCECE")

    tkinter.Label(
        staff_account_win,
        text="Create Staff Account",
        font=("Arial", 16, "bold"),
        bg="#DBCECE"
    ).pack(pady=20)
    
    tkinter.Label(staff_account_win , text="Name:", bg="#DBCECE").pack(pady=5)
    name_entry = tkinter.Entry(staff_account_win , font=("Arial", 11), width=30)
    name_entry.pack(pady=5)
    
    tkinter.Label(staff_account_win , text="Email:", bg="#DBCECE").pack(pady=5)
    email_entry = tkinter.Entry(staff_account_win , font=("Arial", 11), width=30)
    email_entry.pack(pady=5)
    
    tkinter.Label(staff_account_win , text="Password:", bg="#DBCECE").pack(pady=5)
    password_entry = tkinter.Entry(staff_account_win , show="*", font=("Arial", 11), width=30)
    password_entry.pack(pady=5)

    def create_staff():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        
        success, message = backend.create_account(email, password, name, "Staff")
        if success:
            messagebox.showinfo("Success", "Staff account created")
            staff_account_win.destroy()
        else:
            messagebox.showerror("Error", message)
    
    tkinter.Button(
        staff_account_win,
        text="CREATE STAFF ACCOUNT",
        bg="#0C6D99",
        fg="white",
        font=("Arial", 10, "bold"),
        width=20,
        height=2,
        command=create_staff
    ).pack(pady=20)
    


def logout(current_window):
    current_window.destroy()

login_button = tkinter.Button(
    frame,
    text="LOGIN",
    bg="#A4C639",
    fg="white",
    font=("Arial", 11, "bold"),
    width=30,
    height=2,
    bd=0,
    cursor="hand2",
    activebackground="#8FB021",
    activeforeground="white",
    command=lambda: handle_login()
)

register_button = tkinter.Button(
    frame,
    text="REGISTER",
    bg="#0C6D99",
    fg="white",
    font=("Arial", 11, "bold"),
    width=30,
    height=2,
    bd=0,
    cursor="hand2",
    activebackground="#0A5A7F",
    activeforeground="white",
    command=open_register
)

forgot_button = tkinter.Button(
    frame,
    text="FORGOT PASSWORD",
    bg="#0C6D99",
    fg="white",
    font=("Arial", 11, "bold"),
    width=30,
    height=2,
    bd=0,
    cursor="hand2",
    activebackground="#0A5A7F",
    activeforeground="white",
    command=open_forgot_password
)

login_label.grid(row=0, column=0, columnspan=2, pady=(50, 30), padx=20)
email_label.grid(row=1, column=0, sticky="e", padx=(50, 10), pady=12)
email_entry.grid(row=1, column=1, sticky="w", pady=12)
password_label.grid(row=2, column=0, sticky="e", padx=(50, 10), pady=12)
password_entry.grid(row=2, column=1, sticky="w", pady=12)
login_button.grid(row=3, column=0, columnspan=2, pady=(30, 8))
register_button.grid(row=4, column=0, columnspan=2, pady=8)
forgot_button.grid(row=5, column=0, columnspan=2, pady=8)

frame.pack(expand=True)

window.bind('<Return>', lambda event: handle_login())

window.mainloop()