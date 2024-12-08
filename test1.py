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
        return
    
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image to template.")
        return
    
    # Save the fingerprint template in the sensor
    if finger.store_model(1) != adafruit_fingerprint.OK:
        print("Failed to store fingerprint in sensor.")
        return
    
    # Retrieve the template from the sensor
    if finger.load_model(1) != adafruit_fingerprint.OK:
        print("Failed to load fingerprint model from sensor.")
        return

    packet = finger.get_fpdata(sensorbuffer="char")
    if not packet:
        print("Failed to get fingerprint data.")
        return
    
    # Convert the binary data to base64 for storage
    template_base64 = base64.b64encode(packet).decode("utf-8")
    
    # Insert into the SQL database
    cursor.execute("INSERT INTO fingerprints (template) VALUES (?)", (template_base64,))
    conn.commit()
    print("Fingerprint enrolled and saved in the database.")

while True:
    command = input("Enter 'enroll' to enroll a fingerprint or 'exit' to quit: ").strip().lower()
    if command == "enroll":
        enroll_fingerprint()
    elif command == "exit":
        break

# Close the database connection
conn.close()
