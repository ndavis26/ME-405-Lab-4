# ME 405 Lab 4
The objective of this lab is to control two motors simultaneously using a task function. The first part is to identify the  slowest rate at which the performance is not significantly worse than when running the controller at a fast rate. 

We determined that the best run was at a rate of 30ms because it plotted the least amount of over and underhang. 
![image](https://github.com/ndavis26/ME-405-Lab-4/assets/158110649/36a7d717-3df7-4a49-ad44-7f4c5c0eb6df)

We at first tried at a rate of 50ms but it turned out not great for an appropriate run for our motor with both under and overhang when it reached the setpoint. 
![50 ms](https://github.com/ndavis26/ME-405-Lab-4/assets/158110649/394fd6ff-f941-4487-bbce-4d6a593478b2)

We then took it down to 40ms and it gave us a better plot compared to the 50ms plot. 
![50 ms](https://github.com/ndavis26/ME-405-Lab-4/assets/158110649/394fd6ff-f941-4487-bbce-4d6a593478b2)

Therefore we determined 30ms to be the best rate. 

The next part  of the lab was to use an example of a task function and modify it by having it run two separate motors simultaneously, either with the same or different rates. 

