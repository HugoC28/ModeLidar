#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.

# Simple talker demo that published std_msgs/Strings messages
# to the 'chatter' topic

################# IMPORT #################

import rospy
from random import randint
from std_msgs.msg import String
from std_msgs.msg import Header
# Import package for conversion
import time
import serial
from io import BytesIO
# Import of Joysticks library
from sensor_msgs.msg import Joy


################## MACRO ##################
xmoy = 1814
xmax = 4015
ymoy = 1909
ymax = 4030
zmoy = 1871
zmax = 4030


############ READING SERIAL DATA #############
#Creating a serial object that will be used to read the data from the joystick.
ser = serial.Serial(
    port = '/dev/serial0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1)
counter = 0

################# FUNCTIONS ##################
def data_conversion(valInt, valMoy, valMax) :
    """
    This function takes in three values, the first being the value to be converted, the second being the
    average value, and the third being the maximum value. It then converts the first value into a
    percentage of the difference between the average and the maximum
    :param valInt: the value of the data point
    :param valMoy: the average value of the data
    :param valMax: the maximum value of the data
    """
    valInterm = valInt-valMoy
    if valInterm > 0 :
        finalVal = (valInterm/(valMax-valMoy))*100
    else :
        finalVal = (valInterm/(valMoy))*100
    if finalVal > -0.5 and finalVal < 0.5 :
        finalVal = 0
    return finalVal   

#def nombre_aleatoire():
#     """
#     It creates a list of three random numbers between -100 and 100
#     :return: A list of 3 random numbers between -100 and 100
#     """
#    L = [0, 0, 0]
#    for i in range(len(L)):
#        L[i] = float(randint(-100, 100))
#    return (L)

def read_joy():
    x_int = int(ser.read(4))
    y_int = int(ser.read(4))
    z_int = int(ser.read(4))
    i_int = int(ser.read(4))
    valX = float(data_conversion(x_int,xmoy,xmax))
    valY = float(data_conversion(y_int,ymoy,ymax))
    valZ = float(data_conversion(z_int,zmoy,zmax))
    return [valX, valY, valZ]


def talker():
    # Declare that your node is publishing to the "chatter" topic using the message type String
    pub = rospy.Publisher('chatter', Joy, queue_size=10)
    # This line tells rospy the name of your node -- until rospy has this info, it cannot start to communicate with the ROS Master
    rospy.init_node('talker', anonymous=True)
    # "anonymous=True" --> ensures that your node has a unique name by adding random numbers to the end of NAME
    # 10hz				                # Set a loop execution frequency (here : one execution every 10 sec
    rate = rospy.Rate(10)
    # Execute the "while" boucle while the ros system isn't shotdown | Standard rospy construct
    while not rospy.is_shutdown():
        joy = Joy()
        joy.header = Header()
        joy.axes = read_joy()
        # the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout
        joy.buttons = []
        pub.publish(joy)
        rate.sleep()


# This is a standard Python idiom. It is used to guard the main code from being executed when the
# module is imported.
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
