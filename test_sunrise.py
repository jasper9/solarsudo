# SETUP
# pip3 install paho-mqtt

# python 3.6
# python3.6
import datetime
import random
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import sunriset
import astral, astral.sun
from datetime import date, datetime, timezone, timedelta
import pytz

broker = '192.168.1.117'

latitude = 39.95701
longitude = -105.15776
tz_poland = pytz.timezone('America/Denver')
tz_name = 'America/Denver'
for_date = date.today()

print('====== astral ======')
l = astral.LocationInfo('Custom Name', 'My Region', tz_name, latitude, longitude)
s = astral.sun.sun(l.observer, date=for_date)
print(s['sunrise'].astimezone(tz_poland))
print(s['sunset'].astimezone(tz_poland))
