import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print('CONNECTED')


def on_disconnect(client, userdata, rc):
    print('DISCONNECTED')


def on_message(client, userdata, msg):
    print(f'MESSAGE: {msg.payload}')


def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect('127.0.0.1')
    client.subscribe('sandbox')

    client.loop_forever()


if __name__ == '__main__':
    main()