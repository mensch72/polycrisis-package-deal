"""Phase 0, second instance: 3 actors, 2 issues, 9 levers. Built to have contested levers and an empty core.

Issue "access": each actor can grant each of the other two preferential access to markets, technology
or critical minerals (a linkage currency in the plan, WP2). A grant costs the giver, benefits the
receiver and diverts trade from the third actor. The lever is therefore contested: it fails the
orientation test for the third actor. Issue "climate" is the aggregate-effort game of the first instance.

All utilities are in each actor's OWN units. Only the emission shares are sourced. Every other number
is illustrative and was chosen by scanning a few values so that (i) the access issue alone has an empty
core, (ii) the climate issue alone has a core, (iii) the package has an empty core, and (iv) no lever
pays for itself, so that the reference a0 is a Nash point. See PROVENANCE.

The module offers the same names as instance.py, so that mechanism.py and search.py can run on it.
"""
import numpy as np

ACTORS = ['USA', 'CHN', 'EU']
N = len(ACTORS)
ACTOR_INFO = {'USA': dict(name='United States'), 'CHN': dict(name='China'), 'EU': dict(name='European Union')}

# (actor, lever, number of levels, issue); access_X = preferential access granted to X
LEVERS = [
    ('USA', 'access_CHN', 3, 'access'), ('USA', 'access_EU', 3, 'access'), ('USA', 'climate', 4, 'climate'),
    ('CHN', 'access_EU', 3, 'access'), ('CHN', 'access_USA', 3, 'access'), ('CHN', 'climate', 4, 'climate'),
    ('EU', 'access_USA', 3, 'access'), ('EU', 'access_CHN', 3, 'access'), ('EU', 'climate', 4, 'climate'),
]
ISSUES = ['access', 'climate']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
ISSUE_OF = [iss for (_, _, _, iss) in LEVERS]
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
TOP = np.array(SHAPE) - 1
NPROF = int(np.prod(SHAPE))

BASE = {
    # emission shares: EDGAR 2026 report, GHG excl. LULUCF, year 2025 (sourced)
    'e.USA': .1111, 'e.CHN': .2951, 'e.EU': .0578,
    # climate: benefit weight d_i per unit of Q, cost k_i * level^2
    'd.USA': .70, 'd.CHN': .65, 'd.EU': 1.00,
    'k.USA': .10, 'k.CHN': .20, 'k.EU': .10,
    # access: per level granted, benefit b to the receiver, cost g to the giver, harm h to the third actor
    'b': .30, 'g': .10, 'h': .18,
    # aspirations: budget on own cost; red line on access levels exchanged between the other two
    'B.USA': .60, 'B.CHN': .90, 'B.EU': .60,
    'X.USA': 2, 'X.CHN': 2, 'X.EU': 2,
}
PROVENANCE = {
    'e.': dict(status='sourced', source='EDGAR 2026 report, total GHG excl. LULUCF, year 2025',
               url='https://edgar.jrc.ec.europa.eu/report_2026', retrieved='2026-11-10'),
    'default': dict(status='illustrative', source='chosen by the team for the second toy instance, after a scan '
                    'of d in three settings and h in {0.12, 0.15, 0.18, 0.25}; d.CHN lowered from 0.90 to 0.65 for (iv)', who_says='Claude',
                    retrieved='2026-11-10'),
}


def grids(shape=SHAPE):
    return [np.arange(n).reshape([n if j == d else 1 for j in range(len(shape))])
            for d, n in enumerate(shape)]


def lever_index(actor, lever):
    return [d for d, (a, l, _, _) in enumerate(LEVERS) if a == actor and l == lever][0]


def evaluate(p=BASE, light=False):
    """Evaluate the whole profile grid: U (N, *SHAPE), acc (N, *SHAPE), and unless light the indicators
    Q (abatement) and T (access levels granted in total), costs, named aspirations and slack."""
    g = grids()
    Q = sum(p['e.' + a] * g[lever_index(a, 'climate')] for a in ACTORS)
    T = sum(g[d] for d in range(D) if ISSUE_OF[d] == 'access')
    U = np.empty((N,) + SHAPE)
    cost, asp = {}, {}
    acc = np.ones((N,) + SHAPE, bool)
    t = 1e-9
    for i, a in enumerate(ACTORS):
        o1, o2 = [x for x in ACTORS if x != a]
        given = g[lever_index(a, 'access_' + o1)] + g[lever_index(a, 'access_' + o2)]
        got = g[lever_index(o1, 'access_' + a)] + g[lever_index(o2, 'access_' + a)]
        between = g[lever_index(o1, 'access_' + o2)] + g[lever_index(o2, 'access_' + o1)]
        cost[a] = p['k.' + a] * g[lever_index(a, 'climate')] ** 2 + p['g'] * given
        U[i] = p['d.' + a] * Q + p['b'] * got - p['h'] * between - cost[a]
        asp[a] = [('own cost within budget', cost[a] <= p['B.' + a] + t, (p['B.' + a] - cost[a]) / p['B.' + a]),
                  ('access between the other two within red line', between <= p['X.' + a], None)]
        for (_, m, _) in asp[a]:
            acc[i] &= m
    out = dict(U=U, acc=acc)
    if not light:
        slack = np.full(SHAPE, np.inf)
        for a in ACTORS:
            for (_, _, s) in asp[a]:
                if s is not None:
                    slack = np.minimum(slack, s)
        out.update(Q=np.broadcast_to(Q, SHAPE), T=np.broadcast_to(T, SHAPE),
                   cost={a: np.broadcast_to(c, SHAPE) for a, c in cost.items()}, asp=asp, slack=slack)
    return out


def describe(a):
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}
