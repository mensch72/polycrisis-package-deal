"""Independent audit checker for the Phase 0 toy instance.

Written from the definitions in docs/plan.md and the model description in
docs/phase0_results.md, before reading phase0/core.py, mechanism.py, search.py or
run_phase0.py. It takes only the parameter VALUES from results/params.json-equivalent
(instance.BASE) and re-implements the model, the strict core and the equilibrium test.

Base-point arithmetic is exact (integers, utilities scaled by 10^8), so no tolerance
enters any comparison.

Usage: python3 -I audit_core.py <repo>/phase0
"""
import sys, json, itertools, importlib.util
from fractions import Fraction
import numpy as np

PH = sys.argv[1]
spec = importlib.util.spec_from_file_location('instance', PH + '/instance.py')
inst = importlib.util.module_from_spec(spec); spec.loader.exec_module(inst)
BASE = inst.BASE

ACT = ['USA', 'CHN', 'EU', 'IND', 'FEX', 'LIC', 'DEV', 'MDB']
# my own lever order: (owner, name, levels)
LEV = [('USA', 'c', 4), ('USA', 'o', 3), ('CHN', 'c', 4), ('CHN', 'o', 3), ('EU', 'c', 4), ('EU', 'f', 3),
       ('IND', 'c', 4), ('IND', 's', 2), ('FEX', 'c', 4), ('LIC', 's', 3), ('DEV', 's', 4), ('MDB', 'f', 3)]
SHAPE = tuple(l[2] for l in LEV)
NP = int(np.prod(SHAPE))
OWN = [ACT.index(l[0]) for l in LEV]
S = 10 ** 8


def model(p, exact):
    """Return U (8, NP), acc (8, NP), indicators Q, A, P (NP), costs, slack. Flat C order."""
    g = np.indices(SHAPE).reshape(len(LEV), -1)
    cU, oU, cC, oC, cE, fE, cI, sI, cF, sL, sD, fM = [x.astype(np.int64) for x in g]
    if exact:
        def P_(k):
            v = Fraction(str(p[k])) * S
            assert v.denominator == 1, k
            return int(v)
        one = S
    else:
        def P_(k):
            return float(p[k])
        one = 1.0
    # indicators; exact ones scaled so that all stay integer
    # Q = sum e_i c_i
    Q = P_('e.USA') * cU + P_('e.CHN') * cC + P_('e.EU') * cE + P_('e.IND') * cI + P_('e.FEX') * cF
    # A = wmin * min(oU,oC)/2 + wsum*(oU+oC)/4 + wdev*sD/3 ; multiply by 12 to stay integer
    A12 = 6 * P_('wA.min') * np.minimum(oU, oC) + 3 * P_('wA.sum') * (oU + oC) + 4 * P_('wA.dev') * sD
    # P = min(sL, 1+sI)/2 ; times 2
    P2 = np.minimum(sL, 1 + sI)
    cost = [P_('k.USA') * cU ** 2 + P_('h.USA') * oU ** 2,
            P_('k.CHN') * cC ** 2 + P_('h.CHN') * oC ** 2,
            P_('k.EU') * cE ** 2 + P_('f.EU') * fE,
            P_('k.IND') * cI ** 2 + P_('kI.IND') * sI,
            P_('k.FEX') * cF ** 2,
            P_('kL.LIC') * sL,
            P_('m.DEV') * sD ** 2,
            P_('f.MDB') * fM]
    zero = 0 * cU
    # positional term: 2*x to stay integer
    x2 = [-P_('kap.USA') * (oU - oC), -P_('kap.CHN') * (oC - oU), zero, zero, zero,
          2 * P_('r.LIC') * (fE + fM), zero, zero]
    U = []
    for i, a in enumerate(ACT):
        if exact:
            # U * S^2 * 12 would overflow? d*Q ~ 1e8*1e8*... use python-int safe scale:
            # all terms brought to common scale S*S*12 / S = keep as S*12 by dividing products by S
            dq = P_('d.' + a) * Q            # scale S^2
            assert np.all(dq % S == 0)
            aa = P_('al.' + a) * A12          # scale S^2 * 12
            assert np.all(aa % S == 0)
            u = 12 * (dq // S) + aa // S + 6 * P_('pi.' + a) * P2 - 12 * cost[i] + 6 * x2[i]
        else:
            u = P_('d.' + a) * Q + P_('al.' + a) * A12 / 12 + P_('pi.' + a) * P2 / 2 - cost[i] + x2[i] / 2
        U.append(u)
    U = np.array(U)
    B = {a: P_('B.' + a) for a in ACT if 'B.' + a in p}
    t = 0 if exact else 1e-9
    net_lic = cost[5] - x2[5] // 2 if exact else cost[5] - x2[5] / 2
    acc = [(oU <= oC) & (cost[0] <= B['USA'] + t),
           (oC <= oU) & (cost[1] <= B['CHN'] + t),
           (Q >= P_('Qmin.EU') - t) & (cost[2] <= B['EU'] + t),
           cost[3] <= B['IND'] + t,
           cost[4] <= B['FEX'] + t,
           net_lic <= B['LIC'] + t,
           cost[6] <= B['DEV'] + t,
           (fM == 0) | (P2 >= 1)]
    acc = np.array(acc)
    f = float
    slack = np.min(np.array([(B['USA'] - cost[0]) / f(B['USA']), (B['CHN'] - cost[1]) / f(B['CHN']),
                             np.minimum((Q - P_('Qmin.EU')) / f(P_('Qmin.EU')), 1.0),
                             (B['EU'] - cost[2]) / f(B['EU']), (B['IND'] - cost[3]) / f(B['IND']),
                             (B['FEX'] - cost[4]) / f(B['FEX']), (B['LIC'] - net_lic) / f(B['LIC']),
                             (B['DEV'] - cost[6]) / f(B['DEV'])]), axis=0)
    return dict(U=U, acc=acc, Q=Q / one, A=A12 / (12 * one), P=P2 / 2, slack=slack,
                uscale=(12 * S if exact else 1.0), levels=g)


def sub_index(G):
    """Flat indices of all profiles with every lever of non-members at 0. G: iterable of actor ids."""
    rng = [range(n) if OWN[d] in G else (0,) for d, (_, _, n) in enumerate(LEV)]
    arr = np.array(list(itertools.product(*rng)), dtype=np.int64)
    return np.ravel_multi_index(arr.T, SHAPE)


COALS = [tuple(i for i in range(8) if m >> i & 1) for m in range(1, 256)]
SUB = {G: sub_index(G) for G in COALS}


def blocked_by(U, cand, G, eps=0):
    """Boolean per candidate: G has a' (non-members 0) that all members weakly prefer (>= u - eps... exact
    if eps == 0) and one strictly prefers (> u + eps)."""
    G = list(G)
    idx = SUB[tuple(G)]
    UG = U[np.ix_(G, idx)]                      # |G| x S
    UC = U[np.ix_(G, cand)]                     # |G| x m
    keep = np.all(UG >= UC.min(axis=1)[:, None] - eps, axis=0)   # prune: must weakly beat the least demanding candidate
    UG = UG[:, keep]
    out = np.zeros(len(cand), bool)
    if UG.shape[1] == 0:
        return out
    step = max(1, int(4e7 // max(1, UG.shape[1])))
    for s in range(0, len(cand), step):
        c = UC[:, s:s + step]
        ge = np.ones((UG.shape[1], c.shape[1]), bool)
        gt = np.zeros_like(ge)
        for k in range(len(G)):
            d = UG[k][:, None] - c[k][None, :]
            ge &= d >= -eps
            gt |= d > eps
        out[s:s + step] = np.any(ge & gt, axis=0)
    return out


def strict_core(U, cand, eps=0, coalitions=COALS, verbose=False):
    """Return bool per candidate (in strict core) and the per-coalition blocked counts."""
    alive = np.ones(len(cand), bool)
    stats = {}
    for G in sorted(coalitions, key=len):
        b = blocked_by(U, cand, G, eps)
        stats[G] = int(b.sum())
        alive &= ~b
    return alive, stats


def registry(a_star, G, devs):
    """Registry rule l(c): largest mutually feasible profile, by downward fixed-point iteration from TOP.
    Non-members of G file the step function through a_star; members file the constants devs (m x D,
    only members' levers used). Returns outcomes (m x D)."""
    top = np.array(SHAPE) - 1
    a = np.tile(top, (len(devs), 1))
    inG = np.array([OWN[d] in G for d in range(len(LEV))])
    for _ in range(50):
        new = a.copy()
        new[:, inG] = np.minimum(a[:, inG], devs[:, inG])
        for j in range(8):
            if j in G:
                continue
            mine = np.array([OWN[d] == j for d in range(len(LEV))])
            ok = np.all(a[:, ~mine] >= a_star[~mine], axis=1)       # every OTHER signatory at or above its level
            cj = np.where(ok[:, None], a_star[mine][None, :], 0)
            new[:, mine] = np.minimum(a[:, mine], cj)
        if np.array_equal(new, a):
            return a
        a = new
    raise RuntimeError('no fixed point')


_DEVS = {}
def devs_of(G):
    if G not in _DEVS:
        rng = [range(n) if OWN[d] in G else (0,) for d, (_, _, n) in enumerate(LEV)]
        _DEVS[G] = np.array(list(itertools.product(*rng)), dtype=np.int64)
    return _DEVS[G]


def outcomes_closed(a_star, G, devs):
    """Closed form of the registry outcome, derived in the audit report: non-members stay at a_star iff
    every member lever is at or above a_star, else they fall to 0."""
    inG = np.array([OWN[d] in G for d in range(len(LEV))])
    ok = np.all(devs[:, inG] >= a_star[inG], axis=1)
    out = devs.copy()
    out[:, ~inG] = np.where(ok[:, None], a_star[~inG][None, :], 0)
    return out


def equilibrium(U, a_star, eps=0, closed=False):
    """Strictly strong equilibrium of the commitment game at step filings through a_star: no group G and
    no joint deviation (constants suffice, see audit report) after which all members are weakly and one
    strictly better off. Returns list of (G, outcome) violations (first per G)."""
    base = int(np.ravel_multi_index(a_star, SHAPE))
    viol = []
    for G in COALS:
        devs = devs_of(G)
        if closed:
            out = outcomes_closed(np.array(a_star), set(G), devs)
        else:
            out = registry(np.array(a_star), set(G), devs)
            assert np.array_equal(out, outcomes_closed(np.array(a_star), set(G), devs)), 'closed form differs'
        oi = np.unique(np.ravel_multi_index(out.T, SHAPE))
        d = U[np.ix_(list(G), oi)] - U[list(G), base][:, None]
        bad = np.all(d >= -eps, axis=0) & np.any(d > eps, axis=0)
        if bad.any():
            viol.append((G, np.array(np.unravel_index(oi[bad][0], SHAPE)).tolist()))
    return viol


if __name__ == '__main__':
    R = {}
    m = model(BASE, exact=True)
    U, acc = m['U'], m['acc']
    # 0. my utility table against theirs (float), after matching lever order (same order by construction)
    ev = inst.evaluate(BASE)
    Uf = ev['U'].reshape(8, -1)
    R['max_abs_U_diff'] = float(np.max(np.abs(U / m['uscale'] - Uf)))
    R['acc_mismatch'] = int((acc != ev['acc'].reshape(8, -1)).sum())
    # 1. regions
    C = acc.all(axis=0)
    IR = np.all(U >= U[:, [0]], axis=0)
    R['n_acceptable'] = int(C.sum()); R['n_IR'] = int(IR.sum()); R['n_both'] = int((C & IR).sum())
    R['acc_share_per_actor'] = {a: round(float(acc[i].mean()), 4) for i, a in enumerate(ACT)}
    # strong IR: singleton cannot do better alone (same as IR iff own levers are costly at others = 0)
    cand = np.flatnonzero(C & IR)
    # 2. strict core inside C, all 255 coalitions, exact
    alive, stats = strict_core(U, cand)
    core = cand[alive]
    R['n_core_in_C'] = int(alive.sum())
    R['n_pareto_dominated'] = stats[COALS[-1]] if len(COALS[-1]) == 8 else None
    grand = tuple(range(8))
    pd = blocked_by(U, cand, grand)
    proper_only = np.zeros(len(cand), bool)
    for G in COALS:
        if len(G) < 8:
            proper_only |= blocked_by(U, cand, G) & ~pd
    R['n_pareto_dominated'] = int(pd.sum())
    R['n_efficient_but_blocked_by_proper'] = int(proper_only.sum())
    np.save('results/core_idx.npy', core)
    # 3. shape of the core
    L = m['levels'][:, core]
    R['core_shape'] = dict(
        oversight_both_1=int(((L[1] == 1) & (L[3] == 1)).sum()), P_full=int((m['P'][core] == 1).sum()),
        FEX_1=int((L[8] == 1).sum()), FEX_pos=int((L[8] > 0).sum()),
        any_climate3=int((L[[0, 2, 4, 6, 8]] == 3).any(axis=0).sum()),
        Q=[float(m['Q'][core].min()), float(m['Q'][core].max())],
        A=[float(m['A'][core].min()), float(m['A'][core].max())],
        P=[float(m['P'][core].min()), float(m['P'][core].max())])
    # 4. menu criteria
    gain = (U - U[:, [0]]) / m['uscale']
    norm = gain[:, cand].max(axis=1)
    ng = gain[:, core] / norm[:, None]
    nash = np.prod(ng, axis=0)
    prof = lambda k: np.array(np.unravel_index(core[k], SHAPE)).tolist()
    k_nash = int(np.argmax(nash))
    srt = np.sort(ng, axis=0)
    order = sorted(range(len(core)), key=lambda k: (tuple(np.round(srt[:, k], 12)), nash[k]), reverse=True)
    k_lex = order[0]
    sl = m['slack'][core]
    k_deep = max(range(len(core)), key=lambda k: (round(float(sl[k]), 12), nash[k]))
    amb = np.min(np.array([m[x][core] / m[x][core].max() for x in 'QAP']), axis=0)
    k_amb = max(range(len(core)), key=lambda k: (round(float(amb[k]), 12), nash[k]))
    R['menu'] = {n: dict(profile=prof(k), ngain={a: round(float(ng[i, k]), 4) for i, a in enumerate(ACT)},
                         Q=float(m['Q'][core[k]]), A=float(m['A'][core[k]]), P=float(m['P'][core[k]]))
                 for n, k in [('nash', k_nash), ('leximin', k_lex), ('deepest', k_deep), ('ambition', k_amb)]}
    R['ties'] = dict(deepest=int((np.abs(sl - sl.max()) < 1e-12).sum()),
                     ambition=int((np.abs(amb - amb.max()) < 1e-12).sum()),
                     leximin_min=int((np.abs(srt[0] - srt[0].max()) < 1e-12).sum()))
    # 5. equilibrium at each menu profile and at ALL core profiles
    eqv = {}
    for n in R['menu']:
        eqv[n] = equilibrium(U, R['menu'][n]['profile'])
    R['menu_equilibrium_violations'] = {n: v for n, v in eqv.items()}
    print(json.dumps(R, indent=1), flush=True)
    # all core profiles: exact decomposition of the deviation outcomes (see report): a deviation either
    # leaves a member below a_star (then it is a core-type deviation, excluded above) or over-fulfils.
    STRD = np.array([int(np.prod(SHAPE[d + 1:])) for d in range(len(SHAPE))])
    nviol = 0
    for k in range(len(core)):
        a = np.array(prof(k)); f0 = int(a @ STRD); bad = False
        for G in COALS:
            rng = [range(a[d], n) if OWN[d] in G else (a[d],) for d, (_, _, n) in enumerate(LEV)]
            dv = np.array(list(itertools.product(*rng)))
            if len(dv) > 1:
                d = U[np.ix_(list(G), dv @ STRD)] - U[list(G), f0][:, None]
                bad |= bool((np.all(d >= 0, axis=0) & np.any(d > 0, axis=0)).any())
        nviol += bad
    R['core_profiles_not_equilibrium'] = nviol
    print(json.dumps(R, indent=1), flush=True)
    # 6. no-filter variant: efficient & IR, blocked by proper coalitions
    ir = np.flatnonzero(IR)
    pdn = blocked_by(U, ir, grand)
    eff = ir[~pdn]
    R['nofilter_efficient_IR'] = int(len(eff))
    al2, _ = strict_core(U, eff, coalitions=[G for G in COALS if len(G) < 8])
    R['nofilter_blocked_by_proper'] = int((~al2).sum())
    R['nofilter_core'] = int(al2.sum())
    np.save('results/core_nofilter_idx.npy', eff[al2])
    R['nofilter_core_acceptable'] = int(C[eff[al2]].sum())
    json.dump(R, open('results/audit_core.json', 'w'), indent=1)
    print(json.dumps(R, indent=1))
