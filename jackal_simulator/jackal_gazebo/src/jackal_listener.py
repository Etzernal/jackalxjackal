#!/usr/bin/env python
import rospy
import math
import tf2_ros
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class Listener:

	def __init__(self):
		self.odom = Odometry()
		self.listen()


	def listen(self):
		sub = rospy.Subscriber("/amcl_pose", Odometry, self.odomCB)
		self.setupTF2Listener()

	def setupTF2Listener(self):
		rospy.init_node('tf2_jackal_listener')

		tfBuffer = tf2_ros.Buffer()
		listener=tf2_ros.TransformListener(tfBuffer)

		#rospy.wait_for_service('spawn')
		#spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
		jackal_name = 'jackal2'
		#spawner(4,2,0,jackal_name)

		jackal_vel = rospy.Publisher('%s/jackal_velocity_controller/cmd_vel'%jackal_name, Twist, queue_size = 1)

		rate = rospy.Rate(10.0)
	    #listener.waitForTransform("/jackal1", "/base_link", rospy.Time(), rospy.Duration(4.0))
		while not rospy.is_shutdown():
			try:			
				trans = tfBuffer.lookup_transform('base_link', 'jackal1', rospy.Time())
			except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
				rate.sleep()
				continue

			msg = Twist()
			e = euler_from_quaternion([self.odom.pose.pose.orientation.x, self.odom.pose.pose.orientation.y,
									 self.odom.pose.pose.orientation.z, self.odom.pose.pose.orientation.w])
			msg.angular.z = math.atan2(trans.transform.translation.y-e[1], trans.transform.translation.x-e[0])
			msg.linear.x = math.sqrt((trans.transform.translation.x-self.odom.pose.pose.position.x)**2 +
						 (trans.transform.translation.y-self.odom.pose.pose.position.y)**2)
			jackal_vel.publish(msg)
			rate.sleep()


	def odomCB(self, msg):
		self.odom = msg

if __name__ == '__main__':
	a = Listener()
	
	