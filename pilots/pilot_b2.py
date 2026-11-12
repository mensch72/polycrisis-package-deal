"""Pilot B2 skeleton, version 2: entry into a hardwired pause of frontier AI training, as a registry of
conditional commitments among states. Rebuilt on 12 November 2026 on the report's own ledger, after the
whole report had been read. Version 1 (10 November) had invented effect numbers and one wrong lever.

Source: Fithian, Holliday and the Working Group on AI Pause Feasibility (2026), "The Feasibility of a
Hardwired Pause of Frontier AI Training", working paper v1.0.2, https://hardwired-pause.ai/paper.

TAKEN FROM THE REPORT (its illustrative values for a pause at year-end 2026; sections 3.2.3, 6.4, 6.5):
  - the ledger rule: a state's covert-evasion ledger L_E must stay below alpha * F_E, its overt-breakout
    ledger L_B below alpha * F_B, with alpha = 0.25, F_E = 6.4M and F_B = 180M H100e;
  - stocks: United States 35M H100e (20 % of F_B), China 3.1M (1.8 % of F_B);
  - dark compute as a share of F_E under three census scenarios: non-deniable concealment 4.7 % (US) and
    16 % (China), low cooperation 0.94 % and 1.8 %, high cooperation 0.11 % and 0.11 %;
  - other ledger terms can be held near 0.25 % of the thresholds, which gives two orders of magnitude of
    headroom; moving half of the US transitional fleet out of its territory is the report's own example;
  - training efficiency gains of 57 % a year erode the thresholds: one order of magnitude in about 5 years;
  - order of entry: the United States and China first, then the jurisdictions holding supply-chain chokepoints.
DERIVED HERE from those values: durability = headroom in orders of magnitude, min over both states and both
ledgers of log10(alpha * F / L), capped at 2, converted to years at 57 % a year.
ILLUSTRATIVE (Claude, 12 November 2026, fixed before the first run of this version): every preference
number; the grid of retained shares below one half; the effect of the suppliers' levers on durability.
Nothing here says anything about any government.

Levers. Each lead state: pause (0/1); census cooperation (0 concealment, 1 low, 2 high); drawdown of the
training-capable fleet kept in its territory (0 all kept, 1 half, 2 a tenth, 3 about one eightieth).
Suppliers, one bloc: stop production of training-capable chips (0/1); accept monitoring of fabrication (0/1).
"""
import numpy as np

ACTORS = ['USA', 'CHN', 'SUP']
N = len(ACTORS)
ACTOR_INFO = {'USA': 'United States', 'CHN': 'China',
              'SUP': 'Chokepoint jurisdictions (Netherlands, Germany, Japan, Taiwan, South Korea)'}
LEVERS = [('USA', 'pause', 2, 'ai'), ('USA', 'census', 3, 'ai'), ('USA', 'drawdown', 4, 'ai'),
          ('CHN', 'pause', 2, 'ai'), ('CHN', 'census', 3, 'ai'), ('CHN', 'drawdown', 4, 'ai'),
          ('SUP', 'production_stop', 2, 'ai'), ('SUP', 'monitoring', 2, 'ai')]
ISSUES = ['ai']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
CHAIN = [['USA', 'CHN'], ACTORS]
INDICATORS = ['X', 'YEARS']
RETAINED = [1.0, 0.5, 0.1, 0.0125]
LEVER_TEXT = {'pause': 'prohibit training beyond the threshold and stop orders for training-capable chips',
              'census': {1: 'cooperate with the census at the low level', 2: 'cooperate fully with the census'},
              'drawdown': {1: 'keep at most half of its training-capable fleet in its territory',
                           2: 'keep at most a tenth of its training-capable fleet in its territory',
                           3: 'keep only a residual training-capable fleet in its territory'},
              'production_stop': 'stop the production of training-capable chips',
              'monitoring': 'accept monitoring of fabrication'}

BASE = {
    # from the report
    'alpha': .25, 'stockB.USA': .20, 'stockB.CHN': .018,            # allowance; fleet as a share of F_B
    'dark0.USA': .047, 'dark1.USA': .0094, 'dark2.USA': .0011,      # dark compute as a share of F_E by census level
    'dark0.CHN': .16, 'dark1.CHN': .018, 'dark2.CHN': .0011,
    'gain': .57, 'cap': 2.0,                                        # efficiency gain per year; headroom cap (orders of magnitude)
    # illustrative
    'x.sup0': .5, 'x.prod': .25, 'x.mon': .25,                      # share of durability kept without / with the suppliers' levers
    'a.USA': 1.0, 'a.CHN': 1.0, 'a.SUP': .8,                        # value of full durability (X = 1)
    'f.USA': .20, 'f.CHN': .20, 'G': .20, 'sig': .50,               # forgone benefit of pausing; gain from training on alone; exposure
    'kc': .03, 'kd': .03, 'th': .30,                                # cost per census level, per drawdown level; exposure per unit of extra concession
    'r.SUP': .30, 'c.SUP': .05, 'm.SUP': .25,                       # suppliers: lost revenue, monitoring cost, orders lost to a pause
    'gap': .25,                                                     # red line: concession index beyond the rival's
}
PROVENANCE = {
    'report': dict(status='sourced', keys=['alpha', 'stockB.', 'dark', 'gain', 'cap'],
                   source='Fithian, Holliday et al. (2026), sections 3.2.3, 6.1, 6.4, 6.5; illustrative values of the report itself',
                   url='https://hardwired-pause.ai/paper', retrieved='2026-11-12'),
    'default': dict(status='illustrative', source='set by Claude before the first run of version 2', who_says='Claude',
                    retrieved='2026-11-12'),
}
PERTURB = ['a.USA', 'a.CHN', 'a.SUP', 'f.USA', 'f.CHN', 'G', 'sig', 'kc', 'kd', 'th', 'r.SUP', 'c.SUP', 'm.SUP']
TIPPING = PERTURB + ['x.sup0', 'x.prod', 'x.mon']


def grids():
    return [np.arange(n).reshape([n if j == d else 1 for j in range(D)]) for d, n in enumerate(SHAPE)]


def headroom(p, s, cen, draw):
    dark = np.choose(cen, [p[f'dark0.{s}'], p[f'dark1.{s}'], p[f'dark2.{s}']])
    kept = np.choose(draw, RETAINED) * p[f'stockB.{s}']
    return np.minimum(np.log10(p['alpha'] / dark), np.log10(p['alpha'] / kept))


def evaluate(p=BASE, light=False):
    pU, cU, dU, pC, cC, dC, prod, mon = grids()
    both = np.minimum(pU, pC)
    H = np.clip(np.minimum(headroom(p, 'USA', cU, dU), headroom(p, 'CHN', cC, dC)), 0, p['cap'])
    Deff = both * H * (p['x.sup0'] + p['x.prod'] * prod + p['x.mon'] * mon)
    X = Deff / p['cap']
    years = Deff * np.log(10) / np.log(1 + p['gain'])
    conc = {'USA': (cU / 2 + dU / 3) / 2, 'CHN': (cC / 2 + dC / 3) / 2}
    U = np.empty((N,) + SHAPE)
    acc = np.ones((N,) + SHAPE, bool)
    for i, (me, pm, cm, dm, po, ot) in enumerate((('USA', pU, cU, dU, pC, 'CHN'), ('CHN', pC, cC, dC, pU, 'USA'))):
        U[i] = (p['a.' + me] * X - p['f.' + me] * pm - p['sig'] * np.maximum(pm - po, 0) + p['G'] * np.maximum(po - pm, 0)
                - p['kc'] * cm - p['kd'] * dm - p['th'] * np.maximum(conc[me] - conc[ot], 0))
        acc[i] &= (conc[me] <= conc[ot] + p['gap'] + 1e-9) & ((cm + dm == 0) | (pm == 1))
    U[2] = p['a.SUP'] * X - p['r.SUP'] * prod * (1 - 0.5 * both) - p['c.SUP'] * mon - p['m.SUP'] * (pU + pC) / 2
    acc[2] &= (prod == 0) | (both == 1)
    return dict(U=U, acc=acc, X=np.broadcast_to(X, SHAPE), YEARS=np.broadcast_to(years, SHAPE))


def describe(a):
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}


def lever_sentence(d, v):
    t = LEVER_TEXT[LEVERS[d][1]]
    return t[v] if isinstance(t, dict) else t
