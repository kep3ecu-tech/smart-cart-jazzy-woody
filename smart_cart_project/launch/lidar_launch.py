from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. RPLidar A1M8 드라이버 (rplidar_ros 패키지의 rplidar_node 실행)
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar_node',
            parameters=[{
                'channel_type': 'serial',
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,
                'frame_id': 'laser_frame',
                'inverted': False,
                'angle_compensate': True,
            }],
            output='screen'
        ),

        # 2. IMU 노드
        Node(
            package='smart_cart_project',
            executable='imu_node',
            name='imu_node',
            output='screen',
        ),

        # 3. 초음파 센서 노드
        Node(
            package='smart_cart_project',
            executable='ultrasonic_node',
            name='ultrasonic_node',
            output='screen',
        ),

        # 4. 제어 타워 (final_cart)
        Node(
            package='smart_cart_project',
            executable='final_cart',
            name='final_cart',
            output='screen',
        )
    ])
