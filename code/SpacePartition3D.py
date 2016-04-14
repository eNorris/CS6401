import time

__author__ = 'etnc6d'


class SpacePartition3D(object):

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        fit = -1

    def __repr__(self):
        return "fit: " + str(self.fit) + "   Dims:(" + str(len(self.x)) + ',' +  str(len(self.y)) + ',' +str(len(self.z))+ ")\n" + \
        "x: " + str(self.x) + '\n' + \
        "y: " + str(self.y) + '\n' + \
        "z: " + str(self.z)
