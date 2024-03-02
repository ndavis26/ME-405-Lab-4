"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author Nathaniel Davis an Sebastian Bessoudo
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
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
    serv1 = Servo(moe, enc)
    
    # number of data points to run test for (each data point is 10 ms apart)
    num = 500
    
    # run test ad infinitum
    while True:
        # requests Kp
        input_kp = float(input("enter Kp:"))
        serv1.set_Kp(input_kp)
        # requests setpoint
        input_setp = int(input("enter setpoint:"))
        serv1.set_setpoint(input_setp)
        
        # create empty lists for times and positions
        positions = []
        times = [10*x for x in range(num)]
        
        # repeatedly saves position value every 10 ms 
        for n in range(num):
            serv1.set_setpoint(input_setp)
            time.sleep_ms(10)
            positions.append(serv1.encoder.read())
            print(f"{times[n]}, {serv1.encoder.read()}")
        # stop motor at end of test
        serv1.run(0)
        # print End to signal end of data transmission
        print('End')
        yield 


#def task2_fun():
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    #moe2 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, 1,  pyb.Pin.board.PB5, 2, 3)
    #enc2 = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4, 1, 2)
    #cloop2 = Servo(moe2, enc2)
    # Get references to the share and queue which have been passed to this task
    #the_share, the_queue = shares

    #while True:
        # Show everything currently in the queue and the value in the share
        #print(f"Share: {the_share.get ()}, Queue: ", end='')
        #while q0.any():
            #print(f"{the_queue.get ()} ", end='')
        #print('')

        #yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Motor 1", priority=1, period=20,
                        profile=True, trace=False)
    #task2 = cotask.Task(task2_fun, name="Motor 2", priority=2, period=1500,
                        #profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    #cotask.task_list.append(task1_motor2)

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