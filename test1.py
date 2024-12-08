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
    
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Failed to capture fingerprint image.")
        return False
    
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image to template.")
        return False
    
    # Save the fingerprint template in the sensor
    if finger.store_model(1) != adafruit_fingerprint.OK:
        print("Failed to store fingerprint in sensor.")
        return False
    
    # Retrieve the template from the sensor
    if finger.load_model(1) != adafruit_fingerprint.OK:
        print("Failed to load fingerprint model from sensor.")
        return False

    packet = finger.get_fpdata(sensorbuffer="char")
    if not packet:
        print("Failed to get fingerprint data.")
        return False

    # Convert the list of integers to bytes
    template_bytes = bytes(packet)
    
    # Convert the binary data to base64 for storage
    template_base64 = base64.b64encode(template_bytes).decode("utf-8")
    
    # Insert into the SQL database
    cursor.execute("INSERT INTO fingerprints (template) VALUES (?)", (template_base64,))
    conn.commit()
    print("Fingerprint enrolled and saved in the database.")
    return True

def search_fingerprint():
    """Search for a matching fingerprint in the database."""
    print("Place your finger on the sensor for matching...")
    
    # Capture the new fingerprint
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Failed to capture fingerprint image.")
        return None
    
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image to template.")
        return None
    
    # Retrieve the new template data
    new_template_packet = finger.get_fpdata(sensorbuffer="char")
    if not new_template_packet:
        print("Failed to retrieve the new fingerprint data.")
        return None

    new_template_bytes = bytes(new_template_packet)
    
    # Fetch all stored templates from the database
    cursor.execute("SELECT id, template FROM fingerprints")
    fingerprints = cursor.fetchall()
    
    for fingerprint_id, template_base64 in fingerprints:
        # Decode the stored template from Base64
        stored_template_bytes = base64.b64decode(template_base64)
        
        # Convert stored template bytes back to a list of integers
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
            print(f"No match for fingerprint ID {fingerprint_id}.")
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
