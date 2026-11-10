"""Phase 0, second instance (instance2.py): contested levers and an empty core; exercises the fallbacks.

Tests and pass marks, fixed before the first run of this script:
  E1 emptiness reported by the heuristic search: enumeration finds no core profile inside the acceptable
     region. PASS iff none of 8 heuristic runs returns a profile. (A returned profile would be a false
     certificate.) Known weakness, stated in advance: a run that stops because its local search finds
     no candidate looks the same as a run that excluded every candidate.
  E2 mechanism against certificate logic at the fallback profile: every joint deviation of every group
     to unconditional actions is run through the registry rule. PASS iff the groups with a profitable
     deviation are exactly the strict blockers together with the groups that gain by over-fulfilment.
  E3 two code paths agree on emptiness: core.strict_core returns no profile, and fallbacks.strict_blockers
     finds at least one blocking group for every individually rational, acceptable profile. PASS iff both.
Selection rule of the fallback, fixed before the first run: smallest blocking margin among individually
rational, acceptable profiles; ties broken by the largest product of normalised gains, then by flat index.
"""
import json
import os
import sys
import time
from itertools import product
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import instance2
sys.modules['instance'] = instance2          # mechanism.py and search.py read their instance from this name
from instance2 import (ACTORS, N, LEVERS, ISSUES, ISSUE_OF, SHAPE, D, OWNER, DIMS, NPROF, BASE, PROVENANCE,
                       evaluate, describe)
import core
import fallbacks
import mechanism
from search import Search

