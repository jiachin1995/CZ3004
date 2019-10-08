import serial
import time
import settings


class Arduino:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.baud_rate = 115200
        self.serial = None

    def connect(self):
        try:
            print("[@] Connecting to Serial..")
            self.serial = serial.Serial(self.port, self.baud_rate)
            time.sleep(3)
            print("[@] Serial link is connected")
        except Exception as e:
            print("[!] Unable to connect serial link.")
            print(e)

    def close(self):
        if self.serial != None:
            self.serial.close()
        print("[@] Serial link is now closed")

    def write(self, msg=None):
        if msg is None:
            raise Exception(
                "Error: Attempted to write None object to arduino!")

        if settings.comms:
            print("[@] writing msg <{}> to arduino".format(msg))
        try:
            msg = bytes(msg, "utf-8")
            return self.serial.write(msg)
        except Exception as e:
            print("[!] Error writing to serial link")
            print(e)

    def read(self):
        # https://pythonhosted.org/pyserial/shortintro.html#readline
        try:
            msg = self.serial.readline()
            if msg is None:
                print("[!] No message from serial")
                return None

            msg = msg.decode("utf-8")
            if settings.comms:
                print("[@] Receiveed msg <{}> from arduino".format(msg))
            return str(msg)
        except Exception as e:
            print("[!] Error reading from serial link")
            print(e)
