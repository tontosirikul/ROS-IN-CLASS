#!/usr/bin/env python
import rospy
from ros_in_class.srv import yourservicefile,yourservicefileResponse
from ros_in_class.msg import custom

custom_info = custom()

def handle_multiple_num(req):
    return yourservicefileResponse(req.a * req.b * req.c)

def main():
    rospy.init_node('pub_service', anonymous = False)
    s = rospy.Service('multiply', yourservicefile, handle_multiple_num)
    print("Ok")
    rospy.spin()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

