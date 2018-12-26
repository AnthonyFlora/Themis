from Framework.Themis import EventProcessor
import threading
import subprocess


class PingMonitor(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.processor = self.processor + '_' + host
        self.host = host
        self.monitor_thread = threading.Thread(target=self.monitor_thread)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

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