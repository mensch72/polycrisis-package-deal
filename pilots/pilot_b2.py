"""Pilot B2 skeleton: entry into a hardwired pause of frontier AI training, as a registry of conditional
commitments among states.

Shaped on "The Feasibility of a Hardwired Pause of Frontier AI Training" (Working Group on AI Pause
Feasibility, organised by W. Fithian and W.H. Holliday; working paper, version 1.0.2, 26 October 2026,
https://hardwired-pause.ai/paper). TAKEN FROM THE REPORT: the kind of lever (training prohibition, stop of
production of training-capable chips, census, drawdown of retained training-capable stock from about 100 %
to 25 % of a breakout threshold), and the order of entry (the United States and China first, then the
states that control supply-chain chokepoints). The report studies feasibility given willingness to pause;
it does not model preferences.

ALL preference numbers are ILLUSTRATIVE, set by Claude on 10 November 2026 before the first run. They say
nothing about any government. Structure assumed: risk reduction X needs both lead states to pause, and is
made more durable by a production stop, a census and mutual drawdown; a lead state that pauses or draws
down further than its rival is exposed; a rival that keeps training while the other pauses gains G. With
G below the net value of a mutual pause the stage game is a stag hunt, above it a Prisoner's Dilemma.
The lead states' pause costs the supplier states orders, so their levers are contested: a pre-CPEP.
"""
import numpy as np

ACTORS = ['USA', 'CHN', 'SUP']
N = len(ACTORS)
ACTOR_INFO = {'USA': 'United States', 'CHN': 'China', 'SUP': 'Supplier states (chip supply-chain chokepoints)'}
LEVERS = [('USA', 'pause', 2, 'ai'), ('USA', 'drawdown', 4, 'ai'), ('CHN', 'pause', 2, 'ai'), ('CHN', 'drawdown', 4, 'ai'),
          ('SUP', 'production_stop', 2, 'ai'), ('SUP', 'census', 2, 'ai')]
ISSUES = ['ai']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
CHAIN = [['USA', 'CHN'], ACTORS]
INDICATORS = ['X']
LEVER_TEXT = {'pause': 'prohibit training beyond the threshold and stop orders for training-capable chips',
              'drawdown': 'reduce its retained training-capable stock to {pct} % of the breakout threshold',
              'production_stop': 'stop the production of training-capable chips',
              'census': 'join the census and the monitoring of fabrication'}

BASE = {
    'x.base': .5, 'x.prod': .2, 'x.census': .1, 'x.draw': .2,   # effect model of X, given a mutual pause
    'a.USA': 1.0, 'a.CHN': 1.0, 'a.SUP': .8,                    # value of X
    'f.USA': .20, 'f.CHN': .20,                                 # forgone benefit of frontier training when pausing
    'G': .20,                                                   # gain from training on while the rival pauses
    'sig': .50,                                                 # exposure when pausing alone
    'kd': .03, 'th': .15,                                       # drawdown: cost per tier, exposure per tier beyond the rival
    'r.SUP': .30, 'c.SUP': .05, 'm.SUP': .25,                   # supplier: lost revenue, census cost, orders lost to a pause
    'gap': 1,                                                   # red line: drawdown tiers beyond the rival
}
PROVENANCE = {'default': dict(status='illustrative', source='set by Claude before the first run; structure after the '
                              'hardwired-pause report, numbers invented', who_says='Claude', retrieved='2026-11-10')}
PERTURB = ['a.USA', 'a.CHN', 'a.SUP', 'f.USA', 'f.CHN', 'G', 'sig', 'kd', 'th', 'r.SUP', 'c.SUP', 'm.SUP']
TIPPING = [k for k in BASE if k != 'gap']


def grids():
    return [np.arange(n).reshape([n if j == d else 1 for j in range(D)]) for d, n in enumerate(SHAPE)]


def evaluate(p=BASE, light=False):
    pU, dU, pC, dC, prod, cen = grids()
    both = np.minimum(pU, pC)
    X = both * (p['x.base'] + p['x.prod'] * prod + p['x.census'] * cen + p['x.draw'] * np.minimum(dU, dC) / 3)
    U = np.empty((N,) + SHAPE)
    acc = np.ones((N,) + SHAPE, bool)
    for i, (me, pm, dm, po, do) in enumerate((('USA', pU, dU, pC, dC), ('CHN', pC, dC, pU, dU))):
        U[i] = (p['a.' + me] * X - p['f.' + me] * pm - p['sig'] * np.maximum(pm - po, 0) + p['G'] * np.maximum(po - pm, 0)
                - p['kd'] * dm - p['th'] * np.maximum(dm - do, 0))
        acc[i] &= (dm <= do + p['gap']) & ((dm == 0) | (pm == 1))
    U[2] = p['a.SUP'] * X - p['r.SUP'] * prod * (1 - 0.5 * both) - p['c.SUP'] * cen - p['m.SUP'] * (pU + pC) / 2
    acc[2] &= (prod == 0) | (both == 1)
    return dict(U=U, acc=acc, X=np.broadcast_to(X, SHAPE))


def describe(a):
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}


def lever_sentence(d, v):
    lev = LEVERS[d][1]
    return LEVER_TEXT[lev].format(pct={1: 75, 2: 50, 3: 25}.get(v, 100))
