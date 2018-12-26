from Themis import EventProcessor
import threading
import subprocess
from Tkinter import *


class Display(EventProcessor):
    def __init__(self, event_broker, host, root):
        EventProcessor.__init__(self, event_broker)
        self.processor = self.processor + '_' + host
        self.host = host
        self.frame = Frame(root)
        self.frame.pack()
        self.createWidgets()
        self.monitor_thread = threading.Thread(target=self.monitor_thread)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def say_hi(self):
        print "hi there, everyone! XXXs"

    def createWidgets(self):
        self.QUIT = Button(self.frame)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.frame.quit
        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self.frame)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "left"})

    def monitor_thread(self):
        while True:
            self.log('monitor_thread starting..')
            try:
                process = subprocess.Popen(['ping', self.host], stdout=subprocess.PIPE)
                while True:
                    line = process.stdout.readline()
                    if line != '':
                        self.log(line.strip())
            except:
                self.log('monitor_thread stopped..')