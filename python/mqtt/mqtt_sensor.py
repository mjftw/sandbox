import paho.mqtt.client as mqtt
import threading
import time


# TODO: Add security
#   - See: https://www.hivemq.com/mqtt-security-fundamentals/
#   - Authentication with username and password:
#     https://www.hivemq.com/blog/mqtt-security-fundamentals-authentication-username-password/
#   - Authorisation
#     https://www.hivemq.com/blog/mqtt-security-fundamentals-authorization/
#   - Encryption TLS/SSL
#     https://www.hivemq.com/blog/mqtt-security-fundamentals-tls-ssl/

class MQTTSensor:
    ''' MQTT based sensor base class

    This class can be inherited in order to allow sensor read values to
    be published to an MQTT broker, and any clients that are subscribed.

    The inheriting class must impliment the read() method.
    This method should have the code required to read a value from
    the sensor, and return it.

    Optionally the inheriting class can impliment the following methods:
    * on_connect() - Callback called on broker connection.
    * on_disconnect() - Callback called on broker disconnection.
    * on_message() - Callback called when message recieved on subscribed topic.
        If a subscribe topic is given, this callback can be used to recieve
        messages from the broker, process them as needed.
        This could be used to recieve commands from another MQTT client.

    For infomation on the arguments these methods take, see:
        https://pypi.org/project/paho-mqtt/

    Args:
        publish_topic (:obj:`str`): Topic branch to publish sensor readings to.
        subscribe_topic (:obj:`str`, optional): Topic branch to subscuribe to
            in order to recieve messages. Default is None.
        broker_host (:obj:`str`, optional): Host address of MQTT broker server.
            Default is 127.0.0.1 (localhost).
        broker_port (int, optional): Connection port of MQTT broker server.
            Default is 1883 (default unsecured MQTT port)
        publish_qos (int, optional): Quality of Service level to be used when
            publishing messages to the MQTT server.
            Ensure that the broker recieves messages
            0: At most once,
            1: At least once,
            2: Exactly once
            Default is 1
        read_interval (float, optional): Interval in seconds at when sensor
            values should be read, and published to MQTT topic. Default is 1.
        retain_value (bool, optional): Should the retain flag be set on MQTT
            messages? Setting this to True causes the broker to store the
            retained message and corresponding QoS for the topic.
            Default is False.
        keepalive (int, optional): The keepalive timeout for the client in
            seconds. Default is 60.
        birth_message (dict, optional): A dict containing parameters for the client's
            birth message. This message is sent by the client upon connection.
            birth_message = {
                ‘topic’: “<topic>”,
                ‘payload’:”<payload”>,
                ‘qos’:<qos>,
                ‘retain’:<retain>
            }
            Topic is required, other parameters are optional and will default
            to None, 0, and False respectively.
            Default is None (no birth message).
        will_message (dict, optional): A dict containing parameters for the client's
            last will and testiment. This message is sent to other clients by the
            broker if the client disconnects unexpectedly.
            will_message = {
                ‘topic’: “<topic>”,
                ‘payload’:”<payload”>,
                ‘qos’:<qos>,
                ‘retain’:<retain>
            }
            Topic is required, other parameters are optional and will default
            to None, 0, and False respectively.
            Default is None (no will message).
        client_id (:obj:`str`, optional): An ID string to be used by the client
            when connecting to the broker. By default the MAC address of the
            machine will be used.
    '''
    def __init__(self, publish_topic, subscribe_topic=None,
                 broker_host=None, broker_port=None, publish_qos=None,
                 read_interval=None, retain_value=None, keepalive=None,
                 birth_message=None, will_message=None, client_id=None):
        self.publish_topic = publish_topic

        self.subscribe_topic = subscribe_topic
        self.broker_host = broker_host or '127.0.0.1'
        self.broker_port = broker_port or 1883
        self.read_interval = read_interval or 10
        self.publish_qos = publish_qos if publish_qos is not None else 0
        self.retain_value = retain_value or False
        self.keepalive = keepalive or 60

        # Set birth message
        if birth_message:
            if 'topic' not in birth_message:
                raise AttributeError('birth_message must have "topic" key')
            if 'payload' not in birth_message:
                birth_message['payload'] = None
            if 'qos' not in birth_message:
                birth_message['qos'] = 0
            if 'retain' not in birth_message:
                birth_message['retain'] = False
        self.birth_message = birth_message

        # Set will message
        if will_message:
            if 'topic' not in will_message:
                raise AttributeError('will_message must have "topic" key')
            if 'payload' not in will_message:
                will_message['payload'] = None
            if 'qos' not in will_message:
                will_message['qos'] = 0
            if 'retain' not in will_message:
                will_message['retain'] = False
        self.will_message = will_message

        if client_id is not None:
            self.client_id = client_id
        else:
            self.client_id = get_mac_address()

        self._connected = False

        # MQTT client
        self._client = None

        self._read_timer = None
        self._read_timer_running = False

    def on_message(self, client, userdata, message):
        ''' Impliment this callback if you want to recieve messages '''
        pass

    def on_connect(self, client, userdata, flags, rc):
        ''' Impliment this callback if you want to act on connect '''
        pass

    def on_disconnect(self, client, userdata, rc):
        ''' Impliment this callback if you want to act on disconnect '''
        pass

    def read(self):
        ''' Read and return sensor value. This function must be implemented '''
        raise NotImplementedError

    @property
    def reading(self):
        ''' Is a periodic read ongoing? '''
        return self._read_timer_running

    @property
    def connected(self):
        ''' Is client connected to MQTT broker? '''
        return self._connected

    def start(self):
        ''' Connect to MQTT broker and start publishing sensor values '''
        if not self._connected:
            self._start_client()
        if not self._read_timer_running:
            self._start_read_timer()

    def stop(self):
        ''' Disconnect from MQTT broker and stop reading sensor '''
        self._stop_read_timer()
        self._stop_client()

    def read_and_publish(self):
        ''' Read sensor value and publish. Connect to broker if needed.
        Returns:
            Sensor read value
        '''
        # Connect to client if not connected
        if not self._client or not self._connected:
            self._start_client()

        if not self._connected:
            raise RuntimeError(
                'No connection to MQTT broker at {}:{}'.format(
                    self.broker_host, self.broker_port))

        data = self.read()

        self._client.publish(
            topic=self.publish_topic,
            payload=data,
            qos=self.publish_qos,
            retain=self.retain_value
        )

        return data

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
        self._client = mqtt.Client(
            client_id=self.client_id
        )

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self.on_message

        if self.will_message:
            self._client.will_set(
                topic=self.will_message['topic'],
                payload=self.will_message['payload'],
                qos=self.will_message['qos'],
                retain=self.will_message['retain']
            )

        self._client.connect(
            host=self.broker_host,
            port=self.broker_port,
            keepalive=self.keepalive
        )

        self._client.loop_start()

        # Spin until connected
        timeout = 5
        seconds_passed = 0
        while not self.connected:
            if seconds_passed > timeout:
                raise ConnectionError('Timeout waiting to connect to MQTT broker')
            time.sleep(0.1)
            seconds_passed += 0.1

        # Publish birth message
        if self.birth_message:
            self._client.publish(
                topic=self.birth_message['topic'],
                payload=self.birth_message['payload'],
                qos=self.birth_message['qos'],
                retain=self.birth_message['retain']
            )

    def _stop_client(self):
        if self._client:
            self._client.loop_stop()
        self._client = None

    def _on_connect(self, *args, **kwargs):
        self._connected = True

        if self.subscribe_topic:
            self._client.subscribe(self.subscribe_topic)

        self.on_connect(*args, **kwargs)

    def _on_disconnect(self, *args, **kwargs):
        self._connected = False

        self.on_disconnect(*args, **kwargs)


def get_mac_address():
    ''' Helper function to get MAC address of machine and format it nicely '''
    import uuid
    import re

    return ':'.join(
        re.findall('..', '%012x' % uuid.getnode())
    )