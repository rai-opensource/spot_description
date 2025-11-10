<!-- Copyright (c) 2025 Robotics and AI Institute LLC dba RAI Institute. All rights reserved. -->

# Spot URDF Files

| name                      | purpose                                                                                |
|---------------------------|----------------------------------------------------------------------------------------|
| spot.urdf.xacro           | standard URDF for spot                                                                 |
| spot_arm_macro.urdf       | standard URDF macro for spot arm                                                       |
| spot_feet_macro.urdf      | standard URDF macro for spot feet                                                      |
| spot_simple.urdf.xacro    | same purpose as spot.urdf.xacro except details are simplified; suitable for simulation |
| standalone_arm.urdf.xacro | Adds a root link to spot_arm.urdf, making it a valid standalone model                  |
| accessories.urdf.xacro    | For adding payloads, LiDAR, and RealSense mounts. See example below.                   |
| empty.urdf                |                                                                                        |

## Adding accessories

Accessories can be toggled on and off by setting the appropriate environemnt variable, defined in [accessories.urdf.xacro](accessories.urdf.xacro). To include a RealSense mount on the lower jaw, for example, one could run:

```bash
export SPOT_JAW_REALSENSE_MOUNT=1
ros2 launch spot_driver spot_driver.launch.py <args>
```

### Including static transforms for RealSense cameras

There are several approaches to adding static transforms between Spot's joints and external sensors/actuators. One method is to add a `static_transform_publisher` to your launch file:

```python

jaw_to_realsense_tf = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_transform_publisher',
    output='screen',
    arguments=['0', '0', '0', '0', '0', '0', 'jaw_realsense_mount', 'camera_link'] 
)
```

The names for Spot's various frames can be found in their relevant xacro files. `jaw_realsense_mount`, for example, is defined in `accessories.urdf.xacro`. `camera_link` is defined by the `realsense2_description` package. General documentation for RealSense and ROS2 can be found [here](https://github.com/IntelRealSense/realsense-ros).