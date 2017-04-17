#!/usr/bin/python

import MqttClient as MqttClient 
import TadiranACRemoteCmd as TadiranACRemoteCmd


def main():
	mqtt_c = MqttClient.MqttClient() 
	mqtt_c.connect( 'localhost' )
	mqtt_c.LoopStart()
	import time
	while not mqtt_c.is_connected():
		print "Waiting for MQTT client to connect..."
		time.sleep(1)
	print "Connected!"

	#c = TadiranACRemoteCmd.Off( 'ESP12E-d776db' )
	#c = TadiranACRemoteCmd.HeatOn30( 'ESP12E-d776db' )
	#c = TadiranACRemoteCmd.CoolOn26( 'ESP12E-d776db' )

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--id", help="IOT device ID to send the command to" ) 
	parser.add_argument("-d", "--dev", choices = ["ac", "heater", "shades", "irrigation"], help="which home device should the IOT control" ) 
	parser.add_argument("-c", "--command", choices=["off", "on", "cool", "heat", "up", "down"], help="Command to send to home device (cool/heat - for AC, up/down - for Shades)")
	parser.add_argument("-t", "--temp", type=int, help="Temp settings (for AC)")
	args = parser.parse_args()
	if (args.dev == "ac"):
		if (args.command in  [ "off", "cool", "heat"] ):
			if (args.command == "off"):
				c =  TadiranACRemoteCmd.CommandsDic[args.command]( args.id )
			else:
				c = TadiranACRemoteCmd.CommandsDic[args.command][args.temp]( args.id ) 
			c.send_using_client( mqtt_c )
	elif (args.dev == "heater"):
		pass
	elif (args.dev == "heater"):
		pass
	elif (args.dev == "shades"):
		pass
	elif (args.dev == "irrigation"):
		pass

	mqtt_c.LoopStop()
	return 0

if __name__ == "__main__":
	main()
