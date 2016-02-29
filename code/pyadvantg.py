import phasetree
import datetime
import os
import subprocess



FOLDER_ROOT = '/media/data/school/CS6401/code/ex1.gitdnt'
ADV_SRC = FOLDER_ROOT + '/ex1_adv.adv'
MCNP_SRC = FOLDER_ROOT + '/ex1_mcnp.inp'
#FILEEXT = '.dne'

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
    #folder_base = FOLDER_ROOT + "/adv_" + nowstring
    advfilename = FOLDER_ROOT + "/ex1_tmp_adv.adv"
    
    # Create file
    rewrite_advtg(ADV_SRC, advfilename, indiv.x, indiv.y, indiv.z)
    
    
    cmd = "../advrun.sh ex1_tmp_adv.adv"
    subprocess.call(cmd.split())
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0
    
def eval_co_fitness(indiv_x, indiv_y, indiv_z):
    #p# Create folder
    folder_base = FOLDER_ROOT #+ "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
    filename = folder_base + "adv_ea.adv"
    
    # Create file
    rewrite_advtg(filename, 1,2,3)
    
    # Copy MCNP
    
    # cd into the folder
    return 1.0


def rewrite_advtg(adv_in_filename, adv_out_filename, x, y, z):
    
    fin = open(adv_in_filename, 'r')
    fout = open(adv_out_filename, 'w')
    print("Writing ADVANTG file: " + adv_out_filename)
    
    for line in fin.readlines():
        if line.startswith("mesh_x "):
            fout.write('# ' + str(x) + '\n')
            fout.write("mesh_x " + x.get_mesh() + '\n')
        elif line.startswith("mesh_x_ints "):
            fout.write("mesh_x_ints " + x.get_mesh_ints() + '\n')
            
        elif line.startswith("mesh_y "):
            fout.write('# ' + str(y) + '\n')
            fout.write("mesh_y " + y.get_mesh() + '\n')
        elif line.startswith("mesh_y_ints "):
            fout.write("mesh_y_ints " + y.get_mesh_ints() + '\n')
            
        elif line.startswith("mesh_z "):
            fout.write('# ' + str(z) + '\n')
            fout.write("mesh_z " + z.get_mesh() + '\n')
        elif line.startswith("mesh_z_ints "):
            fout.write("mesh_z_ints " + z.get_mesh_ints() + '\n')
            
        else:
            fout.write(line)
            
    fin.close()
    fout.close()
    

    
    
def run_advtg(filename):
    print("Running ADVANTG file: " + filename)
    
    
def run_mcnp(filename):
    print("Running MCNP file: " + filename)
    
    
def parse_mcnp(filename):
    print("Parsing MCNP file: " + filename)
