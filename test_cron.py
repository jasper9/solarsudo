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
import common

broker = '192.168.1.117'

logging.info("Running set_mode.py")

parser = argparse.ArgumentParser(description="Set mode on inverter. Options: Solar, Grid")
parser.add_argument("--mode")
args = parser.parse_args()

mode = args.mode

txt=f"TEST: `{mode}` argument"
print(txt)
logging.info(txt)
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



