# ProgressBar_vs_functions (Using MultiThreading)
Making a progressBar updated while calling functions, using QThread (2 threads + MainThread)

Point is to update a progressBar in PyQT5 while executing functions and without blocking the MainThread i.e. the GUI app. This is the easy way, nothing fancy, just working :)

What's needed to run it:
- py >= 3.5 (should work, I have 3.7.2)
- PyQT5 (QtCore, QtWidgets)
- time
- sys

2 things you need to pay attention to if you use it on your own code:
- I needed 3 functions to be runned while progressBar was updated, but up to you to call more/less... However you'll probably just need to change functions (see below)
- I defined my self.time_limit to 100/3 * 0.1sec + extra 1 sec just to be safe that each class won't redefine the progressBar value at the same time. Because it was approximatively the execution time of each of MY OWN function, but if it is way longer or shorter, just reduce/increase (1), same thing if 0.1 seems to slow/fast, just change (2) :
  - (1) self.time_limit = x => in FuncsWorker()
  - (2) time.sleep(x) => in ProgressBarWorker()

What does not work with => matplotlib, the graph edition calls Tkinter that does not allow running a graphic thread when out of the MainThread, it may therefore make some serious RuneTimeError, depending on the version your using, but it is for sure unstable with mine (matplotlib 3.0.2).

Hope it helps you figured out how this is working, do not hesitate to star if you liked it ;)

Sources :
- To start with : [https://riptutorial.com/fr/pyqt5/example/29500/basic-pyqt-progress-bar]
- To go further and use QThreadPool : [https://www.mfitzp.com/article/multithreading-pyqt-applications-with-qthreadpool/] => Github [https://github.com/mfitzp]
