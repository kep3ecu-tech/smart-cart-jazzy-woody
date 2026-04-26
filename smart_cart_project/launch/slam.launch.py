import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. LiDAR 드라이버 설정 (포트 번호 /dev/ttyUSB0 확인 필수!)
    lidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB1',  # 'ls /dev/ttyUSB*'로 확인한 번호 넣기
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'Sensitivity'
        }],
        output='screen'
    )

    # 2. SLAM Toolbox 설정 (실시간 매핑 및 시간 지연 최적화)
    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'odom_frame': 'base_link',
            'base_frame': 'base_link',
            'map_frame': 'map',
            'scan_topic': '/scan',
            'mode': 'mapping',
            # 아주 미세한 움직임도 지도에 반영하도록 설정
            'minimum_travel_distance': 0.01,
            'minimum_travel_heading': 0.01,
            'map_update_interval': 0.5,
            # TF 시간 오차 에러 방지를 위해 1.0초로 연장
            'transform_timeout': 1.0, 
            'resolution': 0.05,
            'max_laser_range': 12.0,
            'use_map_saver': True
        }]
    )

    # 3. Static TF (base_link와 laser 연결)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0', 
            '--yaw', '0', '--pitch', '0', '--roll', '0', 
            '--frame-id', 'base_link', 
            '--child-frame-id', 'laser'
        ]
    )

    return LaunchDescription([
        lidar_node,
        static_tf,
        slam_node
    ])
