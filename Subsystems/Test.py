from Framework.Themis import EventBroker, StatusProcessor, LogProcessor
from Processors.PerformanceMonitor import PerformanceMonitor
from Processors.PingMonitor import PingMonitor
from Processors.Display import Display
import gtk, gobject

event_broker = EventBroker()
status_processor = StatusProcessor(event_broker)
log_processor = LogProcessor(event_broker)
performance_monitor = PerformanceMonitor(event_broker, 'hyperion.local')
ping_monitor = PingMonitor(event_broker, 'www.google.com')
#ping_monitor_yahoo = PingMonitor(event_broker, 'www.yahoo.com')
#ping_monitor_local = PingMonitor(event_broker, 'localhost')
display = Display(event_broker, 'localhost')

gobject.threads_init()
gtk.main()
