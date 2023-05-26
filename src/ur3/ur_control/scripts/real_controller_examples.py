#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from ur_control import transformations
from ur_control.arm import Arm
import argparse
import rospy
import timeit
import numpy as np
import tf
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=np.inf)
from ur_msgs.srv import *
import sys


class DigitalOutputManager:
    def __init__(self, initial_states):
        self.pin_states = initial_states     #0,1,0: enable, direccion, steps
        self.pins = [0, 1, 2]                                                   
        self.toggle_count = 0 
        self.rate = rospy.Rate(5000)

        for i in range(2):
            rospy.wait_for_service('/ur_hardware_interface/set_io')                                        
        try:
            set_io = rospy.ServiceProxy('/ur_hardware_interface/set_io', SetIO)                        
            resp = set_io(fun=1, pin=i, state=self.pin_states[i])
            # print(resp.success)                                                
        except rospy.ServiceException as e: 
            print("primero")                                    
            print("Service call failed: %s" % e)      

        # self.timer = rospy.Timer(rospy.Duration(1), self.timer_callback) 

        rospy.wait_for_service('/ur_hardware_interface/set_io')                                        
        try:
            set_io = rospy.ServiceProxy('/ur_hardware_interface/set_io', SetIO)                        
            if (self.toggle_count == 0):
                for i in range(800):
                    resp = set_io(fun=1, pin=2, state=self.pin_states[2])
                    # rospy.sleep(0.0005)
                    self.rate.sleep()
                    if self.pin_states[2] == 1.0:
                        self.pin_states[2] = 0.0
                    elif self.pin_states[2] == 0.0:
                        self.pin_states[2] = 1.0 
                    # print("i:")
                    # print(str(i))
                    # print("state:")
                    # print(self.pin_states[2])
                # return resp.success   
                self.toggle_count=1                                             
        except rospy.ServiceException as e: 
            # print("primero")                                    
            print("Service call failed: %s" % e)      


    def toggle_digital_output(self):

        if self.pin_states[2] == 1.0:
            self.pin_states[2] = 0.0
        elif self.pin_states[2] == 0.0:
            self.pin_states[2] = 1.0    

        # rospy.wait_for_service('/ur_hardware_interface/set_io')                                        
        try:
            set_io = rospy.ServiceProxy('/ur_hardware_interface/set_io', SetIO)                        
            resp = set_io(fun=1, pin=2, state=self.pin_states[2])
            # return resp.success                                                
        except rospy.ServiceException as e:  
            print("segundo") 
            print(str(self.toggle_count))                                    
            print("Service call failed: %s" % e)

    def timer_callback(self, event):
        print(str(self.toggle_count))                                    

        if self.toggle_count >= 33:                                             # Rotate x degrees: degrees x 0.5555555
            self.timer.shutdown()
            return

        # Cambia el estado de los pines
        # self.toggle_digital_output(self.pins[2])                                # Which pin to toggle
        self.toggle_digital_output()  

        # Incrementa la cuenta de cambios de estado
        self.toggle_count += 1                                                  # Counter

    def restart_toggling(self):
        # Reinicia el contador de cambios de estado y el Timer
        self.toggle_count = 0                                                   # Restart process
        self.initial_states[1] = not self.initial_states[1]                     # Change direction of the gripper
        self.timer = rospy.Timer(rospy.Duration(0.001), self.timer_callback)    # Excecute toggle function


def move_joints(wait=True):
    q = [-0.0916, -1.971, 2.187, -3.358, -1.626, 0.176]
    arm.set_joint_positions(position=q, wait=wait, t=0.5)
    rospy.sleep(2.0)
    print("MOVIENDO gripper")
    digital_output_manager = DigitalOutputManager([0.0, 0.0, 0.0])       
    print("TERMINÓ de mover gripper")


def follow_trajectory():
    traj = [
        [2.4463, -1.8762, -1.6757, 0.3268, 2.2378, 3.1960],
        [2.5501, -1.9786, -1.5293, 0.2887, 2.1344, 3.2062],
        [2.5501, -1.9262, -1.3617, 0.0687, 2.1344, 3.2062],
        [2.4463, -1.8162, -1.5093, 0.1004, 2.2378, 3.1960],
        [2.3168, -1.7349, -1.6096, 0.1090, 2.3669, 3.1805],
        [2.3168, -1.7997, -1.7772, 0.3415, 2.3669, 3.1805],
        [2.3168, -1.9113, -1.8998, 0.5756, 2.3669, 3.1805],
        [2.4463, -1.9799, -1.7954, 0.5502, 2.2378, 3.1960],
        [2.5501, -2.0719, -1.6474, 0.5000, 2.1344, 3.2062],
    ]
    for t in traj:
        arm.set_joint_positions(position=t, wait=True, t=1.0)


