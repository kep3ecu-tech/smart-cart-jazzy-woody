import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu, LaserScan

class FinalCart(Node):
    def __init__(self):
        super().__init__('final_cart')
        self.get_logger().info('🛒 스마트 카트 메인 시스템 가동!')
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_cb, 10)
        self.imu_sub = self.create_subscription(Imu, '/imu/data_raw', self.imu_cb, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)

    def cmd_cb(self, msg): pass
    def imu_cb(self, msg): pass
    def scan_cb(self, msg): pass

def main(args=None):
    rclpy.init(args=args)
    node = FinalCart()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
