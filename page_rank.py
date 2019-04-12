# PageRank algorithm
# By Peter Bengtsson
#    http://www.peterbe.com/
#    mail@peterbe.com
# License: BSD,http://opensource.org/licenses/bsd-license.php
#
# Requires the numpy module
# http://numpy.scipy.org/

from numpy import *
import numpy.linalg as la
from functools import reduce


def _sum_sequence(seq):
    """ sums up a sequence """

    def _add(x, y): return x + y

    return reduce(_add, seq, 0)


class PageRanker:
    def __init__(self, p, webmatrix):
        assert p >= 0 and p <= 1
        self.p = float(p)
        if type(webmatrix) in [type([]), type(())]:
            webmatrix = array(webmatrix)
        assert webmatrix.shape[0] == webmatrix.shape[1]
        self.webmatrix = webmatrix

        # create the deltamatrix
        imatrix = identity(webmatrix.shape[0])
        for i in range(webmatrix.shape[0]):
            imatrix[i] = imatrix[i] * sum(webmatrix[i, :])
        deltamatrix = la.inv(imatrix)
        self.deltamatrix = deltamatrix

        # create the fmatrix
        self.fmatrix = ones(webmatrix.shape)

        self.sigma = webmatrix.shape[0]

        # calculate the Stochastic matrix
        _f_normalized = (self.sigma ** -1) * self.fmatrix
        _randmatrix = (1 - p) * _f_normalized

        _linkedmatrix = p * dot(deltamatrix, webmatrix)

        M = _randmatrix + _linkedmatrix

        self.stochasticmatrix = M

        self.invariantmeasure = ones((1, webmatrix.shape[0]))

    def improve_guess(self, times=1):
        for i in range(times):
            self._improve()

    def _improve(self):
        self.invariantmeasure = dot(self.invariantmeasure, self.stochasticmatrix)

    def get_invariant_measure(self):
        return self.invariantmeasure

    def getPageRank(self):
        sum = _sum_sequence(self.invariantmeasure[0])
        copy = self.invariantmeasure[0]
        for i in range(len(copy)):
            copy[i] = copy[i] / sum
        return copy


if __name__ == '__main__':
    # Example usage
    web = ((0, 1, 1, 1),
           (1, 0, 1, 1),
           (1, 1, 0, 1),
           (1, 1, 1, 0))

    #  tutorial exercise
    web = ((0, 1, 0),
            (1, 0, 1),
            (1, 0, 0))

    pr = PageRanker(0.85, web)

    pr.improve_guess(100)
    print (pr.getPageRank())

