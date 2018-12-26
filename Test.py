from Themis import EventBroker, StatusProcessor, LogProcessor
from PerformanceMonitor import PerformanceMonitor
from PingMonitor import PingMonitor
from Display import Display
from Tkinter import *

root = Tk()

event_broker = EventBroker()
status_processor = StatusProcessor(event_broker)
log_processor = LogProcessor(event_broker)
performance_monitor = PerformanceMonitor(event_broker, 'hyperion.local')
ping_monitor = PingMonitor(event_broker, 'www.google.com')
#ping_monitor_yahoo = PingMonitor(event_broker, 'www.yahoo.com')
#ping_monitor_local = PingMonitor(event_broker, 'localhost')
display = Display(event_broker, 'localhost', root)

root.mainloop()
root.destroy()