#!/usr/bin/python


class IOTCmd( object ):
	def __init__( self, dest_dev_id, payload ):
		self.payload = payload
		self.topic = dest_dev_id + '/cmd'

	def send_using_client( self, mqtt_client ):
		print "sending to topic: ", self.topic, " payload: ", self.payload
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

class IrSendProtCmd( IOTCmd ):
	def __init__( self, dest_dev_id, prot, hexcmd, nbits ):
		IOTCmd.__init__( self, dest_dev_id, 'irsendprot %s %s %d' % ( prot, hexcmd, nbits ) )

class GpioSetCmd ( IOTCmd ):
	def __init__( self, dest_dev_id, gpio_num, gpio_val ):
		IOTCmd.__init__( self, dest_dev_id, 'write %d %d' % (gpio_num, gpio_val) )

class GpioGetCmd( IOTCmd ):
	def __init__( self, dest_dev_id, gpio_num, res_topic ):
		IOTCmd.__init__( self, dest_dev_id, 'read %d %s' % ( gpio_num, res_topic ) )

class StartA2DCmd( IOTCmd):
	def __init__( self, dest_dev_id, res_topic ):
		IOTCmd.__init__( self, dest_dev_id, 'startA2D %s' % res_topic )

class StopA2DCmd( IOTCmd):
	def __init__( self, dest_dev_id ):
		IOTCmd.__init__( self, dest_dev_id, 'stopA2D' )
#UNIT TEST

import MqttClient as MqttClient 

def main():
	mqtt_c = MqttClient.MqttClient() 
	mqtt_c.connect( 'localhost' )
	mqtt_c.LoopStart()
	import time
	while not mqtt_c.is_connected():
		print "Waiting for MQTT client to connect..."
		time.sleep(1)
	print "Connected!"

	print "IrSendProt"
	IrSendProtCmd( 'ESP12E-d776db', 'NEC', '0x12345678', 36 ).send_using_client( mqtt_c )
	time.sleep ( 1 )
	print "GpioSet"
	GpioSetCmd( 'ESP12E-d776db', 16, 0).send_using_client( mqtt_c )
	time.sleep( 1 )	
	print "GpioSet"
	GpioSetCmd( 'ESP12E-d776db', 16, 1).send_using_client( mqtt_c )
	time.sleep( 1 )
	print "GpioGet"
	mqtt_c.subscribe( "ESP12E-d776db/gpio16" )
	GpioGetCmd( 'ESP12E-d776db', 16, 'gpio16' ).send_using_client( mqtt_c )
	GpioSetCmd( 'ESP12E-d776db', 16, 0).send_using_client( mqtt_c )
	GpioGetCmd( 'ESP12E-d776db', 16, 'gpio16' ).send_using_client( mqtt_c )
	print "ADC"
	mqtt_c.subscribe( "ESP12E-d776db/adc" )
	StartA2DCmd( 'ESP12E-d776db', 'adc' ).send_using_client ( mqtt_c )
	time.sleep( 10 )
	StopA2DCmd( 'ESP12E-d776db' ).send_using_client( mqtt_c )
	time.sleep( 5 )

	mqtt_c.LoopStop()
	return 0

if __name__ == "__main__":
	main()
