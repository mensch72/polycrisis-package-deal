"""Phase 0: a relaxed tower on the contested variant [post hoc exploration; Claude's proposal, not Jobst's].

run_tower.py showed that condition (ii) is demanding: the last stage is a proper CPEP only if the contested
levers are already at their top, and no acceptable first-stage profile allows that. Relaxation tested here:
  (ii') c_k is a strong equilibrium of the stage game, tested directly; the stage game need not be a CPEP.
For step filings this holds iff b_k is in the strict core of the stage game and no group inside the
coalition gains by over-fulfilling (the case distinction of docs/phase0_results.md, which needs no
orientation). Chain as in run_tower.py: I_1 = I minus the harmed actors, I_2 = I.

Selection rule, fixed before the first run: over all pairs (b_1, b_2) with b_1 in the strict core of the
first stage and acceptable to its members, and b_2 in the strict core of the box above b_1, acceptable to
all and free of gains by over-fulfilment: the largest smallest normalised gain over a0 at b_2, then the
largest sum, then the smallest flat indices.
Tests, fixed before the first run, on the selected tower: T1 to T4 exactly as in run_tower.py, with T2
run by direct enumeration of deviations in each stage box.
"""
import json
import os
import sys
import time
from multiprocessing import Pool
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import instance as inst
from instance import ACTORS, N, SHAPE, D, OWNER, BASE
import core
import tower

KAPPA = 0.20
OUT = os.path.join(HERE, 'results2')
T0 = time.time()
ev = inst.evaluate(BASE)
U, acc = ev['U'].copy(), ev['acc']
_g = inst.grids()
U[ACTORS.index('DEV')] -= KAPPA * (_g[1] + _g[3])
Uf = U.reshape(N, -1)
gains = Uf - Uf[:, [0]]
C = acc.all(0).reshape(-1)
scale = gains[:, C & np.all(gains >= -1e-9, axis=0)].max(1)


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def second_stage(b1):
    """All admissible b_2 above b_1: flat indices and their smallest and summed normalised gain over a0."""
    b1 = np.array(b1)
    U2, d2, o2, s2 = tower.stage_game(U, OWNER, range(N), b1)
    c2, _ = core.strict_core(U2, o2, np.ones(s2, bool))
    out = []
    for x in c2:
        b2 = tower.to_full(x, d2, s2, b1, D)
        f2 = int(np.ravel_multi_index(tuple(b2), SHAPE))
        if not C[f2] or core.over_fulfilment(U, OWNER, b2) != 0:
            continue
        g = gains[:, f2] / scale
        out.append((f2, float(g.min()), float(g.sum())))
    return out


