from Framework.Themis import EventProcessor, Event
import paho.mqtt.client as mqtt
import threading
import json


class MqttAdapter(EventProcessor):
    def __init__(self, event_broker, mqtt_addr, mqtt_port):
        EventProcessor.__init__(self, event_broker)
        self.host = 'moo'
        self.processor = self.processor + '_' + self.host
        self.set_event_handler('mqtt_subscription_request', self.on_mqtt_subscribe_event)
        self.set_event_handler('mqtt_send_request', self.on_mqtt_send_event)
        self.mqtt_addr = mqtt_addr
        self.mqtt_subscriptions = set()
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_receive
        self.mqtt_thread = threading.Thread(target=self.mqtt_thread)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

    def on_mqtt_subscribe_event(self, event):
        mqtt_topic = event.data['mqtt_topic']
        self.mqtt_subscriptions.add(mqtt_topic)
        self.mqtt_client.subscribe(mqtt_topic)
        self.log('Subscribed to %s' % (mqtt_topic))

    def on_mqtt_send_event(self, event):
        topic = event.data['topic']
        self.mqtt_client.publish(topic, json.dumps(event.data))

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.log('Connected with code %s' % (rc))
        for topic in self.mqtt_subscriptions:
            self.mqtt_client.subscribe(topic)

    def on_mqtt_receive(self, client, userdata, message):
        self.log(message.topic)
        event = Event(message.topic, self.processor)
        event.data.update(json.loads(message.payload))
        self.event_broker.send(event)

    def mqtt_thread(self):
        while True:
            self.log('mqtt_thread starting..')
            self.log('Connecting to %s' % self.mqtt_addr)
            try:
                self.mqtt_client.connect(self.mqtt_addr)
                self.mqtt_client.loop_forever()
            except Exception as e:
                self.log('Exception: %s' % e)
                self.log('mqtt_thread stopped..')
