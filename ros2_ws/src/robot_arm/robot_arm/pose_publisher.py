#!/usr/bin/env python3
"""
End-Effector Pose Publisher Node
---------------------------------
Looks up the current transform from 'world' to 'end_effector' using TF2
and republishes it as a geometry_msgs/PoseStamped on /end_effector_pose.

Your task (TODO 2):
    Implement _publish_pose() so that:
    - It looks up the transform 'world' → 'end_effector' from the TF buffer
    - Converts the TransformStamped into a PoseStamped message
    - Publishes it on self._publisher at 10 Hz


Error handling requirements:
    - If the transform is not yet available, log a warning and return
      (do NOT crash or raise)
    - Handle at minimum: LookupException, ExtrapolationException,
      ConnectivityException
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.get_logger().info('PosePublisher started.')

        self.publisher = self.create_publisher(PoseStamped, '/end_effector_pose', 10)
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.timer = self.create_timer(0.1, self._publish_pose)

    def _publish_pose(self):
        try:
            t = self.tf_buffer.lookup_transform(
                'world',
                'end_effector',
                rclpy.time.Time())
        except (LookupException, ConnectivityException, ExtrapolationException) as ex:
            self.get_logger().warn(f'Could not transform "world" to "end_effector": {ex}')
            return
            
        pose_msg = PoseStamped()
        pose_msg.header = t.header
        pose_msg.pose.position.x = t.transform.translation.x
        pose_msg.pose.position.y = t.transform.translation.y
        pose_msg.pose.position.z = t.transform.translation.z
        pose_msg.pose.orientation = t.transform.rotation
        
        self.publisher.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)
    node = PosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
