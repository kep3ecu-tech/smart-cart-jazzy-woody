import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, tty, termios, select, time

class Teleop(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel_safe', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.target_twist = Twist()
        self.last_key_time = time.time()
        print("--- 초정밀 매핑 조종 (수정 버전) ---")
        print("W: 전진, S: 후진, A: 좌회전, D: 우회전, Space: 정지")
        print("설정 속도: 0.1m/s (강력한 안정화 로직 적용)")

    def timer_callback(self):
        if time.time() - self.last_key_time > 0.5:
             self.target_twist = Twist()
        self.pub.publish(self.target_twist)

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.01)
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    ch = sys.stdin.read(1)
                    self.last_key_time = time.time()
                    if ch == 'w': self.target_twist.linear.x = 0.1; self.target_twist.angular.z = 0.0
                    elif ch == 's': self.target_twist.linear.x = -0.1; self.target_twist.angular.z = 0.0
                    elif ch == 'a': self.target_twist.angular.z = 0.1; self.target_twist.linear.x = 0.0
                    elif ch == 'd': self.target_twist.angular.z = -0.1; self.target_twist.linear.x = 0.0
                    elif ch == ' ': self.target_twist.linear.x = 0.0; self.target_twist.angular.z = 0.0
                    elif ch == '\x03': break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    rclpy.init()
    node = Teleop()
    try:
        node.run()
    except:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
