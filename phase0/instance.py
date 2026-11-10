"""Phase 0 toy instance: 8 actors, 3 issues, 12 levers.

All utilities are in each actor's OWN units; nothing below compares them across actors.
Only the emission shares are sourced. Every other number is illustrative and was chosen
so that each issue is a social dilemma and every lever passes the orientation test at
the base point. See PROVENANCE.
"""
import numpy as np

ACTORS = ['USA', 'CHN', 'EU', 'IND', 'FEX', 'LIC', 'DEV', 'MDB']
N = len(ACTORS)

ACTOR_INFO = {
    'USA': dict(name='United States', cls='state', role='signatory',
                instrument='statute containing the CCF'),
    'CHN': dict(name='China', cls='state', role='signatory',
                instrument='statute or State Council decision containing the CCF'),
    'EU': dict(name='European Union', cls='supranational polity', role='signatory',
               instrument='regulation containing the CCF'),
    'IND': dict(name='India', cls='state', role='signatory',
                instrument='statute containing the CCF'),
    'FEX': dict(name='Fossil-exporter bloc (Russia, Iran, Saudi Arabia, Iraq, UAE, Kuwait, Qatar)',
                cls='bloc of states', role='signatory', instrument='parallel statutes'),
    'LIC': dict(name='Low-income country bloc', cls='bloc of states', role='signatory',
                instrument='parallel statutes'),
    'DEV': dict(name='Frontier AI developers', cls='bloc of firms', role='signatory',
                instrument='board resolutions and contracts'),
    'MDB': dict(name='Multilateral development banks', cls='intergovernmental finance',
                role='signatory', instrument='board mandate'),
}

# (actor, lever, number of levels, issue)
LEVERS = [
    ('USA', 'climate', 4, 'climate'), ('USA', 'ai_oversight', 3, 'ai'),
    ('CHN', 'climate', 4, 'climate'), ('CHN', 'ai_oversight', 3, 'ai'),
    ('EU', 'climate', 4, 'climate'), ('EU', 'finance_lic', 3, 'pandemic'),
    ('IND', 'climate', 4, 'climate'), ('IND', 'surveillance', 2, 'pandemic'),
    ('FEX', 'climate', 4, 'climate'),
    ('LIC', 'surveillance', 3, 'pandemic'),
    ('DEV', 'ai_safety', 4, 'ai'),
    ('MDB', 'finance_lic', 3, 'pandemic'),
]
LEVER_TEXT = {
    'climate': 'cut own 2025 emissions by a further {v}0 % by 2035, relative to current policies',
    'ai_oversight': {1: 'license and evaluate frontier models',
                     2: 'license and evaluate frontier models, cap compute, hold pause authority'},
    'ai_safety': 'apply safety restraint tier {v} of 3 to development and deployment',
    'surveillance': 'run pathogen surveillance and laboratory capacity at tier {v}',
    'finance_lic': {1: 'give one tranche of grant finance for surveillance in low-income countries',
                    2: 'give two tranches of grant finance for surveillance in low-income countries'},
}
ISSUES = ['climate', 'ai', 'pandemic']
SHAPE = tuple(n for (_, _, n, _) in LEVERS)
D = len(LEVERS)
OWNER = np.array([ACTORS.index(a) for (a, _, _, _) in LEVERS])
ISSUE_OF = [iss for (_, _, _, iss) in LEVERS]
DIMS = {i: [d for d in range(D) if OWNER[d] == i] for i in range(N)}
TOP = np.array(SHAPE) - 1
NPROF = int(np.prod(SHAPE))

