"""Phase 0: negotiation by updating (WP10) and a compliance probe (WP7).

Part 1. Each actor's options are reduced to a ladder: an ordered chain through its own levers,
built greedily by smallest own loss per step with everyone else at level 0. On ladders every actor
has a one-dimensional action, as in the main text of Heitzig (2025). The learning rule of its
Theorem 3 is run in its discrete form: starting from all-zero CCFs, in random order, each actor once
replaces its CCF by the indifference-curve CCF through a favourite point on the others' current CCFs.
The theorem is proved for continuous single-good problems; here it is only tested.

Part 2. Linear compensation on the climate component of the lead candidate, continuous
relaxation, shortfalls measured in abatement units, single actor, one-period shortfall: smallest
compensation factor that makes the shortfall unprofitable. A first-order calculation, not a proof.
"""
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instance import ACTORS, N, LEVERS, SHAPE, D, OWNER, DIMS, BASE, evaluate
import core

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
T = 1e-9


def ladders(U):
    lad = []
    for i in range(N):
        cur = np.zeros(D, int)
        chain = [cur[DIMS[i]].copy()]
        while any(cur[d] < SHAPE[d] - 1 for d in DIMS[i]):
            best = None
            for d in DIMS[i]:
                if cur[d] < SHAPE[d] - 1:
                    nxt = cur.copy()
                    nxt[d] += 1
                    loss = U[i][tuple(cur)] - U[i][tuple(nxt)]
                    if best is None or loss < best[0] - T:
                        best = (loss, d)
            cur[best[1]] += 1
            chain.append(cur[DIMS[i]].copy())
        lad.append(np.array(chain))
    return lad


def ladder_game(U, lad):
    shape = tuple(len(l) for l in lad)
    idx = []
    for d in range(D):
        i = int(OWNER[d])
        j = DIMS[i].index(d)
        idx.append(lad[i][:, j].reshape([shape[i] if a == i else 1 for a in range(N)]))
    return U[(slice(None),) + tuple(idx)], shape


def outcome(c, shape):
    k = np.array(shape) - 1
    while True:
        changed = False
        for i in range(N):
            lim = int(c[i][tuple(np.delete(k, i))])
            if lim < k[i]:
                k[i] = lim
                changed = True
        if not changed:
            return k


def learn_once(UL, shape, order, caps=None, acc=None):
    """caps[i]: i's aspiration constraints that are down-sets in its own action; they cap its CCF.
    acc[i]: all of i's aspiration constraints; they restrict its choice of favourite point if possible."""
    c = [np.zeros(tuple(np.delete(shape, i)), int) for i in range(N)]
    ax = [np.arange(shape[i]).reshape([shape[i] if a == i else 1 for a in range(N)]) for i in range(N)]
    for i in order:
        feas = np.ones(shape, bool)
        for j in range(N):
            if j != i:
                feas &= ax[j] <= np.expand_dims(c[j], j)
        if acc is not None and (feas & acc[i]).any():
            feas = feas & acc[i]
        vals = np.where(feas, UL[i], -np.inf)
        ut = float(vals.max())                       # utility at a favourite point
        ok = UL[i] >= ut - T                         # a down-set along axis i
        if caps is not None:
            ok = ok & caps[i]
        c[i] = np.maximum(ok.sum(axis=i) - 1, 0)
    return outcome(c, shape)


def to_ladder(arr, lad, shape):
    """Map an array over the full lever grid (leading axes allowed) to the ladder grid."""
    idx = []
    for d in range(D):
        i = int(OWNER[d])
        idx.append(lad[i][:, DIMS[i].index(d)].reshape([shape[i] if a == i else 1 for a in range(N)]))
    return arr[(Ellipsis,) + tuple(idx)]


def weakly_blocked(UL, owner, f):
    n = UL.shape[0]
    Uf = UL.reshape(n, -1)
    for G in core.coalitions(n):
        rows = core.rows_for(UL, G, owner)
        if np.any(np.all(rows > Uf[list(G), f] + T, axis=1)):
            return True
    return False


