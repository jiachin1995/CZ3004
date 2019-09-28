from android import Android

if __name__ == "__main__":
    android = Android()
    android.connect()
    while True:
        msg = android.read()
        if msg == None:
            continue
        print("[@] Got from Android: {}".format(msg))
        try:
            msg = input("Enter msg to send: ")
            print("[@] Writing to Bluetooth: {}".format(msg))
            android.write(msg)
            msg = android.read()
            print("[@] Got from Bluetooth: {}".format(msg))
            print("[@] Closing socket.")
            # android.close()
        except Exception as e:
            print(e)
