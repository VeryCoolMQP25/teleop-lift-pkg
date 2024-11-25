import rclpy
import rclpy.executors
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from rclpy.publisher import Publisher
from rclpy.logging import LoggingSeverity

LIFT_ENABLE_BTN = 5 # right bumper
LIFT_AXIS = 3 # right stick Y

power: float = 0.0

class JoyListener(Node):
    def __init__(self):
        self.get_logger().set_level(LoggingSeverity.INFO)
        super().__init__('joy_listener')
        # Subscriber to the /joy topic
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10  # Queue size
        )
        self.get_logger().info('Started listening to /joy messages')
    def joy_callback(self, msg):
        global power
        # Print out the button and axis values
        buttons = msg.buttons  # List of button states (0 or 1)
        axes = msg.axes  # List of axis states (e.g., for analog sticks)
        command = 0.0
        if (msg.buttons[LIFT_ENABLE_BTN]):
            command = msg.axes[LIFT_AXIS]
        power = command
        self.get_logger().info(f'States: {buttons[LIFT_ENABLE_BTN]}, {axes[LIFT_AXIS]}')

class LiftPublisher(Node):
    def __init__(self):
        super().__init__('lift_raw_publisher')
        self.topic = "/lift_raw"
        self.period = 0.1 #s
        self.msg = Float32()
        self.publisher: Publisher = self.create_publisher(Float32, self.topic, 1)
        self.timer = self.create_timer(self.period, self.callback)
        self.get_logger().info('started publishing to {} every {}s.'.format(self.topic, self.period))

    def callback(self):
        self.msg.data = float(power)
        self.publisher.publish(self.msg)
        if abs(power) < 0.001:
            self.get_logger().info('Lift stopped.')
        else:
            self.get_logger().info('set lift to {}% power.'.format(self.msg.data*100))

def main(args=None):
    print("rcl init")
    rclpy.init(args=args)
    executor = rclpy.executors.MultiThreadedExecutor()
    joy_listener = JoyListener()
    lift_publish = LiftPublisher()
    executor.add_node(joy_listener)
    executor.add_node(lift_publish)
    print("spinning")
    executor.spin()
    joy_listener.destroy_node()
    lift_publish.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
