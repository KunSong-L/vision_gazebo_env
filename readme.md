# 基于realsense的gazebo仿真环境
基于ubuntu 16.04LTS和ROS kinetic 实现视觉仿真环境，并实现了相机的任意轨迹运动。可用于SFM或者SLAM等工作。

注意gazebo的版本，通过`gazebo -v`查看，不要使用gazebo 7.0.0。 可以通过如下方式升级

```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

sudo apt-get update

sudo apt-get install gazebo7 -y
```

## 安装

```
cd ~/catkin_ws/src
git clone https://github.com/KunSong-L/vision_gazebo_env.git
cd ..
catkin_make
```

## 运行
运行仅有相机的仿真环境
```
roslaunch vision_gazebo_env vision_gazebo_env.launch
rosrun vision_gazebo_env control_camera
```
运行整个机器人的仿真环境
```
roslaunch vision_gazebo_env vision_robot.launch
rosrun vision_gazebo_env control_joint.py
```

# Gazebo simulation environment based on realsense
Based on ubuntu 16.04LTS and ROS kinetic, the visual simulation environment is realized, and the arbitrary trajectory motion of the camera is realized. It can be used for SFM or SLAM.

Pay attention to the gazebo version, check with `gazebo -v`, do not use gazebo 7.0.0. It can be upgraded as follows

````
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

sudo apt-get update

sudo apt-get install gazebo7 -y
````

## Install
### Install dependencies

````
cd ~/catkin_ws/src
git clone https://github.com/nilseuropa/realsense_ros_gazebo
````
If the compilation encounters errors of Name() and SimTime(), you can change Name() to GetName(), and then change SimTime() to GetSimTime().

### Install

````
cd ~/catkin_ws/src
git clone https://github.com/KunSong-L/vision_gazebo_env.git
cd..
catkin_make
````

## run
for camera simulation
```
roslaunch vision_gazebo_env vision_gazebo_env.launch
rosrun vision_gazebo_env control_camera
```

for robot simulation
```
roslaunch vision_gazebo_env vision_robot.launch
rosrun vision_gazebo_env control_joint.py
```