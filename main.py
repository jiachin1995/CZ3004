import time
import queue 
import threading

from android import Android
from arduino import Arduino

from interface import Interface

class Main:
    interface = Interface()

    listen_rate = 1

    def __init__(self):
        threading.Thread.__init__(self)

        #self.pc = PC(tcp_ip="192.168.1.1")
        self.android = Android()
        self.serial = Serial()

        #self.pc.connect()
        self.android.connect()
        self.serial.connect()

        time.sleep(1)
        
        

    def write_to_pc(self, msg):
        self.pc.write(msg)
        print("[@] Sent to PC: {}".format(msg))

    def read_from_pc(self):
        msg = self.pc.read()
        if msg == None:
            return print("[#] nothing to read [read_from_pc]")


    def start_listening(self):
        while True:
            msg = self.android.read()
            if msg == None:
                return print("[#] nothing to read [read_from_android]")
                
            try: 
                results = self.interface.readinstructions(msg)
                
                if results is None:
                    self.android.write("done")
                else:
                    self.android.write(results)
                
            except Exception as e:
                print("[@] Error reading instructions")
                print(e)  
                time.sleep(listen_rate)

    def close_all_connections(self):
        self.pc.close()
        self.android.close()
        self.serial.close()


if __name__ == "__main__":
    print("[@] Starting main program..")
    app = Main()
    try:
        app.initialise_threads()
        app.start_listening()
    except Exception as e:
        print("[@] Error running main")
        app.close_all_connections()
        print(e)