#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import SetModelConfiguration
from gazebo_msgs.srv import SetModelConfigurationRequest
import math
rospy.init_node('robot_control')

reset_joints = rospy.ServiceProxy(
    '/gazebo/set_model_configuration', SetModelConfiguration)

# bottom joint name
bottom_joint_list = []
for i in range(1, 4):
    for j in range(1, 6):
        bottom_joint_list.append('bottom_joint_' + str(i) + '_' + str(j))

# upper joint name
upper_joint_list = []
for i in range(1, 4):
    for j in range(1, 6):
        upper_joint_list.append('upper_joint_' + str(i) + '_' + str(j))

# upper base joint
upper_base_joint = ['upper_base_joint']
# camera joint
upper_camera_joint = ['upper_camera_joint']


reset_req = SetModelConfigurationRequest()
reset_req.model_name = 'robot_model'
reset_req.urdf_param_name = 'robot_description'
reset_req.joint_names = bottom_joint_list + upper_joint_list + upper_base_joint + upper_camera_joint  # list

print(reset_req.joint_names)
# for bottom or upper joint: 1 :increase; 0:hold; -1:decrease
# for upper base joint: 1:increase;0 : hold; -1:decrease
# upper camera joint: the same

state_control = [0, 0, 0, 1]

del_theta = 0.05  
del_pos = 0.05  
del_camera = 0.1  

lower_theta = -0.5
upper_theta = 0.6
lower_upper_base_pos = -0.13
upper_upper_base_pos = 0.03
lower_camera_theta = -math.pi-0.3
upper_camera_theta = math.pi+0.3


bottom_now_theta = lower_theta
upper_now_theta = upper_theta
upper_base_pos = upper_upper_base_pos
camera_theta = 0


rate = rospy.Rate(5)  # 10hz


while not rospy.is_shutdown():
    now_joint_positions = []
    # state control
    for i in range(0, 4):
        if i == 0:
            bottom_now_theta = bottom_now_theta + state_control[i]*abs(del_theta)
            for j in range(0,3):
                now_joint_positions = now_joint_positions + [-bottom_now_theta, 2*bottom_now_theta, -bottom_now_theta, bottom_now_theta, -2*bottom_now_theta]
        elif i == 1:
            upper_now_theta = upper_now_theta + state_control[i]*abs(del_theta)
            for j in range(0,3):
                now_joint_positions = now_joint_positions + [-upper_now_theta, 2*upper_now_theta, -upper_now_theta, upper_now_theta, -2*upper_now_theta]
        elif i==2:
            upper_base_pos = upper_base_pos + state_control[i]*abs(del_pos)
            now_joint_positions = now_joint_positions + [upper_base_pos]
        elif i==3:
            camera_theta = camera_theta + state_control[i]*abs(del_camera)
            now_joint_positions = now_joint_positions + [camera_theta]

    # check range
    for i in range(0,4):
        if bottom_now_theta > upper_theta:
            state_control[0] = -1
    print(now_joint_positions)
    reset_req.joint_positions = now_joint_positions  # list
    # reset_req.joint_positions = [-theta,2*theta,-theta] #list
    res = reset_joints(reset_req)
    rate.sleep()
