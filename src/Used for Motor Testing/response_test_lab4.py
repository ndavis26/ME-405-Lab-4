"""! @file main.py
Takes account of time as it measures the number of ticks to measure its distance into a list
This becomes graphed onto a a TK window with a Matplotlib plot
@author Nathaniel Davis
@author Sebastian Bessoudo
@author reference:
@date 2024-2-21
"""

import math
import time
import tkinter
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Resets the target arduino and formats the time and distance the motor has travelled
    from the arduino into a list to be plotted.
    Calls 'End' when enough data has been gathered
    @param plot_axes The function that plots the given data onto the generated axes
    @param plot_canvas The function that displays the plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    
    """
    timeExp = []
    posExp = []
    with serial.Serial('COM7') as ser:  
        ser.write(b'\x03')
        ser.write(b'\x04')
        ser.write(b'50\r\n')
        while True:
            data = ser.readline().decode('utf-8')
            if ',' in data:
                squib = data.strip().split(',')
                try:
                    timeExp.append(float(squib[0]))
                    posExp.append(int(squib[1]))
                except ValueError:
                    continue
            elif 'End' in data:
                break
            else:
                continue
    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(timeExp, posExp)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Position (Ticks)",
               title="Experimental Response, Feedback Time = 50 ms")


