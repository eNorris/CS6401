import time
import random

import SpacePartition1D
import SpacePartition3D
import matplotlib.pyplot as pyplot

__author__ = 'etnc6d'


class EvolAlg(object):

    def __init__(self):
        self.max_evals = 10
        self.timeout = 5  # Seconds
        self.pop_size = 5
        self.children = 5

    def begin(self):
        evalHist = []
        terminated = False
        start_time = time.time()
        bestSolution = None
        generation = 0
        generationHist = []
        bestSolutionHist = []
        popSize = []

        #xpop = PopInitializer.PopInitializer.initialize(5)
        #ypop = PopInitializer.PopInitializer.initialize(5)
        #zpop = PopInitializer.PopInitializer.initialize(5)

        xpop = EvolAlg.initialize(self.pop_size, 10)
        ypop = EvolAlg.initialize(self.pop_size, 10)
        zpop = EvolAlg.initialize(self.pop_size, 10)

        allpairs = EvolAlg.pair_indivs(xpop, ypop, zpop, 5)
        solutions = []
        for pair in allpairs:
            sol = SpacePartition3D.SpacePartition3D()
            sol.x = pair[0]
            sol.y = pair[1]
            sol.z = pair[2]
            sol.fit = EvolAlg.evaluate_team(sol.x, sol.y, sol.z)
            solutions.append(sol)

        maxfit = -1
        for sol in solutions:
            if sol.fit > maxfit:
                bestSolution = sol
        #xfit, yfit, zfit = EvolAlg.evaluate_indivs(xpop, ypop, zpop)

        generationHist.append(0)
        bestSolutionHist.append(bestSolution)
        popSize.append(self.pop_size)
        evalHist.append(len(solutions))

        while not terminated:
            generation += 1
            #print('Next generation...')
            #xparents, yparents, zparents = ParentSelector.ParentSelector.select(xpop, ypop, zpop)
            xparents, yparents, zparents = EvolAlg.select_parents(xpop, ypop, zpop)
            #xoff, yoff, zoff = SpacePartitionXOver.SpacePartitionXOver.xover3(xparents, yparents, zparents)
            #xoff, yoff, zoff = SpacePartitionMutator.SpacePartitionMutator.mutate3(xoff, yoff, zoff)
            xoff, yoff, zoff = EvolAlg.xover_coev(xparents, yparents, zparents, self.children)

            xoff = [EvolAlg.mutate(x) for x in xoff]
            yoff = [EvolAlg.mutate(y) for y in yoff]
            zoff = [EvolAlg.mutate(z) for z in zoff]
            #xoff, yoff, zoff = EvolAlg.mutate(xoff, yoff, zoff)

            xpop.extend(xoff)
            ypop.extend(yoff)
            zpop.extend(zoff)

            #xpop, ypop, zpop = Tournament.Tournament.do_tournament(xpop, ypop, zpop)
            xpop, ypop, zpop = EvolAlg.tournament(xpop, ypop, zpop, solutions)

            #print('The best:')
            #print(bestSolution)
            for sol in solutions:
                if sol.fit > bestSolution.fit:
                    bestSolution = sol

            generationHist.append(generation)
            bestSolutionHist.append(bestSolution)
            popSize.append(len(xpop))
            evalHist.append(len(solutions))

            if len(solutions) > self.max_evals:
                terminated = True
                print('Max evaluations reached')

            if time.time() - start_time > self.timeout:
                terminated = True
                print('Timeout')

        print("Generations: " + str(generation))
        print("Evaluations: " + str(len(solutions)))
        print(bestSolution)

        pyplot.plot(generationHist, [s.fit for s in bestSolutionHist])
        pyplot.title('Best Fitness')
        pyplot.xlabel('Generation')
        pyplot.ylabel('Fitness')
        pyplot.show()

    @staticmethod
    def evaluate_team(xindiv, yindiv, zindiv):
        """Takes an individual from each coev pop and evaluates the 
        """
        return random.random()

    @staticmethod
    def pair_indivs(xpop, ypop, zpop, pair_count):
        """Pairs members of the coev pops together
        xpop - A list of x SpacePartition1D individuals
        ypop - A list of y SpacePartition1D individuals
        zpop - A list of z SpacePartition1D individuals
        pair_count - The number of pairings that will be made
        """

        tups = []
        for i in range(pair_count):
            x = random.choice(xpop)
            y = random.choice(ypop)
            z = random.choice(zpop)
            tups.append((x, y, z))

        return tups

    @staticmethod
    def select_parents(xpop, ypop, zpop):
        return xpop, ypop, zpop

    @staticmethod
    def xover1D(parent1, parent2):
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
    def xover3D(x1, y1, z1, x2, y2, z2):
        xchildren = EvolAlg.xover1D(x1, x2)
        ychildren = EvolAlg.xover1D(y1, y2)
        zchildren = EvolAlg.xover1D(z1, z2)
        return xchildren, ychildren, zchildren

    @staticmethod
    def xover_coev(xpop, ypop, zpop, xover_count):
        xchildren = []
        ychildren = []
        zchildren = []

        for i in range(xover_count):
            p1 = random.randint(0, len(xpop)-1)
            p2 = random.randint(0, len(xpop)-1)
            xc, yc, zc = EvolAlg.xover3D(xpop[p1], ypop[p1], zpop[p1], xpop[p2], ypop[p2], zpop[p2])
            xchildren.extend(xc)
            ychildren.extend(yc)
            zchildren.extend(zc)

        return xchildren, ychildren, zchildren

    @staticmethod
    def mutate(indiv):
        indiv.relBins.append(random.random())
        indiv.relBins = sorted(indiv.relBins)
        return indiv

    @staticmethod
    def tournament(x, y, z, solutions):
        return x, y, z

    @staticmethod
    def initialize(indivCount, max_genes):
        init_pop = []

        for i in range(indivCount):
            new_indiv = SpacePartition1D.SpacePartition1D()
            EvolAlg.randomize(new_indiv, random.randint(5, max_genes))
            init_pop.append(new_indiv)

        return init_pop

    @staticmethod
    def randomize(indiv, genes):
        for i in range(genes):
            indiv.relBins.append(random.random())
            indiv.relBins = sorted(indiv.relBins)
        return indiv





