import RPi.GPIO as GPIO

class RelayController(object):
  """docstring for RelayController"""
  def __init__(self):
    relay_mapping_array = [ 40, 38, 36, 32, 31, 26, 24, 22]
    relay_state = [False]*8
    GPIO.setmode(GPIO.BOARD) # physical pin count numbering
    for relay in relay_mapping:
      GPIO.setup(relay, GPIO.OUT, initial=GPIO.HIGH) # default state to high for non engaged relay

  def off(self, relay):
    self.relay_state[relay] = False
    GPIO.output(self.relay_mapping_array[relay], GPIO.HIGH)

  def on(self, relay):
    self.relay_state[relay] = True
    GPIO.output(self.relay_mapping_array[relay], GPIO.LOW)

  def toggle(self, relay):
    GPIO.output(self.relay_mapping_array[relay], not self.relay_state[relay])
    self.relay_state[relay] = not self.relay_state[relay]

  def status(self, relay):
    return self.relay_state[relay]