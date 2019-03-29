# ProgressBar_vs_functions (Using MultiThreading)
Making a progressBar updated while calling functions, using QThread (2 threads + MainThread)

Point is to update a progressBar in PyQT5 while executing functions and without blocking the MainThread i.e. the GUI app. This is the easy way, nothing fancy, just working :)

What's needed to run it:
- py >= 3.5 (should work, I have 3.7.2)
- PyQT5 (QtCore, QtWidgets)
- time

2 things you need to pay attention to if you use it on your own code:
- I needed 3 functions to be runned while progressBar was updated, but up to you to call more/less... However you'll probably need to change few stuffs, no big deal.
- I defined my TIME_LIMIT to 4 in order to 100/3 * 0.1sec rounded to 4. Because it was approximatively the execution time of each  function, but if it is way longer or shorter, just reduce/increase :
  - TIME_LIMIT = x
  - time.sleep(x) => in ProgressBarWorker()
    
Before starting, you need to update 2 things : the import of your 3 functions (that was for me in 3 different modules) and where they will be called (in the list_func) so basically change:
- imports at the beginning
```
  import function1
  import function2
  import function3
```
- functions around line 122 (in the ```__init__``` section in class Actions(QDialog)):
```
self.list_func = ('function1.function1', 'function2.function2', 'function3.function3')
```

What it won't work with at this point => matplotlib, the graph edition, it calls Tkinter that does not allowed running graphic thread out of the MainThread, it may therefore work or not, depending on the version your using, but it is atm for sure unstable.

Hope it helps you figured out how this is working, do not hesitate to star if you liked it ;)
