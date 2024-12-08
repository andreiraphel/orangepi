import serial
import adafruit_fingerprint

# Initialize UART connection
uart = serial.Serial("/dev/ttyS1", baudrate=57600, timeout=1)

# Create a fingerprint sensor object
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Check if the sensor is working
if finger.read_templates() == adafruit_fingerprint.OK:
    print(f"Fingerprint templates available: {finger.templates}")
else:
    print("Failed to read templates from AS608!")

# Add more functionality, like enrolling or searching fingerprints
def get_fingerprint_count():
    if finger.count_templates() == adafruit_fingerprint.OK:
        print(f"Fingerprints stored: {finger.template_count}")
    else:
        print("Failed to get fingerprint count.")

get_fingerprint_count()
