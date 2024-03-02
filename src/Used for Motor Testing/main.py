"""! @file main.py
Defines Servo class.
If this is the main.py file on the Nucleo,
it will run a motor response test.
@author Nathaniel Davis
@author Sebastian Bessoudo
@date 02-13-2024
"""

import micropython
import pyb
import time
import cqueue
from motor_driver_updated import MotorDriver
from encoder_reader_updated import Encoder

# Allow interrupts to display errors
micropython.alloc_emergency_exception_buf(100)

class Servo:
    """!
    This class uses motor control and encoder reading for the user to input a Kp value
    and its setpoint
    """
    def __init__(self, motor, encoder):
        """!
        Initializes the servo. Requires the already existing motor driver and encoder.
        @param motor Currently exisiting motor driver class object
        @param encoder Currently exisiting encoder class object
        """
        self.motor = motor
        self.encoder = encoder
        self.Kp = 0.1
        self.error = 0
        
    def run(self, level):
        """!
        Sets the duty cycle for the motor to run based on
        @param level The level (from 0 - 100) for the motor to run at
        """
        self.motor.set_duty_cycle(level)
        
    def set_setpoint(self, setpoint):
        """!
        Directs the motor to go to a certain position
        @param setpoint Position for the motor to travel to 
        """
        self.encoder.read()
        self.error = setpoint - self.encoder.pos
        self.PWM = self.Kp*self.error
        self.motor.set_duty_cycle(self.PWM)
        
    def set_Kp(self, Kp):
        """!
        Sets the Kp of the motor
        @param Kp The Kp to set for the motor
        """
        self.Kp = Kp
        
    
if __name__ == "__main__":  
    # run motor response test
    # set up MotorDriver class object
    moe = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, 1,  pyb.Pin.board.PB5, 2, 3)
    # set up Encoder class object
    enc = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8, 1, 2)
    # set up Servo class object using the MotorDriver and Encoder objects specified
    serv = Servo(moe, enc)
    
    # run test ad infinitum
    while True:
        # requests ms between control feedback
        ms = int(input("ms between control feedback: "))
        # number of data points to run test for (each data point is 10 ms apart)
        num = int(5000/ms)
        # Kp
        serv.set_Kp(0.05)
        # setpoint
        input_setp = 100000
        serv.set_setpoint(input_setp)
        
        # create empty lists for times and positions
        positions = []
        times = [float(ms)*x for x in range(num)]
        
        # repeatedly saves position value every 10 ms 
        for n in range(num):
            serv.set_setpoint(input_setp)
            time.sleep_ms(ms)
            positions.append(serv.encoder.read())
            print(f"{times[n]}, {serv.encoder.read()}")
        # stop motor at end of test
        serv.run(0)
        enc.zero()
        # print End to signal end of data transmission
        print('End')
            
    