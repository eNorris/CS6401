import random

__author__ = 'etnc6d'


class SpacePartitionMutator(object):

    def __init__(self):
        pass

    @staticmethod
    def mutate(indiv):
        indiv.relBin.append(random.random())
        indiv.relBin = sorted(indiv.relBin)

    @staticmethod
    def mutate3(xpop, ypop, zpop):
        return [], [], []