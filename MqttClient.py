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
