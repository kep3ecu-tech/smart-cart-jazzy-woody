from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # GPIO 쓰는 애들 (sudo로 launch 실행하면 같이 살아남)
        Node(package='smart_cart_project', executable='motor_node', output='screen'),
        Node(package='smart_cart_project', executable='sensor_node', output='screen'),

        # 일반 노드들
        Node(package='smart_cart_project', executable='imu_node', output='screen'),
        Node(package='smart_cart_project', executable='planner', output='screen'),

        # ✅ vision_node만 venv python으로 실행 (mediapipe가 venv에 있으니까)
        ExecuteProcess(
            cmd=[
                '/home/hyeon/venv_smartcart/bin/python',
                '/home/hyeon/ros2_ws/install/smart_cart_project/lib/smart_cart_project/vision_node'
            ],
            output='screen'
        ),
    ])
