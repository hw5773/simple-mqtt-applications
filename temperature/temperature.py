import paho.mqtt.client as paho
import time 
import random
import argparse
import logging

class TempData:
    def __init__(self, temperature):
        self.temperature = temperature
        self.connected = False

    def set_connected(self):
        self.connected = True

    def get_connected(self):
        return self.connected

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature

def on_connect(temperature, tempdata, flags, rc):
    if rc == 0:
        logging.debug("Connected to broker")
        tempdata.set_connected()
    else:
        logging.debug("Connection failed")

def on_message(temperature, userdata, message):
    time.sleep(1)
    try:
        logging.debug("received message = {}".format(str(message.payload.decode("utf-8"))))
    except:
        temperature.disconnect()
        temperature.loop_stop()

def run(address, port=1883, domain="home", name="temperature"):
    connected = False
    temp_data = TempData(25)
    temperature = paho.Client(name, userdata=temp_data)
    temperature.on_connect = on_connect
    temperature.on_message = on_message
    temperature.connect(address, port)
    temperature.loop_start()
    topic = "{}/{}".format(domain, name)

    while not temp_data.get_connected():
        time.sleep(0.1)

    while True:
        temp = temp_data.get_temperature()
        rand = int(random.random() * 10) * 0.01
        sign = random.random() > 0.5
        if sign:
            temp = round(temp * (1 + rand), 2)
        else:
            temp = round(temp * (1 - rand), 2)
        ret = temperature.publish(topic, str(temp))
        time.sleep(3)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", metavar="<broker address>", help="broker address", type=str, required=True)
    parser.add_argument("-p", "--port", metavar="<broker port>", help="broker port", type=int, required=True)
    parser.add_argument("-d", "--domain", metavar="<name of domain>", help="name of domain", type=str, required=True)
    parser.add_argument("-n", "--name", metavar="<name of itself>", help="name of itself", type=str)
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)>", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)
    if args.name:
        run(args.address, args.port, args.domain, args.name)
    else:
        run(args.address, args.port, args.domain)

if __name__ == "__main__":
    main()
