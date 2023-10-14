# SETUP
# pip3 install paho-mqtt

# python 3.6
# python3.6
import datetime
import random
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

broker = '192.168.1.117'

def run():


    while True:
        msg = subscribe.simple("solar_assistant/inverter_1/device_mode/state", hostname=broker)
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        device_mode = msg.payload.decode()
        time.sleep(2)
    

if __name__ == '__main__':
    run()