BASE = {
    # emission shares: EDGAR 2026 report, GHG excl. LULUCF, year 2025 (sourced)
    'e.USA': .1111, 'e.CHN': .2951, 'e.EU': .0578, 'e.IND': .0833, 'e.FEX': .1033,
    # climate: benefit weight d_i per unit of Q, cost k_i * level^2
    'd.USA': .35, 'd.CHN': .45, 'd.EU': .50, 'd.IND': .90, 'd.FEX': .15,
    'd.LIC': 1.00, 'd.DEV': .05, 'd.MDB': .40,
    'k.USA': .10, 'k.CHN': .20, 'k.EU': .10, 'k.IND': .15, 'k.FEX': .40,
    # AI: benefit weight al_i per unit of the risk-reduction index A
    'al.USA': 1.0, 'al.CHN': .8, 'al.EU': .8, 'al.IND': .5, 'al.FEX': .4,
    'al.LIC': .3, 'al.DEV': .6, 'al.MDB': .2,
    # AI: oversight cost h_i * level^2, positional cost kap_i * (own - rival) / 2
    'h.USA': .20, 'h.CHN': .20, 'kap.USA': .30, 'kap.CHN': .30,
    'm.DEV': .08,                      # developers' safety cost m * level^2
    # pandemic: benefit weight pi_i per unit of protection P
    'pi.USA': .5, 'pi.CHN': .5, 'pi.EU': .6, 'pi.IND': .5, 'pi.FEX': .3,
    'pi.LIC': .6, 'pi.DEV': .2, 'pi.MDB': .6,
    # pandemic: surveillance cost per level, finance cost per tranche, value of a tranche to LIC
    'kL.LIC': .50, 'kI.IND': .30, 'f.EU': .08, 'f.MDB': .15, 'r.LIC': .25,
    # effect model of the AI index
    'wA.min': .5, 'wA.sum': .2, 'wA.dev': .3,
    # aspiration parameters (budgets in own units, EU's climate floor)
    'B.USA': .9, 'B.CHN': .9, 'B.EU': .8, 'B.IND': .6, 'B.FEX': .4, 'B.LIC': .3, 'B.DEV': .35,
    'Qmin.EU': .5,
}
PROVENANCE = {
    'e.': dict(status='sourced', source='EDGAR 2026 report, total GHG excl. LULUCF, year 2025; '
               'FEX = Russia + Iran + Saudi Arabia + Iraq + UAE + Kuwait + Qatar',
               url='https://edgar.jrc.ec.europa.eu/report_2026', retrieved='2026-11-10'),
    'default': dict(status='illustrative', source='chosen by the team for the toy instance',
                    who_says='Claude', retrieved='2026-11-10'),
}
# parameters that vary over the robustness set (valuations and costs, not shares or model weights)
PERTURB = [k for k in BASE if k.split('.')[0] in
           ('d', 'k', 'al', 'h', 'kap', 'm', 'pi', 'kL', 'kI', 'f', 'r')]


def grids(shape=SHAPE):
    return [np.arange(n).reshape([n if j == d else 1 for j in range(len(shape))])
            for d, n in enumerate(shape)]


