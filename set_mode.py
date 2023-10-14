# SETUP
# pip3 install paho-mqtt

# python 3.6
# python3.6
import datetime
import random
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import logging
import argparse

#mode = "Solar first"

broker = '192.168.1.117'

logging.basicConfig(filename="/var/log/solarsudo.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running set_mode.py")

parser = argparse.ArgumentParser(description="Set mode on inverter. Options: Solar, Grid")
parser.add_argument("--mode")
args = parser.parse_args()

mode = args.mode

if mode == "Solar" or mode == "solar":
    mode = "Solar first"
elif mode == "Grid" or mode == "grid":
    mode = "Utility first"
else:
    print(f"ERROR: `{mode}` is not an option")
    quit()

logging.info(f"Attempting to set mode `{mode}`")

msg = subscribe.simple("solar_assistant/inverter_1/device_mode/state", hostname=broker)
txt=f"Received `{msg.payload.decode()}` from `{msg.topic}` topic"
#print(txt)
#logging.info(txt)
device_mode = msg.payload.decode()

publish.single("solar_assistant/inverter_1/output_source_priority/set", mode, hostname=broker)

txt=f"Output source priority switched from `{device_mode}` to `{mode}`"
print(txt)
logging.info(txt)



