import time
import random
import numpy

import pyadvantg
import SpacePartition1D
import SpacePartition3D
import matplotlib
import matplotlib.pyplot as pyplot

__author__ = 'etnc6d'


class EvolAlg(object):

    def __init__(self):
        self.max_evals = 1E5
        self.timeout = 30*60  # Seconds
        self.pop_size = 15
        self.children = 5

    def begin(self):
        eval_hist = []
        terminated = False
        start_time = time.time()
        best_solution = None
        generation = 0
        generation_hist = []
        best_solution_hist = []
        pop_size_hist = []
        gen_best_solution = []

        xpop = EvolAlg.initialize(self.pop_size, 10)
        # for i in range(len(xpop)):
        #    EvolAlg.fixify_x(xpop[i])
        ypop = EvolAlg.initialize(self.pop_size, 10)
        zpop = EvolAlg.initialize(self.pop_size, 10)

        xpop[0].relBins = [0, .3, .7, 1]
        xpop[1].relBins = [0, .6, .9, 1]

        # Comment

        print(xpop[0])
        print(xpop[1])
        print(str(xpop[0].diff(xpop[1])) + "   " + str(xpop[0].diff(xpop[1], True)))

        print(xpop[0])
        print(xpop[2])
        print(str(xpop[0].diff(xpop[2])) + "   " + str(xpop[0].diff(xpop[2], True)))

        print(xpop[0])
        print(xpop[3])
        print(str(xpop[0].diff(xpop[3])) + "   " + str(xpop[0].diff(xpop[3], True)))

        teams = EvolAlg.make_teams(xpop, ypop, zpop, 5)
        solutions = []
        for team in teams:
            sol = SpacePartition3D.SpacePartition3D()
            sol.x = team[0]
            sol.y = team[1]
            sol.z = team[2]
            sol.fit = EvolAlg.evaluate_team(sol.x, sol.y, sol.z)
            solutions.append(sol)

        maxfit = -1
        for sol in solutions:
            if sol.fit.fomavg > maxfit:
                maxfit = sol.fit.fomavg
                best_solution = sol

        generation_hist.append(0)
        best_solution_hist.append(best_solution)
        gen_best_solution.append(best_solution)
        pop_size_hist.append(self.pop_size)
        eval_hist.append(len(solutions))

        while not terminated:
            generation += 1

            xparents, yparents, zparents = EvolAlg.select_parents(xpop, ypop, zpop)
            xoff, yoff, zoff = EvolAlg.xover_coev(xparents, yparents, zparents, self.children)

            xoff = [EvolAlg.mutate(x) for x in xoff]

            # for i in range(len(xoff)):
            #    EvolAlg.fixify_x(xoff[i])

            yoff = [EvolAlg.mutate(y) for y in yoff]
            zoff = [EvolAlg.mutate(z) for z in zoff]

            for xx in xoff:
                if xx.get_bin_count() < 4:
                    print("Problem!")

            for xx in yoff:
                if xx.get_bin_count() < 4:
                    print("Problem!")

            for xx in zoff:
                if xx.get_bin_count() < 4:
                    print("Problem!")

            xpop.extend(xoff)
            ypop.extend(yoff)
            zpop.extend(zoff)

            # xpop, ypop, zpop = EvolAlg.tournament(xpop, ypop, zpop, self.pop_size, solutions)
            teams = EvolAlg.make_teams(xpop, ypop, zpop, 5)
            # solutions = []
            for team in teams:
                sol = SpacePartition3D.SpacePartition3D()
                sol.x = team[0]
                sol.y = team[1]
                sol.z = team[2]
                sol.fit = EvolAlg.evaluate_team(sol.x, sol.y, sol.z)
                solutions.append(sol)

            xpop, ypop, zpop = EvolAlg.tournament(xpop, ypop, zpop, self.pop_size, solutions)

            for sol in solutions:
                if sol.fit.fomavg > best_solution.fit.fomavg:
                    best_solution = sol

            generation_hist.append(generation)
            best_solution_hist.append(best_solution)
            pop_size_hist.append(len(xpop))
            eval_hist.append(len(solutions))

            if len(solutions) > self.max_evals:
                terminated = True
                print('Max evaluations reached')

            if time.time() - start_time > self.timeout:
                terminated = True
                print('Timeout')

        print("Generations: " + str(generation))
        print("Evaluations: " + str(len(solutions)))
        print(best_solution)

        matplotlib.rcParams.update({'font.size': 22})
        matplotlib.rcParams.update({'figure.autolayout': True})

        pyplot.figure()
        pyplot.plot(generation_hist, [s.fit.fomavg for s in best_solution_hist])
        pyplot.title('Best Fitness')
        pyplot.xlabel('Generation')
        pyplot.ylabel('Fitness')
        # pyplot.title('Best Fitness', fontname="Times New Roman")
        # pyplot.xlabel('Generation', fontname="Times New Roman")
        # pyplot.ylabel('Fitness', fontname="Times New Roman")

        pyplot.figure()
        pyplot.loglog(generation_hist, [s.fit.fomavg for s in best_solution_hist])
        pyplot.title('Best Fitness (Log Log)')
        pyplot.xlabel('Generation')
        pyplot.ylabel('Fitness')

        pyplot.figure()
        pyplot.plot([s.fit.fomavg for s in solutions])
        pyplot.title('Fitness with Evaluations')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Fitness')

        pyplot.figure()
        pyplot.plot([s.x.get_bin_count() for s in solutions])
        pyplot.title('X Bin Size')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('X Bins')

        pyplot.figure()
        pyplot.plot([s.y.get_bin_count() for s in solutions])
        pyplot.title('Y Bin Size')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Y Bins')

        pyplot.figure()
        pyplot.plot([s.z.get_bin_count() for s in solutions])
        pyplot.title('Z Bin Size')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Z Bins')

        pyplot.figure()
        pyplot.plot([s.fit.mcnp_t for s in solutions])
        pyplot.title('MCNP Runtime')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Runtime')

        pyplot.figure()
        pyplot.plot([s.fit.adv_t for s in solutions])
        pyplot.title('ADVANTG Runtime')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Runtime')

        pyplot.figure()
        totaltime = [s.fit.adv_t + s.fit.mcnp_t for s in solutions]
        cumsumtime = numpy.cumsum(totaltime).tolist()
        globalfit = [s.fit.fomavg / ct for s, ct in zip(solutions, cumsumtime)]
        pyplot.plot(globalfit)
        pyplot.title('Global Fitness')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Fitness')

        pyplot.figure()
        totaltime = [s.fit.adv_t + s.fit.mcnp_t for s in solutions]
        cumsumtime = numpy.cumsum(totaltime).tolist()
        globalfit = [s.fit.fomavg / ct for s, ct in zip(best_solution_hist, cumsumtime)]
        pyplot.plot(globalfit)
        pyplot.title('Global Best Fitness')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Fitness')

        pyplot.figure()
        pyplot.plot([s.fit.avg_unc() for s in solutions])
        pyplot.title('Average Uncertainty')
        pyplot.xlabel('Evaluation')
        pyplot.ylabel('Uncertainty')

        fig = pyplot.figure()
        fig.set_alpha(0.5)

        voxel_count = [s.x.get_bin_count()*s.y.get_bin_count()*s.z.get_bin_count() for s in solutions]
        time_per_voxel = [t/v for t, v in zip(totaltime, voxel_count)]
        # pyplot.scatter(voxel_count, time_per_voxel, c='k', alpha=.2)
        pyplot.scatter(voxel_count, totaltime, c='k', alpha=.2)
        # pyplot.ylim(0, 1.01*max(time_per_voxel))
        pyplot.ylim(0, 1.01*max(totaltime))
        pyplot.title('Time per voxel')
        pyplot.xlabel('Voxel Count')
        pyplot.ylabel('Evaluation Time / Voxel [min]')

        pyplot.figure()
        pyplot.plot(generation_hist, pop_size_hist)
        pyplot.title('Population Size')
        pyplot.xlabel('Generation')
        pyplot.ylabel('# Of Individuals per dimension')

        pyplot.show()

    @staticmethod
    def evaluate_team(xindiv, yindiv, zindiv):
        """Takes an individual from each coev pop and evaluates the 
        """
        return pyadvantg.eval_co_fitness(xindiv, yindiv, zindiv)  # random.random()

    @staticmethod
    def make_teams(xpop, ypop, zpop, pair_count):
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
        while child1.get_bin_count() < 4:
            EvolAlg.mutate_add(child1)

        # Construct child 2 form parent2 and parent1
        for gene in parent2.relBins:
            if gene < xpt:
                child2.relBins.append(gene)
        for gene in parent1.relBins:
            if gene >= xpt:
                child2.relBins.append(gene)
        while child2.get_bin_count() < 4:
            EvolAlg.mutate_add(child2)

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

            #for i in range(len(xc)):
            #    EvolAlg.fixify_x(xc[i])
            xchildren.extend(xc)
            ychildren.extend(yc)
            zchildren.extend(zc)

        return xchildren, ychildren, zchildren

    @staticmethod
    def mutate(indiv):
        if random.random() < 0.5:
            EvolAlg.mutate_add(indiv)
        else:
            EvolAlg.mutate_delete(indiv)

        # EvolAlg.fixify(indiv)

        return indiv

    # @staticmethod
    # def fixify_x(indiv):
    #    if 107.5/112.5 not in indiv.relBins:
    #        indiv.relBins.append(107.5/112.5)
    #        indiv.relBins = sorted(indiv.relBins)

    @staticmethod
    def mutate_add(indiv):
        indiv.relBins.append(random.random())
        indiv.relBins = sorted(indiv.relBins)

    @staticmethod
    def mutate_densify(indiv):
        p = 0.3

        t1 = random.random()
        t2 = random.random()
        pt1 = min(t1, t2)
        pt2 = max(t1, t2)

        tlist = []
        for i in range(0, indiv.get_bin_count()):
            if random.random() < p and (pt1 < indiv.relBins[i] < pt2 or pt1 < indiv.relBins[i+1] < pt2):
                r = random.random()
                r = (indiv.relBins[i] - indiv.relBins[i+1])*r + indiv.relBins[i]
                tlist.append(r)

        indiv.relBins.extend(tlist)
        indiv.relBins = sorted(indiv.relBins)


    @staticmethod
    def mutate_sparcify(indiv):
        p = 0.3

        t1 = random.random()
        t2 = random.random()
        pt1 = min(t1, t2)
        pt2 = max(t1, t2)

        for i in range(indiv.get_bin_count(), -1, -1):
            if random.random() < p and pt1 < indiv.relBins[i] < pt2:
                del self.relBins[i]


    @staticmethod
    def mutate_delete(indiv):
        if indiv.get_bin_count() > 4:
            remove_gene = random.randint(0, len(indiv.relBins)-1)
            del indiv.relBins[remove_gene]

    @staticmethod
    def tournament(x, y, z, survivor_count, solutions):

        newx = EvolAlg.tournament_single(x, survivor_count, solutions)
        newy = EvolAlg.tournament_single(y, survivor_count, solutions)
        newz = EvolAlg.tournament_single(z, survivor_count, solutions)

        return newx, newy, newz

    @staticmethod
    def tournament_single(x, survivor_count, solutions):

        if survivor_count >= len(x):
            return x

        xfit = []
        for indiv in x:
            ifit = 0
            icnt = 0
            for sol in solutions:
                if sol.x == indiv:
                    ifit += sol.fit.fomavg
                    icnt += 1
            if icnt > 0:
                ifit /= icnt
            xfit.append(ifit)

        mostfit = max(xfit)
        pressure = 2.0

        xfit = [q+(mostfit/pressure) for q in xfit]

        xfitsum = sum(xfit)

        if xfitsum == 0:
            return numpy.random.choice(x, survivor_count, False).tolist()

        xfit = [q/xfitsum for q in xfit]

        return numpy.random.choice(x, survivor_count, False, xfit).tolist()

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





