# used for MCST

from math import inf, sqrt, log


class Node(object):
    def __init__(self, data, turn, parent=None, children=None, wins=0, num_rollout=0):
        self.data = data
        self.turn = turn
        self.wins = wins
        self.num_rollout = num_rollout
        self.uct = float(inf)
        self.parent = parent
        self.children = children

    def calc_uct(self, total):
        if self.num_rollout == 0:
            self.uct = float(inf)
        self.uct = self.wins/self.num_rollout + 1.5 * (sqrt(log(total) / self.num_rollout))
