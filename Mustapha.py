import datetime
from multiprocessing import log_to_stderr
import time
import threading
from collections import deque


################################################################################
#   Handle all connections and rights for the server
################################################################################
class Machine:
    name = None
    priority = -1
    period = -1
    execution_time = -1
    need = -1
    product = None

    ############################################################################
    def __init__(self, name, priority, period, need, product, execution_time):
        self.name = name
        self.priority = priority
        self.need = need
        self.period = period
        self.execution_time = execution_time
        self.product = product

    ############################################################################
    def run(self):
        global tank, stock_motor, stock_wheel, executing
        if self.need > tank:
            executing = True
            print(self.name + " producing 1 " + self.product)
            time.sleep(self.execution_time)
            tank -= self.need
            if self.product == "motor":
                stock_motor += 1
            if self.name == "wheel":
                stock_wheel += 1

            print(self.name + " has finished producing " + self.product)
            print("**** motors = ", str(stock_motor) + " wheels = " + str(stock_wheel) + " *****")
            executing = False



################################################################################
#   Handle all connections and rights for the server
################################################################################
class Pump:
    name = None
    priority = -1
    period = -1
    execution_time = -1
    amount = -1

    ############################################################################
    def __init__(self, name, priority, period, amount, execution_time):
        self.name = name
        self.priority = priority
        self.amount = amount
        self.period = period
        self.execution_time = execution_time

    ############################################################################
    def run(self):
        global tank, executing
        if executing == False and tank < tank_limit :
            executing = True
            print(self.name + " started pumping " + str(self.amount))
            tank += self.amount
            time.sleep(self.execution_time)
            print(self.name + " has finished pumping " + "tank is at " + str(tank))
            time.sleep(self.period)
            executing = False


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':

    print("here")

    global tank, stock_wheel, stock_motor, tank_limit, executing
    tank = 0
    stock_wheel = 0
    stock_motor = 0
    tank_limit = 50
    executing = False

    last_execution = datetime.datetime.now()

    # Instanciation of task objects
    task_list = []

    task_list.append \
        (Pump(name="Pump 1", priority=1, period=5, amount=10, execution_time=2))

    task_list.append \
        (Pump(name="Pump 2", priority=1, period=5, amount=20, execution_time=3))
    task_list.append \
        (Machine(name="Machine 1", priority=1, period=10, need=10, product="motor", execution_time=5))
    task_list.append \
        (Machine(name="Machine 2", priority=1, period=10, need=10, product="wheel", execution_time=3))

    # Global scheduling loop
    while 1:

        print("\nScheduler tick : " + datetime.datetime.now().strftime("%H:%M:%S"))

        task_to_run = None

        for currentTask in task_list:
            currentTask.run()
