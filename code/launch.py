
ADV_SRC = '/media/data/x.dne'

FOLDER_ROOT = '/media/data/school/CS6401'
FILEEXT = '.dne'

xs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
ys = [10]
zs = [10]

def eval_fitness(x):
    
    # Create folder
    folder_base = FOLDER_ROOT + "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
    filename = folder_base + "adv_ea.adv"
    
    # Create file
    write_advtg(filename, x, y, z)
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0
    
def do_terminate():
    return True
    
    
def initialize():
    return [], []
    
    
def select_mates(population_fit, population):
    return population_fit, population
    
    
def generate_offspring(parent_fit, parent_pop):
    return []


def tournament(parent_fit, parent_pop, child_fit, child_pop):
    return [], []

global_best_indiv = None
global_best_fit = None

fitness, pop = initialize()

while not do_terminate():
    
    parent_fit, parent_pool = select_mates(fitness, pop)
    children = generate_offspring(parent_fit, parent_pool)
    child_fit = [eval_fitness(child) for child in children]
    #children = [(e, c) for (e, c) in zip(children, child_fit)]

    fitness, pop = tournament(fitness, pop, child_fit, children)









