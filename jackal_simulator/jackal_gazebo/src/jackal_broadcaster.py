#!/usr/bin/env python
import rospy
import tf_conversions
import tf2_ros
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *

def handle_jackal_pose(msg, jackal_name):
	br = tf2_ros.TransformBroadcaster()
	t = TransformStamped()
	t.header.stamp  = rospy.Time.now()
	t.header.frame_id = "map"
	t.child_frame_id = jackal_name + "/base_link"
	t.transform.translation.x = msg.pose.pose.position.x
	t.transform.translation.y = msg.pose.pose.position.y
	t.transform.translation.z = 0.0
	t.transform.rotation = msg.pose.pose.orientation

	br.sendTransform(t)

if __name__ == "__main__":
	rospy.init_node('tf2_jackal_broadcaster')
	jackal_name = rospy.get_param("~jackalname")
	
	rospy.Subscriber('/%s/amcl_pose'%jackal_name, PoseWithCovarianceStamped, handle_jackal_pose, jackal_name)
	rospy.spin()

