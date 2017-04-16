#!/usr/bin/python

import MqttClient as MqttClient 
import TadiranACRemoteCmd as TadiranACRemoteCmd



mqtt_c = MqttClient.MqttClient() 
mqtt_c.connect( 'localhost' )
mqtt_c.LoopStart()
import time
while not mqtt_c.is_connected():
	print "Waiting for MQTT client to connect..."
	time.sleep(1)
print "Connected!"


c = TadiranACRemoteCmd.Off( 'ESP12E-d776db' )
#c = TadiranACRemoteCmd.HeatOn30( 'ESP12E-d776db' )
#c = TadiranACRemoteCmd.CoolOn26( 'ESP12E-d776db' )
c.send_using_client( mqtt_c )

mqtt_c.LoopStop()


def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--iot-dev_id", help="IOT device ID to send the command to" ) 
	parser.add_argument("-d", "--home-device", choices = ["ac", "boiler", "shade"], help="which home device should the IOT control" ) 
	parser.add_argument("-c", "--command", choices=["off", "on", "mode", "up", "down"], help="Command to send to home device")
	parser.add_argument("-m", "--mode", choices=["off", "on", "cool", "heat"], help="Mode to set home device to")
	parser.add_argument("-t", "--temp", type=int, help="Temp settings (for AC only)")
	args = parser.parse_args()
	answer = args.square**2
	if args.verbosity == 2:
	    print "the square of {} equals {}".format(args.square, answer)
	elif args.verbosity == 1:
	    print "{}^2 == {}".format(args.square, answer)
	else:
	    print answer
	
if __name__ == "__main__":
	return main()
