import serial
import adafruit_fingerprint
import sqlite3
import base64

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Initialize SQLite Database
conn = sqlite3.connect("fingerprint.db")
cursor = conn.cursor()

# Create a table to store fingerprints
cursor.execute("""
CREATE TABLE IF NOT EXISTS fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template BLOB NOT NULL
)
""")
conn.commit()

def enroll_fingerprint():
    """Enroll a fingerprint and store it in the database."""
    print("Place your finger on the sensor...")

    # Step 1: Capture the fingerprint image
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Failed to capture fingerprint image.")
        return False

    # Step 2: Convert image to a template
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image to template.")
        return False

    # Step 3: Store the template in the sensor
    if finger.store_model(1) != adafruit_fingerprint.OK:
        print("Failed to store fingerprint in sensor.")
        return False

    # Step 4: Retrieve the template data from the sensor
    template_packet = finger.get_fpdata(sensorbuffer="char")
    if not template_packet:
        print("Failed to retrieve the fingerprint template.")
        return False

    # Convert the template packet to bytes for storage
    template_bytes = bytes(template_packet)

    # Encode the binary data as Base64
    template_base64 = base64.b64encode(template_bytes).decode("utf-8")

    # Insert the encoded template into the SQLite database
    cursor.execute("INSERT INTO fingerprints (template) VALUES (?)", (template_base64,))
    conn.commit()

    print("Fingerprint enrolled successfully.")
    print(template_base64)
    return True

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
        stored_template_packet = list(stored_template_bytes)

        # Send the stored template to the sensor for comparison
        if finger.send_fpdata(stored_template_packet, sensorbuffer="char") != adafruit_fingerprint.OK:
            print(f"Failed to send stored template for fingerprint ID {fingerprint_id}.")
            continue

        # Compare with the new template
        match_result = finger.template_2_compare()
        if match_result == adafruit_fingerprint.OK:
            print(f"Fingerprint matched with ID {fingerprint_id}.")
            return fingerprint_id
        elif match_result == adafruit_fingerprint.NOMATCH:
            continue
        else:
            print(f"Error comparing fingerprint ID {fingerprint_id}.")

    print("No matching fingerprint found.")
    return None

while True:
    command = input("Enter 'enroll' to enroll, 'search' to find, or 'exit' to quit: ").strip().lower()
    if command == "enroll":
        if enroll_fingerprint():
            print("Enrollment successful.")
    elif command == "search":
        match = search_fingerprint()
        if match:
            print(f"Fingerprint found in database with ID {match}.")
        else:
            print("Fingerprint not found.")
    elif command == "exit":
        break

# Close the database connection
conn.close()