OUT = os.path.join(HERE, 'results2')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def prof(f):
    return np.array(np.unravel_index(int(f), SHAPE))


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def main(heur_seeds=8):
    R = dict(meta=dict(date='2026-11-10', n_profiles=NPROF, n_actors=N, n_levers=D, n_coalitions=2 ** N - 1))
    ev = evaluate(BASE)
    U, acc = ev['U'], ev['acc']
    Uf = U.reshape(N, -1)
    U0 = Uf[:, 0].copy()
    gains = Uf - U0[:, None]

    # ---- orientation test: which levers are contested
    viol = core.orientation(U, OWNER)
    R['orientation'] = dict(
        passed=len(viol) == 0,
        owner_side=[f'{LEVERS[d][0]}.{LEVERS[d][1]}' for d, i, n, mx in viol if i == OWNER[d]],
        contested=[dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', harmed=ACTORS[i], largest=mx)
                   for d, i, n, mx in viol if i != OWNER[d]])
    log('orientation: contested levers', len(R['orientation']['contested']), '| owner side', R['orientation']['owner_side'])

    # ---- acceptable region and core
    C = acc.all(0)
    ir = np.all(Uf >= U0[:, None] - 1e-9, axis=0)
    cand = np.flatnonzero(C.reshape(-1) & ir)
    scale = gains[:, cand].max(1)
    scale = np.where(scale > 0, scale, 1.0)
    R['acceptable'] = dict(n=int(C.sum()), per_actor={a: float(acc[i].mean()) for i, a in enumerate(ACTORS)},
                           n_ir=int(ir.sum()), n_ir_and_acceptable=int(len(cand)))
    R['scale'] = {a: float(scale[i]) for i, a in enumerate(ACTORS)}
    core_idx, info = core.strict_core(U, OWNER, C)
    R['core'] = dict(n_candidates=info['n_candidates'], n_efficient=info.get('n_efficient', 0), n_core=int(len(core_idx)),
                     blocked={gname(G): n for G, n in info['blocked'].items()})
    core_all, info_all = core.strict_core(U, OWNER, np.ones(SHAPE, bool))
    R['core_without_aspirations'] = dict(n_ir=info_all['n_ir'], n_efficient=info_all.get('n_efficient', 0),
                                         n_core=int(len(core_all)))
    log('core inside C:', len(core_idx), 'of', len(cand), 'candidates | without aspirations:', len(core_all),
        'of', info_all['n_ir'])

    # ---- E3: second code path
    n_unblocked = sum(len(fallbacks.strict_blockers(U, OWNER, int(f))) == 0 for f in cand)
    R['E3'] = dict(strict_core_empty=len(core_idx) == 0, candidates_without_blocker=int(n_unblocked),
                   passed=bool(len(core_idx) == 0 and n_unblocked == 0))
    log('E3', 'PASSED' if R['E3']['passed'] else 'NOT PASSED')

    # ---- fallback 1: smallest blocking margin
    lm = fallbacks.least_margin(U, OWNER, cand, scale)
    Gn = gains[:, cand] / scale[:, None]
    logn = np.where((Gn > 0).all(0), np.log(np.maximum(Gn, 1e-300)).sum(0), -np.inf)
    rows = lm['minimiser_rows']
    j = int(rows[np.lexsort((cand[rows], -logn[rows]))[0]])
    f = int(cand[j])
    a = prof(f)
    Gs = lm['coalitions']
    blockers = fallbacks.strict_blockers(U, OWNER, f)
    over = core.over_fulfilment(U, OWNER, a)
    R['fallback1'] = dict(
        eps=lm['eps'], n_minimisers=int(len(rows)), flat=f, profile=describe(a),
        margin_distribution=dict(min=float(lm['worst'].min()), median=float(np.median(lm['worst'])),
                                 max=float(lm['worst'].max())),
        gain={ACTORS[i]: float(gains[i, f]) for i in range(N)},
        norm_gain={ACTORS[i]: float(gains[i, f] / scale[i]) for i in range(N)},
        Q=float(ev['Q'].reshape(-1)[f]), T=int(ev['T'].reshape(-1)[f]),
        margins={gname(G): float(lm['E'][j, k]) for k, G in enumerate(Gs)},
        strict_blockers=[gname(G) for G in blockers],
        smallest_blocking_group=min(len(G) for G in blockers) if blockers else None,
        pareto_efficient=tuple(range(N)) not in blockers,
        coalitions_gaining_by_over_fulfilment=over)
    log('fallback 1: eps', round(lm['eps'], 4), '| minimisers', len(rows), '| profile', [int(x) for x in a], '| blockers',
        R['fallback1']['strict_blockers'])

    # ---- [post hoc] added after the first run showed that the fallback profile is Pareto-dominated:
    # the same selection rule restricted to candidates that no profile Pareto-dominates
    eff = info.get('efficient_idx', np.array([], int))
    if len(eff):
        pe = np.flatnonzero(np.isin(cand, eff))
        we = lm['worst'][pe]
        re_ = pe[np.flatnonzero(we <= we.min() + 1e-12)]
        je = int(re_[np.lexsort((cand[re_], -logn[re_]))[0]])
        fe = int(cand[je])
        R['fallback1_efficient_post_hoc'] = dict(
            n_efficient_candidates=int(len(eff)), eps=float(lm['worst'][je]), flat=fe, profile=describe(prof(fe)),
            norm_gain={ACTORS[i]: float(gains[i, fe] / scale[i]) for i in range(N)},
            Q=float(ev['Q'].reshape(-1)[fe]), T=int(ev['T'].reshape(-1)[fe]),
            strict_blockers=[gname(G) for G in fallbacks.strict_blockers(U, OWNER, fe)],
            coalitions_gaining_by_over_fulfilment=core.over_fulfilment(U, OWNER, prof(fe)))
        log('fallback 1 among efficient candidates [post hoc]: eps', round(float(lm['worst'][je]), 4),
            '| profile', [int(x) for x in prof(fe)])

    # ---- E2: registry rule at the fallback profile, all deviations to unconditional actions
    ccfs = [mechanism.canonical(i, a) for i in range(N)]
    R['fallback1']['registry_returns_profile'] = bool(np.array_equal(mechanism.outcome(ccfs), a))
    ua = Uf[:, f]
    dev_groups, n_dev, mism = {}, 0, 0
    for G in core.coalitions(N):
        own = [d for i in G for d in DIMS[i]]
        for x in product(*[range(SHAPE[d]) for d in own]):
            xa = np.zeros(D, int)
            xa[own] = x
            cc = [mechanism.constant(i, xa[DIMS[i]]) if i in G else ccfs[i] for i in range(N)]
            o = mechanism.outcome(cc)
            n_dev += 1
            mism += int(not np.array_equal(o, mechanism.closed_form_deviation(a, G, {i: xa[DIMS[i]] for i in G})))
            uo = Uf[:, int(np.ravel_multi_index(tuple(o), SHAPE))]
            g = list(G)
            if np.all(uo[g] >= ua[g] - 1e-9) and np.any(uo[g] > ua[g] + 1e-9):
                dev_groups[G] = dev_groups.get(G, 0) + 1
    over_groups = set()
    for G in core.coalitions(N):
        idx = tuple(slice(int(a[d]), None) if OWNER[d] in G else int(a[d]) for d in range(D))
        rws = np.stack([np.asarray(U[i][idx]).reshape(-1) for i in G], axis=1)
        u = ua[list(G)]
        ge = np.all(rws >= u - 1e-9, axis=1)
        if ge.any() and np.any(rws[ge] > u + 1e-9):
            over_groups.add(G)
    expect = set(blockers) | over_groups
    R['E2'] = dict(n_deviations=n_dev, registry_vs_closed_form_mismatches=mism,
                   groups_with_profitable_deviation={gname(G): n for G, n in dev_groups.items()},
                   expected_groups=sorted(gname(G) for G in expect),
                   no_single_actor_deviates=not any(len(G) == 1 for G in dev_groups),
                   passed=bool(set(dev_groups) == expect and mism == 0))
    log('E2', 'PASSED' if R['E2']['passed'] else 'NOT PASSED', '| deviating groups', R['E2']['groups_with_profitable_deviation'])

    # ---- fallback 3: sub-packages
    sp = fallbacks.subpackage_cores(U, OWNER, ISSUE_OF, ISSUES, acc)
    R['fallback3'] = {k: {x: y for x, y in v.items() if x.startswith('n_')} for k, v in sp.items()}
    best = None
    for k, v in sp.items():
        if v['n_core_in_C'] == 0:
            continue
        dims = v['dims']
        sub_shape = tuple(SHAPE[d] for d in dims)
        full = []
        for fl in v['core_in_C_flat']:
            b = np.zeros(D, int)
            b[dims] = np.unravel_index(int(fl), sub_shape)
            full.append(int(np.ravel_multi_index(tuple(b), SHAPE)))
        full = np.array(full)
        gk = gains[:, full] / scale[:, None]
        lg = np.where((gk > 0).all(0), np.log(np.maximum(gk, 1e-300)).sum(0), -np.inf)
        fb = int(full[int(np.argmax(lg))])
        Eb, _ = fallbacks.margin_table(U, OWNER, np.array([fb]), scale)
        blk = fallbacks.strict_blockers(U, OWNER, fb)
        R['fallback3'][k]['nash_point'] = dict(
            flat=fb, profile=describe(prof(fb)), acceptable_to_all=bool(C.reshape(-1)[fb]),
            gain={ACTORS[i]: float(gains[i, fb]) for i in range(N)},
            norm_gain={ACTORS[i]: float(gains[i, fb] / scale[i]) for i in range(N)},
            Q=float(ev['Q'].reshape(-1)[fb]),
            margin_in_package_game=float(Eb.max()), blockers_in_package_game=[gname(G) for G in blk])
        best = k
    R['fallback3']['subpackage_with_core'] = best
    log('fallback 3:', {k: (v['n_core'], v['n_core_in_C']) for k, v in sp.items()})

    # ---- [exploration, no pass mark] bounded coordination and diplomatic channels (plan, section
    # "Bounded rationality and diplomatic knowledge"). Added on Jobst's request after the tests above.
    # Which candidates are stable if only some groups can coordinate, or if actors move only for a
    # normalised gain above a threshold? CHANNELS is an illustrative relationship graph [assumption]:
    # USA and CHN have no bilateral channel; a group can coordinate iff it is connected in the graph.
    CHANNELS = [('USA', 'EU'), ('CHN', 'EU')]

    def connected(G):
        G = set(G)
        seen, todo = set(), [min(G)]
        while todo:
            i = todo.pop()
            seen.add(i)
            for x, y in CHANNELS:
                x, y = ACTORS.index(x), ACTORS.index(y)
                for u, v in ((x, y), (y, x)):
                    if u == i and v in G and v not in seen:
                        todo.append(v)
        return seen == G
    families = {'all groups': list(Gs),
                'single actors only': [G for G in Gs if len(G) == 1],
                'groups of at most two': [G for G in Gs if len(G) <= 2],
                'groups connected by a channel': [G for G in Gs if connected(G)]}
    blk_all = [set(fallbacks.strict_blockers(U, OWNER, int(x))) for x in cand]
    R['restricted'] = dict(channels=CHANNELS, families={})
    for name, fam in families.items():
        cols = [Gs.index(G) for G in fam]
        worst = lm['E'][:, cols].max(1)
        stable = np.array([not (b & set(fam)) for b in blk_all])
        rws = np.flatnonzero(worst <= worst.min() + 1e-12)
        jf = int(rws[np.lexsort((cand[rws], -logn[rws]))[0]])
        entry = dict(groups=[gname(G) for G in fam], n_stable=int(stable.sum()), least_margin=float(worst.min()),
                     least_margin_profile=describe(prof(cand[jf])),
                     least_margin_norm_gain={ACTORS[i]: float(Gn[i, jf]) for i in range(N)},
                     least_margin_blockers_among_all_groups=[gname(G) for G in sorted(blk_all[jf])],
                     least_margin_among_all_groups=float(lm['worst'][jf]))
        if stable.any():
            st = np.flatnonzero(stable)
            jb = int(st[int(np.argmax(logn[st]))])
            fb = int(cand[jb])
            entry['nash_among_stable'] = dict(
                flat=fb, profile=describe(prof(fb)), Q=float(ev['Q'].reshape(-1)[fb]), T=int(ev['T'].reshape(-1)[fb]),
                norm_gain={ACTORS[i]: float(gains[i, fb] / scale[i]) for i in range(N)},
                blockers_among_all_groups=[gname(G) for G in sorted(blk_all[jb])],
                margin_among_all_groups=float(lm['worst'][jb]))
        R['restricted']['families'][name] = entry
    R['restricted']['n_candidates_with_margin_at_most'] = {
        f'{e:.2f}': int((lm['worst'] <= e + 1e-12).sum()) for e in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)}
    log('restricted families:', {k: (v['n_stable'], round(v['least_margin'], 3)) for k, v in R['restricted']['families'].items()},
        '| by threshold:', R['restricted']['n_candidates_with_margin_at_most'])

    # ---- E1: heuristic search on an instance with an empty core
    runs = []
    for s in range(heur_seeds):
        S = Search(U, acc, scale, np.random.default_rng(2000 + s))
        res = S.run(max_rounds=600)
        runs.append(dict(seed=s, returned_profile=res['profile'] is not None, rounds=res['rounds'], cuts=res['cuts'],
                         evals=res['evals'], candidates_left_uncut=int((S.ok & ~S.excl).sum())))
        log(f'  E1 seed {s}:', runs[-1])
    R['E1'] = dict(runs=runs, passed=bool(not any(r['returned_profile'] for r in runs)),
                   runs_that_excluded_every_candidate=sum(r['candidates_left_uncut'] == 0 for r in runs))
    log('E1', 'PASSED' if R['E1']['passed'] else 'NOT PASSED')

    json.dump(dict(base=BASE, provenance=PROVENANCE,
                   levers=[dict(actor=a_, lever=l, levels=n, issue=iss) for a_, l, n, iss in LEVERS]),
              open(os.path.join(OUT, 'params.json'), 'w'), indent=1)
    R['meta']['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
    log('done')
    return R


if __name__ == '__main__':
    main()
