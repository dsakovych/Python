import time
import sys
from abc import abstractmethod
import zope.interface


class solver_interface(zope.interface.Interface):  # interface for our solvers
    name = zope.interface.Attribute('')            # key feature is required method compute in our solver
    def compute(self, inp):
        pass


class Problem:  # base class with all required due to task methods

    solvers = []
    count = 10

    @abstractmethod  # this method will be redefined in heir class
    def inputs(self):
        pass

    @abstractmethod  # this method will be redefined in heir class
    def outputs(self):
        pass

    def add_solver(self, obj):
        if obj in solvers:
            print('solver is already added')  # avoiding adding similar solver twice
            return
        try:
            if type(obj) is "solver_interface":  # compliance with our solver interface
                solvers.append(obj)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def profile_solvers(self):
        time_list = []  # storing all compute times here
        for item in solvers:
            start_time = time.time()  # start counter
            for i in range(len(item.compute(self.inputs()))):  # loop through all input elements
                print('Solving "SumUpToN" with "%s"' % item.name, 'input=', item.compute(self.inputs())[i])
                try:
                    for j in range(count):  # 10 times as in description
                        item.compute(self.inputs()[i])
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    break
            time_calcul = time.time() - start_time  # stop counter
            time_list.append(time_calcul)
            print('10 loops took %d seconds' % time_calcul / len(item.compute(self.inputs())), 'on average')
        print('total computing time is %d' % sum(time_list))


class SumUpToN(Problem):
    name = 'SumUpToN'
    def inputs(self):
        return 100, 1000000

    def outputs(self):
        return 5050, 500000500000


class Naive(solver_interface):
    name = 'Naive'
    def compute(self, N):
        return reduce(lambda x, y: x + y, range(1, N + 1))

class ConstTime(solver_interface):
    name = 'ConstTime'
    def compute(self, N):
        return (N + 1) * N / 2

class Wrong(solver_interface):
    name = 'Wrong'
    def compute(self, N):
        return 100


prob = SumUpToN()

prob.add_solver(Naive())
prob.add_solver(ConstTime())
prob.add_solver(Wrong())
prob.profile_solvers()
