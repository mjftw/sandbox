from mqtt_sensor import MQTTSensor
from random import randint


class MockMQTTSensor(MQTTSensor):
    def read(self):
        return randint(0, 100)

    def on_message(self,  client, userdata, msg):
        print(f'Recieved: {msg.payload}')

    def on_connect(self, *args, **kwargs):
        print('Connected')

    def on_disconnect(self, *args, **kwargs):
        print('Disconnected')

def main():
    sensor = MockMQTTSensor(
        publish_topic='sandbox/mock/tx',
        subscribe_topic='sandbox/mock/rx',
        will={
            'topic': 'sandbox/mock/dead',
            'payload': 'I have died!',
            'qos': 2,
            'retain': True
        }
    )

    sensor.start()

    while(1):
        pass

if __name__ == '__main__':
    main()