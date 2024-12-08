import serial

# Initialize UART1 for AS608
ser = serial.Serial('/dev/ttyS1', baudrate=57600, timeout=1)

if ser.is_open:
    print("UART1 is open. Communicating with AS608...")

    # Send 'Handshake' command to AS608
    # This is an example command in AS608 protocol
    handshake_command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
    ser.write(handshake_command)

    # Read response from AS608
    response = ser.read(12)  # Adjust byte count as needed for the response
    print("Response from AS608:", response)

    if response:
        print("Communication with AS608 successful!")
    else:
        print("No response from AS608. Check connections or power.")
else:
    print("Failed to open UART1.")
ser.close()
