"""Phase 0: towers in a pre-CPEP (see tower.py), on the two toys with contested levers.

Usage: python3 run_tower.py contested | instance2

Chain rule, fixed before the first run: H is the set of actors harmed by some contested lever at the base
point (orientation test). The chain is I_1 = I minus H, I_2 = I. If I_1 is empty there is no chain.
Selection rule, fixed before the first run: at each stage, among the strict-core profiles of the stage
game that are acceptable to the stage's members (at the last stage: to all), and, before the last stage,
leave a proper CPEP for the next stage: the largest smallest normalised gain of a member over the stage
reference, then the largest sum of these gains, then the smallest flat index. If the aspiration filter
leaves nothing at some stage, the whole tower is rebuilt without the filter and the result is labelled so.

Tests and pass marks, fixed before the first run:
  T1 registry: the nested step filing returns b_m. If the newcomers of stage k file zero, it returns
     b_(k-1) on the old members' levers (b_0 = 0). PASS iff both hold for every stage.
  T2 condition (ii) by direct test: in every stage game, no group inside the coalition has a profitable
     deviation inside the stage box. PASS iff none.
  T3 original game, inside the last box: over all groups and all unconditional deviations, run through the
     registry rule, no profitable deviation has an outcome at or above b_(m-1). PASS iff none.
  T4 original game, who can upset the tower: every group with a profitable deviation contains a newcomer
     of the last stage and a member of an earlier stage. PASS iff so.
T3 and T4 follow from (ii) for step towers; they test the software and the argument, not Jobst's conjecture.
The conjecture itself ("c should be pretty stable in the original pre-CPEP") is reported as a finding:
which groups can still gain, by how many deviations, and at what margin.
"""
import importlib
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
which = sys.argv[1] if len(sys.argv) > 1 else 'contested'
inst = importlib.import_module('instance2' if which == 'instance2' else 'instance')
ACTORS, N, LEVERS, SHAPE, D, OWNER, DIMS, BASE = (inst.ACTORS, inst.N, inst.LEVERS, inst.SHAPE, inst.D,
                                                 inst.OWNER, inst.DIMS, inst.BASE)
import core
import tower

KAPPA = 0.20
OUT = os.path.join(HERE, 'results2')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def build(U, acc, viol, chain, scale, use_asp):
    """Build one tower along the chain by the selection rule. Returns (stages, info) or (None, info)."""
    Uf = U.reshape(N, -1)
    lower = np.zeros(D, int)
    stages, info = [], []
    for k, members in enumerate(chain):
        last = k == len(chain) - 1
        Uk, dims, owner_k, sub = tower.stage_game(U, OWNER, members, lower)
        st = dict(members=[ACTORS[i] for i in members], lower=[int(x) for x in lower],
                  box_profiles=int(np.prod(sub)), is_cpep=bool(tower.box_is_cpep(viol, OWNER, members, lower)))
        if not st['is_cpep']:
            info.append(st)
            return None, info
        ck, ci = core.strict_core(Uk, owner_k, np.ones(sub, bool))
        st['n_core'] = int(len(ck))
        full = np.array([tower.to_full(f, dims, sub, lower, D) for f in ck]).reshape(-1, D)
        fl = np.ravel_multi_index(full.T, SHAPE) if len(full) else np.array([], int)
        keep = np.ones(len(fl), bool)
        if use_asp:
            who = list(range(N)) if last else list(members)
            keep &= acc.reshape(N, -1)[np.ix_(who, fl)].all(0)
        st['n_core_acceptable'] = int(keep.sum())
        if not last:
            nxt = chain[k + 1]
            keep &= np.array([tower.box_is_cpep(viol, OWNER, nxt, b) for b in full], bool) if len(full) else keep
        st['n_candidates'] = int(keep.sum())
        if not keep.any():
            info.append(st)
            return None, info
        ref = int(np.ravel_multi_index(tuple(lower), SHAPE))
        m = list(members)
        g = (Uf[np.ix_(m, fl[keep])] - Uf[m, ref][:, None]) / scale[m][:, None]
        order = np.lexsort((fl[keep], -g.sum(0), -g.min(0)))
        j = np.flatnonzero(keep)[order[0]]
        b = full[j]
        st.update(flat=int(fl[j]), profile=inst.describe(b), smallest_stage_gain=float(g[:, order[0]].min()),
                  stage_gain={ACTORS[i]: float(x) for i, x in zip(m, g[:, order[0]])},
                  nontrivial=bool(np.any(b != lower)))
        info.append(st)
        stages.append((set(members), b.copy()))
        lower = b.copy()
    return stages, info