def evaluate(p=BASE, light=False):
    """Evaluate the whole profile grid. Returns a dict with
    U (N, *SHAPE), acc (N, *SHAPE) acceptability per actor, and, unless light,
    indicators, costs, named aspiration constraints and slacks."""
    cU, oU, cC, oC, cE, fE, cI, sI, cF, sL, sD, fM = grids()
    Q = p['e.USA'] * cU + p['e.CHN'] * cC + p['e.EU'] * cE + p['e.IND'] * cI + p['e.FEX'] * cF
    A = p['wA.min'] * np.minimum(oU, oC) / 2 + p['wA.sum'] * (oU + oC) / 4 + p['wA.dev'] * sD / 3
    P = np.minimum(sL, 1 + sI) / 2
    cost = {
        'USA': p['k.USA'] * cU ** 2 + p['h.USA'] * oU ** 2,
        'CHN': p['k.CHN'] * cC ** 2 + p['h.CHN'] * oC ** 2,
        'EU': p['k.EU'] * cE ** 2 + p['f.EU'] * fE,
        'IND': p['k.IND'] * cI ** 2 + p['kI.IND'] * sI,
        'FEX': p['k.FEX'] * cF ** 2,
        'LIC': p['kL.LIC'] * sL,
        'DEV': p['m.DEV'] * sD ** 2,
        'MDB': p['f.MDB'] * fM,
    }
    extra = {a: 0.0 for a in ACTORS}
    extra['USA'] = -p['kap.USA'] * (oU - oC) / 2
    extra['CHN'] = -p['kap.CHN'] * (oC - oU) / 2
    extra['LIC'] = p['r.LIC'] * (fE + fM)
    U = np.empty((N,) + SHAPE)
    for i, a in enumerate(ACTORS):
        U[i] = p['d.' + a] * Q + p['al.' + a] * A + p['pi.' + a] * P - cost[a] + extra[a]
    t = 1e-9
    asp = {
        'USA': [('oversight not ahead of China', oU <= oC, None),
                ('own cost within budget', cost['USA'] <= p['B.USA'] + t, (p['B.USA'] - cost['USA']) / p['B.USA'])],
        'CHN': [('oversight not ahead of the United States', oC <= oU, None),
                ('own cost within budget', cost['CHN'] <= p['B.CHN'] + t, (p['B.CHN'] - cost['CHN']) / p['B.CHN'])],
        'EU': [('climate progress at or above floor', Q >= p['Qmin.EU'] - t,
                np.minimum((Q - p['Qmin.EU']) / p['Qmin.EU'], 1.0)),
               ('own cost within budget', cost['EU'] <= p['B.EU'] + t, (p['B.EU'] - cost['EU']) / p['B.EU'])],
        'IND': [('own cost within budget', cost['IND'] <= p['B.IND'] + t, (p['B.IND'] - cost['IND']) / p['B.IND'])],
        'FEX': [('own cost within budget', cost['FEX'] <= p['B.FEX'] + t, (p['B.FEX'] - cost['FEX']) / p['B.FEX'])],
        'LIC': [('net cost within budget', cost['LIC'] - extra['LIC'] <= p['B.LIC'] + t,
                 (p['B.LIC'] - cost['LIC'] + extra['LIC']) / p['B.LIC'])],
        'DEV': [('own cost within budget', cost['DEV'] <= p['B.DEV'] + t, (p['B.DEV'] - cost['DEV']) / p['B.DEV'])],
        'MDB': [('finance only with protection', (fM == 0) | (P >= 0.5), None)],
    }
    acc = np.ones((N,) + SHAPE, bool)
    for i, a in enumerate(ACTORS):
        for (_, m, _) in asp[a]:
            acc[i] &= m
    out = dict(U=U, acc=acc)
    if not light:
        slack = np.full(SHAPE, np.inf)
        for a in ACTORS:
            for (_, _, s) in asp[a]:
                if s is not None:
                    slack = np.minimum(slack, s)
        out.update(Q=np.broadcast_to(Q, SHAPE), A=np.broadcast_to(A, SHAPE), P=np.broadcast_to(P, SHAPE),
                   cost={a: np.broadcast_to(c, SHAPE) for a, c in cost.items()}, asp=asp, slack=slack)
    return out


def perturbed(rng, spread=0.25, base=BASE):
    """One element of the robustness set: each valuation and cost parameter is multiplied
    by an independent log-uniform factor in [1/(1+spread), 1+spread]."""
    p = dict(base)
    f = {}
    for k in PERTURB:
        f[k] = float(np.exp(rng.uniform(-np.log(1 + spread), np.log(1 + spread))))
        p[k] = base[k] * f[k]
    return p, f


def describe(a):
    """Human-readable lever levels of a profile (length-D integer vector)."""
    return {f'{act}.{lev}': int(a[d]) for d, (act, lev, _, _) in enumerate(LEVERS)}


def lever_sentence(d, v):
    act, lev, _, _ = LEVERS[d]
    t = LEVER_TEXT[lev]
    if isinstance(t, dict):
        return t[v]
    return t.format(v=v)
