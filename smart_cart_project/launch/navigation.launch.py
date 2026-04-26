import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    map_yaml = LaunchConfiguration("map", default="/home/an/my_smart_cart_map.yaml")
    base_frame = "base_link"

    # 1. 지도 서버 및 AMCL 노드
    map_server = Node(package="nav2_map_server", executable="map_server", name="map_server", parameters=[{"yaml_filename": map_yaml, "use_sim_time": False}])
    amcl = Node(package="nav2_amcl", executable="amcl", name="amcl", parameters=[{"use_sim_time": False, "base_frame_id": base_frame, "global_frame_id": "map", "odom_frame_id": "odom", "scan_topic": "/scan"}])
    lifecycle_mgr = Node(package="nav2_lifecycle_manager", executable="lifecycle_manager", name="lifecycle_manager_localization", parameters=[{"autostart": True, "node_names": ["map_server", "amcl"]}])
    
    # 2. 좌표 변환 (TF) - 라이다 및 IMU
    static_tf_laser = Node(package="tf2_ros", executable="static_transform_publisher", name="base_to_laser", arguments=["0", "0", "0.1", "3.14159", "0", "0", "base_link", "laser_frame"])
    static_tf_imu = Node(package="tf2_ros", executable="static_transform_publisher", name="base_to_imu", arguments=["0", "0", "0", "0", "0", "0", "base_link", "imu_link"])
    
    # 3. 로봇 핵심 노드 (가상 오도메트리, 네비게이터, 모터)
    fake_odom = Node(package="smart_cart_project", executable="/usr/bin/python3", name="fake_odom", arguments=["/home/an/ws/src/smart_cart_project/smart_cart_project/fake_odom.py"])
    simple_nav = Node(package="smart_cart_project", executable="simple_nav", name="simple_navigator", parameters=[{"global_frame": "map", "robot_frame": base_frame, "goal_tolerance_m": 0.20, "max_linear_speed": 0.15}])
    motor_node = Node(package="smart_cart_project", executable="motor_node", name="motor_node", parameters=[{"cmd_vel_topic": "/cmd_vel", "cmd_timeout_sec": 2.0}])

    # 4. [자동화] 켜지고 7초 뒤에 자동으로 "전체 지도에서 위치 찾기" 실행
    auto_global_localization = TimerAction(
        period=7.0,
        actions=[
            ExecuteProcess(
                cmd=["ros2", "service", "call", "/reinitialize_global_localization", "std_srvs/srv/Empty", "{}"],
                output="screen"
            )
        ]
    )

    return LaunchDescription([
        map_server,
        amcl,
        lifecycle_mgr,
        static_tf_laser,
        static_tf_imu,
        fake_odom,
        simple_nav,
        motor_node,
        auto_global_localization
    ])
