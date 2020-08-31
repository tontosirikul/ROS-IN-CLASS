#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

PI = 3.1415926535897
vel = Twist()
pos = Pose()
updated_pose = Pose()
init = True
updated = False
isLinear = True
isAngular = False
isHorizontal = True

def callback_pose(data):
    global pos,init,updated,updated_pose
    pos = data
    if (init == True) or (updated == True):
        updated_pose = pos
        init = False
        updated = False
    if pos.theta < 0:
        pos.theta = pos.theta + 2 * PI
    rospy.loginfo("Robot x = %f : y = %f : z = %f\n",data.x,data.y,data.theta)

def initial_vel():
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 0

def move():
    global pos, updated_pos, init, updated, isLinear, isAngular, isHorizontal
    while not rospy.is_shutdown():
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
                    # rate.sleep()
                    velocity_publisher.publish(vel)
                
                vel.linear.x = 0
                velocity_publisher.publish(vel)
                rospy.sleep(1)
            else:
                while (abs(pos.y - updated_pose.y) <= goal_distance):
                    # rate.sleep()
                    velocity_publisher.publish(vel)

                vel.linear.x = 0
                velocity_publisher.publish(vel)
                rospy.sleep(1)
            isHorizontal = not isHorizontal
            isLinear = False
            updated = True
            isAngular = True

        elif isAngular == True:
            vel.linear.x = 0
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.x = 0
            vel.angular.y = 0
            vel.angular.z = 10 * 2 * PI/360
            goal_angle = 90 * 2 * PI/360

            while (abs(pos.theta - updated_pose.theta) <= goal_angle):
                velocity_publisher.publish(vel)
            vel.angular.z = 0
            velocity_publisher.publish(vel)   
            isAngular = False
            isLinear = True
            updated = True


if __name__ == '__main__':
    try:
        rospy.init_node('turtle_move', anonymous=True)
        rate = rospy.Rate(10) # 10 Hz
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=10)
        pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, callback_pose)

        rospy.sleep(1)
        move()
    
    except rospy.ROSInterruptException:
        pass
    