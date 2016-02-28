ADV_SRC = '/media/data/x.dne'

FOLDER_ROOT = '/media/data/school/CS6401'
FILEEXT = '.dne'

def eval_fitness(indiv):
    #p# Create folder
    folder_base = FOLDER_ROOT #+ "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
    filename = folder_base + "adv_ea.adv"
    
    # Create file
    write_advtg(filename, 1,2,3)
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0

def write_advtg(filename, x, y, z):
    print("Writing ADVANTG file: " + filename)
    
    
def run_advtg(filename):
    print("Running ADVANTG file: " + filename)
    
    
def run_mcnp(filename):
    print("Running MCNP file: " + filename)
    
    
def parse_mcnp(filename):
    print("Parsing MCNP file: " + filename)
