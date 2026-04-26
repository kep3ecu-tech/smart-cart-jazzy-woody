import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import mediapipe as mp

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.pub = self.create_publisher(String, '/cart_command', 10)
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.create_timer(0.1, self.detect)
        self.get_logger().info('✋ 제스처 인식 시작...')

    def detect(self):
        ret, frame = self.cap.read()
        if not ret: return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.mp_hands.process(rgb)
        if res.multi_hand_landmarks:
            for lm in res.multi_hand_landmarks:
                if lm.landmark[8].y < lm.landmark[6].y: # 검지 펴짐
                    msg = String(); msg.data = "RESUME"; self.pub.publish(msg)
                    self.get_logger().info('✋ RESUME 감지!')

def main(args=None):
    rclpy.init(args=args); node = VisionNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.cap.release(); node.destroy_node(); rclpy.shutdown()