#!/usr/bin/env python
import rospy
import sys
from ros_in_class.srv import addTwoInt
from ros_in_class.srv import addTwoIntRequest
from ros_in_class.srv import addTwoIntResponse

def add_two_int_client(x,y):
    rospy.wait_for_service('add_two_int',addTwoInt)
    try:
        add_two_int = rospy.ServiceProxy('add_two_int',addTwoInt)
        respl = add_two_int(x,y)
        return respl.sum
    except rospy.ServiceException, e:
        print("Service call failed: {}".format(e))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print("Error")
        sys.exit(1)
    print("Requesting {} + {}".format(x, y))
    s = add_two_int_client(x, y)
    print("%s + %s = %s",x, y, s)