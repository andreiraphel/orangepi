import serial
import adafruit_fingerprint

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_fingerprint():
    finger_test = finger.get_image()
    print(finger_test)

def search_fingerprint():
    """Search for a matching fingerprint in the database."""
    print("Place your finger on the sensor for matching...")

    # Step 1: Capture and convert a new fingerprint to a template
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Failed to capture fingerprint image.")
        return None

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image to template.")
        return None

    # Step 2: Retrieve the new template data
    new_template_packet = finger.get_fpdata(sensorbuffer="char")
    if not new_template_packet:
        print("Failed to retrieve the new fingerprint template.")
        return None

    # Convert the packet to bytes
    new_template_bytes = bytes(new_template_packet)

    # Step 3: Fetch all stored fingerprints from the database
    cursor.execute("SELECT id, template FROM fingerprints")
    fingerprints = cursor.fetchall()

    for fingerprint_id, template_base64 in fingerprints:
        # Decode the stored template from Base64
        stored_template_bytes = base64.b64decode(template_base64)

        # Compare the stored template with the newly captured template
        if stored_template_bytes == new_template_bytes:
            print("Fingerprint matched!")
            return fingerprint_id

    return None


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
       print(cursor.execute("SELECT id, template FROM fingerprints"))
       print(cursor.fetchall())
    elif command == "0":
        break

# Close the database connection
conn.close()
