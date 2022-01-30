import paho.mqtt.client as paho
import time 
import argparse
import logging

class UserData:
    def __init__(self, domain):
        self.domain = domain

    def get_domain(self):
        return self.domain

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ("Connected to broker")
        global connected
        connected = True
    else:
        print ("Connection failed")

def on_message(hub, userdata, message):
    time.sleep(1)
    domain = userdata.get_domain()
    topic = message.topic

    if "temperature" in topic:
        temperature = float(message.payload.decode("utf-8"))
        logging.debug("received temperature: {}".format(temperature))
        if temperature > 26:
            logging.debug("need to turn on the air conditioner")
            airconditioner = "{}/airconditioner".format(domain)
            hub.publish(airconditioner, "on")

        else:
            logging.debug("need to turn off the air conditioner")
            airconditioner = "{}/airconditioner".format(domain)
            hub.publish(airconditioner, "off")
    elif "airconditioner" in topic:
        result = message.payload.decode("utf-8")
        logging.debug("result: {}".format(result))
    #except:
    #    hub.disconnect()
    #    hub.loop_stop()
    
def run(address, port, domain):
    connected = False
    data = UserData(domain)
    hub = paho.Client("hub", userdata=data)
    hub.on_connect = on_connect
    hub.on_message = on_message
    hub.connect(address, port)
    hub.subscribe("{}/#".format(domain), 0)
    hub.loop_start()

    while connected != True:
        time.sleep(0.1)

    while True:
        pass

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", metavar="<broker address>", help="broker address", type=str, required=True)
    parser.add_argument("-p", "--port", metavar="<broker port>", help="broker port", type=int, required=True)
    parser.add_argument("-d", "--domain", metavar="<name of domain>", help="name of domain", type=str, required=True)
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)>", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)
    run(args.address, args.port, args.domain)

if __name__ == "__main__":
    main()
