"""! @file main.py
Runs two motors simultaneously.
@author Nathaniel Davis an Sebastian Bessoudo
@date   3-1-2024
"""

import gc
import pyb
import cotask
import task_share
import time
from motor_driver_updated import MotorDriver
from encoder_reader_updated import Encoder
from servo_updated import Servo


def task1_fun():
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    
    # run motor response test
    # set up MotorDriver class object
    moe1 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, 1,  pyb.Pin.board.PB5, 2, 3)
    # set up Encoder class object
    enc1 = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8, 1, 2)
    # set up Servo class object using the MotorDriver and Encoder objects specified
    serv1 = Servo(moe1, enc1)
    
    # number of data points to run test for (each data point is 10 ms apart)
    
    # run ad infinitum
    while True:
        # Kp
        input_kp = 0.05
        serv1.set_Kp(input_kp)
        # setpoint
        input_setp = 100000
        serv1.set_setpoint(input_setp)
        
        # repeatedly saves position value every 10 ms 
        while True:
            serv1.set_setpoint(input_setp)
            yield 


def task2_fun():
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # run motor response test
    # set up MotorDriver class object
    moe2 = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, 1,  pyb.Pin.board.PA1, 2, 5)
    # set up Encoder class object
    enc2 = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4, 1, 2)
    # set up Servo class object using the MotorDriver and Encoder objects specified
    serv2 = Servo(moe2, enc2)
    
    # number of data points to run test for (each data point is 10 ms apart)
    
    # run test ad infinitum
    while True:
        # Kp
        input_kp = 0.05
        serv2.set_Kp(input_kp)
        # setpoint
        input_setp = -150000
        serv2.set_setpoint(input_setp)
        
        # repeatedly saves position value every 10 ms 
        while True:
            serv2.set_setpoint(input_setp)
            yield 

if __name__ == "__main__":
    print("Press Ctrl-C to stop and show diagnostics.")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Motor 1", priority=1, period=30, profile=True, trace=False)
    task2 = cotask.Task(task2_fun, name="Motor 2", priority=2, period=30, profile=True, trace=False)
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
ç