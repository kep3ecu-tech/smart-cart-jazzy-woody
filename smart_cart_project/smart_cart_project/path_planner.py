import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        
        # 구독자 설정
        self.menu_sub = self.create_subscription(String, '/selected_menu', self.menu_callback, 10)
        self.cmd_sub = self.create_subscription(String, '/cart_command', self.command_callback, 10)
        
        # 발행자 설정 (모터 제어)
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.is_paused = True
        self.current_goal = None
        
        self.get_logger().info('🗺️ 경로 플래너 대기 중... QR을 보여주세요.')

    def menu_callback(self, msg):
        if self.current_goal != msg.data: # 중복 로그 방지
            self.current_goal = msg.data
            self.get_logger().info(f'📍 목적지 설정 완료: {self.current_goal}. 손을 펴서 출발하세요!')

    def command_callback(self, msg):
        if msg.data == "RESUME":
            if self.current_goal is not None:
                if self.is_paused:
                    self.is_paused = False
                    self.get_logger().info(f'🚀 출발합니다! 목적지: {self.current_goal}')
                    self.start_moving()
            else:
                self.get_logger().warn('⚠️ 목적지가 없습니다. QR 코드를 먼저 보여주세요.')

    def start_moving(self):
        # 테스트용: 0.2 m/s로 전진
        # 주의: 별도의 정지 명령이 없으면 계속 갑니다! (테스트 시 바퀴 띄울 것)
        move_msg = Twist()
        move_msg.linear.x = 0.2
        self.vel_pub.publish(move_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PathPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()