#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time

PI = 3.1415926535897
angle_lst = []
vel = Twist()
goal = Pose()

def callback_pose(data):
    rospy.loginfo("Robot x = %f : y = %f : z = %f\n",data.x,data.y,data.theta)


def move_forward ():
    linear_speed = 5
    goal_distance = 3
    vel.linear.x = linear_speed
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 0
    
    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()
        current_distance = 0    
        while (current_distance < goal_distance):
            velocity_publisher.publish(vel)
            t1 = rospy.Time.now().to_sec()
            current_distance = linear_speed * (t1-t0)
        
        vel.linear.x = 0
        velocity_publisher.publish(vel)
        rate.sleep()
        break

def move_rotate ():
    angular_speed = 10 * 2 * PI/360
    goal_angle = 90 * 2 * PI/360
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = angular_speed
    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while (current_angle < goal_angle):
            velocity_publisher.publish(vel)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed * (t1-t0)
        
        vel.angular.z = 0
        velocity_publisher.publish(vel)
        rate.sleep()
        break
        
if __name__ == '__main__':
    try:
        rospy.init_node('turtle_move', anonymous=True)
        rate = rospy.Rate(10) # 10 Hz
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=10)
        pose_publisher = rospy.Subscriber('/turtle1/pose',Pose, callback_pose)
        rospy.sleep(2)
        move_forward ()
        rospy.sleep(2)
        move_rotate()
        rospy.sleep(2)
        move_forward ()
        rospy.sleep(2)
        move_rotate()
        rospy.sleep(2)
        move_forward ()
        rospy.sleep(2)
        move_rotate()
        rospy.sleep(2)
        move_forward ()
        rospy.sleep(2)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass