import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from gpiozero import DistanceSensor

class UltrasonicNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_node')
        # TRIG: GPIO 5 (물리 29), ECHO: GPIO 6 (물리 31)
        # gpiozero는 BCM 번호를 기본으로 사용합니다.
        self.sensor = DistanceSensor(echo=6, trigger=5, max_distance=2.0)
        self.publisher_ = self.create_publisher(Float32, '/ultrasonic_distance', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz
        self.get_logger().info('📏 초음파 센서 노드 가동 시작!')

    def timer_callback(self):
        msg = Float32()
        msg.data = self.sensor.distance * 100.0 # m -> cm 변환
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
