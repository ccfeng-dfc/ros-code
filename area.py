#!/usr/bin/env python3
# coding=utf-8

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point32
from shapely.geometry import Polygon

# 全局变量
scan_data = None
previous_polygon = None
accumulated_area = 0.0

def scan_callback(msg):
    global scan_data, previous_polygon, accumulated_area
    scan_data = msg

def calculate_known_area():
    global previous_polygon, accumulated_area
    rospy.init_node('known_area_calculator', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rate = rospy.Rate(1)  # 每秒一次的循环速率

    while not rospy.is_shutdown():
        if scan_data is not None:
            ranges = scan_data.ranges
            angle_min = scan_data.angle_min
            angle_increment = scan_data.angle_increment

            polygon_points = []
            for i, range_value in enumerate(ranges):
                if range_value < scan_data.range_max and range_value > scan_data.range_min:
                    angle = angle_min + i * angle_increment
                    x = range_value * math.cos(angle)
                    y = range_value * math.sin(angle)
                    polygon_points.append(Point32(x, y, 0.0))

            polygon = Polygon([[point.x, point.y] for point in polygon_points])
            area = polygon.area

            if previous_polygon is not None:
                overlap_polygon = previous_polygon.intersection(polygon)
                overlap_area = overlap_polygon.area
                area -= overlap_area

            accumulated_area += area  # 更新累积面积
            rospy.loginfo('Accumulated area: %.2f square units (%.2f)' % (accumulated_area, area))


            previous_polygon = polygon

        rate.sleep()

if __name__ == '__main__':
    try:
        calculate_known_area()
    except rospy.ROSInterruptException:
        pass