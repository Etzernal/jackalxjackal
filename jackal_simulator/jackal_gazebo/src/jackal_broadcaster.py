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
	t.header.frame_id = "base_link"
	t.child_frame_id = jackal_name
	t.transform.translation.x = msg.pose.pose.position.x
	t.transform.translation.y = msg.pose.pose.position.y
	t.transform.translation.z = 0.0
	# q = tf_conversions.transformations.quaternion_from_euler(0,0,msg.theta)
	# t.transform.rotation.x = q[0]
	# t.transform.rotation.y = q[1]
	# t.transform.rotation.z = q[2]
	# t.transform.rotation.w = q[3]
	t.transform.rotation = msg.pose.pose.orientation

	br.sendTransform(t)

if __name__ == "__main__":
	rospy.init_node('tf2_jackal_broadcaster')
	jackal_name = 'jackal1'
	rospy.Subscriber('/jackal1/jackal_velocity_controller/odom', Odometry, handle_jackal_pose, jackal_name)
	rospy.spin()

