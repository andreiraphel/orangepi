import serial

# Open UART1
ser = serial.Serial('/dev/ttyS1', baudrate=57600, timeout=1)

if ser.is_open:
    print("UART1 is open. Communicating with AS608...")

    # Handshake command for AS608
    handshake_command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
    ser.write(handshake_command)

    # Read the response
    response = ser.read(12)  # Expected response length
    print("Handshake Response:", response)

    if response.startswith(b'\xEF\x01'):  # Check if it's a valid response
        print("AS608 Handshake successful!")
    else:
        print("Unexpected response from AS608.")
else:
    print("Failed to open UART1.")
ser.close()
