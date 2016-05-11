import matplotlib
import matplotlib.pyplot as pyplot
import re
import numpy

#logfilename = "logfile_2016_5_8_10_19.log"
logfilename = "logfile_2016_5_7_14_28.log"

file = open(logfilename, 'r')

linecount = 0

evallist = []
timelist = []
xlist = []
ylist = []
zlist = []
timelist = []
xcountlist = []
ycountlist = []
zcountlist = []
fomlist = []

for line in file:
    #print(linecount)
    if linecount % 5 == 0:
        tokens = line.split()
        evallist.append(int(tokens[1]))
    elif linecount % 5 == 1:
        xlist.append(line)
        xcountlist.append(len(line.split()) - 1)
    elif linecount % 5 == 2:
        ylist.append(line)
        ycountlist.append(len(line.split()) - 1)
    elif linecount % 5 == 3:
        zlist.append(line)
        zcountlist.append(len(line.split()) - 1)
    elif linecount % 5 == 4:
        tokens = line.split()
        fomlist.append(float(tokens[1]))
        if tokens[1] == "0":
            timelist.append(0.0)
        else:
            ts = tokens[5]
            ts2 = re.search('\(.*\)', ts)
            ts2 = ts2.group(0)
            tmcnp, tadv = ts2.split('+')
            #print(tmcnp)
            #print(tmcnp[1:])
            #print(tadv)
            #print(tadv[:-1])
            timelist.append(float(tmcnp[1:]) + float(tadv[:-1]))
    linecount += 1

fulllines = len(fomlist)

evallist = evallist[:fulllines]
xlist = xlist[:fulllines]
ylist = ylist[:fulllines]
zlist = zlist[:fulllines]
timelist = timelist[:fulllines]
xcountlist = xcountlist[:fulllines]
ycountlist = ycountlist[:fulllines]
zcountlist = zcountlist[:fulllines]
fomlist = fomlist[:fulllines]

pyplot.figure()
pyplot.plot(evallist, fomlist)
pyplot.title('Fitness')
pyplot.xlabel('Evaluation')
pyplot.ylabel('FOM [min^-1]')

pyplot.figure()
pyplot.plot(evallist, xcountlist)
pyplot.title('X Node Count')
pyplot.xlabel('Evaluation')
pyplot.ylabel('Nodes [#]')

pyplot.figure()
pyplot.plot(evallist, ycountlist)
pyplot.title('Y Node Count')
pyplot.xlabel('Evaluation')
pyplot.ylabel('Nodes [#]')

pyplot.figure()
pyplot.plot(evallist, zcountlist)
pyplot.title('Z Node Count')
pyplot.xlabel('Evaluation')
pyplot.ylabel('Nodes [#]')

pyplot.figure()
voxel_count = [xc*yc*zc for xc, yc, zc in zip(xcountlist, ycountlist, zcountlist)]
tpv = [t/v for t, v in zip(timelist, voxel_count)]
pyplot.scatter(voxel_count, tpv, c='k', alpha=.1)
pyplot.ylim(0, 1.01*max(tpv))
pyplot.title('Time per voxel')
pyplot.xlabel('Voxel Count')
pyplot.ylabel('Evaluation Time / Voxel [min]')

pyplot.figure()
voxel_count = [xc*yc*zc for xc, yc, zc in zip(xcountlist, ycountlist, zcountlist)]
tpv = [t/v for t, v in zip(timelist, voxel_count)]
pyplot.scatter(voxel_count, timelist, c='k', alpha=.1)
pyplot.ylim(0, 1.01*max(timelist))
pyplot.title('Runtime')
pyplot.xlabel('Voxel Count')
pyplot.ylabel('Evaluation Time [min]')

evaln = numpy.array(evallist)
timen = numpy.array(timelist)

v = (timen > .01)
evaln = evaln[v]
timen = timen[v]
voxn = numpy.array(voxel_count)[v]
tpv2 = timen / voxn
print(timen)

pyplot.figure()
pyplot.plot(evaln, timen)
pyplot.ylim(0, 1.01*max(timen))
pyplot.title('Runtime')
pyplot.xlabel('Evaluation')
pyplot.ylabel('Evaluation Time [min]')

pyplot.figure()
pyplot.plot(evaln, tpv2)
pyplot.ylim(0, 1.01*max(tpv2))
pyplot.title('Runtime per Voxel')
pyplot.xlabel('Evaluation')
pyplot.ylabel('Evaluation Time / Voxel [min]')

pyplot.show()