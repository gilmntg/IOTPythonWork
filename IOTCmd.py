#!/usr/bin/python


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


