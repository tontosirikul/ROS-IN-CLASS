#!/usr/bin/env python
import rospy
from ros_in_class.msg import custom

customs = custom()

if __name__ == '__main__':
    try:
        rospy.init_node('pub_msg', anonymous=True)
        rate = rospy.Rate(10) # 10 Hz
        publisher = rospy.Publisher('/custom_info', custom,queue_size=10)
        while not rospy.is_shutdown():
            customs.id = 1
            publisher.publish(customs)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass