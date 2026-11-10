"""Pilot A skeleton: a conditional-pledge registry for a country platform, shaped on South Africa's
Just Energy Transition Partnership (JETP).

Actors: South Africa (ZAF) and the four largest members of the International Partners Group at 30 June 2026:
Germany (DEU), United Kingdom (GBR), European Union with EIB (EU), France (FRA). Denmark and the
Netherlands are left out to keep the instance small; the United States withdrew in 2025.

SOURCED (JET Project Management Unit, Quarterly Progress Report, 30 June 2026, Table 3; retrieved 10 November
2026, https://justenergytransition.co.za/wp-content/uploads/2026/11/JET-IP-Quarterly-Progress-Report-Q2-2026.pdf):
pledge totals and grant components in USD million. South Africa's 2030 range of 350 to 420 MtCO2-eq is from
https://justenergytransition.co.za/ (2021 NDC).
ILLUSTRATIVE (set by Claude on 10 November 2026, before the first run): every valuation, cost, budget and
red line, the grant-equivalent weight of loans, and the effect model. These are exactly what people with
knowledge of the partnership would have to correct. No output says anything about the real actors.

Levers. ZAF: ambition tier 0 to 3 inside its pledged 2030 range (0 = top of the range), reform tier 0 to 2
(enabling reforms). Each donor: thirds of its pledge allocated, 0 to 3.
CHAIN: South Africa with Germany and the United Kingdom first (largest pledge; chair), then all five.
"""
import numpy as np

ACTORS = ['ZAF', 'DEU', 'GBR', 'EU', 'FRA']
N = len(ACTORS)
ACTOR_INFO = {'ZAF': 'South Africa', 'DEU': 'Germany', 'GBR': 'United Kingdom', 'EU': 'European Union and EIB',
              'FRA': 'France'}
DONORS = ['DEU', 'GBR', 'EU', 'FRA']
LEVERS = [('ZAF', 'ambition', 4, 'jetp'), ('ZAF', 'reform', 3, 'jetp')] + [(d, 'finance', 4, 'jetp') for d in DONORS]
ISSUES = ['jetp']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
CHAIN = [['ZAF', 'DEU', 'GBR'], ACTORS]
INDICATORS = ['M', 'F', 'GE']

BASE = {
    # sourced: pledged total and grant component, USD million, 30 June 2026
    'S.DEU': 2898, 'S.GBR': 1875, 'S.EU': 1592, 'S.FRA': 1084,
    'G.DEU': 338, 'G.GBR': 75, 'G.EU': 264, 'G.FRA': 4,
    # illustrative from here on
    'conc': .25,                       # grant-equivalent weight of the non-grant part of a pledge
    'v.ZAF': 1.0,                      # value to ZAF of the full mitigation index M = 1
    'rho': 1.2,                        # value to ZAF of one USD billion of grant-equivalent finance
    'ca': .25, 'cr': .30,              # ZAF cost: ca * ambition^2 + cr * reform
    'w.DEU': 1.6, 'w.GBR': .9, 'w.EU': 1.0, 'w.FRA': .5,   # value to each donor of M = 1, in USD bn of own grant-equivalent
    'B.ZAF': .6,                       # ZAF: cost net of finance received must stay below this
    'GEmin': .8,                       # ZAF: no reform unless at least this much grant-equivalent finance (USD bn)
    'smax.DEU': .55, 'smax.GBR': .40, 'smax.EU': .40, 'smax.FRA': .25,   # donors: largest acceptable own share
}
PROVENANCE = {
    'S.': dict(status='sourced', source='JET PMU Quarterly Progress Report 30 June 2026, Table 3, total pledged',
               url='https://justenergytransition.co.za/wp-content/uploads/2026/11/JET-IP-Quarterly-Progress-Report-Q2-2026.pdf',
               retrieved='2026-11-10'),
    'G.': dict(status='sourced', source='same table, grants pledged', retrieved='2026-11-10'),
    'default': dict(status='illustrative', source='set by Claude before the first run; to be corrected by people '
                    'who know the partnership', who_says='Claude', retrieved='2026-11-10'),
}
PERTURB = ['v.ZAF', 'rho', 'ca', 'cr', 'w.DEU', 'w.GBR', 'w.EU', 'w.FRA']
TIPPING = [k for k in BASE if k.split('.')[0] not in ('S', 'G')]
LEVER_TEXT = {'ambition': 'hold 2030 emissions at ambition tier {v} of 3 inside its pledged range of 350 to 420 MtCO2-eq',
              'reform': 'carry out enabling reforms at tier {v} of 2'}


def grids():
    return [np.arange(n).reshape([n if j == d else 1 for j in range(D)]) for d, n in enumerate(SHAPE)]


def evaluate(p=BASE, light=False):
    g = grids()
    amb, ref = g[0], g[1]
    fin = {d: g[2 + j] for j, d in enumerate(DONORS)}
    ge_full = {d: (p['G.' + d] + p['conc'] * (p['S.' + d] - p['G.' + d])) / 1000 for d in DONORS}   # USD bn
    F = sum(p['S.' + d] / 1000 * fin[d] / 3 for d in DONORS)
    GEd = {d: ge_full[d] * fin[d] / 3 for d in DONORS}
    GE = sum(GEd.values())
    M = (amb / 3) * (0.6 + 0.2 * ref)
    U = np.empty((N,) + SHAPE)
    acc = np.ones((N,) + SHAPE, bool)
    cost = p['ca'] * amb ** 2 + p['cr'] * ref
    U[0] = p['v.ZAF'] * M + p['rho'] * GE - cost
    acc[0] &= (cost - p['rho'] * GE <= p['B.ZAF'] + 1e-9) & ((ref == 0) | (GE >= p['GEmin'] - 1e-9))
    for j, d in enumerate(DONORS):
        U[1 + j] = p['w.' + d] * M - GEd[d]
        acc[1 + j] &= (fin[d] == 0) | (GEd[d] <= p['smax.' + d] * GE + 1e-9)
    return dict(U=U, acc=acc, M=np.broadcast_to(M, SHAPE), F=np.broadcast_to(F, SHAPE), GE=np.broadcast_to(GE, SHAPE))


def describe(a):
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}


def lever_sentence(d, v):
    act, lev, _, _ = LEVERS[d]
    if lev == 'finance':
        return f"allocate {v} third{'s' if v > 1 else ''} of its pledge of USD {BASE['S.' + act]:,} million"
    return LEVER_TEXT[lev].format(v=v)
