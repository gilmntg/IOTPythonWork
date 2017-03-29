#!/usr/bin/python


import paho.mqtt.client as mqtt


class MqttClient(object):
	def __init__( self ):
		self.client = mqtt.Client()
		if self.client is not None:
			print "Setting callbacks..."
			self.client.on_connect = self.on_connect
			self.client.on_message = self.on_message
		self.connected = False

	def on_connect(self, client, userdata, flags, rc):
    		print("Connected with result code "+str(rc))
		self.connected = True

	def on_message(self, client, userdata, msg):
    		print(msg.topic+" "+str(msg.payload))
	
	def connect( self, hostname ):
		self.client.connect( hostname, 1883, 60 )

	def publish( self, topic, payload, qos, retain ):
		if not self.connected:
			print "Tried to publish when client is not connected"
			return False
		self.client.publish( topic, payload, qos, retain )
		return True

	def subscribe (self, topic ):
		if not self.connected:
			print "Tried to subscribe when client is not connected"
			return False
		self.client.subscribe( topic )
		return True

	def is_connected ( self ):
		return self.connected
	def LoopStart( self ):
		self.client.loop_start()
	def LoopStop( self ):
		self.client.loop_stop()
		

class IOTCmd( object ):
	def __init__( self, dest_dev_id, payload ):
		self.payload = payload
		self.topic = dest_dev_id + '/cmd'

	def send_using_client( self, mqtt_client ):
		return mqtt_client.publish( self.topic, self.payload, 1, False )		


class IrRawBeginIOTCmd( IOTCmd ):
	def __init__( self, dest_dev_id ):
		IOTCmd.__init__( self, dest_dev_id, 'irrawbegin' ) 

class IrRawPartIOTCmd( IOTCmd ):
	def __init__( self, dest_dev_id, payload_part ):
		IOTCmd.__init__( self, dest_dev_id, 'irrawpart ' + payload_part ) 

class IrRawEndIOTCmd( IOTCmd ):
	def __init__( self, dest_dev_id ):
		IOTCmd.__init__( self, dest_dev_id, 'irrawend' ) 

#TODO: More IOT commands

class TadiranACRemoteCmd(object):
	def __init__( self, irbuf, dest_dev_id):
		self.irbuf = irbuf
		self.offset = 0
		self.dev_id = dest_dev_id

	def send_using_client( self, mqtt_client ):
		IrRawBeginIOTCmd( self.dev_id ).send_using_client( mqtt_client ) 
		for i in xrange(len(self.irbuf)/10):
			payload = ''
			for j in xrange(10):
				payload += '%d ' % abs(self.irbuf[self.offset])
				self.offset+=1
			IrRawPartIOTCmd( self.dev_id, payload ).send_using_client ( mqtt_client )
			
		if self.offset < len(self.irbuf):
			payload = ''
			for j in xrange(len(self.irbuf)-self.offset):
				payload += '%d ' % abs(self.irbuf[self.offset])
				self.offset += 1
			IrRawPartIOTCmd( self.dev_id, payload ).send_using_client ( mqtt_client )

		IrRawEndIOTCmd( self.dev_id ).send_using_client ( mqtt_client )
			

class Heat25(TadiranACRemoteCmd):
	def __init__( self, device_id):
		buf = [8980, -4560, 580, -564, 640, -628, 580, -1728, 580, -1728, 580, -568, 640, -628, 576, -1672, 636, -628, 580, -1684, 
                       624, -568, 640, -568, 640, -1728, 580, -564, 644, -580, 624, -572, 636, -568, 640, -624, 580, -572, 636, -568, 640,
                       -624, 580, -628, 580, -1728, 580, -1676, 632, -572, 632, -580, 604, -592, 640, -568, 640, -576, 628, -1672, 636, -568, 
                       640, -1728, 580, -572, 636, -628, 576, -1676, 636, -568, 636, -20064, 580, -1672, 640, -568, 636, -572, 632, -576, 632, 
                       -576, 604, -596, 636, -572, 636, -568, 640, -572, 632, -568, 640, -628, 580, -568, 636, -572, 636, -568, 640, -572, 632, 
                       -628, 552, -600, 636, -564, 644, -568, 636, -572, 636, -624, 580, -628, 580, -568, 640, -568, 640, -564, 640, -572, 636, 
                       -568, 636, -572, 636, -1680, 628, -1676, 632, -1668, 640, -1668, 640]
		TadiranACRemoteCmd.__init__( self, buf, device_id) 

#TODO: more TadiranAC commands...

mqtt_c = MqttClient() 
mqtt_c.connect( 'localhost' )
mqtt_c.LoopStart()
import time
while not mqtt_c.is_connected():
	print "Waiting for MQTT client to connect..."
	time.sleep(1)
print "Connected!"

c = Heat25( 'ESP12E-d776db' )
c.send_using_client( mqtt_c )

mqtt_c.LoopStop()
