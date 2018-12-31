from Framework.Themis import EventBroker, StatusProcessor, LogProcessor, Event
from Processors.PerformanceMonitor import PerformanceMonitor
from Processors.PingMonitor import PingMonitor
from Processors.Display import Display
from Processors.MqttAdapter import  MqttAdapter
import gtk, gobject
import time

event_broker = EventBroker()
status_processor = StatusProcessor(event_broker)
log_processor = LogProcessor(event_broker)
#performance_monitor = PerformanceMonitor(event_broker, 'hyperion.local')
#ping_monitor = PingMonitor(event_broker, 'www.google.com')
#ping_monitor_yahoo = PingMonitor(event_broker, 'www.yahoo.com')
#ping_monitor_local = PingMonitor(event_broker, 'localhost')
display = Display(event_broker, 'localhost')

mqtt_adapter = MqttAdapter(event_broker, 'iot.eclipse.org', '1883')
ms = Event('mqtt_subscription_request', 'main')
ms.data['mqtt_topic'] = 'hyperion/test'
event_broker.send(ms)

time.sleep(5.0)
me = Event('hyperion/test', 'main')
me.data['aa'] = 'cow'
event_broker.send(me)

gobject.threads_init()
gtk.main()