def summary(res, tot):
    """Count-weighted description of the outcomes of the learning process."""
    w = np.array([r['count'] for r in res]) / tot
    return dict(share_fex_contributes=float(sum(wi for wi, r in zip(w, res) if r['profile']['FEX.climate'] > 0)),
                mean_Q=float(sum(wi * r['Q'] for wi, r in zip(w, res))),
                mean_A=float(sum(wi * r['A'] for wi, r in zip(w, res))),
                mean_P=float(sum(wi * r['P'] for wi, r in zip(w, res))))


def main(n_orders=200, seed=3, delta=0.9):
    ev = evaluate(BASE)
    U = ev['U']
    lad = ladders(U)
    UL, shape = ladder_game(U, lad)
    owner = np.arange(N)
    R = dict(ladders={ACTORS[i]: [[int(x) for x in row] for row in lad[i]] for i in range(N)},
             ladder_profiles=int(np.prod(shape)),
             orientation_on_ladders=len(core.orientation(UL, owner)) == 0)
    rng = np.random.default_rng(seed)
    U0 = UL.reshape(N, -1)[:, 0]
    outs, by_pos = {}, np.zeros((N, 2))
    for _ in range(n_orders):
        order = rng.permutation(N)
        k = learn_once(UL, shape, order)
        f = int(np.ravel_multi_index(tuple(k), shape))
        outs.setdefault(f, []).append(order.tolist())
        g = UL.reshape(N, -1)[:, f] - U0
        for pos, i in enumerate(order):
            by_pos[pos] += (g[i] > T, 1)
    res = []
    for f, orders in outs.items():
        k = np.array(np.unravel_index(f, shape))
        full = np.zeros(D, int)
        for i in range(N):
            full[DIMS[i]] = lad[i][k[i]]
        ff = int(np.ravel_multi_index(tuple(full), SHAPE))
        g = UL.reshape(N, -1)[:, f] - U0
        res.append(dict(count=len(orders),
                        profile={f'{LEVERS[d][0]}.{LEVERS[d][1]}': int(full[d]) for d in range(D)},
                        gain={ACTORS[i]: round(float(g[i]), 3) for i in range(N)},
                        Q=float(ev['Q'].reshape(-1)[ff]), A=float(ev['A'].reshape(-1)[ff]),
                        P=float(ev['P'].reshape(-1)[ff]),
                        ladder_weak_core=not weakly_blocked(UL, owner, f),
                        ladder_strict_core=bool(core.in_strict_core(UL, owner, f)[0]),
                        full_strict_core=bool(core.in_strict_core(U, OWNER, ff)[0]),
                        acceptable=bool(ev['acc'].reshape(N, -1)[:, ff].all())))
    res.sort(key=lambda r: -r['count'])
    tot = sum(r['count'] for r in res)
    R['learning'] = dict(
        n_orders=n_orders, distinct_outcomes=len(res),
        share_ladder_weak_core=sum(r['count'] for r in res if r['ladder_weak_core']) / tot,
        share_ladder_strict_core=sum(r['count'] for r in res if r['ladder_strict_core']) / tot,
        share_full_strict_core=sum(r['count'] for r in res if r['full_strict_core']) / tot,
        share_acceptable=sum(r['count'] for r in res if r['acceptable']) / tot,
        share_with_positive_gain_by_position_in_order=[round(float(a / b), 3) for a, b in by_pos],
        **summary(res, tot),
        most_frequent=res[:5])

    # ---- capped variant: aspirations enter the CCFs
    accL = to_ladder(ev['acc'], lad, shape)
    caps = np.ones((N,) + shape, bool)
    excluded = []
    for i, a in enumerate(ACTORS):
        for (label, m, _) in ev['asp'][a]:
            mL = to_ladder(np.broadcast_to(m, SHAPE), lad, shape)
            if np.all(np.diff(mL.astype(int), axis=i) <= 0):       # a down-set in the own action
                caps[i] &= mL
            else:
                excluded.append(f'{a}: {label}')
    coreC = set(json.load(open(os.path.join(OUT, 'core_acceptable.json'))))
    rng = np.random.default_rng(seed + 1)
    outs2 = {}
    for _ in range(n_orders):
        order = rng.permutation(N)
        k = learn_once(UL, shape, order, caps=caps, acc=accL)
        f = int(np.ravel_multi_index(tuple(k), shape))
        outs2[f] = outs2.get(f, 0) + 1
    res2 = []
    for f, cnt in outs2.items():
        k = np.array(np.unravel_index(f, shape))
        full = np.zeros(D, int)
        for i in range(N):
            full[DIMS[i]] = lad[i][k[i]]
        ff = int(np.ravel_multi_index(tuple(full), SHAPE))
        g = UL.reshape(N, -1)[:, f] - U0
        res2.append(dict(count=cnt, profile={f'{LEVERS[d][0]}.{LEVERS[d][1]}': int(full[d]) for d in range(D)},
                         gain={ACTORS[i]: round(float(g[i]), 3) for i in range(N)},
                         Q=float(ev['Q'].reshape(-1)[ff]), A=float(ev['A'].reshape(-1)[ff]),
                         P=float(ev['P'].reshape(-1)[ff]),
                         acceptable=bool(ev['acc'].reshape(N, -1)[:, ff].all()),
                         individually_rational=bool(np.all(g >= -T)),
                         in_core_inside_acceptable_region=ff in coreC,
                         full_strict_core=bool(core.in_strict_core(U, OWNER, ff)[0])))
    res2.sort(key=lambda r: -r['count'])
    tot2 = sum(r['count'] for r in res2)
    R['learning_capped'] = dict(
        n_orders=n_orders, distinct_outcomes=len(res2), constraints_not_usable_as_caps=excluded,
        share_acceptable=sum(r['count'] for r in res2 if r['acceptable']) / tot2,
        share_individually_rational=sum(r['count'] for r in res2 if r['individually_rational']) / tot2,
        share_in_core_inside_acceptable_region=sum(r['count'] for r in res2 if r['in_core_inside_acceptable_region']) / tot2,
        share_full_strict_core=sum(r['count'] for r in res2 if r['full_strict_core']) / tot2,
        **summary(res2, tot2),
        most_frequent=res2[:5])

    # ---- Part 2: linear compensation probe on the climate component of the lead candidate
    main_res = json.load(open(os.path.join(OUT, 'results.json')))
    rec = main_res['menu'][main_res['lead']]['profile']
    emit = [a for a in ACTORS if f'{a}.climate' in rec]
    active = [a for a in emit if rec[f'{a}.climate'] > 0]
    n = len(active)
    alpha = {}
    for a in active:
        q = rec[f'{a}.climate']
        ratio = BASE['d.' + a] * BASE['e.' + a] / (2 * BASE['k.' + a] * q)     # marginal benefit / marginal cost
        alpha[a] = round((1 - ratio) / (delta * (1 - 1 / n)), 3)
    R['linc_probe'] = dict(delta=delta, actors_with_positive_targets=active, n=n, alpha_min=alpha,
                           alpha_needed=max(alpha.values()))
    json.dump(R, open(os.path.join(OUT, 'dynamics.json'), 'w'), indent=1)
    return R


if __name__ == '__main__':
    R = main()
    L = R['learning']
    print('ladders', {a: len(v) for a, v in R['ladders'].items()}, '| profiles', R['ladder_profiles'],
          '| orientation ok', R['orientation_on_ladders'])
    print({k: v for k, v in L.items() if k != 'most_frequent'})
    for r in L['most_frequent']:
        print(r['count'], list(r['profile'].values()), r['gain'], 'weak', r['ladder_weak_core'],
              'strict', r['ladder_strict_core'], 'full', r['full_strict_core'], 'acc', r['acceptable'])
    C2 = R['learning_capped']
    print('capped:', {k: v for k, v in C2.items() if k != 'most_frequent'})
    for r in C2['most_frequent']:
        print(r['count'], list(r['profile'].values()), r['gain'], 'acc', r['acceptable'],
              'coreC', r['in_core_inside_acceptable_region'], 'full', r['full_strict_core'])
    print('LinC probe', R['linc_probe'])
