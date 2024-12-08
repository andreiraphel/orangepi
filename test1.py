import serial

# Replace 'ttyS1' with your UART port
ser = serial.Serial('/dev/ttyS1', baudrate=57600, timeout=1)

if ser.is_open:
    print("UART1 is open. Testing loopback...")
    test_data = b"Hello, UART1!"
    ser.write(test_data)

    # Read back the sent data
    response = ser.read(len(test_data))
    if response == test_data:
        print("Loopback successful. UART1 is working!")
    else:
        print("Loopback failed. Check connections or device.")
else:
    print("Failed to open UART1.")
ser.close()
