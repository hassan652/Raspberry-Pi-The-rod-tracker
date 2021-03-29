import time
from motor_controller import MotorController

motor_controller = MotorController()

for x in range(5):
  if not motor_controller.is_working():
    motor_controller.start_motor()
    time.sleep(5)
