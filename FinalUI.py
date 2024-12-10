import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.geometry("480x320")  # Set the resolution
root.title("Attendance Checker")

password = "password"

# Add a label
attendance_label = tk.Label(
    root, 
    text = "Attendance Checker", 
    font = ("Arial", 18)
)

admin_login_button = tk.Button(
    root, 
    text = "Log In", 
    font = ("Arial", 12), 
    command = lambda: LoginPage()
)

scan_button = tk.Button(
    root, 
    text = "Scan", 
    font = ("Arial", 12),
    height = 5,
    width = 20,
    command = lambda: ScanPage()
)

login_label = tk.Label(
    root, 
    text = "Log In", 
    font = ("Arial", 18)
)

backtoMain = tk.Button(
    root, 
    text = "Back", 
    font = ("Arial", 12), 
    command = lambda: MainPage()
)

backtoAdmin = tk.Button(
    root, 
    text = "Back", 
    font = ("Arial", 12), 
    command = lambda: AdminPanel()
)

passkey_entry = tk.Entry(
    root, 
    font = ("Arial", 12)
)

passkey_label = tk.Label(
    root,
    text = "Enter Passkey:",
    font = ("Arial", 12)
)

submit_passkey_button = tk.Button(
    root, 
    text = "Submit", 
    font = ("Arial", 12), 
    command = lambda: submitpasskey()
)

admin_label = tk.Label(
    root, 
    text = "Admin Panel", 
    font = ("Arial", 18)
)

enroll_button = tk.Button(
    root,
    text = "Enroll",
    font = ("Arial", 12),
    width = 10,
    command = lambda: EnrollPage() 
)

delete_button = tk.Button(
    root,
    text = "Delete Entry",
    font = ("Arial", 12),
    width = 10, 
    command = lambda: DeletePage()    
)

wrongpasskey = tk.Label(
    root,
    text = " > Wrong Password",
    font = ("Arial", 10),
)

enroll_label = tk.Label(
    root, 
    text = "Enroll", 
    font = ("Arial", 18)
)

delete_label = tk.Label(
    root, 
    text = "Delete Entry", 
    font = ("Arial", 18)
)

scan_label = tk.Label(
    root, 
    text = "Scan", 
    font = ("Arial", 18)
)

def empty():
    return

def submitpasskey():
    text = passkey_entry.get()
    
    if (text == password):
        AdminPanel()
        passkey_entry.delete(0, tk.END)
    else : wrongpasskey.place(relx = 0.0, rely = 1.0, anchor = "sw")

def MainPage():
    clear()
    attendance_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    admin_login_button.place(relx = 1.0, rely = 0.0, anchor = "ne")
    scan_button.place(relx = 0.5, rely = 0.5, anchor = "center")

def LoginPage():
    clear()
    login_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoMain.place(relx = 1.0, rely = 0.0, anchor = "ne")
    passkey_label.place(relx = 0.5, rely = 0.35, anchor = "center")
    passkey_entry.place(relx = 0.5, rely = 0.5, anchor = "center")
    submit_passkey_button.place(relx = 0.5, rely = 0.65, anchor = "center")
    
def AdminPanel():
    clear()
    admin_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoMain.place(relx = 1.0, rely = 0.0, anchor = "ne")
    enroll_button.place(relx = 0.5, rely = 0.20, anchor = "center")
    delete_button.place(relx = 0.5, rely = 0.35, anchor = "center")
    
def EnrollPage():
    clear()
    enroll_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoAdmin.place(relx = 1.0, rely = 0.0, anchor = "ne")
    
def DeletePage():
    clear()
    delete_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoAdmin.place(relx = 1.0, rely = 0.0, anchor = "ne")   
    
def ScanPage():
    clear()
    scan_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoMain.place(relx = 1.0, rely = 0.0, anchor = "ne")   
    

def clear():
    attendance_label.place_forget()
    admin_login_button.place_forget()
    scan_button.place_forget()
    login_label.place_forget()
    backtoMain.place_forget()
    passkey_entry.place_forget()
    passkey_label.place_forget()
    submit_passkey_button.place_forget()
    admin_label.place_forget()
    enroll_button.place_forget()
    delete_button.place_forget()
    wrongpasskey.place_forget()
    backtoAdmin.place_forget()
    enroll_label.place_forget()
    delete_label.place_forget()
    scan_label.place_forget()
    
# Run the Tkinter loop
MainPage()
root.mainloop() 
