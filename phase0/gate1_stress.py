"""Gate 1 stress tests.

Added after the first run showed that the criterion fixed in run_phase0.py was met without the
coalitional refinement ever being used (no cut was needed). Variant used here: the same instance
without the aspiration filter, in which enumeration finds efficient, individually rational
profiles that proper coalitions block.

Criteria, fixed before these tests were run:
  B1 oracle recall: the oracle finds a block for at least 95 % of a random sample of 300 profiles
     that enumeration knows to be efficient, individually rational and blocked by a proper coalition.
  B1 hold-out (added after the repair of the oracle): the same test for the second oracle on 300
     further blocked profiles that no oracle had been run on. Same pass mark.
  B2 actor-optimal core points: for each actor, maximise that actor's normalised gain (weight 1,
     all other actors 0.01) over the core, 3 seeds each. Pass iff every returned profile is in the
     exact strict core and at least 75 % of the runs are within 0.01 of the enumerated optimum.
"""
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instance import ACTORS, N, SHAPE, OWNER, NPROF, BASE, evaluate
import core
from search import Search

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def main():
    ev = evaluate(BASE)
    U = ev['U']
    Uf = U.reshape(N, -1)
    U0 = Uf[:, 0].copy()
    acc = np.ones((N,) + SHAPE, bool)
    cache = os.path.join(OUT, 'cache_core_no_aspirations.npz')
    if os.path.exists(cache):
        z = np.load(cache)
        core_idx, eff_idx = z['core_idx'], z['eff_idx']
    else:
        core_idx, info = core.strict_core(U, OWNER, np.ones(SHAPE, bool), log)
        eff_idx = info['efficient_idx']
        np.savez(cache, core_idx=core_idx, eff_idx=eff_idx)
    blocked = np.setdiff1d(eff_idx, core_idx)
    log('no-aspiration variant: efficient IR', len(eff_idx), '| strict core', len(core_idx),
        '| blocked by proper coalitions', len(blocked))
    ir = np.all(Uf >= U0[:, None] - 1e-9, axis=0)
    gains = Uf - U0[:, None]
    scale = gains[:, ir].max(1)
    R = dict(n_efficient=int(len(eff_idx)), n_core=int(len(core_idx)), n_blocked=int(len(blocked)))

    # B1: oracle recall on known-blocked profiles
    rng = np.random.default_rng(7)
    sample = rng.choice(blocked, size=min(300, len(blocked)), replace=False)
    S = Search(U, acc, scale, np.random.default_rng(8))
    hit = hit1 = bad = 0
    sizes = {}
    for f in sample:
        a = np.array(np.unravel_index(int(f), SHAPE))
        if S.oracle_v1(a) is not None:
            hit1 += 1
        blk = S.oracle(a)
        if blk is not None:
            hit += 1
            Gc, b = blk
            g_ = list(Gc)
            dl = S.G[g_, S.flat(b)] - S.G[g_, int(f)]
            outs = [d for d in range(len(SHAPE)) if OWNER[d] not in Gc]
            if not (dl.min() >= -1e-9 and dl.max() > 1e-9 and np.all(b[outs] == 0)):
                bad += 1
            sizes[len(Gc)] = sizes.get(len(Gc), 0) + 1
    # false alarms: the oracle must find nothing on profiles that enumeration puts in the core
    fa = 0
    for f in rng.choice(core_idx, size=200, replace=False):
        if S.oracle(np.array(np.unravel_index(int(f), SHAPE))) is not None:
            fa += 1
    R['B1'] = dict(n=int(len(sample)), detected=hit, recall=hit / len(sample), passed=hit / len(sample) >= 0.95,
                   detected_by_first_version=hit1, recall_first_version=hit1 / len(sample),
                   invalid_blocks=bad, blocking_coalition_sizes=sizes, false_alarms_on_200_core_profiles=fa)
    log('B1 oracle recall: v2', hit, '/', len(sample), '| v1', hit1, '| invalid', bad, '| false alarms', fa, '| sizes', sizes)

    # B1b, added after the repair: the second oracle on a hold-out sample it was never run on before
    rest = np.setdiff1d(blocked, sample)
    hold = np.random.default_rng(11).choice(rest, size=min(300, len(rest)), replace=False)
    S = Search(U, acc, scale, np.random.default_rng(12))
    hit_h = sum(S.oracle(np.array(np.unravel_index(int(f), SHAPE))) is not None for f in hold)
    R['B1_holdout'] = dict(n=int(len(hold)), detected=int(hit_h), recall=hit_h / len(hold),
                           passed=hit_h / len(hold) >= 0.95)
    log('B1 hold-out: v2', hit_h, '/', len(hold))

    # B2: actor-optimal core points
    Gn = gains[:, core_idx] / scale[:, None]
    core_set = set(int(x) for x in core_idx)
    runs = []
    for i in range(N):
        w = np.full(N, 0.01)
        w[i] = 1.0
        best = float((w[:, None] * np.log(np.maximum(Gn, 1e-3))).sum(0).max())
        for s in range(3):
            S = Search(U, acc, scale, np.random.default_rng(100 * i + s), weights=w)
            t = time.time()
            res = S.run(max_rounds=300)
            if res['profile'] is None:
                runs.append(dict(actor=ACTORS[i], seed=s, found=False, rounds=res['rounds'], cuts=res['cuts']))
                log(f'  B2 {ACTORS[i]} seed {s}: no profile returned after', res['rounds'], 'rounds')
                continue
            f = int(np.ravel_multi_index(tuple(res['profile']), SHAPE))
            val = float((w * np.log(np.maximum(gains[:, f] / scale, 1e-3))).sum())
            runs.append(dict(actor=ACTORS[i], seed=s, found=True, in_core=f in core_set, gap=best - val,
                             rounds=res['rounds'], cuts=res['cuts'], evals=res['evals'],
                             seconds=round(time.time() - t, 1)))
            log(f'  B2 {ACTORS[i]} seed {s}:', {k: runs[-1][k] for k in ('in_core', 'gap', 'rounds', 'cuts', 'seconds')})
    all_core = all(r.get('found') and r['in_core'] for r in runs)
    share = float(np.mean([bool(r.get('found')) and r['gap'] <= 0.01 for r in runs]))
    R['B2'] = dict(runs=runs, all_in_core=all_core, share_reaching_optimum=share,
                   passed=bool(all_core and share >= 0.75),
                   mean_cuts=float(np.mean([r['cuts'] for r in runs])),
                   mean_share_of_profiles_evaluated=float(np.mean([r.get('evals', NPROF) for r in runs]) / NPROF))
    R['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, 'gate1_stress.json'), 'w'), indent=1)
    log('B1', 'PASSED' if R['B1']['passed'] else 'NOT PASSED', '| B2', 'PASSED' if R['B2']['passed'] else 'NOT PASSED',
        '| all in core:', all_core, '| share reaching optimum:', share)


if __name__ == '__main__':
    main()
