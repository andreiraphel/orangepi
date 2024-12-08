import serial
import adafruit_fingerprint

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_fingerprint():
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Not found")
    else:
        finger.image_2_tz(1)
        finger.create_model()
        finger.store_model(1)

def search_fingerprint():
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Not found")
    else:
        finger.image_2_tz(1)
        finger.create_model()
        finger.finger_fast_search()

while True:
    command = input("Enter '1' to enroll, '2' to find, '3' - database,  or '0' to quit: ").strip().lower()
    if command == "1":
        if enroll_fingerprint():
            print("Enrollment successful.")
    elif command == "2":
        s_finger = search_fingerprint()
        if s_finger != None:
            print(f"Fingerprint found in database with ID {s_finger}.")
        else:
            print("Fingerprint not found.")
    elif command == "3":
       finger.soft_reset()
    elif command == "0":
        break
