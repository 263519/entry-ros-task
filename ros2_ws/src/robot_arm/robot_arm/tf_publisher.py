#!/usr/bin/env python3
"""
TF Publisher Node
-----------------
Publishes the TF2 transform chain for a 2-DOF robot arm.

Chain layout:
    world
      └── base_link       (static, identity)
            └── link1     (dynamic, rotates around Z over time)
                  └── link2  (static offset: x=0.3m from link1)
                        └── end_effector  (static offset: x=0.2m from link2)

Your task (TODO 1):
    Implement the _broadcast() method so that:
    - 'world' → 'base_link'       is a static identity transform
    - 'base_link' → 'link1'       rotates around Z with amplitude 45° (0.785 rad)
                                  at a frequency of 0.5 Hz
    - 'link1' → 'link2'           is a static transform with x=0.3m offset
    - 'link2' → 'end_effector'    is a static transform with x=0.2m offset

    Use StaticTransformBroadcaster for transforms that never change.
    Use TransformBroadcaster for transforms that change over time.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster

class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')

        self.static_broadcaster = StaticTransformBroadcaster(self)
        self.dynamic_broadcaster = TransformBroadcaster(self)

        self.start_time  = self.get_clock().now()

        self.publish_static_transforms()

        self.timer = self.create_timer(1.0/50.0, self._broadcast)
        self.get_logger().info('TFPublisher is running...')
    
    def publish_static_transforms(self):
        tfs = []
        now = self.get_clock().now().to_msg()

        tf_world_base_link = TransformStamped()
        tf_world_base_link.header.stamp = now
        tf_world_base_link.header.frame_id = 'world'
        tf_world_base_link.child_frame_id = 'base_link'
        tf_world_base_link.transform.translation.x = 0.0
        tf_world_base_link.transform.translation.y = 0.0
        tf_world_base_link.transform.translation.z = 0.0
        tf_world_base_link.transform.rotation.x = 0.0
        tf_world_base_link.transform.rotation.y = 0.0
        tf_world_base_link.transform.rotation.z = 0.0
        tf_world_base_link.transform.rotation.w = 1.0
        tfs.append(tf_world_base_link)

        tf_l1_l2 = TransformStamped()
        tf_l1_l2.header.stamp = now
        tf_l1_l2.header.frame_id = 'link1'
        tf_l1_l2.child_frame_id = 'link2'
        tf_l1_l2.transform.translation.x = 0.3
        tf_l1_l2.transform.translation.y = 0.0
        tf_l1_l2.transform.translation.z = 0.0
        tf_l1_l2.transform.rotation.x = 0.0
        tf_l1_l2.transform.rotation.y = 0.0
        tf_l1_l2.transform.rotation.z = 0.0
        tf_l1_l2.transform.rotation.w = 1.0
        tfs.append(tf_l1_l2)


        # link 2 to end effector
        tf_l2_ee = TransformStamped()
        tf_l2_ee.header.stamp = now
        tf_l2_ee.header.frame_id = 'link2'
        tf_l2_ee.child_frame_id = 'end_effector'
        tf_l2_ee.transform.translation.x = 0.2
        tf_l2_ee.transform.translation.y = 0.0
        tf_l2_ee.transform.translation.z = 0.0
        tf_l2_ee.transform.rotation.x = 0.0
        tf_l2_ee.transform.rotation.y = 0.0
        tf_l2_ee.transform.rotation.z = 0.0
        tf_l2_ee.transform.rotation.w = 1.0
        tfs.append(tf_l2_ee)
        
        self.static_broadcaster.sendTransform(tfs)

    def _broadcast(self):
        now = self.get_clock().now()

        # convertion to seconds
        dt = (now - self.start_time).nanoseconds / 1e9

        amplitude = 0.785
        frequency = 0.5
        yaw = amplitude * math.sin(2 * math.pi * frequency * dt)
        q_z = math.sin(yaw / 2.0)
        q_w = math.cos(yaw / 2.0)

        tf_base_l1 = TransformStamped()
        tf_base_l1.header.stamp = now.to_msg()
        tf_base_l1.header.frame_id = 'base_link'
        tf_base_l1.child_frame_id = 'link1'
        tf_base_l1.transform.translation.x = 0.0
        tf_base_l1.transform.translation.y = 0.0
        tf_base_l1.transform.translation.z = 0.0
        tf_base_l1.transform.rotation.x = 0.0
        tf_base_l1.transform.rotation.y = 0.0
        tf_base_l1.transform.rotation.z = q_z
        tf_base_l1.transform.rotation.w = q_w

        self.dynamic_broadcaster.sendTransform(tf_base_l1)

        

def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
