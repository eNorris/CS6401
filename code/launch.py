
ADV_SRC = '/media/data/x.dne'

FOLDER_ROOT = '/media/data/'
FILEEXT = '.dne'

xs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
ys = [10]
zs = [10]

for x in xs:
    for y in ys:
        for z in zs:
            #new_filename = FOLDER_ROOT + "_" + str(x) + "_" + str(y) + "_" + str(z) + FILEEXT
            
            # Create folder
            folder_base = FOLDER_ROOT + "xyz_" + str(x) + "_" + str(y) + "_" + str(z) + "/"
            filename = folder_base + "adv_ea.adv"
            # Create file
            
            write_advtg(filename, x, y, z)
            
            # Copy MCNP
            
            # cd into the folder