#!/usr/bin/env python
import rospy
from ros_in_class.srv import addTwoInt
from ros_in_class.srv import addTwoIntRequest
from ros_in_class.srv import addTwoIntResponse

def handle_add_two_int(req):
    print(type(req.a))
    print("Returning {} + {} = {}\n".format(req.a,req.b,(req.a+req.b)))
    return addTwoIntResponse(req.a+req.b)

def add_two_int_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_int',addTwoInt,handle_add_two_int)
    print("Ready to add two ints")
    rospy.spin()

if __name__ == "__main__":
    add_two_int_server()
