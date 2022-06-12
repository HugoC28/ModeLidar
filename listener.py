#!/usr/bin/env python
import rospy
# Import of Joysticks library
from sensor_msgs.msg import Joy
import time
import serial

################## MACROS ####################
JOY_LEFT_X = 0
JOY_LEFT_Y = 1
JOY_RIGHT_X = None
JOY_RIGHT_Y = 2

############ READING SERIAL DATA #############
#Creating a serial object that will be used to read the data from the joystick.
ser = serial.Serial(
    port = '/dev/serial0',
    #port = '/dev/ttyUSB0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1)
counter = 0

################ FUNCTIONS #################

def callback(data):
    """
    The function callback() is called every time a message is received on the topic /chatter. 
    The function callback() is defined as taking one argument, data, which is the message received. 
    The function callback() prints the message data to the screen using the loginfo() function
    :param data: The message data
    """
    commandMotorLeft = int(data.axes[JOY_LEFT_Y])
    commandMotorRight = int(data.axes[JOY_RIGHT_Y])
    
    commandMotor = "%+04dL %+04dR\r\n" % (commandMotorLeft, commandMotorRight)
    
    rospy.loginfo(" %s", commandMotor)
    sendData(commandMotor)


def sendData(data):
    ser.write(bytes(data,"ascii"))


def listener():
    """
    `rospy.Subscriber("chatter", Joy, callback)`
    This line creates a subscriber to the topic `chatter` which is of type `Joy`. When a message is
    received, the callback function `callback` is called
    """
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", Joy, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

