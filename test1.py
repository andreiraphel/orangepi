import serial

# Test different baud rates
baud_rates = [9600, 19200, 38400, 57600, 115200]

for baud in baud_rates:
    print(f"Testing baud rate: {baud}")
    try:
        ser = serial.Serial('/dev/ttyS1', baudrate=baud, timeout=1)

        if ser.is_open:
            print(f"UART1 open at {baud}. Sending handshake...")
            handshake_command = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
            ser.write(handshake_command)

            response = ser.read(12)
            print(f"Response at {baud}: {response}")
            if response:
                print(f"AS608 responded at {baud} baud rate!")
                break
        ser.close()
    except Exception as e:
        print(f"Error at {baud}: {e}")
