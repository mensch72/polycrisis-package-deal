"""Phase 0: contested-lever variant of the first instance; a harder test of the heuristic search.

Variant: developers bear a compliance burden of KAPPA per level of state AI oversight. Both oversight
levers then harm DEV, so the orientation test fails at the base point and the theorems of Heitzig (2025)
do not apply. Stability is therefore certified directly. KAPPA = 0.20 is illustrative (Claude,
10 November 2026). It was chosen after a scan of 0.10 to 0.40: at 0.10 no proper coalition blocks an
efficient profile inside the acceptable region, at 0.20 proper coalitions do. Everything else is instance.py.

Criterion G1c, fixed before the first run of this script; it is the Gate 1 criterion of run_phase0.py:
  PASS iff (a) every heuristic run returns a profile that the exhaustive search confirms to be acceptable
  and in the strict core, and (b) at least 75 % of the runs reach the enumerated optimum of the focal
  objective (difference in log Nash product <= 0.01). 8 runs, seeds 3000 to 3007.
"""
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instance import ACTORS, N, LEVERS, SHAPE, D, OWNER, NPROF, BASE, evaluate, describe, grids
import core
import mechanism
from search import Search

KAPPA = 0.20
OUT = os.path.join(HERE, 'results2')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def main(heur_seeds=8):
    ev = evaluate(BASE)
    U, acc = ev['U'].copy(), ev['acc']
    g = grids()
    U[ACTORS.index('DEV')] -= KAPPA * (g[1] + g[3])
    Uf = U.reshape(N, -1)
    U0 = Uf[:, 0].copy()
    gains = Uf - U0[:, None]
    C = acc.all(0)
    R = dict(kappa=KAPPA)
    viol = core.orientation(U, OWNER)
    R['orientation'] = dict(passed=len(viol) == 0, violations=[
        dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', actor=ACTORS[i], largest=mx) for d, i, n, mx in viol])
    core_idx, info = core.strict_core(U, OWNER, C, log)
    ir = np.all(Uf >= U0[:, None] - 1e-9, axis=0)
    sel = C.reshape(-1) & ir
    scale = gains[:, sel].max(1)
    n_proper = sum(n for G, n in info['blocked'].items() if len(G) < N)
    R['core'] = dict(n_ir=info['n_ir'], n_candidates=info['n_candidates'], n_efficient=info['n_efficient'],
                     n_core=int(len(core_idx)), blocked_by_proper_coalitions=int(n_proper),
                     blocked={gname(G): n for G, n in info['blocked'].items()})
    log('core inside C:', len(core_idx), '| efficient', info['n_efficient'], '| blocked by proper coalitions', n_proper)
    Gn = gains[:, core_idx] / scale[:, None]
    logn = np.where((Gn > 0).all(0), np.log(np.maximum(Gn, 1e-300)).sum(0), -np.inf)
    best_log = float(logn.max())
    f = int(core_idx[int(np.argmax(logn))])
    a = np.array(np.unravel_index(f, SHAPE))
    ok, _ = core.in_strict_core(U, OWNER, f)
    ccfs = [mechanism.canonical(i, a) for i in range(N)]
    over = core.over_fulfilment(U, OWNER, a)
    reg = bool(np.array_equal(mechanism.outcome(ccfs), a))
    R['nash'] = dict(flat=f, profile=describe(a), norm_gain={ACTORS[i]: float(gains[i, f] / scale[i]) for i in range(N)},
                     Q=float(ev['Q'].reshape(-1)[f]), A=float(ev['A'].reshape(-1)[f]), P=float(ev['P'].reshape(-1)[f]),
                     certificate=dict(individually_rational=bool(np.all(gains[:, f] >= -1e-9)),
                                      acceptable_to_all=bool(C.reshape(-1)[f]), strict_core_by_direct_test=bool(ok),
                                      registry_returns_profile=reg, coalitions_gaining_by_over_fulfilment=over,
                                      strictly_strong_equilibrium_certified=bool(ok and reg and over == 0)))
    log('Nash point', [int(x) for x in a], R['nash']['certificate'])
    # ---- [post hoc] added after the first run showed that the Nash point is in the strict core but is not
    # an equilibrium: which core profiles are also free of gains by over-fulfilment, and which groups gain?
    P = np.array(np.unravel_index(core_idx, SHAPE)).T
    nover = np.array([core.over_fulfilment(U, OWNER, p) for p in P])
    eq = nover == 0
    groups = []
    ua = Uf[:, f]
    for G in core.coalitions(N):
        idx = tuple(slice(int(a[d]), None) if OWNER[d] in G else int(a[d]) for d in range(D))
        rows = np.stack([np.asarray(U[i][idx]).reshape(-1) for i in G], axis=1)
        u = ua[list(G)]
        ge = np.all(rows >= u - 1e-9, axis=1)
        if ge.any() and np.any(rows[ge] > u + 1e-9):
            groups.append(G)
    minimal = [G for G in groups if not any(set(H) < set(G) for H in groups)]
    R['over_fulfilment_post_hoc'] = dict(
        core_profiles=int(len(core_idx)), core_profiles_that_are_equilibria=int(eq.sum()),
        minimal_groups_gaining_at_nash=[gname(G) for G in minimal],
        dev_gain_at_nash=float(gains[ACTORS.index('DEV'), f]),
        equilibria_with_any_oversight=int((eq & ((P[:, 1] > 0) | (P[:, 3] > 0))).sum()),
        core_profiles_with_any_oversight=int(((P[:, 1] > 0) | (P[:, 3] > 0)).sum()))
    if eq.any():
        je = int(np.flatnonzero(eq)[int(np.argmax(logn[eq]))])
        fe = int(core_idx[je])
        R['over_fulfilment_post_hoc']['nash_among_equilibria'] = dict(
            flat=fe, profile=describe(P[je]), log_nash_gap_to_core_optimum=float(best_log - logn[je]),
            norm_gain={ACTORS[i]: float(gains[i, fe] / scale[i]) for i in range(N)},
            Q=float(ev['Q'].reshape(-1)[fe]), A=float(ev['A'].reshape(-1)[fe]), P=float(ev['P'].reshape(-1)[fe]))
    log('[post hoc] core profiles that are equilibria:', int(eq.sum()), 'of', len(core_idx),
        '| minimal over-fulfilling groups at the Nash point:', [gname(G) for G in minimal])
    runs = []
    core_set = set(int(x) for x in core_idx)
    for s in range(heur_seeds):
        S = Search(U, acc, scale, np.random.default_rng(3000 + s))
        t = time.time()
        res = S.run()
        if res['profile'] is None:
            runs.append(dict(seed=s, found=False, rounds=res['rounds'], cuts=res['cuts'], evals=res['evals']))
            log(f'  seed {s}: no profile returned')
            continue
        fh = int(np.ravel_multi_index(tuple(res['profile']), SHAPE))
        ln = float(np.log(np.maximum(gains[:, fh] / scale, 1e-300)).sum())
        runs.append(dict(seed=s, found=True, in_core=fh in core_set, acceptable=bool(C.reshape(-1)[fh]),
                         gap=best_log - ln, same_as_enumeration=fh == f, rounds=res['rounds'], cuts=res['cuts'],
                         evals=res['evals'], seconds=round(time.time() - t, 1)))
        log(f'  seed {s}:', {k: runs[-1][k] for k in ('in_core', 'gap', 'rounds', 'cuts', 'evals')})
    a_ok = all(r.get('found') and r['in_core'] and r['acceptable'] for r in runs)
    b_share = float(np.mean([bool(r.get('found')) and r['gap'] <= 0.01 for r in runs]))
    R['G1c'] = dict(runs=runs, all_in_core=a_ok, share_reaching_optimum=b_share, passed=bool(a_ok and b_share >= 0.75),
                    runs_with_cuts=sum(r['cuts'] > 0 for r in runs),
                    mean_share_of_profiles_evaluated=float(np.mean([r['evals'] for r in runs]) / NPROF))
    log('G1c:', 'PASSED' if R['G1c']['passed'] else 'NOT PASSED', '| all in core:', a_ok, '| share reaching optimum:', b_share)
    R['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, 'contested.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
