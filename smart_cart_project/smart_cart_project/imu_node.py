import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import smbus2
import numpy as np

class ImuNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.publisher_ = self.create_publisher(Imu, '/imu/data_raw', 10)
        self.bus = smbus2.SMBus(1)
        self.address = 0x68
        try:
            self.bus.write_byte_data(self.address, 0x6B, 0)
            self.get_logger().info('🧭 IMU 연결 성공!')
        except Exception as e:
            self.get_logger().error(f'🚨 IMU 연결 실패: {e}')
        self.timer = self.create_timer(0.05, self.publish_imu)

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        val = (high << 8) | low
        return val - 65536 if val > 32768 else val

    def publish_imu(self):
        try:
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'imu_link'
            acc_scale, gyro_scale = 16384.0, 131.0
            msg.linear_acceleration.x = (self.read_raw_data(0x3B) / acc_scale) * 9.80665
            msg.linear_acceleration.y = (self.read_raw_data(0x3D) / acc_scale) * 9.80665
            msg.linear_acceleration.z = (self.read_raw_data(0x3F) / acc_scale) * 9.80665
            msg.angular_velocity.x = np.radians(self.read_raw_data(0x43) / gyro_scale)
            msg.angular_velocity.y = np.radians(self.read_raw_data(0x45) / gyro_scale)
            msg.angular_velocity.z = np.radians(self.read_raw_data(0x47) / gyro_scale)
            msg.orientation.w = 1.0 
            self.publisher_.publish(msg)
        except: pass

def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
