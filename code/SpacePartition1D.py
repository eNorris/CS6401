
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

    def get_mesh(self):
        msh = ""
        for mbin in self.abs_bins():
            msh += str(mbin) + " "
        return msh

    def get_mesh_ints(self):
        msh = ""
        for i in range(len(self.relBins)+1):
            msh += "1 "
        return msh

    def get_bin_count(self):
        return len(self.relBins) + 1

    def set_range(self, range_min, range_max):
        self.bounds = [range_min, range_max]

    def validate(self):
        if len(self.bounds) != 2:
            raise Exception('The bounds is still empty')

        if self.bounds[1] - self.bounds[0] <= 0:
            raise Exception('The bin boundaries are identical or backwards')

        if len(self.relBins) > 0:
            if self.relBins[0] <= 0:
                raise Exception('The lowest bin is < 0')
            if self.relBins[-1] >= 1:
                raise Exception('The highest bin is > 1')

        for i in range(len(self.relBins)-1):
            if self.relBins[i+1] <= self.relBins[i]:
                raise Exception('Bin ' + str(i+1) + ' is less than or equal to bin ' + str(i))

    def __len__(self):
        return len(self.bounds) + len(self.relBins) - 1

    def __repr__(self):
        return str(self.abs_bins())

    def diff(self, other, normalizing=False):
        my_index = 0
        other_index = 0
        last_val = 0
        # current_index = 0
        # current_bins = None
        # who = 0
        exhausted = False
        total_diff = 0

        while not exhausted:

            if my_index >= len(self.relBins) or other_index >= len(other.relBins):
                exhausted = True
                continue

            if self.relBins[my_index] < other.relBins[other_index]:
                current_bins = self.relBins
                current_index = my_index
            else:
                current_bins = other.relBins
                current_index = other_index

            dx = current_bins[current_index] - last_val
            if normalizing:
                myPMF = 1/((self.relBins[my_index] - self.relBins[my_index-1])*(len(self.relBins)+1))
                otherPMF = 1/((other.relBins[other_index] - other.relBins[other_index-1])*(len(other.relBins)+1))
            else:
                myPMF = 1/(self.relBins[my_index] - self.relBins[my_index-1])
                otherPMF = 1/(other.relBins[other_index] - other.relBins[other_index-1])
            dPMF = abs(myPMF - otherPMF)

            total_diff += dPMF * dx

            # Update the appropriate pointer
            if self.relBins[my_index] < other.relBins[other_index]:
                my_index += 1
            else:
                other_index += 1

            last_val = current_bins[current_index]

        return total_diff


