import paho.mqtt.client as mqtt
import threading
import time


class MQTTSensor:
    def __init__(self, publish_topic, subscribe_topic=None,
                 broker_host=None, broker_port=None, publish_qos=None,
                 read_interval=None, retain_value=None):
        self.publish_topic = publish_topic

        self.subscribe_topic = subscribe_topic
        self.broker_host = broker_host or '127.0.0.1'
        self.broker_port = broker_port or 1883
        self.read_interval = read_interval or 1
        self.publish_qos = publish_qos if publish_qos is not None else 1
        self.retain_value = read_interval or False

        self.connected = False

        # MQTT client
        self._client = None

        self._read_timer = None
        self._read_timer_running = False

    def on_message(self, client, userdata, message):
        pass

    def on_connect(self, client, userdata, flags, rc):
        pass

    def on_disconnect(self, client, userdata, rc):
        pass

    def read(self):
        raise NotImplementedError

    @property
    def reading(self):
        return self._read_timer_running

    def start(self):
        self._start_client()
        self._start_read_timer()

    def stop(self):
        self._stop_read_timer()
        self._stop_client()

    def read_and_publish(self):
        data = self.read()

        if not self._client:
            return

        if not self.connected:
            return

        self._client.publish(
            topic=self.publish_topic,
            payload=data,
            qos=self.publish_qos,
            retain=self.retain_value
        )

    def _start_read_timer(self):
        if not self._read_timer_running:
            self._read_timer = threading.Timer(
                interval=self.read_interval,
                function=self._run_and_restart_timer
            )
            self._read_timer.start()
            self._read_timer_running = True

    def _run_and_restart_timer(self):
        self.read_and_publish()

        self._read_timer_running = False
        self._start_read_timer()

    def _stop_read_timer(self):
        if self._read_timer_running:
            if self._read_timer:
                self._read_timer.cancel()
            self._read_timer_running = False

    def _start_client(self):
        self._client = mqtt.Client()

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self.on_message

        self._client.connect(
            host=self.broker_host,
            port=self.broker_port
        )

        self._client.loop_start()

    def _stop_client(self):
        self._client.loop_stop()
        self._client = None

    def _on_connect(self, *args, **kwargs):
        self.connected = True

        if self.subscribe_topic:
            self._client.subscribe(self.subscribe_topic)

        self.on_connect(*args, **kwargs)

    def _on_disconnect(self, *args, **kwargs):
        self.connected = False

        self.on_disconnect(*args, **kwargs)