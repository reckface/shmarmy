import threading
import time
from datetime import datetime
from queue import Queue
from psonic import *
from utilities import *
import csv
from time import sleep
import os, sys
import serial
import time


print_lock = threading.Lock()
    
class ListenerThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]
        self.sound = None
        self._stop_event = threading.Event()
        self.logFileName = "/home/pi/Desktop/logs/%s-shmarmy.csv" % time.strftime("%Y-%m-%d-%H:%M:%S")
        with open(self.logFileName, "a", newline='') as csv_file:
            fieldnames = ['Time', 'Reading']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def stop(self):
        self._stop_event.set()
        stop()
        
    def restart(self):
        self._stop_event = threading.Event()
        
    def log(self, reading):
        with open(self.logFileName, "a", newline='') as csv_file:
            fieldnames = ['Time', 'Reading']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            line = {'Time': datetime.utcnow().strftime('%H:%M:%S.%f')[:-3], 'Reading': reading}
            writer.writerow(line)
            print(line)


    def play(self, reading):
        self.log(reading)
##        stop()
        use_synth(PULSE)
        duration = "{0:.2f}".format(.25)
        if(reading >= 86):
            run("""
                play :G5, sustain: 60
                #notes = (scale :e3, :minor_pentatonic)
                #sn = synth :prophet, note: :e1, release: 8, cutoff: 100
                #sleep 1
                #16.times do
                #  control sn, note: notes.tick
                #  sleep 0.125
                #end
                """)
            return
        elif reading <= 0:
            pass
        elif reading > 20:
            duration = "{0:.2f}".format(.15)
        else:
            duration = "{0:.2f}".format(.30)
        
        run("""
            live_loop :foo do
              play :Eb5
              sleep %s
            end
            """ % duration)

    def run(self):
        print ("\n", threading.currentThread().getName(), self.receive_messages)
        while True:
            val = self.queue.get()
            if val is None:   # If you send `None`, the thread will exit.
                self.stop()
                return
            self.play(val)
            
if __name__ == '__main__':
        
    jobQueue = Queue()
    listener = ListenerThread(jobQueue, args=(True,))
    listener.start()
    command = input("\nPress Enter to continue...")
    
    value = 0
    oldValue = 0
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 35)
    ser.flushInput()
    
##    while (command != 'y'):
##        if(is_numeric(command)):
##            value = float(command)
##            listener.play(value)
##            command = input("\nPress Enter to continue...")
    counter = 0
    while True:
##        ser.write("a".encode())
        value = int(ser.readline().decode())
        counter += 1
        if(value <= 0):
            continue
        if(counter > 10 or abs(value - oldValue) > 5):            
            oldValue = value
            listener.play(value)
            counter = 0
	
##    while (command != 'y'):
##        if(is_numeric(command)):
##            value = float(command)
##            listener.play(value)
##        command = input("\nPress Enter to continue...")
    stop()
    listener.queue.put(None)
    listener.stop()
    listener.join()



