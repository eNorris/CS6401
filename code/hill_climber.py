import phasetree
import pyadvantg
import numpy
import time
import matplotlib.pyplot as pyplot

INIT_POP_SIZE = 5
    
def do_terminate():
    return True
    
    
xsteps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
ysteps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
zsteps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]

x = -1
y = 5
z = 5

bestfit = -numpy.inf
bestind = None

xfits = []
xindivs = []
yfits = []
yindivs = []
zfits = []
zindivs = []

start = time.time()

bestfit = -numpy.inf
for z in zsteps:
    indiv = phasetree.SingletonPhaseSpace()
    indiv.x.set_uniform(5)
    indiv.y.set_uniform(5)
    indiv.z.set_uniform(z)
    
    fit = pyadvantg.eval_fitness(indiv)
    
    zfits.append(fit)
    zindivs.append(indiv)
    
    if sum(fit.fom) > bestfit:
        bestfit = sum(fit.fom)
        bestind = indiv
        
bestz = bestind.z.node_count()-1
print("Best z: " + str(bestz))

    
bestfit = -numpy.inf
for y in ysteps:
    indiv = phasetree.SingletonPhaseSpace()
    indiv.x.set_uniform(5)
    indiv.y.set_uniform(y)
    indiv.z.set_uniform(bestz)
    
    fit = pyadvantg.eval_fitness(indiv)
    
    yfits.append(fit)
    yindivs.append(indiv)
    
    if sum(fit.fom) > bestfit:
        bestfit = sum(fit.fom)
        bestind = indiv
        
besty = bestind.y.node_count()-1
print("Best y: " + str(besty))

for x in xsteps:
    indiv = phasetree.SingletonPhaseSpace()
    indiv.x.set_uniform(x)
    indiv.y.set_uniform(besty)
    indiv.z.set_uniform(bestz)
    
    fit = pyadvantg.eval_fitness(indiv)
    
    xfits.append(fit)
    xindivs.append(indiv)
    
    #print("fits: " + str(fit))
    #raise Exception("FUCK PYTHON!")
    
    if sum(fit.fom) > bestfit:
        bestfit = sum(fit.fom)
        bestind = indiv
        
bestx = bestind.x.node_count()-1

print("Best x: " + str(bestx))
print("Best y: " + str(besty))
print("Best z: " + str(bestz))
print("Best fit: " + str(bestfit))

stop = time.time()
elapsed = stop - start
print("Total time: " + str(elapsed) + " [sec]")

pyplot.plot(numpy.linspace(1,len(xsteps), len(xsteps)), [sum(fit.fom) for fit in xfits], 'b',
            numpy.linspace(1+len(xsteps), 1+len(xsteps)+len(ysteps), len(ysteps)), [sum(fit.fom) for fit in yfits], 'r', 
            numpy.linspace(2+len(xsteps)+len(ysteps), 2+len(xsteps)+len(ysteps)+len(zsteps), len(zsteps)), [sum(fit.fom) for fit in zfits], 'g')
pyplot.title('Fitness')
pyplot.xlabel('Evaluation')
pyplot.ylabel('FOM [min^{-1}]')
pyplot.show()