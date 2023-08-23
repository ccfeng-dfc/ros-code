#!/usr/bin/env python3
# coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

count = 0

# 激光雷达回调函数
def lidar_callback(msg):
    global vel_pub
    global count
    middle = len(msg.ranges)//2
    #dist = msg.ranges[middle]
    dist = msg.ranges[0]
    rospy.loginfo("Front distance = %f m",dist)
    vel_cmd = Twist()
    if count > 0:
        count = count -1
        rospy.logwarn("TURN-count = %d",count)
        return
    
    vel_cmd =  Twist()
    if dist < 1.0:
        vel_cmd.angular.z = 0.5
        #count = 50
    else:
        vel_cmd.linear.x = 0.2
    vel_pub.publish(vel_cmd)

# 主函数
if __name__ == "__main__":
    rospy.init_node("lidar_behavior")
    # 订阅激光雷达的数据话题
    lidar_sub = rospy.Subscriber("scan",LaserScan,lidar_callback,queue_size=10)
    # 发布机器人运动控制话题
    vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
    rospy.spin()