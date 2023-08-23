#!/usr/bin/env python3
# coding=utf-8

import rospy
from geometry_msgs.msg import Twist
distance_traveled = 0.0

def cmd_vel_callback(msg):
    global distance_traveled
    linear_velocity = msg.linear.x
    time_interval = 0.1  # Assuming a publishing rate of 10Hz
    distance_traveled += linear_velocity * time_interval
    rospy.loginfo("Total distance traveled:  %f m",distance_traveled)

rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback) 

# Access the final distance traveled
if __name__ == "__main__":
    rospy.init_node("distance_calc")
    # 订阅激光雷达的数据话题
    vel_sub = rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback, queue_size=10)
    rospy.spin()
    print("Total distance traveled: ", distance_traveled)