def main():
    ev = inst.evaluate(BASE)
    U, acc = ev['U'].copy(), ev['acc']
    if which == 'contested':
        g = inst.grids()
        U[ACTORS.index('DEV')] -= KAPPA * (g[1] + g[3])
    Uf = U.reshape(N, -1)
    gains = Uf - Uf[:, [0]]
    C = acc.all(0).reshape(-1)
    ir = np.all(gains >= -1e-9, axis=0)
    scale = gains[:, C & ir].max(1)
    scale = np.where(scale > 0, scale, 1.0)
    viol = tower.violation_steps(U, OWNER)
    harmed = sorted({i for (d, i) in viol if i != OWNER[d]})
    R = dict(instance=which, contested=[dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', harmed=ACTORS[i])
                                        for (d, i) in viol if i != OWNER[d]],
             owner_side=[f'{LEVERS[d][0]}.{LEVERS[d][1]}' for (d, i) in viol if i == OWNER[d]],
             harmed=[ACTORS[i] for i in harmed])
    # which bases leave a proper CPEP for the grand coalition? (needed for any last stage)
    grid = np.array(np.unravel_index(np.arange(int(np.prod(SHAPE))), SHAPE)).T
    okb = np.array([tower.box_is_cpep(viol, OWNER, range(N), b) for b in grid])
    active = np.array([[grid[:, DIMS[i]].any(1)] for i in range(N)]).reshape(N, -1)
    R['bases'] = dict(n_profiles=int(len(grid)), n_leaving_a_cpep_for_all=int(okb.sum()),
                      of_these_with_an_inactive_actor=int((okb & ~active.all(0)).sum()),
                      coalitions_that_form_a_cpep_from_zero=[gname(G) for G in core.coalitions(N)
                                                             if tower.box_is_cpep(viol, OWNER, G, np.zeros(D, int))])
    log('harmed:', R['harmed'], '| bases leaving a CPEP for all:', R['bases']['n_leaving_a_cpep_for_all'],
        '| with an inactive actor:', R['bases']['of_these_with_an_inactive_actor'])
    I1 = [i for i in range(N) if i not in harmed]
    if not I1:
        R['tower'] = None
        R['reason'] = 'chain rule gives an empty first coalition'
        log('no chain: every actor is harmed by some contested lever')
        json.dump(R, open(os.path.join(OUT, f'tower_{which}.json'), 'w'), indent=1)
        return
    chain = [I1, list(range(N))]
    R['chain'] = [[ACTORS[i] for i in S] for S in chain]
    stages, info = build(U, acc, viol, chain, scale, use_asp=True)
    R['with_aspirations'] = dict(found=stages is not None, stages=info)
    log('with aspirations:', 'tower found' if stages else 'no tower', [(s.get('n_core'), s.get('n_core_acceptable'), s.get('n_candidates')) for s in info])
    R['aspiration_filter_used'] = stages is not None
    if stages is None:
        stages, info2 = build(U, acc, viol, chain, scale, use_asp=False)
        R['without_aspirations'] = dict(found=stages is not None, stages=info2)
        log('without aspirations:', 'tower found' if stages else 'no tower', [(s.get('n_core'), s.get('n_candidates')) for s in info2])
    if stages is None:
        R['tower'] = None
        json.dump(R, open(os.path.join(OUT, f'tower_{which}.json'), 'w'), indent=1)
        return
    bs = [b for _, b in stages]
    bm = bs[-1]
    fm = int(np.ravel_multi_index(tuple(bm), SHAPE))
    R['tower'] = dict(outcomes=[inst.describe(b) for b in bs], final_flat=fm,
                      final_acceptable_to_all=bool(C[fm]),
                      final_gain_over_a0={ACTORS[i]: float(gains[i, fm]) for i in range(N)},
                      final_norm_gain_over_a0={ACTORS[i]: float(gains[i, fm] / scale[i]) for i in range(N)},
                      indicators={k: float(ev[k].reshape(-1)[fm]) for k in ('Q', 'A', 'P') if k in ev},
                      stage1_indicators={k: float(ev[k].reshape(-1)[int(np.ravel_multi_index(tuple(bs[0]), SHAPE))])
                                         for k in ('Q', 'A', 'P') if k in ev})
    # T1
    zero = np.zeros((1, D), int)
    t1 = bool(np.array_equal(tower.registry(stages, SHAPE, OWNER, set(), zero)[0], bm))
    prev = np.zeros(D, int)
    for k, (members, b) in enumerate(stages):
        new = members - (stages[k - 1][0] if k else set())
        o = tower.registry(stages, SHAPE, OWNER, new, zero)[0]
        old = np.array([OWNER[d] not in new for d in range(D)])
        t1 &= bool(np.array_equal(o[old], prev[old]))
        prev = b
    R['T1'] = dict(passed=t1)
    # T2
    lower = np.zeros(D, int)
    t2 = {}
    for k, (members, b) in enumerate(stages):
        res = tower.stage_deviations(U, SHAPE, OWNER, members, lower, b)
        t2[f'stage {k + 1}'] = {gname(G): n for G, n in res.items()}
        lower = b
    R['T2'] = dict(profitable_by_stage=t2, passed=all(len(v) == 0 for v in t2.values()))
    log('T1', 'PASSED' if R['T1']['passed'] else 'NOT PASSED', '| T2', 'PASSED' if R['T2']['passed'] else 'NOT PASSED')
    # T3, T4 and the finding: all groups, all unconditional deviations, original game
    bprev = bs[-2] if len(bs) > 1 else np.zeros(D, int)
    earlier = stages[-2][0] if len(stages) > 1 else set()
    newcomers = stages[-1][0] - earlier
    old_levers = np.array([OWNER[d] in earlier for d in range(D)])
    groups, inside, n_dev = {}, 0, 0
    best = {}
    for G in core.coalitions(N):
        dv = tower.all_devs(SHAPE, OWNER, G)
        out = tower.registry(stages, SHAPE, OWNER, set(G), dv)
        pm = tower.profitable(U, SHAPE, G, out, fm)
        n_dev += len(dv)
        if pm.any():
            groups[G] = int(pm.sum())
            inside += int(np.all(out[pm][:, old_levers] >= bprev[old_levers], axis=1).sum())
            fl = np.ravel_multi_index(out[pm].T, SHAPE)
            dl = (Uf[np.ix_(list(G), fl)] - Uf[list(G), fm][:, None]) / scale[list(G)][:, None]
            j = int(np.argmax(dl.min(0)))
            best[G] = (float(dl.min(0)[j]), inst.describe(out[pm][j]))
    R['T3'] = dict(profitable_deviations_inside_last_box=inside, passed=inside == 0)
    R['T4'] = dict(passed=all(set(G) & newcomers and set(G) & earlier for G in groups))
    minimal = [G for G in groups if not any(set(H) < set(G) for H in groups)]
    top = max(best, key=lambda G: best[G][0]) if best else None
    R['original_game'] = dict(
        n_deviations=n_dev, n_groups=2 ** N - 1, groups_with_profitable_deviation=len(groups),
        minimal_groups=[gname(G) for G in minimal],
        largest_margin=None if top is None else dict(group=gname(top), margin=best[top][0], outcome=best[top][1]),
        strictly_strong_equilibrium=len(groups) == 0)
    log('T3', 'PASSED' if R['T3']['passed'] else 'NOT PASSED', '| T4', 'PASSED' if R['T4']['passed'] else 'NOT PASSED',
        '| groups that can still gain:', len(groups), '| minimal:', R['original_game']['minimal_groups'])
    R['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, f'tower_{which}.json'), 'w'), indent=1)
    log('done')


if __name__ == '__main__':
    main()
