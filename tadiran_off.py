
#!/usr/bin/python


import os
import paho.mqtt.client as mqtt
from  struct import *

irbuf = [8984, -4500, 644, -564, 640, -564, 644, -1664, 644, -560, 648, -564, 640, -568, 640, -1664, 644, -560, 648, -1660, 648, -564, 644, -560, 644, -1672, 640, -560, 644, -560, 648, -564, 640, -564, 644, -564, 644, -560, 644, -560, 648, -564, 640, -560, 648, -1664, 644, -568, 640, -564, 640, -568, 640, -620, 584, -564, 644, -564, 644, -1660, 644, -564, 644, -1668, 640, -564, 644, -560, 648, -1660, 648, -564, 640, -19996, 648, -1664, 644, -564, 644, -568, 640, -564, 644, -564, 640, -560, 648, -564, 640, -564, 644, -564, 640, -564, 644, -568, 640, -560, 644, -568, 640, -568, 640, -564, 640, -568, 640, -624, 580, -564, 644, -564, 644, -564, 640, -568, 640, -568, 640, -564, 644, -564, 640, -564, 644, -564, 640, -568, 640, -564, 644, -1668, 640, -1664, 644, -1668, 640, -564, 644,
]

		
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

