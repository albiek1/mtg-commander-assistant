import random
import math

deck_size = 99

class Card():
    def __init__(self, cost, effect):
        self.cost = cost
        self.effect = effect

    def __repr__(self):
        return (("Card: %r, %r") % (self.cost, self.effect))

deck = []
hand = []

#def draw_hand(deck):

#this is the hypergeometric probaility calculations
def calc_perm(n, r):
    return math.factorial(n)/math.factorial(n-r)

def calc_combi(n, r):
    return calc_perm(n, r)/math.factorial(r)

def hyper_calc(N, k, n, x):
    #N = deck size
    #k = amount of ramp/lands
    #n = draw cards
    #x = amount of ramp/lands we want in hand
    return calc_combi(k, x)*calc_combi((N-k), (n-x))/calc_combi(N, n)

def hyper_calc_fin(N, k, n, x):
    result = 0.0
    for i in range(x, n):
        result += hyper_calc(N, k, n, i)
    return result

def fix_ratios(m, g, t):
    #we want g chance at m mana by t turn
    N = 99
    k1 = 14
    n = t
        