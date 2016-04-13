import SpacePartition1D
import random

__author__ = 'etnc6d'


class PopInitializer(object):

    def __init__(self):
        pass

    @staticmethod
    def initialize(indivCount):
        init_pop = []

        for i in range(indivCount):
            new_indiv = SpacePartition1D.SpacePartition1D()
            PopInitializer.randomize(new_indiv)
            init_pop.append(new_indiv)

        return init_pop

    @staticmethod
    def randomize(indiv):
        for i in range(4):
            indiv.relBins.append(random.random())
            indiv.relBins = sorted(indiv.relBins)
        return indiv