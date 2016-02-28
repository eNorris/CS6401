import random
import numpy

class PhaseTreeException(Exception):
    pass

class PhaseTree(object):
    
    def __init__(self):
        self.nodes = []
        self.type = None
        
    def __cmp__(self, rhs):
        if self.right_bound () < rhs.left_bound():
            return -1
        if self.left_bound() > rhs.right_bound():
            return 1
        raise PhaseTreeException('PhaseTreeException::__cmp__(self, rhs): failed')
        
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
        return None
        
        
    def randomize_uniform(self, n_max):
        self.nodes = []
        
        if n_max < 1:
            raise PhaseTreeException("PhaseTreeException::randomize_uniform(self): n_max < 1")
        segments = random.randint(1, n_max+1)
        
        segment_pts = numpy.linspace(0, 1.0, segments+1)
        
        for pt in segment_pts:
            self.nodes.append(pt)
        
        
    #def randomize(self):
        
        
        
        
        
        