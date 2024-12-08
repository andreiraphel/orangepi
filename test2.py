import serial
import adafruit_fingerprint

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_fingerprint():
    """Enroll a new fingerprint."""
    print("Place your finger on the sensor...")
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Fingerprint not detected. Please try again.")
        return False
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Error processing fingerprint. Please try again.")
        return False

    print("Remove your finger and place it again.")
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Fingerprint not detected the second time. Please try again.")
        return False
    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        print("Error processing fingerprint the second time. Please try again.")
        return False

    if finger.create_model() != adafruit_fingerprint.OK:
        print("Failed to create a fingerprint model.")
        return False

    # Store the model in the next available slot
    position = 1  # Choose a valid position ID
    if finger.store_model(position) == adafruit_fingerprint.OK:
        print(f"Fingerprint successfully enrolled at position {position}.")
        return True
    else:
        print("Failed to store fingerprint.")
        return False

def search_fingerprint():
    """Search for a fingerprint."""
    print("Place your finger on the sensor...")
    if finger.get_image() != adafruit_fingerprint.OK:
        print("Fingerprint not detected.")
        return None
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Error processing fingerprint.")
        return None

    if finger.finger_fast_search() == adafruit_fingerprint.OK:
        print(f"Fingerprint found! ID: {finger.finger_id}, Confidence: {finger.confidence}")
        return finger.finger_id
    else:
        print("No match found.")
        return None

# Main loop
while True:
    command = input("Enter '1' to enroll, '2' to find, '3' to reset sensor, or '0' to quit: ").strip()
    if command == "1":
        if enroll_fingerprint():
            print("Enrollment successful.")
    elif command == "2":
        finger_id = search_fingerprint()
        if finger_id is not None:
            print(f"Fingerprint found in database with ID {finger_id}.")
    elif command == "3":
        if finger.soft_reset() == adafruit_fingerprint.OK:
            print("Sensor successfully reset.")
        else:
            print("Failed to reset sensor.")
    elif command == "0":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please enter '1', '2', '3', or '0'.")
