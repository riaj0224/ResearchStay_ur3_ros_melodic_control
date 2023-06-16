# UR3 Berry Harvesting Project

This repository contains the code and resources for the UR3 Berry Harvesting Project, which aims to develop an automated berry harvesting system using the UR3 robot arm, Intel D435F camera, and a custom-made gripper. The project focuses on integrating different technologies to enable the robot arm to detect and harvest berries with high precision.

## :wrench: Technologies Used

The project leverages the following technologies:

- UR3 Robot Arm: A collaborative robot arm used for berry harvesting tasks.
- Intel D435F Camera: A depth camera used for vision-based object detection and pose estimation.
- ROS Noetic: The Robot Operating System used for communication and control of the UR3 arm.
- Gazebo: A robotics simulation environment used for testing and validation.
- RViz: A 3D visualization tool for ROS that allows you to visualize the robot arm, camera, and detected objects.
- RQT: A framework for developing ROS graphical user interfaces (GUIs) that enables you to monitor and control the robot arm.

## :file_folder: Project Structure

The project has the following file structure:

```
├── workspace
│ ├── src
│ │ ├── universal_robots_ros_driver
│ │ │ ├── ur_robot_driver
│ │ │ │ ├── launch
│ │ │ │ │ └── example_rviz.launch
│ │ │ │ └── ur3_bringup.launch
│ │ ├── ur3
│ │ │ └── ur_control
│ │ │ └── scripts
│ │ │ └── real_controller_examples.py
│ └── CMakeLists.txt
├── Dockerfile
└── README.md
```

- `workspace`: The root directory of the project workspace.
- `src/universal_robots_ros_driver/ur_robot_driver/launch/example_rviz.launch`: Launch file for visualizing the UR3 robot arm in RViz.
- `src/universal_robots_ros_driver/ur_robot_driver/launch/ur3_bringup.launch`: Launch file for bringing up the UR3 robot arm.
- `src/ur3/ur_control/scripts/real_controller_examples.py`: Script for controlling the vision system, calculating pose, and performing other tasks.

## :rocket: Getting Started

To run the UR3 Berry Harvesting project using Docker, follow these steps:

1. Install Docker on your machine.
2. Clone this repository and navigate to the project directory.
3. Build the Docker image using the provided Dockerfile
4. Run a Docker container from the built image, mapping the necessary ports and volumes
Replace `/path/to/workspace` with the absolute path to your local workspace directory.
5. Launch the UR3 robot arm, RViz, and RQT using the appropriate launch files:
```
roslaunch universal_robots_ros_driver ur3_bringup.launch robot_ip:=<UR3_IP_ADDRESS>
roslaunch universal_robots_ros_driver example_rviz.launch robot_ip:=<UR3_IP_ADDRESS>
rqt
```
Replace `<UR3_IP_ADDRESS>` with the IP address of your UR3 robot arm.
6. Run the `real_controller_examples.py` script to control the vision system and perform berry harvesting tasks.

## :raising_hand: Acknowledgements

This project acknowledges the valuable resources and guidance provided by the following repositories:

- [ROS-Industrial](https://github.com/ros-industrial)
- [Universal Robots](https://github.com/ros-industrial/universal_robot)
- [joint_trajectory_controller](https://github.com/ros-controls/ros_controllers/tree/noetic-devel/joint_trajectory_controller)

## :email: Contact

For any questions or inquiries related to this project, please feel free to reach out to jair2000.0224@hotmail.com.

## :page_facing_up: License

This project is licensed under the terms of the MIT License. You are free to use, modify, and distribute the code for educational or commercial purposes.


