#include <ros/ros.h>
#include <gazebo_msgs/ModelState.h>
#include <geometry_msgs/Pose.h>
#include <gazebo_msgs/SetModelState.h>
#include <math.h>
#include <iostream>
#include <string>
using namespace std;

int main(int argc, char **argv) {
    
    ros::init(argc, argv, "move_gazebo_model");
    ros::NodeHandle n;
    ros::ServiceClient client = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");
    gazebo_msgs::SetModelState set_model_state_srv;
    gazebo_msgs::ModelState des_model_state;
    geometry_msgs::Twist twist;

    twist.linear.x = 0.0;
    twist.linear.y = 0.0;
    twist.linear.z = 0.0;
    twist.angular.x = 0.0;
    twist.angular.y = 0.0;
    twist.angular.z = 0.0;

    geometry_msgs::Pose pose;
    geometry_msgs::Quaternion quat;

    pose.orientation= quat;
    des_model_state.model_name = "test_model";  //设置模型的名称
    des_model_state.pose = pose;
    des_model_state.twist = twist;
    des_model_state.reference_frame = "world";

    double sim_time_step = 0.1;//多少时间更新一次模型
    double angle_T = 20;//旋转周期
    double z_T_size = 0.2;//旋转一周上升距离

    double qx,qy,qz,qw;
    double theta = 0;
    double init_pos_theta = M_PI;
    double del_theta = sim_time_step * 2*M_PI / angle_T;
    double x,y,z;
    double del_z = z_T_size * sim_time_step / angle_T;
    double R = 0.15;

    z = 0.18;//保持这个值和初始状态一致
    //先旋转一周然后向上
    del_z = 0;
    for(int i =0; i < int(angle_T/sim_time_step);i++)
    {
        theta += del_theta;

        qw = cos(theta/2);
        qx = 0.0;
        qy = 0.0;
        qz = sin(theta/2);

        x = R*cos(theta + init_pos_theta);
        y = R*sin(theta + init_pos_theta);
        z += del_z;

        double norm = sqrt(qx*qx+qy*qy+qz*qz+qw*qw);
        quat.w = qw/norm;
        quat.x = qx/norm;
        quat.y = qy/norm;
        quat.z = qz/norm;
        
        std::cout<<"R= "<<R<<"  x="<<x<<" y= "<<y<<" z=  "<<z<<" theta ="<<theta<<std::endl;

        pose.orientation= quat;
        pose.position.x = x;
        pose.position.y = y;
        pose.position.z = z;
        des_model_state.pose = pose;
        set_model_state_srv.request.model_state = des_model_state;
        client.call(set_model_state_srv);
        ros::spinOnce();
        ros::Duration(sim_time_step).sleep();
    }

    del_z = z_T_size * sim_time_step / angle_T;
    while(ros::ok()) {
        
        theta += del_theta;

        qw = cos(theta/2);
        qx = 0.0;
        qy = 0.0;
        qz = sin(theta/2);

        x = R*cos(theta + init_pos_theta);
        y = R*sin(theta + init_pos_theta);
        z += del_z;

        double norm = sqrt(qx*qx+qy*qy+qz*qz+qw*qw);
        quat.w = qw/norm;
        quat.x = qx/norm;
        quat.y = qy/norm;
        quat.z = qz/norm;
        
        std::cout<<"R= "<<R<<"  x="<<x<<" y= "<<y<<" z=  "<<z<<" theta ="<<theta<<std::endl;

        pose.orientation= quat;
        pose.position.x = x;
        pose.position.y = y;
        pose.position.z = z;
        des_model_state.pose = pose;
        set_model_state_srv.request.model_state = des_model_state;
        client.call(set_model_state_srv);
        ros::spinOnce();
        ros::Duration(sim_time_step).sleep();
    }

    return 0;
}

