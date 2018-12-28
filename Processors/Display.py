from Framework.Themis import EventProcessor
import threading
import subprocess
import gtk
import datetime


class Display(EventProcessor):
    def __init__(self, event_broker, host):
        EventProcessor.__init__(self, event_broker)
        self.processor = self.processor + '_' + host
        self.host = host
        self.window = gtk.Window()
        self.window.set_border_width(10)
        self.createWidgets()
        self.window.connect('destroy', gtk.main_quit)
        self.window.show_all()
        self.set_event_handler('log', self.on_log_event)

    def on_log_event(self, event):
        entry = '%s : %s -> %s' % (datetime.datetime.now(), event.processor, event.entry)
        self.label.set_text(entry)
        print 'label updated to %s' % (entry)

    def createWidgets(self):
        self.label = gtk.Label('The quick brown fox jumps over the lazy dog')
        self.window.add(self.label)
