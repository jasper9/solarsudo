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

broker = '192.168.1.xxx'

soc_low_point = 30
pv_low_point = 150

#now = datetime.datetime.now()
#print(now.year, now.month, now.day, now.hour, now.minute, now.second)
def wait_for_settings():
    secs_to_wait = 60*3
    print(f"Sleeping {secs_to_wait}s to let the settings kick in.")
    time.sleep(secs_to_wait)

def run():
    print("--------------------------------------------------------------------------------")
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
    print(f"Average PV generation == {pv_avg}")

    #msg = subscribe.simple("solar_assistant/inverter_1/pv_power/state", hostname=broker)
    #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #pv_power = int(msg.payload.decode())

    soc_topic = "solar_assistant/total/battery_state_of_charge/state"
    #soc_topic = "solar_assistant/battery_1/state_of_charge/state"
    msg = subscribe.simple(soc_topic, hostname=broker)
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    state_of_charge = int(msg.payload.decode())

    msg = subscribe.simple("solar_assistant/inverter_1/device_mode/state", hostname=broker)
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    device_mode = msg.payload.decode()

    # for some reason this is hanging
    #msg = subscribe.simple("solar_assistant/inverter_1/output_source_priority/set", hostname=broker)
    #print(f"SET Output Souce Priority: `{msg.payload.decode()}`")
    #msg = subscribe.simple("solar_assistant/inverter_1/output_source_priority/state", hostname=broker)
    #print(f"STATE Output Souce Priority: `{msg.payload.decode()}`")

    if state_of_charge < soc_low_point: 
        print(f"State of charge is below low point of `{soc_low_point}`")
        
        ## SEND ALERT HERE



        # Solar/Grid
        # Bypass
        # Utility first
        # Solar first

        if device_mode == "Solar/Battery":
            print(f"SOC is low, and since we're running on solar & battery, turn on `Utility First` mode.")
            publish.single("solar_assistant/inverter_1/output_source_priority/set", "Utility first", hostname=broker)
            
            wait_for_settings()


    elif device_mode == "Bypass" or device_mode == "Solar/Grid":
            if pv_avg > 150 and soc_topic > (soc_low_point + 10):
                print(f"Since we're running on the grid and solar is available AND soc is 10% over low point, turn on `Solar First` mode.")
                publish.single("solar_assistant/inverter_1/output_source_priority/set", "Solar first", hostname=broker)
                
                wait_for_settings()

    else:
        print(f"No changes needed.")
    


    if (pv_avg < pv_low_point) and (device_mode == "Solar/Battery"):
        print(f"***WARNING*** PV generation is below low point. Since we're running on battery, turn on `Utility First` mode.")
        publish.single("solar_assistant/inverter_1/output_source_priority/set", "Utility first", hostname=broker)
        
        wait_for_settings()

def main():
    while True:
        run()
        print(f"Sleeping for 1 minute(s)......")
        time.sleep(60)

if __name__ == '__main__':
    main()