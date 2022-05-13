#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import SetModelConfiguration
from gazebo_msgs.srv import SetModelConfigurationRequest
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
import math
rospy.init_node('robot_control')

state_msg = ModelState()
state_msg.model_name = 'robot_model'
state_msg.pose.position.x = 0
state_msg.pose.position.y = 0
state_msg.pose.position.z = 0
state_msg.pose.orientation.x = 0
state_msg.pose.orientation.y = 0
state_msg.pose.orientation.z = 0
state_msg.pose.orientation.w = 1

reset_joints = rospy.ServiceProxy('/gazebo/set_model_configuration', SetModelConfiguration)
reset_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

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

# for bottom or upper joint: 1 :increase; 0:hold; -1:decrease
# for upper base joint: 1:increase;0 : hold; -1:decrease
# upper camera joint: the same

state_control_total = [[0, -1, 0, 1],[0, 0, 1, 1],[0, 1, 0, 1],[-1, 0, 0, 1],[0, 0, -1, 1],[1, 0, 0, 1]]
state_num = 0

del_theta = 0.05  
del_pos = 0.02  
del_camera = 0.1  

lower_theta = -0.5
upper_theta = 0.3
lower_upper_base_pos = -0.10
upper_upper_base_pos = 0.03
lower_camera_theta = -math.pi-0.3
upper_camera_theta = math.pi+0.3


bottom_now_theta = upper_theta
upper_now_theta = upper_theta
upper_base_pos = lower_upper_base_pos
camera_theta = 0
base_pose = 0.5

rate = rospy.Rate(5)  # 10hz


while not rospy.is_shutdown():
    state_control = state_control_total[state_num]

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

    # add base move
    

    for i in range(0,3):
        if abs(state_control[i])==0:
            continue
        else:
            if i == 0:
                if bottom_now_theta > upper_theta or bottom_now_theta < lower_theta:
                    state_num = (state_num + 1)%6
            if i == 1:
                if upper_now_theta > upper_theta or upper_now_theta < lower_theta:
                    state_num = (state_num + 1)%6
            if i==2:
                if upper_base_pos > upper_upper_base_pos or upper_base_pos < lower_upper_base_pos:
                    state_num = (state_num + 1)%6
    
    # check camera
    if camera_theta > upper_camera_theta:
        state_control[3] = -1
    elif camera_theta < lower_camera_theta:
        state_control[3] = 1

    reset_req.joint_positions = now_joint_positions  # list
    # reset_req.joint_positions = [-theta,2*theta,-theta] #list
    res = reset_joints(reset_req)

    if state_num == 4:
        base_pose = base_pose + del_pos
    state_msg.pose.position.z = base_pose
    reset_state(state_msg)
    rate.sleep()
