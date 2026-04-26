import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist

class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        self.goal_sub = self.create_subscription(PoseStamped, '/goal_pose', self.goal_callback, 10)
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = None
        self.get_logger().info('🚀 [직진 올인 모드] 활성화! 화살표를 찍으면 5초간 무조건 직진합니다.')

    def goal_callback(self, msg):
        self.get_logger().info('🏁 주행 신호 감지! 5초간 전진합니다.')
        if self.timer: self.timer.cancel()
        self.cnt = 0
        self.timer = self.create_timer(0.1, self.move_forward)

    def move_forward(self):
        move_msg = Twist()
        self.vel_pub.publish(move_msg)
        self.cnt += 1
        if self.cnt > 50: # 5초
            self.timer.cancel()
            self.vel_pub.publish(Twist()) # 정지
            self.get_logger().info('🏁 전진 테스트 종료.')

def main(args=None):
    rclpy.init(args=args)
    node = PathPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
