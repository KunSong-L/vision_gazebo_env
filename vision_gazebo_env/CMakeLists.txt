cmake_minimum_required(VERSION 3.0.2)
project(vision_gazebo_env)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES vision_gazebo_env
#  CATKIN_DEPENDS roscpp rospy std_msg
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(control_camera src/control_camera.cpp)
target_link_libraries(control_camera ${catkin_LIBRARIES})

add_executable(circle_control src/circle_control.cpp)
target_link_libraries(circle_control ${catkin_LIBRARIES})
