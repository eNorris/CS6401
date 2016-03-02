import phasetree
import datetime
import os
import subprocess
import time
import meshtaldata
import numpy
import shutil


FOLDER_ROOT = '/media/data/school/CS6401/code'
FOLDER_WORKING = FOLDER_ROOT + "/ex2.gitdnt"
ADV_SRC = FOLDER_ROOT + '/ex2_adv.adv'
TMP_ADV = FOLDER_WORKING + "/ex2_tmp_adv.adv"
MCNP_SRC = FOLDER_ROOT + '/ex2_mcnp.inp'
TMP_MCNP = FOLDER_WORKING + '/ex2_mcnp.inp'

def eval_fitness(indiv):
    if not type(indiv) == phasetree.SingletonPhaseSpace:
        raise Exception('eval_fitness requires a singleton population, did you mean to use the _co version?')
    
    #xlen = indiv.x.node_count()
    #ylen = indiv.y.node_count()
    #zlen = indiv.z.node_count()
    
    rightnow = datetime.datetime.now()
    nowstring = ""
    nowstring += str(rightnow.year) + "_"
    nowstring += str(rightnow.month) + "_"
    nowstring += str(rightnow.day) + "___"
    nowstring += str(rightnow.hour) + "_"
    nowstring += str(rightnow.minute) + "_"
    nowstring += str(rightnow.second)
    
    # Move to the working folder
    if not os.path.exists(FOLDER_WORKING):
        os.makedirs(FOLDER_WORKING)
    os.chdir(FOLDER_WORKING)
    
    shutil.copyfile(MCNP_SRC, TMP_MCNP)
    
    #p# Create folder
    #folder_base = FOLDER_ROOT + "/adv_" + nowstring
    advfilename = TMP_ADV
    
    # Create file
    rewrite_advtg(ADV_SRC, advfilename, indiv.x, indiv.y, indiv.z)
    
    # Run ADVANTG
    cmd = "../advrun.sh " + TMP_ADV  # ex1_tmp_adv.adv"
    adv_start = time.time() 
    subprocess.call(cmd.split())
    adv_stop = time.time()
    adv_elapsed = (adv_stop - adv_start)/60.0
    print("ADVANTG time elapsed: " + str(adv_elapsed))
    
    # Move to the output folder, run MCNP, and move back to current folder
    os.chdir("output")
    mcnp_start = time.time() 
    cmd = "../../mcnprun.sh inp"
    subprocess.call(cmd.split())
    mcnp_stop = time.time()
    mcnp_elapsed = (mcnp_stop - mcnp_start)/60.0
    print("MCNP time elapsed: " + str(mcnp_elapsed))
    
    fit_funct = parse_mcnp_out(FOLDER_WORKING + "/output/oua.out")
    v = numpy.array([f[0] for f in fit_funct])
    u = numpy.array([f[1] for f in fit_funct])
    
    #fom = 1.0/((adv_elapsed + mcnp_elapsed) * u**2)
    #print("FOM array [min^-1]: " + str(fom))
    
    fitness = phasetree.PhaseFitness()
    fitness.v = v
    fitness.u = u
    #fitness.fom = fom
    fitness.mcnp_t = mcnp_elapsed
    fitness.adv_t = adv_elapsed
    fitness.calc_fom()
    
    os.chdir("..")
    
    # Copy MCNP
    
    # cd into the folder
    return fitness
    
    
def eval_co_fitness(indiv_x, indiv_y, indiv_z):
    #p# Create folder
    folder_base = FOLDER_WORKING #+ "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
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
    
    
def parse_mcnp_out(mcnp_out_filename):
    print("Parsing MCNP results in: " + mcnp_out_filename)
    
    tallydata = []
    
    if not os.path.isfile(mcnp_out_filename):
        raise Exception('The file "' + str(mcnp_out_filename) + '" does not exist!')
        
    with open(mcnp_out_filename) as f:
        lines = f.readlines()
        
        for i in range(len(lines)):
            if lines[i].startswith("1tally  "):
                tokens = lines[i+9].split()
                print("tokens = " + str(tokens))
                v = float(tokens[0])
                u = float(tokens[1])
                tallydata.append((v,u))
                
    return tallydata
    
    
def parse_mcnp_mesh(mcnp_out_filename):
    print("Parsing MCNP results: " + mcnp_out_filename)
    
    if not os.path.isfile(mcnp_out_filename):
        raise Exception('The file "' + str(mcnp_out_filename) + '" does not exist!')
    with open(mcnp_out_filename) as f:
        lines = f.readlines()
        #cline = 2
        
        f.next()
        f.next()
        nps = int(f.next()[-1])
        if nps == 0:
            raise Exception('The file "' + str(mcnp_out_filename) + '" does not track any particles!')
        
        datas = []
        nextdata = meshtaldata.MeshtalData()
        while parseNextTally(nextdata, f):
            datas.append(nextdata)
            nextdata = meshtaldata.MeshtalData()
            
    
    time.sleep(2.0)


def parseNextTally(data, file):
    
    # Check to see if EOF is reached

    data.tally_num = float(file.next().split()[-1])
    if data.tally_num == 0:
        return False
        
    line = file.next()
    if line.startswith("    "):  # Then a comment
        data.particle_type = file.next().split()[0]
    else:
        data.particle_type = line.split()[0]
        
    if data.particle_type != "neutron" and data.particle_type != "photon" and data.particle_type != "electron":
        raise Exception('Illegal particle type: ' + str(data.particle_type))
        
    line = file.next()
    if line.trim().empty():
        file.next()
    file.next()

    xtokens = file.next().split()
    data.x = [float(x) for x in xtokens[2:]]
    
    ytokens = file.next().split()
    data.y = [float(y) for y in ytokens[2:]]
    
    ztokens = file.next().split()
    data.z = [float(z) for z in ztokens[2:]]
    
    etokens = file.next().split()
    data.e = [float(e) for e in etokens[3:]]

    tallysize = (len(data.x)-1) * (len(data.y)-1) * (len(data.z)-1) * (len(data.e)-1)
    data.v = numpy.zeros((tallysize, 1))
    data.u = numpy.zeros((tallysize, 1))
    
    file.next()
    file.next()
    
    if data.particle_type == "photon" or len(data.e) > 2:
        for i in range(tallysize):
            tokens = file.next().split()
            if len(tokens) < 4:
                raise Exception('Tally line ' + str(i) + ' was too short!')
                
            data.v[i] = float(tokens[4])
            data.u[i] = float(tokens[5])
    else:
        for i in range(tallysize):
            tokens = file.next().split()
            if len(tokens) < 5:
                raise Exception('Tally line ' + str(i) + ' was too short!')
                
            data.v[i] = float(tokens[3])
            data.u[i] = float(tokens[4])

    file.next()
    
    return True







