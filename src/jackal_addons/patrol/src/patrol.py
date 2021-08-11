#! /usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def waypoint_client(entry):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    # Create goal
    goal = MoveBaseGoal()
    goal.target_pose.header.seq = 8
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = entry[0]
    goal.target_pose.pose.position.y = entry[1]
    goal.target_pose.pose.orientation.w = 1

    # Sends goal
    client.send_goal(goal)

    # Waits for server to complete
    client.wait_for_result()
    rospy.loginfo("Reached!")
    return


if __name__ == '__main__':
    patrol_list = [[7.2,5.6], [-4,8], [-5.5,-4], [9,-8]]
    rospy.init_node('patrol_waypoints')
    try:
        for i in range(len(patrol_list)):
            waypoint_client(patrol_list[i])
    except rospy.ROSInterruptException:
        pass