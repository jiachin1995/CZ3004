from arduino import Arduino

if __name__ == '__main__':
    serial = Arduino(port="/dev/virtual-tty")
    serial.connect()
    try:
        msg = input("Enter msg to send: ")
        print("[@] Writing to Arduino: {}".format(msg))
        serial.write(msg)
        msg = serial.read()
        print("[@] Got from Arduino: {}".format(msg))
        print("[@] Closing socket.")
        # serial.close()
    except Exception as e:
        print(e)