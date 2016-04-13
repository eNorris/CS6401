import random
import SpacePartition1D

__author__ = 'etnc6d'


class SpacePartitionXOver(object):

    def __init__(self):
        pass

    @staticmethod
    def xover(parent1, parent2):
        children = []

        xpt = random.random()

        child1 = SpacePartition1D.SpacePartition1D()
        child2 = SpacePartition1D.SpacePartition1D()

        # Construct child 1 from parent1 and parent2
        for gene in parent1.relBins:
            if gene < xpt:
                child1.relBins.append(gene)
        for gene in parent2.relBins:
            if gene >= xpt:
                child1.relBins.append(gene)

        # Construct child 2 form parent2 and parent1
        for gene in parent2.relBins:
            if gene < xpt:
                child2.relBins.append(gene)
        for gene in parent1.relBins:
            if gene >= xpt:
                child2.relBins.append(gene)

        children.append(child1)
        children.append(child2)

        return children

    @staticmethod
    def xover3(xpar, ypar, zpar):
        return [], [], []
