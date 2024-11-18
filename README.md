# Telop Lift Node

This ROS node piggybacks on the `teleop_twist_joy` package to provide direct motor power commands for the robot lift.

## Usage
This guide assumes that you have a working ROS2 Humble workspace, and are using the tourbot pico controller.
When installed, you can use the Y axis of the right stick to move the arm while the right bumper is held down.

### 1) Ensure that the teleop package is running:
```bash
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox'
```
### 2) Install this node to your ROS workspace
```bash
cd <ros ws>/src
git clone https://github.com/VeryCoolMQP25/teleop-lift-pkg
```
### 3) Build and Install the Package
```bash
colcon build
source setup/install.bash 
```
Note: change extension of install script for your shell of choice (`install.zsh`, etc...)
### 4) Run the Node
```bash
ros2 run teleop_lift teleop
```
