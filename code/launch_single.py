import phasetree
import pyadvantg

INIT_POP_SIZE = 5
    
def do_terminate():
    return True
    
    
def initialize(pop_size):
    
    init_indivs = []
    init_fits = []
    
    for i in range(pop_size):
        indiv = phasetree.SingletonPhaseSpace()
        indiv.randomize_uniform(10, 10, 10)
        fit = pyadvantg.eval_fitness(indiv)
        
        init_indivs.append(indiv)
        init_fits.append(fit)
        
    return init_fits, init_indivs
    

def initialize_co(pop_size):
    
    init_indivs = []
    init_fits = []
    
    for i in range(pop_size):
        indiv = phasetree.PhaseTree()
        indiv.randomize_uniform(10)
        fit = pyadvantg.eval_fitness(indiv)
        
        init_indivs.append(indiv)
        init_fits.append(fit)
        
    return init_fits, init_indivs
    
    
def select_mates(population_fit, population):
    return population_fit, population
    
    
def generate_offspring(parent_fit, parent_pop):
    return []


def tournament(parent_fit, parent_pop, child_fit, child_pop):
    return [], []

global_best_indiv = None
global_best_fit = None

fitness, pop = initialize(INIT_POP_SIZE)

while not do_terminate():
    
    parent_fit, parent_pool = select_mates(fitness, pop)
    children = generate_offspring(parent_fit, parent_pool)
    child_fit = [pyadvantg.eval_fitness(child) for child in children]
    #children = [(e, c) for (e, c) in zip(children, child_fit)]

    fitness, pop = tournament(fitness, pop, child_fit, children)









