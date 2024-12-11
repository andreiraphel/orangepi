import tkinter as tk
import asyncio
import serial
import adafruit_fingerprint

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart) # type: ignore

# Initialize the main window
root = tk.Tk()
root.geometry("480x320")  # Set the resolution
root.title("Attendance Checker")

# Variables
password = "password"
enroll_main_text = ""
scan_main_text = ""

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

enroll_main = tk.Label(
    root, 
    text = enroll_main_text, 
    font = ("Arial", 18)
)

scan_main = tk.Label(
    root, 
    text = scan_main_text, 
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
    enroll_button.place(relx = 0.5, rely = 0.2, anchor = "center")
    delete_button.place(relx = 0.5, rely = 0.35, anchor = "center")
    
def EnrollPage():
    clear()
    enroll_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoAdmin.place(relx = 1.0, rely = 0.0, anchor = "ne")
    enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
    enroll_fingerprint()
    
def DeletePage():
    clear()
    delete_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoAdmin.place(relx = 1.0, rely = 0.0, anchor = "ne")   
    
def ScanPage():
    clear()
    scan_label.place(relx = 0.0, rely = 0.0, anchor = "nw")
    backtoMain.place(relx = 1.0, rely = 0.0, anchor = "ne")
    search_fingerprint()
    
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
    enroll_main.place_forget()
    scan_main.place_forget()
    
# Run the Tkinter loop
MainPage()
root.mainloop() 

'''
// Functions for Fingerprint
'''

"""Find the next available fingerprint slot."""
def find_empty_slot():
    for slot in range(1, 128):
        if finger.read_templates() == adafruit_fingerprint.OK:
            if slot not in finger.templates:
                return slot
    return None

"""Enroll a new fingerprint."""
async def enroll_fingerprint():
    global enroll_main_text
    enroll_main_text = "Place your finger on the sensor..."
    enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")

    await asyncio.sleep(2)
    enroll_main.place_forget()

    if finger.get_image() != adafruit_fingerprint.OK:
        enroll_main_text = "Fingerprint not detected. Please try again."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return
    
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        enroll_main_text = "Error processing fingerprint. Please try again."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return
    
    enroll_main_text = "Remove your finger and place it again."
    enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
    await asyncio.sleep(2)
    enroll_main.place_forget()
    
    if finger.get_image() != adafruit_fingerprint.OK:
        enroll_main_text = "Fingerprint not detected the second time. Please try again."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return
    
    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        enroll_main_text = "Error processing fingerprint the second time. Please try again."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return

    if finger.create_model() != adafruit_fingerprint.OK:
        enroll_main_text = "Failed to create a fingerprint model."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return

    position = find_empty_slot()
    if position is None:
        enroll_main_text = "No available slots for new fingerprints."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return

    if finger.store_model(position) == adafruit_fingerprint.OK:
        enroll_main_text = f"Fingerprint successfully enrolled at position {position}."
        enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        enroll_main.place_forget()
        return
    
    enroll_main_text = "Failed to store fingerprint."
    enroll_main.place(relx = 0.5, rely = 0.5, anchor = "center")
    await asyncio.sleep(2)
    enroll_main.place_forget()
    return

"""Search for a fingerprint."""
async def search_fingerprint():
    global scan_main_text
    scan_main_text = "Place your finger on the sensor..."
    scan_main.place(relx = 0.5, rely = 0.5, anchor = "center")
    await asyncio.sleep(2)
    scan_main.place_forget()
    
    if finger.get_image() != adafruit_fingerprint.OK:
        scan_main_text = "Fingerprint not detected."
        scan_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        scan_main.place_forget()    
        return None
    
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        scan_main_text = "Error processing fingerprint."
        scan_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        scan_main.place_forget()
        return None

    if finger.finger_fast_search() == adafruit_fingerprint.OK:
        scan_main_text = f"Fingerprint found! ID: {finger.finger_id}, Confidence: {finger.confidence}"
        scan_main.place(relx = 0.5, rely = 0.5, anchor = "center")
        await asyncio.sleep(2)
        scan_main.place_forget()
        return finger.finger_id
    
    scan_main_text = "No match found."
    scan_main.place(relx = 0.5, rely = 0.5, anchor = "center")
    await asyncio.sleep(2)
    scan_main.place_forget()
    return None

"""Delete a fingerprint by its ID."""
def delete_fingerprint(position):
    if finger.delete_model(position) == adafruit_fingerprint.OK:
        print(f"Fingerprint at position {position} successfully deleted.")
        return True
    else:
        print(f"Failed to delete fingerprint at position {position}.")
        return False

"""List all stored fingerprints."""
def list_fingerprints():
    if finger.read_templates() == adafruit_fingerprint.OK:
        print("Stored Fingerprints:", finger.templates)
    else:
        print("Failed to read templates.")
