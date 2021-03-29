import RPi.GPIO as GPIO # For testing in Raspberry Pi
import time

class MotorController(object):

  def __init__(self):
    self.working = False

  def start_motor(self):
    self.PIN_STEP = 25 # do not change
    self.PIN_DIR = 8 # do not change
    self.working = True
    ClockRotation = 1
    CounterClockRotation = 0
    StepsPerRevolution = 48    #(360/7.5 degrees)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.PIN_DIR, GPIO.OUT)
    GPIO.setup(self.PIN_STEP, GPIO.OUT)
    GPIO.output(self.PIN_DIR, ClockRotation)
 
    step_count = StepsPerRevolution
    delay = .0208   #(1 second/48)
 
    for x in range(step_count):
      GPIO.output(self.PIN_STEP, GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(self.PIN_STEP, GPIO.LOW)
      time.sleep(delay)

    time.sleep(.5)

    GPIO.output(self.PIN_DIR, CounterClockRotation)
    for x in range(step_count):
      GPIO.output(self.PIN_STEP, GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(self.PIN_STEP, GPIO.LOW)
      time.sleep(delay)
    MODE = (14,15,18)
    GPIO.setup(MODE,GPIO.OUT)
    RESOLUTION = {'Full':(0,0,0),
    'Half': (1,0,0),
    '1/4': (0,1,0),
    '1/8': (1,1,0),
    '1/16': (0,0,1),
    '1/32': (1,0,1)}
    GPIO.output(MODE, RESOLUTION['1/32'])

    step_count = StepsPerRevolution * 32
    delay = .0208 / 32
    print('Motor started')
 
    GPIO.cleanup()
    
  def is_working(self):
    return self.working
