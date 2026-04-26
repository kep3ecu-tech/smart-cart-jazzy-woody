import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO
import time

class UltrasonicNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.pub = self.create_publisher(Range, '/ultrasonic_range', 10)
        self.TRIG, self.ECHO = 5, 6 # 물리 29, 31번
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT); GPIO.setup(self.ECHO, GPIO.IN)
        self.create_timer(0.1, self.measure)
        self.get_logger().info('🦇 초음파 센서 구동 중...')

    def measure(self):
        GPIO.output(self.TRIG, True); time.sleep(0.00001); GPIO.output(self.TRIG, False)
        start, stop = time.time(), time.time()
        while GPIO.input(self.ECHO) == 0: start = time.time()
        while GPIO.input(self.ECHO) == 1: stop = time.time()
        dist = ((stop - start) * 34300) / 2
        msg = Range(); msg.range = float(dist)
        self.pub.publish(msg)
        self.get_logger().info(f'거리: {dist:.1f} cm')

def main(args=None):
    rclpy.init(args=args); node = UltrasonicNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: GPIO.cleanup(); node.destroy_node(); rclpy.shutdown()