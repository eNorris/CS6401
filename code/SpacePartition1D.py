
class SpacePartition1D(object):

    def __init__(self):
        self.bounds = []
        self.relBins = []

    def abs_bins(self):
        self.validate()

        mult = self.bounds[1] - self.bounds[0]
        addr = self.bounds[0]

        return [mult * bbin + addr for bbin in self.relBins]

    def validate(self):
        if len(self.bounds) != 2:
            raise Exception('The bounds is still empty')

        if not len(self.relBins) >= 2:
            raise Exception('There is no data in self.bins')

        if self.relBins[0] != 0:
            raise Exception('The first element is corrupt, it should be 0')

        if self.relBins[-1] != 1:
            raise Exception('The last element is corrupt, it should be 1')

        if self.bounds[1] - self.bounds[0] <= 0:
            raise Exception('The bin boundaries are identical or backwards')