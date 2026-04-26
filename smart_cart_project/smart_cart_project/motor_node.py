import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from gpiozero import PWMOutputDevice, DigitalOutputDevice

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        
        # --- 핀 설정 (창현님 핀맵 기반 BCM 번호) ---
        # STBY (공통)
        self.stby = DigitalOutputDevice(25) # 물리 22
        self.stby.on()

        # [TB6612 #1 - 앞바퀴]
        self.front_left_pwm = PWMOutputDevice(18) # 물리 12
        self.front_left_in1 = DigitalOutputDevice(23) # 물리 16
        self.front_left_in2 = DigitalOutputDevice(24) # 물리 18
        
        self.front_right_pwm = PWMOutputDevice(13) # 물리 33
        self.front_right_in1 = DigitalOutputDevice(27) # 물리 13
        self.front_right_in2 = DigitalOutputDevice(22) # 물리 15

        # [TB6612 #2 - 뒷바퀴]
        self.back_left_pwm = PWMOutputDevice(12) # 물리 32
        self.back_left_in1 = DigitalOutputDevice(16) # 물리 36
        self.back_left_in2 = DigitalOutputDevice(20) # 물리 38

        self.back_right_pwm = PWMOutputDevice(19) # 물리 35
        self.back_right_in1 = DigitalOutputDevice(26) # 물리 37
        self.back_right_in2 = DigitalOutputDevice(21) # 물리 40

        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.get_logger().info('🚀 4WD TB6612FNG 시스템 준비 완료!')

    def cmd_callback(self, msg):
        # 차동 주행 계산 (Differential Drive)
        left_speed = msg.linear.x - msg.angular.z
        right_speed = msg.linear.x + msg.angular.z

        # 앞/뒤 왼쪽 모터 제어
        self.set_motor(self.front_left_pwm, self.front_left_in2, self.front_left_in1, left_speed)
        self.set_motor(self.back_left_pwm, self.back_left_in2, self.back_left_in1, left_speed)
        
        # 앞/뒤 오른쪽 모터 제어
        self.set_motor(self.front_right_pwm, self.front_right_in1, self.front_right_in2, right_speed)
        self.set_motor(self.back_right_pwm, self.back_right_in1, self.back_right_in2, right_speed)

    def set_motor(self, pwm_pin, in1, in2, speed):
        speed = max(min(speed, 1.0), -1.0) # 속도 제한
        if speed > 0: # 전진
            in1.on(); in2.off(); pwm_pin.value = speed
        elif speed < 0: # 후진
            in1.off(); in2.on(); pwm_pin.value = abs(speed)
        else: # 정지
            in1.off(); in2.off(); pwm_pin.value = 0

def main(args=None):
    rclpy.init(args=args)
    node = MotorNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
