import random
import numpy

class PhaseTreeException(Exception):
    pass

class PhaseTree(object):
    
    def __init__(self):
        self.nodes = []
        self.type = None
        self.dim_min = None
        self.dim_max = None
        
    def __cmp__(self, rhs):
        if self.right_bound () < rhs.left_bound():
            return -1
        if self.left_bound() > rhs.right_bound():
            return 1
        raise PhaseTreeException('PhaseTreeException::__cmp__(self, rhs): failed')
        
    def __repr__(self):
        return "[" + ", ".join([repr(node) for node in self.nodes]) + "]"
        #s = "["
        #
        #s += ", ".join([repr(node) for node in self.nodes])
        #for node in self.nodes:
        #    if type(node) is PhaseTree:
        #        s += repr(node)  #node.__repr__()
        #    s += str(node)
        #s += "]"
        #return s
        
    def to_list(self):
        sol = []
        
        for node in self.nodes:
            if type(node) is PhaseTree:
                sol.append(node.to_list())
            else:
                sol.append(node)
        
        return sol
        
    def left_bound(self):
        leftnode = self.nodes[0]
        if type(leftnode) is PhaseTree:
            return leftnode.left_bound()
        else:
            return leftnode
            
    def right_bound(self):
        rightnode = self.nodes[-1]
        if type(rightnode) is PhaseTree:
            return rightnode.right_bound()
        else:
            return rightnode
            
    def is_valid(self):
        #for (i,node) in enumerate(self.nodes):
        for i in range(len(self.nodes)-1):
            if type(self.nodes[i]) is PhaseTree:
                if not self.nodes[i].is_valid():
                    return False
            if self.nodes[i] >= self.nodes[i+1]:
                return False
        return True
            
            
    def uniform_expand(self, expval):
        raise NotImplementedError('uniform_expand is not written yet')
        
        
    def randomize_uniform(self, n_max):
        self.nodes = []
        
        if n_max < 5:
            raise PhaseTreeException("PhaseTreeException::randomize_uniform(self): n_max < 1")
        segments = random.randint(5, n_max+1)
        
        segment_pts = numpy.linspace(0, 1.0, segments+1)
        
        for pt in segment_pts:
            self.nodes.append(pt)
            
    def set_uniform(self, segments):
        self.nodes = []
        segment_pts = numpy.linspace(0.0, 1.0, segments+1)
        
        for pt in segment_pts:
            self.nodes.append(pt)
            
    def node_count(self):
        c = 0
        for n in self.nodes:
            if type(n) is PhaseTree:
                c += c.node_count()
            else:
                c += 1
        return c
                
    def get_mesh(self):
        return str(" ".join([str(self.automap_to(x)) for x in self.to_list()]))
        
        
    def get_mesh_ints(self):
        return str(" ".join([str(x) for x in [1]*(self.node_count()-1)]))
        
        
    def map_to(self, x, xmin, xmax):
        return x * (xmax - xmin) + xmin
        
        
    def automap_to(self, x):
        if self.dim_min is None or self.dim_max is None:
            raise PhaseTreeException('PhaseTree::automap_to(self, x): min/max dim was not set')
        return self.map_to(x, self.dim_min, self.dim_max)
        

        
        
class SingletonPhaseSpace(object):
    def __init__(self):
        self.x = PhaseTree()
        self.y = PhaseTree()
        self.z = PhaseTree()
        
        self.x.dim_min = 0  #-208.3575
        self.x.dim_max = 150  #213.12
        
        self.y.dim_min = 0  #-204.865
        self.y.dim_max = 100  #378.5375
        
        self.z.dim_min = 0  #-84.215
        self.z.dim_max = 100  #224.55
        
    def __repr__(self):
        return str(self.x) + str(self.y) + str(self.z)
        
    def randomize_uniform(self, xmax, ymax, zmax):
        self.x.randomize_uniform(xmax)
        self.y.randomize_uniform(ymax)
        self.z.randomize_uniform(zmax)
        return
        
        
    def set_uniform_x(self, xbins):
        self.x.set_uniform(xbins)
        
        
    def set_uniform_y(self, ybins):
        self.y.set_uniform(ybins)
        
        
    def set_uniform_z(self, zbins):
        self.z.set_uniform(zbins)
        
        
class PhaseFitness(object):
    def __init__(self):
        self.v = []
        self.u = []
        self.fom = []
        self.fomavg = None
        self.adv_t = -1
        self.mcnp_t = -1
        
    def __repr__(self):
        return str(self.fom) + " = 1/(" + str(self.mcnp_t) + "+" + str(self.adv_t) + ")(" + str(self.u) + ")^2"

    def avg_unc(self):
        return sum(self.u)/float(len(self.u))

    def detail_string(self):
        return str(self.fomavg) + " " + str(self.fom) + " = 1/(" + str(self.mcnp_t) + "+" + str(self.adv_t) + ")(" + str(self.u) + ")^2"
        
    def calc_fom(self):
        if self.adv_t <= 0 or self.mcnp_t <= 0 or len(self.u) == 0:
            raise Exception('Either an illegal time or u length was encountered')

        t = numpy.copy(self.u)
        t[t == 0.0] = numpy.inf
        self.fom = 1.0/((self.adv_t + self.mcnp_t) * t**2)

        self.fomavg = numpy.mean(self.fom)
        
        
        