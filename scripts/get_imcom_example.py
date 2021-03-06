#!/usr/bin/env python

import numpy as np
import cv2
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def rgb_cb(data):
  global cv_image
  bridge = CvBridge()
  cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
  # cv2.imshow("Image window", cv_image)
  # cv2.waitKey(3)

def cmdvel_cb(data):
  global cmd_vel
  cmd_vel = data
  rospy.logdebug("cmd_vel: {}".format(cmd_vel))

if __name__ == '__main__':
  command_pool = []
  image_pool = []
  cmd_vel = Twist()
  cv_image = np.zeros((480,640,3),dtype=np.uint8)	
  rospy.loginfo("Initializing node... ")
  rospy.init_node("collect_data", anonymous=True, log_level=rospy.DEBUG)
  rospy.Subscriber("/cmd_vel", Twist, cmdvel_cb)
  rospy.Subscriber("/camera/color/image_raw", Image, rgb_cb)
  rate = rospy.Rate(5) # 5 Hz
  while not rospy.is_shutdown():
    command_pool.append(cmd_vel)
    image_pool.append(cv_image)
    rate.sleep()
  # cv2.destroyAllWindows()
