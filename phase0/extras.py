"""Phase 0: supporting numbers quoted in the write-up that the main pipeline does not store.

Reads results/results.json and results/core_acceptable.json; writes results/extras.json.
"""
import json
import os
import sys
from itertools import product
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instance import ACTORS, N, LEVERS, ISSUES, ISSUE_OF, SHAPE, D, OWNER, BASE, evaluate, perturbed
import core

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')


def main():
    R = json.load(open(os.path.join(OUT, 'results.json')))
    core_idx = np.array(json.load(open(os.path.join(OUT, 'core_acceptable.json'))))
    core_set = set(int(x) for x in core_idx)
    lead = R['menu'][R['lead']]['flat']
    ev = evaluate(BASE)
    U = ev['U']
    X = {}

    # 1. which actor's aspirations fail at the lead candidate, over the robustness set (same draws)
    rng = np.random.default_rng(R['meta']['seed'] + 1)
    fails = {a: 0 for a in ACTORS}
    n_fail = 0
    for _ in range(R['robustness']['n']):
        p, _fac = perturbed(rng)
        acc = evaluate(p, light=True)['acc'].reshape(N, -1)[:, lead]
        n_fail += int(not acc.all())
        for i, a in enumerate(ACTORS):
            fails[a] += int(not acc[i])
    X['lead_draws_not_acceptable'] = n_fail
    X['lead_failing_aspirations_by_actor'] = {a: v for a, v in fails.items() if v}

    # 2. the core inside the acceptable region: how often each lever level occurs
    cp = np.array(np.unravel_index(core_idx, SHAPE))
    X['core_level_counts'] = {f'{LEVERS[d][0]}.{LEVERS[d][1]}': np.bincount(cp[d], minlength=SHAPE[d]).tolist()
                              for d in range(D)}

    # 3. single-issue cores (no aspiration filter) and their combinations
    parts, X['single_issue_core_profiles'] = {}, {}
    for iss in ISSUES:
        dims = [d for d in range(D) if ISSUE_OF[d] == iss]
        idx = tuple(slice(None) if ISSUE_OF[d] == iss else 0 for d in range(D))
        Uk = U[(slice(None),) + idx]
        ck, _ = core.strict_core(Uk, OWNER[dims], np.ones(Uk.shape[1:], bool))
        prof = np.array(np.unravel_index(ck, Uk.shape[1:])).T
        parts[iss] = (dims, prof)
        X['single_issue_core_profiles'][iss] = dict(
            levers=[f'{LEVERS[d][0]}.{LEVERS[d][1]}' for d in dims], profiles=prof.tolist())
    C = ev['acc'].all(0).reshape(-1)
    n_comb = n_acc = n_core_C = n_core_full = 0
    for combo in product(*[parts[iss][1] for iss in ISSUES]):
        a = np.zeros(D, int)
        for iss, sub in zip(ISSUES, combo):
            a[parts[iss][0]] = sub
        f = int(np.ravel_multi_index(tuple(a), SHAPE))
        n_comb += 1
        n_acc += int(C[f])
        n_core_C += int(f in core_set)
        n_core_full += int(core.in_strict_core(U, OWNER, f)[0])
    X['combinations_of_single_issue_core_profiles'] = dict(
        n=n_comb, acceptable_to_all=n_acc, in_package_core_inside_acceptable_region=n_core_C,
        in_package_strict_core_ignoring_aspirations=n_core_full)
    X['indicator_max'] = {}
    for key, iss in zip('QAP', ISSUES):
        dims, prof = parts[iss]
        vals = []
        for sub in prof:
            a = np.zeros(D, int)
            a[dims] = sub
            vals.append(float(ev[key][tuple(a)]))
        X['indicator_max'][key] = dict(single_issue_core=max(vals),
                                       package_core=float(ev[key].reshape(-1)[core_idx].max()),
                                       lead=float(ev[key].reshape(-1)[lead]))
    json.dump(X, open(os.path.join(OUT, 'extras.json'), 'w'), indent=1)
    return X


if __name__ == '__main__':
    print(json.dumps(main(), indent=1))
