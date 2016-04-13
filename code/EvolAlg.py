import PopInitializer
import ParentSelector
import SpacePartitionXOver
import SpacePartitionMutator
import Tournament
import time

__author__ = 'etnc6d'


class EvolAlg(object):

    def __init__(self):
        self.max_evals = 10
        self.timeout = 60  # Seconds

    def begin(self):
        evals = 0
        terminated = False
        start_time = time.time()

        xpop = PopInitializer.PopInitializer.initialize(5)
        ypop = PopInitializer.PopInitializer.initialize(5)
        zpop = PopInitializer.PopInitializer.initialize(5)

        xfit, yfit, zfit = EvolAlg.evaluate_indivs(xpop, ypop, zpop)

        while not terminated:
            xparents, yparents, zparents = ParentSelector.ParentSelector.select(xpop, ypop, zpop)
            xoff, yoff, zoff = SpacePartitionXOver.SpacePartitionXOver.xover3(xparents, yparents, zparents)
            xoff, yoff, zoff = SpacePartitionMutator.SpacePartitionMutator.mutate3(xoff, yoff, zoff)

            xpop.extend(xoff)
            ypop.extend(yoff)
            zpop.extend(zoff)

            xpop, ypop, zpop = Tournament.Tournament.do_tournament(xpop, ypop, zpop)

            if evals > self.max_evals:
                terminated = True
                print('Max evaluations reached')

            if time.time() - start_time > self.timeout:
                terminated = True
                print('Timeout')

    @staticmethod
    def evaluate_indivs(xpop, ypop, zpop):
        return [], [], []