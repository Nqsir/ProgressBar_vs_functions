# # # # # # # # # # # # # # # 
#
#
# Need to import your 3 functions see under import function1, 2, 3 => Line 14, 15, 16
#
# Need to write in the list the 3 functions you want to call => Line 129 : 
#   # self.list_func = ('function1.function1', 'function2.function2', 'function3.function3')
#
#
# # # # # # # # # # # # # # # 

import sys
import time
import function1
import function2
import function3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton)

TIME_LIMIT = 4


class Signals(QObject):
    """
    Signals class is made to override / define signals we need by pyqtSignal() in our Worker class i.e.
        - ProgressBarWorker
        - FuncsWorker

    Signals Class is called in each ProgressBarWorker() and FuncsWorker() creation

    Our 3 signals give us the possibility to catch signals when starting progressing and finishing the run method, you
    can choose what you want to be returned in my need (int) while progress none for the rest
    """
    starting = pyqtSignal()
    progress = pyqtSignal(int)
    finish = pyqtSignal()


class ProgressBarWorker(QThread):
    """
    Inherits from QThread to not freeze our soft => This is what this is about right ?
    That class object is made too show updates with a defining time.sleep() to make it look smooth. The sleep duration
    goes with the TIME_LIMIT in the above class FuncsWorker().

    A classic while loop that emits signal => signals.progress() to set value to the progressBar

    Taking 2 params first one that defines the limit and the second that defines the start.
    """

    # Initialising class, and transfert params + taking our signals to self to be used in the run method
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self):
        self.signals.starting.emit()
        count = self.args[1]
        while count < 99 and count < self.args[0]:
            count += 1
            time.sleep(0.1)
            self.signals.progress.emit(count)

        self.signals.finish.emit()

    # Gives the information when class is destroyed
    def __del__(self):
        print(object, 'PROGRESSBAR DESTROYED')


class FuncsWorker(QThread):
    """
    Inherits from QThread to not freeze our soft => This is what this is about right ?

    FuncsWorker, is a class that execute our list of functions we have defined in our list_func,
    here caught as args[0].

    It also emits an int (remember progress = pyqtSignal(int) in class Signals) from 0 to len(list_func) each time
     a func is about to be executed => In order to give the limit to the progressBar (see above).

    Using time.time() makes us catch how long it takes to execute a function, in  order to make sure
    that the progressBar has the time to set its value => If function is executed faster than the progressBar growth
     it will make it look weird like a ping-pong progressing.

    The limit comes from : Each time a function is about to be executed, send a signal (self.signals.progress.emit(c))
    that will make progressbar grow, that growth takes (see in ProgressBarWorker time.sleep(0.1)) 0.1 sec * 100/3
    => I want to go to 100% I've got 3 functions = Approx 4 (3.33) seconds, as a function can be faster executed,
    I am checking the time it took to executed it (exec_time) and making it sleep until progressbar has reached its
    defined limit, approx 4 seconds.
    """

    # Initialising class, and transfert params + taking our signals to self to be used in the run method
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self):
        self.signals.starting.emit()
        for c, func in enumerate(self.args[0]):
            start_time = time.time()
            self.signals.progress.emit(c)
            print(func)
            exec(func)
            exec_time = round((time.time() - start_time), 2)
            if exec_time < TIME_LIMIT:
                time.sleep(TIME_LIMIT - exec_time)

        self.signals.finish.emit()

    # Gives the information when class is destroyed
    def __del__(self):
        print(object, 'FUNCS DESTROYED')


class Actions(QDialog):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button results in the start of a timer and
    updates the progress bar.
    """

    def __init__(self):
        super().__init__()
        # Defining the functions we want to execute in a list, imported from function1.py function2.py function3.py
        self.list_func = ('function1.function1', 'function2.function2', 'function3.function3')
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

    # Method that is called when button is clicked
    # It then creates a class FuncsWorker, and defining what the signals must do :
        # progress => Each time a function is about to be executed => call funcs_progress_return
        # finish => When the execution of all our functions is done => call closing
    def start_button_click(self):
        self.funcs = FuncsWorker(self.list_func)
        self.start_button.hide()
        self.funcs.signals.progress.connect(self.funcs_progress_return)
        self.funcs.signals.finish.connect(self.closing)
        self.funcs.start()

    # Creates a ProgressBarWorker class each time a function is about to be executed and defines the limits
    # of the progression => first from 0 to 34, then 34 to 67 then ...
    # initialises progress signal of ProgressBarWorker to progressbar_update method
    def funcs_progress_return(self, value):
        self.graphic = ProgressBarWorker((100 / self.len_list_func) * (value + 1), (100 / self.len_list_func) * value)
        self.graphic.start()
        self.graphic.signals.progress.connect(self.progressbar_update)

    # Called above, change the value of the progressBar
    def progressbar_update(self, value):
        self.progress.setValue(value)

    # Called when funcs.finish signal is emitted
    def closing(self):
        print('DONE')
        self.progress.setValue(100)
        self.start_button.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    sys.exit(app.exec_())
