#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class SimplePoseVerifier(Node):
    def __init__(self):
        super().__init__('simple_pose_verifier')
        self.subscription = self.create_subscription(
            PoseStamped,
            '/end_effector_pose',
            self.listener_callback,
            10
        )
        self.last_position = None
        self.get_logger().info('Listening for /end_effector_pose messages...')

    def listener_callback(self, msg):
        current_pos = msg.pose.position
        
        if self.last_position is None:
            self.last_position = current_pos
            return
            
        if abs(current_pos.x - self.last_position.x) > 0.001 or abs(current_pos.y - self.last_position.y) > 0.001:
            self.get_logger().info('Position changed! It is okay.')
        else:
            self.get_logger().info('Position remained identical.')
            
        self.last_position = current_pos

def main(args=None):
    rclpy.init(args=args)
    verifier = SimplePoseVerifier()
    try:
        rclpy.spin(verifier)
    except KeyboardInterrupt:
        pass
    finally:
        verifier.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()