#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from ros_in_class.srv import yourservicefile, yourservicefileResponse

PI = 3.1415926535897
vel = Twist()
pos = Pose()
updated_pose = Pose()
init = True
updated = False
isLinear = True
isAngular = False
isHorizontal = True

updated_degree = 0
checker_degree = 0

running = False

def start(request):
    global running
    running = True
    print("i")
    return yourservicefileResponse()

def stop(request):
    global running
    running = False
    print("i")
    return yourservicefileResponse()

def callback_pose(data):
    global pos,init,updated,updated_pose, updated_degree,checker_degree
    pos = data
    if pos.theta < 0 :
        checker_degree = pos.theta * 180 / PI + 360
    else:
        checker_degree = pos.theta * 180 / PI

    if (init == True) or (updated == True):
        updated_pose = pos
        updated_degree = checker_degree
        init = False
        updated = False
        
    rospy.loginfo("Robot x = %f : y = %f : z = %f\n",data.x,data.y,data.theta)

def move():
    global pos, updated_pos, init, updated, isLinear, isAngular, isHorizontal, checker_degree, updated_degree, running
    while not rospy.is_shutdown():
        if running == True:
            if isLinear == True:
                vel.linear.x = 5
                vel.linear.y = 0
                vel.linear.z = 0
                vel.angular.x = 0
                vel.angular.y = 0
                vel.angular.z = 0
                goal_distance = 3
                if isHorizontal == True:
                    while (abs(pos.x - updated_pose.x) <= goal_distance):
                        velocity_publisher.publish(vel)
                
                    vel.linear.x = 0
                    velocity_publisher.publish(vel)

                else:
                    while (abs(pos.y - updated_pose.y) <= goal_distance):
                        velocity_publisher.publish(vel)

                    vel.linear.x = 0
                    velocity_publisher.publish(vel)

                isHorizontal = not isHorizontal
                isLinear = False
                isAngular = True
                updated = True

            elif isAngular == True:
                vel.linear.x = 0
                vel.linear.y = 0
                vel.linear.z = 0
                vel.angular.x = 0
                vel.angular.y = 0
                vel.angular.z = 10 * 2 * PI/360
                goal_angle = 90
                while (abs(checker_degree - updated_degree) <= goal_angle):
                    velocity_publisher.publish(vel)

                vel.angular.z = 0
                velocity_publisher.publish(vel)

                isAngular = False
                isLinear = True
                updated = True

            rate.sleep()    
        
if __name__ == '__main__':
    try:
        rospy.init_node('turtle_move', anonymous=True)
        rate = rospy.Rate(20) # 10 Hz
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=10)
        pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, callback_pose)
        start_service = rospy.Service("start",yourservicefile,start)
        stop_service = rospy.Service("stop",yourservicefile,stop)

        move()
        

    except rospy.ROSInterruptException:
        pass
    