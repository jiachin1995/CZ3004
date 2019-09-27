import time
import queue 
import threading

from android import Android
from arduino import Arduino

from interface import Interface

class Main:
    interface = None

    listen_rate = 1
    
    android=None
    arduino=None
    

    def __init__(self):
        threading.Thread.__init__(self)

        #self.pc = PC(tcp_ip="192.168.1.1")
        self.android = Android()
        self.arduino = Arduino()

        #self.pc.connect()
        self.android.connect()
        self.arduino.connect()

        time.sleep(1)
        
        self.interface = Interface(arduino = self.arduino)

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
            print("Received msg is {}".format(msg))
                
            try: 
                results = self.interface.readinstructions(str(msg))
                
                if results is None:
                    self.android.write(bytes("done", 'utf-8'))
                else:
                    self.android.write(bytes(results, 'utf-8'))
                
            except Exception as e:
                print("[@] Error reading instructions")
                print(e)  
                time.sleep(self.listen_rate)
                
                import sys, os
                
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    def close_all_connections(self):
        #self.pc.close()
        self.android.close()
        self.arduino.close()


if __name__ == "__main__":
    print("[@] Starting main program..")
    app = Main()
    try:
        app.start_listening()
    except Exception as e:
        print("[@] Error running main")
        app.close_all_connections()
        print(e)