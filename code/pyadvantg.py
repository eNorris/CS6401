import phasetree
import datetime
import os



FOLDER_ROOT = '/media/data/school/CS6401/ex1'
ADV_SRC = FOLDER_ROOT + '/av.dne'
MCNP_SRC = FOLDER_ROOT + '/mc.dne'
FILEEXT = '.dne'

def eval_fitness(indiv):
    if not type(indiv) == phasetree.SingletonPhaseSpace:
        raise Exception('eval_fitness requires a singleton population, did you mean to use the _co version?')
    
    xlen = indiv.x.node_count()
    ylen = indiv.y.node_count()
    zlen = indiv.z.node_count()
    
    rightnow = datetime.datetime.now()
    nowstring = ""
    nowstring += str(rightnow.year) + "_"
    nowstring += str(rightnow.month) + "_"
    nowstring += str(rightnow.day) + "___"
    nowstring += str(rightnow.hour) + "_"
    nowstring += str(rightnow.minute) + "_"
    nowstring += str(rightnow.second)
    
    # Move to the working folder
    if not os.path.exists(FOLDER_ROOT):
        os.makedirs(FOLDER_ROOT)
    os.chdir(FOLDER_ROOT)
    
    #p# Create folder
    folder_base = FOLDER_ROOT + nowstring
    advfilename = folder_base + "adv_ea.adv"
    
    # Create file
    rewrite_advtg(ADV_SRC, advfilename, 1,2,3)
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0
    
def eval_co_fitness(indiv_x, indiv_y, indiv_z):
    #p# Create folder
    folder_base = FOLDER_ROOT #+ "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
    filename = folder_base + "adv_ea.adv"
    
    # Create file
    write_advtg(filename, 1,2,3)
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0

def rewrite_advtg(adv_in_filename, adv_out_filename, x, y, z):
    print("Writing ADVANTG file: " + adv_out_filename)
    
    
def run_advtg(filename):
    print("Running ADVANTG file: " + filename)
    
    
def run_mcnp(filename):
    print("Running MCNP file: " + filename)
    
    
def parse_mcnp(filename):
    print("Parsing MCNP file: " + filename)
