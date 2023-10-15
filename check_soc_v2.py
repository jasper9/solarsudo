# DOCS:
# https://github.com/JJSlabbert/Solar-Assistant-MQTT-client
# http://mqtt-explorer.com/



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
import common

broker = '192.168.1.117'

soc_low_point = 30
pv_low_point = 100

#logging.basicConfig(filename="/var/log/solarsudo.log",
#                    filemode='a',
#                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                    datefmt='%H:%M:%S',
#                    level=logging.DEBUG)
#lines = "--------------------------------------------------------------------------------"
#logging.info(lines)
#logging.info("Running check_soc_v2.py")

#logger = logging.getLogger('urbanGUI')

#now = datetime.datetime.now()
#print(now.year, now.month, now.day, now.hour, now.minute, now.second)
def wait_for_settings():
    secs_to_wait = 60*5
    print(f"Sleeping {secs_to_wait}s to let the settings kick in.")
    time.sleep(secs_to_wait)

def getCurrentPV():
    print(f"Checking average PV generation...")
    x=0
    pv_sum=0
    while x < 5:
        msg = subscribe.simple("solar_assistant/inverter_1/pv_power/state", hostname=broker)
        pv_power=int(msg.payload.decode())
        #print(f"pv_power == {pv_power}")
        x=x+1
        pv_sum = pv_sum + pv_power
        time.sleep(2)

    pv_avg = pv_sum/5
    #print(f"Average PV generation == {pv_avg}")
    return(round(pv_avg))

def run():

    pv_avg = getCurrentPV()

    soc_topic = "solar_assistant/total/battery_state_of_charge/state"
    #soc_topic = "solar_assistant/battery_1/state_of_charge/state"
    msg = subscribe.simple(soc_topic, hostname=broker)
    txt=f"Received `{msg.payload.decode()}` from `{msg.topic}` topic"
    #print(txt)
    #logging.info(txt)

    state_of_charge = int(msg.payload.decode())

    msg = subscribe.simple("solar_assistant/inverter_1/device_mode/state", hostname=broker)
    txt=f"Received `{msg.payload.decode()}` from `{msg.topic}` topic"
    #print(txt)
    #logging.info(txt)

    device_mode = msg.payload.decode()

    # for some reason this is hanging
    #msg = subscribe.simple("solar_assistant/inverter_1/output_source_priority/set", hostname=broker)
    #print(f"SET Output Souce Priority: `{msg.payload.decode()}`")
    #msg = subscribe.simple("solar_assistant/inverter_1/output_source_priority/state", hostname=broker)
    #print(f"STATE Output Souce Priority: `{msg.payload.decode()}`")

    if state_of_charge < soc_low_point: 
        txt=(f"State of charge `{state_of_charge}%` is below low point of `{soc_low_point}%`")
        print(txt)
        logging.info(txt)

        
        ## SEND ALERT HERE

        # Solar/Grid
        # Bypass
        # Utility first
        # Solar first

        if device_mode == "Solar/Battery":
            txt=f"SOC is low, and since we're running on solar & battery, turn on `Utility First` mode."
            print(txt)
            logging.info(txt)
            publish.single("solar_assistant/inverter_1/output_source_priority/set", "Utility first", hostname=broker)
    else:
        if device_mode == "Solar/Battery":
            txt=f"[{device_mode} - {pv_avg}w] SOC is `{state_of_charge}%` -  We're above the low point (`{soc_low_point}`), we good."
        else:
            txt=f"[{device_mode}] SOC is `{state_of_charge}%` -  We're above the low point (`{soc_low_point}`), we good."

        print(txt)
        logging.info(txt)
            
            # v2, disable
            #wait_for_settings()

    # v2, disable
    #elif device_mode == "Bypass" or device_mode == "Solar/Grid":
    #        if pv_avg > pv_low_point and state_of_charge > (soc_low_point + 10):
    #            print(f"Since we're running on the grid and solar is available AND soc is 10% over low point, turn on `Solar First` mode.")
    #            publish.single("solar_assistant/inverter_1/output_source_priority/set", "Solar first", hostname=broker)
    #            
    #            wait_for_settings()
    #
    #else:
    #    print(f"No changes needed.")
    


    #if (pv_avg < pv_low_point) and (device_mode == "Solar/Battery"):
    #    print(f"***WARNING*** PV generation is below low point. Since we're running on battery, turn on `Utility First` mode.")
    #    publish.single("solar_assistant/inverter_1/output_source_priority/set", "Utility first", hostname=broker)
    #    
    #    wait_for_settings()

def main():
    #while True:
    run()
        
        # disable loop
        #print(f"Sleeping for 5 minute(s)......")
        #time.sleep(5*60)

if __name__ == '__main__':
    main()
