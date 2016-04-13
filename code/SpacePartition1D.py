
class SpacePartition1D(object):

    def __init__(self):
        self.bounds = [0, 1]
        self.relBins = []

    def abs_bins(self):
        self.validate()

        mult = self.bounds[1] - self.bounds[0]
        addr = self.bounds[0]

        absBins = [self.bounds[0]]
        absBins.extend([mult * bbin + addr for bbin in self.relBins])
        absBins.append(self.bounds[1])

        return absBins

    def validate(self):
        if len(self.bounds) != 2:
            raise Exception('The bounds is still empty')

        if self.bounds[1] - self.bounds[0] <= 0:
            raise Exception('The bin boundaries are identical or backwards')

        if len(self.relBins) > 0:
            if self.relBins[0] <= 0:
                raise Exception('The lowest bin is < 0')
            if(self.relBins[-1] >= 1):
                raise Exception('The highest bin is > 1')

        for i in range(len(self.relBins)-1):
            if self.relBins[i+1] <= self.relBins[i]:
                raise Exception('Bin ' + str(i+1) + ' is less than or equal to bin ' + str(i))

    def __len__(self):
        return len(self.bounds) + len(self.relBins) - 1

    def __repr__(self):
        return str(self.abs_bins())
