#! /usr/bin/python

import collections
import datetime
import Queue
import threading
import collections


# -- Core Messages ------------------------------------------------------------

class Event:
    def __init__(self, topic, processor):
        self.data = collections.defaultdict(lambda: None)
        self.data['topic'] = topic
        self.data['processor'] = processor


class LogEvent(Event):
    def __init__(self, processor, entry):
        Event.__init__(self, 'log', processor)
        self.data['entry'] = entry


class StatusEvent(Event):
    def __init__(self, processor, status):
        Event.__init__(self, 'status', processor)
        self.data['status'] = status


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
                topic = event.data['topic']
                event_handler = self.event_handlers[topic]
                event_handler(event)
            except Exception as e:
                self.log('Exception: %s' % e)
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
        self.subscibers.topic.remove(processor)

    def send(self, event):
        for processor in self.subscribers[event.data['topic']]:
            processor.queue_event(event)


class LogProcessor(EventProcessor):
    def __init__(self, event_broker):
        EventProcessor.__init__(self, event_broker)
        self.set_event_handler('log', self.on_log_event)

    def on_log_event(self, event):
        print '%s : %s -> %s' % (datetime.datetime.now(), event.data['processor'], event.data['entry'])


class StatusProcessor(EventProcessor):
    def __init__(self, event_broker):
        EventProcessor.__init__(self, event_broker)
        self.set_event_handler('status', self.on_status_event)

    def on_status_event(self, event):
        processor = event.data['processor']
        status = event.data['status']
        self.log('Got status - %s %s' % (processor, status))