def main():
    viol = tower.violation_steps(U, OWNER)
    harmed = sorted({i for (d, i) in viol if i != OWNER[d]})
    I1 = [i for i in range(N) if i not in harmed]
    Uk, dims, owner_k, sub = tower.stage_game(U, OWNER, I1, np.zeros(D, int))
    ck, _ = core.strict_core(Uk, owner_k, np.ones(sub, bool))
    b1s = [tower.to_full(f, dims, sub, np.zeros(D, int), D) for f in ck]
    b1s = [b for b in b1s if acc.reshape(N, -1)[I1, int(np.ravel_multi_index(tuple(b), SHAPE))].all()]
    log('acceptable first-stage core profiles:', len(b1s))
    with Pool(4) as pool:
        res = pool.map(second_stage, [b.tolist() for b in b1s])
    pairs = [(mn, sm, -int(np.ravel_multi_index(tuple(b1), SHAPE)), -f2, b1) for b1, r in zip(b1s, res) for (f2, mn, sm) in r]
    newc = harmed
    R = dict(chain=[[ACTORS[i] for i in I1], ACTORS], n_first_stage=len(b1s),
             n_first_stage_with_a_second=sum(len(r) > 0 for r in res), n_pairs=len(pairs),
             n_pairs_nontrivial=sum(-p[3] != -p[2] for p in pairs),
             n_pairs_newcomer_at_or_above_a0=sum(all(gains[i, -p[3]] >= -1e-9 for i in newc) for p in pairs),
             n_pairs_all_at_or_above_a0=sum(bool(np.all(gains[:, -p[3]] >= -1e-9)) for p in pairs))
    log({k: v for k, v in R.items() if k.startswith('n_')})
    if not pairs:
        R['tower'] = None
        json.dump(R, open(os.path.join(OUT, 'tower_relaxed.json'), 'w'), indent=1)
        return
    mn, sm, nf1, nf2, b1 = max(pairs, key=lambda p: p[:4])
    fm = -nf2
    bm = np.array(np.unravel_index(fm, SHAPE))
    stages = [(set(I1), np.array(b1)), (set(range(N)), bm)]
    R['tower'] = dict(stage1=inst.describe(np.array(b1)), final=inst.describe(bm),
                      final_norm_gain_over_a0={ACTORS[i]: float(gains[i, fm] / scale[i]) for i in range(N)},
                      stage1_norm_gain_over_a0={ACTORS[i]: float(gains[i, -nf1] / scale[i]) for i in range(N)},
                      indicators={k: float(ev[k].reshape(-1)[fm]) for k in 'QAP'},
                      stage1_indicators={k: float(ev[k].reshape(-1)[-nf1]) for k in 'QAP'},
                      in_strict_core_of_original_game=bool(core.in_strict_core(U, OWNER, fm)[0]),
                      last_stage_is_proper_cpep=bool(tower.box_is_cpep(viol, OWNER, range(N), np.array(b1))))
    zero = np.zeros((1, D), int)
    t1 = bool(np.array_equal(tower.registry(stages, SHAPE, OWNER, set(), zero)[0], bm))
    o = tower.registry(stages, SHAPE, OWNER, set(newc), zero)[0]
    old = np.array([OWNER[d] not in newc for d in range(D)])
    t1 &= bool(np.array_equal(o[old], np.array(b1)[old]))
    R['T1'] = dict(passed=t1)
    t2 = {'stage 1': tower.stage_deviations(U, SHAPE, OWNER, I1, np.zeros(D, int), np.array(b1)),
          'stage 2': tower.stage_deviations(U, SHAPE, OWNER, range(N), np.array(b1), bm)}
    R['T2'] = dict(profitable_by_stage={k: {gname(G): n for G, n in v.items()} for k, v in t2.items()},
                   passed=all(len(v) == 0 for v in t2.values()))
    log('T1', R['T1']['passed'], '| T2', R['T2']['passed'])
    earlier, newcomers = set(I1), set(newc)
    old_levers = np.array([OWNER[d] in earlier for d in range(D)])
    groups, inside, best = {}, 0, {}
    for G in core.coalitions(N):
        dv = tower.all_devs(SHAPE, OWNER, G)
        out = tower.registry(stages, SHAPE, OWNER, set(G), dv)
        pm = tower.profitable(U, SHAPE, G, out, fm)
        if pm.any():
            groups[G] = int(pm.sum())
            inside += int(np.all(out[pm][:, old_levers] >= np.array(b1)[old_levers], axis=1).sum())
            fl = np.ravel_multi_index(out[pm].T, SHAPE)
            dl = (Uf[np.ix_(list(G), fl)] - Uf[list(G), fm][:, None]) / scale[list(G)][:, None]
            best[G] = float(dl.min(0).max())
    R['T3'] = dict(profitable_deviations_inside_last_box=inside, passed=inside == 0)
    R['T4'] = dict(passed=all(set(G) & newcomers and set(G) & earlier for G in groups))
    minimal = [G for G in groups if not any(set(H) < set(G) for H in groups)]
    R['original_game'] = dict(groups_with_profitable_deviation=len(groups), minimal_groups=[gname(G) for G in minimal],
                              largest_margin=max(best.values()) if best else None,
                              strictly_strong_equilibrium=len(groups) == 0)
    log('T3', R['T3']['passed'], '| T4', R['T4']['passed'], '| groups that can still gain:', len(groups))
    R['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, 'tower_relaxed.json'), 'w'), indent=1)
    log('done')


if __name__ == '__main__':
    main()
