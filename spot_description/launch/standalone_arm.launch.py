# Copyright (c) 2023-2024 Robotics and AI Institute LLC dba RAI Institute. All rights reserved.

import os

import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> launch.LaunchDescription:
    pkg_share = FindPackageShare(package="spot_description").find("spot_description")
    default_model_path = os.path.join(pkg_share, "urdf/standalone_arm.urdf.xacro")
    default_rviz2_path = os.path.join(pkg_share, "rviz/standalone_arm.rviz")
    return launch.LaunchDescription(
        [
            DeclareLaunchArgument(
                name="gui", default_value="True", description="Flag to enable joint_state_publisher_gui"
            ),
            DeclareLaunchArgument(
                name="model", default_value=default_model_path, description="Absolute path to robot urdf file"
            ),
            DeclareLaunchArgument(
                name="rviz",
                default_value="True",
                choices=["True", "true", "False", "false"],
                description="Flag to enable rviz gui",
            ),
            DeclareLaunchArgument(
                name="rvizconfig", default_value=default_rviz2_path, description="Absolute path to rviz config file"
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": Command(["xacro ", LaunchConfiguration("model")])}],
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                condition=launch.conditions.UnlessCondition(LaunchConfiguration("gui")),
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                condition=launch.conditions.IfCondition(LaunchConfiguration("gui")),
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                condition=launch.conditions.IfCondition(LaunchConfiguration("rviz")),
                arguments=["-d" + default_rviz2_path],
            ),
        ]
    )
