import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask, request # pip install flask 필요

app = Flask(__name__)
node_instance = None

@app.route('/select', methods=['POST'])
def select_menu():
    menu = request.form.get('menu')
    if node_instance and menu:
        msg = String(); msg.data = menu
        node_instance.publisher_.publish(msg)
        return "OK", 200
    return "Fail", 400

class AppNode(Node):
    def __init__(self):
        super().__init__('app_node')
        global node_instance
        node_instance = self
        self.publisher_ = self.create_publisher(String, '/selected_menu', 10)
        self.get_logger().info('📱 핸드폰 신호 대기 서버 시작...')

def main(args=None):
    rclpy.init(args=args)
    node = AppNode()
    # Flask 서버를 별도 스레드에서 돌리거나 간단히 여기서 실행
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    rclpy.spin(node)
    node.destroy_node(); rclpy.shutdown()