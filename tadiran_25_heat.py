
#!/usr/bin/python


import os
import paho.mqtt.client as mqtt
from  struct import *

irbuf = [8980, -4560, 580, -564, 640, -628, 580, -1728, 580, -1728, 580, -568, 640, -628, 576, -1672, 636, -628, 580, -1684, 624, -568, 640, -568, 640, -1728, 580, -564, 644, -580, 624, -572, 636, -568, 640, -624, 580, -572, 636, -568, 640, -624, 580, -628, 580, -1728, 580, -1676, 632, -572, 632, -580, 604, -592, 640, -568, 640, -576, 628, -1672, 636, -568, 640, -1728, 580, -572, 636, -628, 576, -1676, 636, -568, 636, -20064, 580, -1672, 640, -568, 636, -572, 632, -576, 632, -576, 604, -596, 636, -572, 636, -568, 640, -572, 632, -568, 640, -628, 580, -568, 636, -572, 636, -568, 640, -572, 632, -628, 552, -600, 636, -564, 644, -568, 636, -572, 636, -624, 580, -628, 580, -568, 640, -568, 640, -564, 640, -572, 636, -568, 636, -572, 636, -1680, 628, -1676, 632, -1668, 640, -1668, 640]

		

client = mqtt.Client()

client.connect("localhost", 1883, 60)

offset = 0;
topic = 'ESP12E-d776db/cmd'
#os.system ("mosquitto_pub -h raspberrypi-desktop -t ESP12E-d776db/cmd -q 1 -m irrawbegin")
client.publish(topic, payload='irrawbegin', qos=1, retain=False)
for i in xrange(len(irbuf)/10):
	#print abs_irbuf[offset:offset+10]
	payload = ''
	for j in xrange(10):
		payload += '%d ' % abs(irbuf[offset])
		offset+=1
	#os.system("mosquitto_pub -h raspberrypi-desktop -t ESP12E-d776db/cmd -q 1 -m \"irrawpart %s\"" % payload)
	client.publish(topic, payload='irrawpart %s' % payload, qos=1, retain=False)
	#print "payload = %s" % payload
	
if offset < len(irbuf):
	payload = ''
	for j in xrange(len(irbuf)-offset):
		payload += '%d ' % abs(irbuf[offset])
		offset += 1
	#print "payload = %s" % payload
	#os.system("mosquitto_pub -h raspberrypi-desktop -t ESP12E-d776db/cmd -q 1 -m \"irrawpart %s\"" % payload)
	client.publish(topic, payload='irrawpart %s' % payload, qos=1, retain=False)

#os.system ("mosquitto_pub -h raspberrypi-desktop -t ESP12E-d776db/cmd -q 1 -m irrawend")
client.publish(topic, payload='irrawend', qos=1, retain=False)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

