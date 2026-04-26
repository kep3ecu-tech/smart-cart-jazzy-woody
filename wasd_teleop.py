import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = '''
SLAM WASD Teleop (Hardware-Matched Mode)
-----------------------------------------
      [ w ]
 [ a ] [ s ] [ d ]

w/s : Forward/Backward (Matched to your hardware)
a/d : Turn Left/Right

Current Speed: 0.5 (Stronger for motor friction)

Hold key to move, release to stop.
CTRL-C to quit
'''

class WASDTeleop(Node):
    def __init__(self):
        super().__init__('wasd_teleop')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel_safe', 10)
        self.speed = 0.5
        self.turn = 0.5

    def run(self):
        settings = termios.tcgetattr(sys.stdin)
        try:
            print(msg)
            while rclpy.ok():
                key = self.getKey(settings)
                twist = Twist()
                # Based on user report: A/D was forward/backward
                # So we map W/S to the angular.z channel and A/D to linear.x
                if key == 'w': twist.angular.z = self.speed
                elif key == 's': twist.angular.z = -self.speed
                elif key == 'a': twist.linear.x = self.speed
                elif key == 'd': twist.linear.x = -self.speed
                elif key == '\x03': break
                else: 
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
                
                self.publisher_.publish(twist)
        finally:
            twist = Twist()
            self.publisher_.publish(twist)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def getKey(self, settings):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

def main():
    rclpy.init()
    node = WASDTeleop()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
