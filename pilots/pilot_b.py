"""Pilot B skeleton: conditional safety commitments among frontier AI developers.

Five stylised developers, not named companies: A and B stand for the two developers with the most detailed
published safety frameworks, C and D for two further frontier developers, E for a developer that releases
model weights openly. Each has two levers on top of what it does today (level 0 = current framework):
  safeguards: tier 0 to 3 of security and deployment safeguards tied to capability thresholds;
  access: tier 0 to 2 of access for external evaluators before deployment.

ALL preference and cost numbers are ILLUSTRATIVE, set by Claude on 10 November 2026 before the first run,
and are exactly what people who know the developers would have to correct. Structure assumed:
  - the industry-wide risk reduction X has a weakest-link part, an average part and an access part;
  - a tier costs its owner quadratically, access linearly;
  - a developer loses KAPPA per tier that it stands above the average of its rivals, and gains when below;
  - aspirations: a cost budget, and for A to D the red line "at most one tier above the least strict of
    the other three", which mirrors the adjustment clauses in published frameworks (see docs/pilot_B_frontier_ai.md).
CHAIN: the two leading developers first, then all five.
"""
import numpy as np

ACTORS = ['A', 'B', 'C', 'D', 'E']
N = len(ACTORS)
ACTOR_INFO = {'A': 'Developer A (leading, detailed framework)', 'B': 'Developer B (leading, detailed framework)',
              'C': 'Developer C (frontier)', 'D': 'Developer D (frontier)', 'E': 'Developer E (open weights)'}
LEVERS = [(a, lev, n, 'ai') for a in ACTORS for lev, n in (('safeguards', 4), ('access', 3))]
ISSUES = ['ai']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
CHAIN = [['A', 'B'], ['A', 'B', 'C', 'D', 'E']]
INDICATORS = ['X', 'smin']
LEVER_TEXT = {'safeguards': 'apply safeguard tier {v} of 3 above its current framework',
              'access': 'give external evaluators access at tier {v} of 2 before deployment'}

BASE = {
    'w.min': .40, 'w.avg': .35, 'w.acc': .25,                       # effect model of X
    'al.A': 1.2, 'al.B': 1.2, 'al.C': .9, 'al.D': .9, 'al.E': .6,   # value of X to each developer
    'k.A': .10, 'k.B': .10, 'k.C': .12, 'k.D': .12, 'k.E': .15,     # cost of a safeguard tier: k * tier^2
    'tau.A': .06, 'tau.B': .06, 'tau.C': .08, 'tau.D': .08, 'tau.E': .10,   # cost per access tier
    'kap.A': .12, 'kap.B': .12, 'kap.C': .12, 'kap.D': .12, 'kap.E': .06,   # positional cost per tier ahead
    'B.A': .95, 'B.B': .95, 'B.C': .60, 'B.D': .60, 'B.E': .45,     # cost budgets
    'gap': 1,                                                       # red line: tiers above the least strict rival
}
PROVENANCE = {'default': dict(status='illustrative', source='set by Claude before the first run; to be corrected by '
                              'people who know the developers', who_says='Claude', retrieved='2026-11-10')}
PERTURB = [k for k in BASE if k.split('.')[0] in ('al', 'k', 'tau', 'kap')]
TIPPING = [k for k in BASE if k != 'gap']          # every illustrative number, one at a time


def grids():
    return [np.arange(n).reshape([n if j == d else 1 for j in range(D)]) for d, n in enumerate(SHAPE)]


def evaluate(p=BASE, light=False):
    g = grids()
    s = [g[2 * i] for i in range(N)]
    t = [g[2 * i + 1] for i in range(N)]
    smin = np.minimum.reduce(np.broadcast_arrays(*s))
    X = p['w.min'] * smin / 3 + p['w.avg'] * sum(s) / (3 * N) + p['w.acc'] * sum(t) / (2 * N)
    U = np.empty((N,) + SHAPE)
    acc = np.ones((N,) + SHAPE, bool)
    for i, a in enumerate(ACTORS):
        rivals = sum(s[j] for j in range(N) if j != i) / (N - 1)
        cost = p['k.' + a] * s[i] ** 2 + p['tau.' + a] * t[i]
        U[i] = p['al.' + a] * X - cost - p['kap.' + a] * (s[i] - rivals)
        acc[i] &= cost <= p['B.' + a] + 1e-9
        if a != 'E':
            others = [s[j] for j, b in enumerate(ACTORS) if b not in (a, 'E')]
            acc[i] &= s[i] <= p['gap'] + np.minimum.reduce(np.broadcast_arrays(*others))
    return dict(U=U, acc=acc, X=np.broadcast_to(X, SHAPE), smin=np.broadcast_to(smin, SHAPE))


def describe(a):
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}


def lever_sentence(d, v):
    return LEVER_TEXT[LEVERS[d][1]].format(v=v)
