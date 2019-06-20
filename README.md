# ProgressBar_vs_functions (Using MultiThreading)
Making a progressBar updated while calling functions, using QThread (2 threads + MainThread)

Point is to update a progressBar in PyQT5 while executing functions and without blocking the MainThread i.e. the GUI app. This is the easy way, nothing fancy, just working :)

What's needed to run it:
- py >= 3.5 (should work, I have 3.7.2)
- PyQT5 (QtCore, QtWidgets)

Sources :
- To start with : [https://riptutorial.com/fr/pyqt5/example/29500/basic-pyqt-progress-bar]
- To go further and use QThreadPool : [https://www.mfitzp.com/article/multithreading-pyqt-applications-with-qthreadpool/] => Github [https://github.com/mfitzp]
