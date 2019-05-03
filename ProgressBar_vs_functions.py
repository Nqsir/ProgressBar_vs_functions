import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton)


class Signals(QObject):
    """
    Signals class is made to override / define signals we need by pyqtSignal() in our Worker class i.e.
        - ProgressBarWorker
        - FuncsWorker
    Signals Class is called in each ProgressBarWorker() and FuncsWorker() creation
    
    Our 3 signals give us the possibility to catch signals when starting, progressing and finishing the run method, you
    can choose what you want to be returned. In my case, I needed an int while progressing and none for the rest
    """

    starting = pyqtSignal()
    progress = pyqtSignal(int)
    finish = pyqtSignal()


class ProgressBarWorker(QThread):
    """
    Only called with Method 1 !
    Inherits from QThread to not freeze our soft => This is what this is about right ?

    That class object is made too show updates with a defining time.sleep() to make it look smooth. The sleep duration
    goes with the self.time_limit in the below class FuncsWorker().
    """
    # Initialising class, and transfer params + taking our signals to self to be used in the run method
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self):
        self.signals.starting.emit()
        count = (100 / self.args[1]) * self.args[0]
        stop = (100 / self.args[1]) * (self.args[0] + 1)
        while count < 99 and count < stop:
            count += 1
            time.sleep(0.1)
            self.signals.progress.emit(count)

        self.signals.finish.emit()


class FuncsWorker(QThread):
    """
    It also emits an int (remember progress = pyqtSignal(int) in class Signals) from 0 to len(list_func) each time
     a func is about to be executed => In order to give to the progressBar which of the 3 functions is executed.

    The self.time_limit makes us catch how long it takes to execute a function, in  order to make sure
    that the progressBar has the time to set its value

    => I want to go to 100% I've got 3 functions = 3.33 seconds and added and extra 1 sec to be sure,
    as a function can be faster executed, just checking the time it took to execute it (exec_time) and  if needed make
     it wait until progressbar has reached its defined limit => self.time_limit.
    """

    # Initialising class, and transfert params + taking our signals to self to be used in the run method
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()
        self.time_limit = ((100 / len(self.args[0])) * 0.1 + 1)

    def run(self):
        self.signals.starting.emit()
        for c, func in enumerate(self.args[0]):
            start_time = time.time()
            self.signals.progress.emit(c)
            print(func)
            func()
            exec_time = round((time.time() - start_time), 2)
            if exec_time < self.time_limit:
                time.sleep(self.time_limit - exec_time)

        self.signals.finish.emit()


class Actions(QDialog):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button updates the progress bar.
    """

    def __init__(self):
        super().__init__()
        # Defining the functions we want to execute in a list
        self.list_func = (function1, function2, function3)
        self.len_list_func = len(self.list_func)
        self.init_ui()

    # Initialise our window
    def init_ui(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.start_button = QPushButton('Start', self)
        self.start_button.move(0, 30)
        self.start_button.clicked.connect(self.start_button_click)
        self.show()

    # Method that is called when button is clicked and defines bounds with signals
    def start_button_click(self):
        self.funcs = FuncsWorker(self.list_func)
        self.start_button.hide()
        self.funcs.signals.progress.connect(self.funcs_progress_return)
        self.funcs.signals.finish.connect(self.closing)
        self.funcs.start()

    # -------- Either Pick METHOD 1 or 2 and comment the other

    # --- METHOD 1 => Creates each time a Qthread in order to update the progressBar and is obviously smoother
    def funcs_progress_return(self, value):
        self.graphic = ProgressBarWorker(value, self.len_list_func)
        self.graphic.start()
        self.graphic.signals.progress.connect(self.progress.setValue)

    # --- METHOD 2 => A simple method called to update progressBar without Thread and is therefor less effective
    # def funcs_progress_return(self, value):
    #     count = (100 / self.len_list_func) * value
    #     stop = (100 / self.len_list_func) * (value + 1)
    #     while count < 99 and count < stop:
    #         count += 1
    #         time.sleep(0.1)
    #         self.progress.setValue(count)

    def closing(self):
        print('DONE')
        self.progress.setValue(100)
        self.start_button.show()


# ---- The 3 or more functions to be executed

def function1():
    time.sleep(5)


def function2():
    time.sleep(5)


def function3():
    time.sleep(5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    sys.exit(app.exec_())