def move_endeffector(wait=True):
    cpose = arm.end_effector()
    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    d_cam_corr_x = -0.0678
    d_cam_corr_y = -0.0254
    corr_gripper_y = 0.145
    corr_gripper_x = -0.09
    corr_gripper_z = 0.07


    while not rospy.is_shutdown():
        # for i in range(10):
        try:
            # cpose = [transAruco[0]+d_cam_corr_x+corr_gripper_x, transAruco[1]+d_cam_corr_y+corr_gripper_y, transAruco[2]+corr_gripper_z, rotEE[0], rotEE[1], rotEE[2], rotEE[3]]
            (transAruco,rotAruco) = listener.lookupTransform('/base_link', '/aruco_marker_frame', rospy.Time(0))
            (transEE,rotEE) = listener.lookupTransform('/base_link', '/wrist_3_link', rospy.Time(0))
            
            Zpose = arm.end_effector()
            # print("current pose")
            # print(Zpose)
            # print("transEE")
            # print(transEE)
            # print("rotEE")
            # print(rotEE)

            # Zpose = [Zpose[0], Zpose[1], transAruco[2]+corr_gripper_z, Zpose[3], Zpose[4], Zpose[5], Zpose[6]]
            # print("Va a moverse en Z")
            # arm.set_target_pose(pose=Zpose, wait=True, t=1.0)
            # Ypose = arm.end_effector()
            # Ypose = [Ypose[0], transAruco[1]+d_cam_corr_y+corr_gripper_y, Ypose[2],  Ypose[3], Ypose[4], Ypose[5], Ypose[6]]
            # print("Va a moverse en Y")
            # arm.set_target_pose(pose=Ypose, wait=True, t=1.0)
            # Xpose = arm.end_effector()
            # Xpose = [transAruco[0]+d_cam_corr_x+corr_gripper_x, Xpose[1], Xpose[2],  Xpose[3], Xpose[4], Xpose[5], Xpose[6]]
            # print("Va a moverse en X")
            # arm.set_target_pose(pose=Xpose, wait=True, t=1.0)

            Zpose = [transAruco[0]+d_cam_corr_x+corr_gripper_x, transAruco[1]+d_cam_corr_y+corr_gripper_y, transAruco[2]+corr_gripper_z, Zpose[3], Zpose[4], Zpose[5], Zpose[6]]
            print("Va a moverse")
            arm.set_target_pose(pose=Zpose, wait=True, t=1.0)

            print("Terminó de moverse")
            print("MOVIENDO gripper")
            rospy.sleep(2.0)
            digital_output_manager = DigitalOutputManager([0.0, 1.0, 0.0])       
            print("TERMINÓ de mover gripper")
            rospy.sleep(2.0)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("NO se va a mover. NO encontró tf")
            continue
        rate.sleep()

    # cpose_rot = 0.51339687 -0.50204173  0.49461101 -0.48963016
    # cpose = [0.31039883, -0.26478611, 0.32612011, 0.54907157, 0.48249772, 0.50090525, 0.4634763]
    # arm.set_target_pose(pose=cpose, wait=True, t=1.0)
    # 0.38132267  0.33066657  0.18569623 -0.45880805  0.53243781 -0.49661238  0.5092949
    # rospy.wait_for_service('/ur_hardware_interface/set_io')  
    # try:                                     
    #     set_io = rospy.ServiceProxy('/ur_hardware_interface/set_io', SetIO)
    #     resp = set_io(fun=1, pin=16, state=1)
    #     return resp.success
    # except rospy.ServiceException as e:                                     
    #     print("Service call failed: %s" % e)


    # ## PRUEBAS GRIPPER
    # print("ABRIENDO gripper")
    # digital_output_manager = DigitalOutputManager([0.0, 0.0, 0.0])       
    # print("TERMINÓ de mover gripper")

def move_gripper():
    # very different than simulation
    from robotiq_urcap_control.msg import Robotiq2FGripper_robot_input as inputMsg
    from robotiq_urcap_control.msg import Robotiq2FGripper_robot_output as outputMsg
    from robotiq_urcap_control.robotiq_urcap_control import RobotiqGripper
    print("Connecting to gripper")
    robot_ip = rospy.get_param("/ur_hardware_interface/robot_ip")
    gripper = RobotiqGripper(robot_ip=robot_ip)
    # The Gripper status is published on the topic named 'Robotiq2FGripperRobotInput'
    pub = rospy.Publisher('Robotiq2FGripperRobotInput', inputMsg, queue_size=1)

    # The Gripper command is received from the topic named 'Robotiq2FGripperRobotOutput'
    rospy.Subscriber('Robotiq2FGripperRobotOutput', outputMsg, gripper.send_command)

    gripper.connect()
    gripper.activate()
    # gripper.move_and_wait_for_pos(position=100, speed=10, force=10)
    # gripper.move_and_wait_for_pos(position=0, speed=10, force=10)
    # gripper.move_and_wait_for_pos(position=255, speed=10, force=10)
    gripper.disconnect()


def main():
    """ Main function to be run. """
    parser = argparse.ArgumentParser(description='Test force control')
    parser.add_argument('-m', '--move', action='store_true',
                        help='move to joint configuration')
    parser.add_argument('-t', '--move_traj', action='store_true',
                        help='move following a trajectory of joint configurations')
    parser.add_argument('-e', '--move_ee', action='store_true',
                        help='move to a desired end-effector position')
    parser.add_argument('-g', '--gripper', action='store_true',
                        help='Move gripper')
    parser.add_argument('-r', '--rotation', action='store_true',
                        help='Rotation slerp')
    parser.add_argument('--relative', action='store_true', help='relative to end-effector')
    parser.add_argument('--rotation_pd', action='store_true', help='relative to end-effector')

    args = parser.parse_args()

    rospy.init_node('ur3e_script_control')

    global arm
    arm = Arm(
        ft_sensor=True,  # get Force/Torque data or not
        gripper=False,  # Enable gripper
    )

    real_start_time = timeit.default_timer()
    ros_start_time = rospy.get_time()
    if args.move:
        move_joints()
    if args.move_traj:
        follow_trajectory()
    if args.move_ee:
        move_endeffector()
    if args.gripper:
        move_gripper()

    print("real time", round(timeit.default_timer() - real_start_time, 3))
    print("ros time", round(rospy.get_time() - ros_start_time, 3))


if __name__ == "__main__":
    main()
