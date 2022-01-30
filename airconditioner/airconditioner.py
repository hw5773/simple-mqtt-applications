import paho.mqtt.client as paho
import time 
import argparse
import logging

class ACData:
    def __init__(self):
        self.state = False

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.debug("Connected to broker")
        global connected
        connected = True
    else:
        logging.debug("Connection failed")

def on_message(client, acdata, message):
    time.sleep(1)
    control = message.payload.decode("utf-8")
    logging.debug("received control: {}".format(control))
    state = acdata.get_state()
    if control == "on":
        logging.debug("turn on the air conditioner")
        acdata.set_state(True)
    elif control == "off":
        if state:
            logging.debug("turn off the air conditioner")
            acdata.set_state(False)
        else:
            logging.debug("nothing to do")

def run(address, port=1883, domain="home", name="airconditioner"):
    connected = False
    acdata = ACData()
    client = paho.Client(name, userdata=acdata)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(address, port)
    topic = "{}/{}".format(domain, name)
    client.subscribe(topic, 1)
    client.loop_start()

    while connected != True:
        time.sleep(0.1)

    while True:
        time.sleep(10)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", metavar="<broker address>", help="broker address", type=str, required=True)
    parser.add_argument("-p", "--port", metavar="<broker port>", help="broker port", type=int, default=1883)
    parser.add_argument("-d", "--domain", metavar="<name of domain>", help="name of domain", type=str, required=True)
    parser.add_argument("-n", "--name", metavar="<name of itself>", help="name of itself", type=str, required=True)
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)>", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)
    run(address=args.address, port=args.port, domain=args.domain, name=args.name)

if __name__ == "__main__":
    main()
