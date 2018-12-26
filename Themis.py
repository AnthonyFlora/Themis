#! /usr/bin/python

import collections
import datetime
import Queue
import subprocess
import threading
from Tkinter import *


# -- Core Messages ------------------------------------------------------------

class Event:
    def __init__(self, topic, processor):
        self.topic = topic
        self.processor = processor


class LogEvent(Event):
    def __init__(self, processor, entry):
        Event.__init__(self, 'log', processor)
        self.entry = entry


class StatusEvent(Event):
    def __init__(self, processor, status):
        Event.__init__(self, 'status', processor)
        self.status = status


# -- Core Processing ----------------------------------------------------------

class EventProcessor:
    def __init__(self, event_broker):
        self.processor = self.__class__.__name__
        self.status = 'STARTUP'
        self.event_broker = event_broker
        self.event_handlers = {}
        self.event_queue = Queue.Queue()
        self.set_event_handler('status_request', self.on_status_request_event)
        self.send_status()
        self.processing_thread = threading.Thread(target=self.processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def log(self, entry):
        self.event_broker.send(LogEvent(self.processor, entry))

    def set_event_handler(self, event_topic, event_handler):
        self.event_handlers[event_topic] = event_handler
        self.event_broker.subscribe(event_topic, self)

    def queue_event(self, event):
        self.event_queue.put(event)

    def processing_loop(self):
        self.status = 'RUNNING'
        self.send_status()
        while True:
            try:
                event = self.event_queue.get()
                event_handler = self.event_handlers[event.topic]
                event_handler(event)
            except:
                self.log('Could not process event.')
        self.status = 'OFFLINE'
        self.send_status()

    def on_status_request_event(self, event):
        self.send_status()

    def send_status(self):
        self.event_broker.send(StatusEvent(self.processor, self.status))


class EventBroker():
    def __init__(self):
        self.subscribers = collections.defaultdict(lambda: set())

    def subscribe(self, topic, processor):
        self.subscribers[topic].add(processor)

    def unsubscribe(self, topic, processor):
        self.subscibers[topic].remove(processor)

    def send(self, event):
        for processor in self.subscribers[event.topic]:
            processor.queue_event(event)


class LogProcessor(EventProcessor):
    def __init__(self, event_broker):
        EventProcessor.__init__(self, event_broker)
        self.set_event_handler('log', self.on_log_event)

    def on_log_event(self, event):
        print '%s : %s -> %s' % (datetime.datetime.now(), event.processor, event.entry)


class StatusProcessor(EventProcessor):
    def __init__(self, event_broker):
        EventProcessor.__init__(self, event_broker)
        self.set_event_handler('status', self.on_status_event)

    def on_status_event(self, event):
        self.log('Got status - %s %s' % (event.processor, event.status))

# -- Processors ---------------------------------------------------------------


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


class PerformanceMonitor(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.host = host
        self.processor = self.processor + '_' + host
        self.metric_params = []
        self.metric_values = []
        self.metrics = {}
        self.monitor_thread = threading.Thread(target=self.monitor_thread)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_thread(self):
        while True:
            self.log('monitor_thread starting..')
            try:
                process = subprocess.Popen(['ssh', 'pi@hyperion.local', 'sar', '-u', '-r', '5'], stdout=subprocess.PIPE)
                while True:
                    line = process.stdout.readline()
                    if line != '':
                        self.log(line.strip())
                        tokens = line.split()
                        if len(tokens) == 0:
                            self.metric_params = []
                            self.metric_values = []
                            self.metrics = {}
                        else:
                            if len(self.metric_params) == 0:
                                for token in tokens[2:]:
                                    self.metric_params.append(token)
                            else:
                                self.metrics['time'] = tokens[0] + ' ' + tokens[1]
                                for token in tokens[2:]:
                                    self.metric_values.append(token)
                                for i in range(len(self.metric_params)):
                                    self.metrics[self.metric_params[i]] = self.metric_values[i]
                                for k,v in self.metrics.iteritems():
                                    self.log('%s - %s' % (k, v))
                    else:
                        break
            except:
                self.log('monitor_thread stopped..')


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

# -- Main ---------------------------------------------------------------------

root = Tk()

event_broker = EventBroker()
status_processor = StatusProcessor(event_broker)
log_processor = LogProcessor(event_broker)
performance_monitor = PerformanceMonitor(event_broker, 'hyperion.local')
#ping_monitor = PingMonitor(event_broker, 'www.google.com')
#ping_monitor_yahoo = PingMonitor(event_broker, 'www.yahoo.com')
#ping_monitor_local = PingMonitor(event_broker, 'localhost')
display = Display(event_broker, 'localhost', root)

root.mainloop()
root.destroy()


#while True:
#    time.sleep(1)
