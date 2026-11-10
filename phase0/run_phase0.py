"""Phase 0, first increment: run the toy instance through the pipeline and write results/.

Gate 1 criterion, fixed before the first run:
  PASS iff (a) every heuristic run returns a profile that the exhaustive search confirms
  to be acceptable and in the strict core, and (b) at least 75 % of the runs reach the
  enumerated optimum of the focal objective (difference in log Nash product <= 0.01).

Changed after the first run (the criterion above is untouched): the pipeline no longer recommends
the Nash-product point. It returns a menu of core profiles, and the lead candidate is the core
profile that keeps all properties in the largest share of the robustness set. Reason: the
Nash-product point stayed acceptable in only 60 % of that set.
"""
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instance import (ACTORS, ACTOR_INFO, N, LEVERS, ISSUES, ISSUE_OF, SHAPE, D, OWNER, DIMS, TOP,
                      NPROF, BASE, PROVENANCE, PERTURB, evaluate, perturbed, describe, lever_sentence, grids)
import core
import mechanism
from search import Search

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def prof(f):
    return np.array(np.unravel_index(int(f), SHAPE))


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def main(seed=0, n_theta=150, heur_seeds=8):
    R = dict(meta=dict(date='2026-11-10', seed=seed, n_profiles=NPROF, n_actors=N, n_levers=D,
                       n_coalitions=2 ** N - 1))
    ev = evaluate(BASE)
    U, acc = ev['U'], ev['acc']
    Uf = U.reshape(N, -1)
    U0 = Uf[:, 0].copy()

    # ---------------- WP3: orientation test
    viol = core.orientation(U, OWNER)
    R['orientation'] = dict(passed=len(viol) == 0, violations=[
        dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', actor=ACTORS[i], steps=n, largest=mx) for d, i, n, mx in viol])
    # contested variant: developers bear a compliance burden from state oversight
    Uc = U.copy()
    g = grids()
    Uc[ACTORS.index('DEV')] = Uc[ACTORS.index('DEV')] - 0.10 * (g[1] + g[3])
    violc = core.orientation(Uc, OWNER)
    R['orientation_contested_variant'] = [
        dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', actor=ACTORS[i], steps=n, largest=mx) for d, i, n, mx in violc]
    del Uc
    log('orientation test:', 'passed' if not viol else f'{len(viol)} violations',
        '| contested variant flags', len(violc), 'lever-actor pairs')

    # ---------------- WP1: sufficient groups per issue (targets: two thirds of the indicator's range)
    R['sufficiency'] = {}
    for iss, key in zip(ISSUES, ['Q', 'A', 'P']):
        ind = ev[key]
        target = 1.0 if key == 'P' else 2 / 3 * float(ind.max())
        dims = [d for d in range(D) if np.ptp(np.moveaxis(ind, d, 0).reshape(SHAPE[d], -1), axis=0).max() > 0]
        minimal, veto = core.sufficient_groups(ind, OWNER, dims, target, N)
        R['sufficiency'][iss] = dict(indicator=key, target=target, max=float(ind.max()),
                                     minimal_groups=[gname(sorted(S)) for S in minimal],
                                     veto=[ACTORS[i] for i in sorted(veto)])
    log('sufficiency:', {k: v['veto'] for k, v in R['sufficiency'].items()})

    # ---------------- WP4: acceptable region
    C = acc.all(0)
    ir = np.all(Uf >= U0[:, None] - 1e-9, axis=0).reshape(SHAPE)
    R['acceptable'] = dict(n=int(C.sum()), share=float(C.mean()),
                           per_actor={a: float(acc[i].mean()) for i, a in enumerate(ACTORS)},
                           n_ir=int(ir.sum()), n_ir_and_acceptable=int((C & ir).sum()))
    log('acceptable region:', R['acceptable']['n'], 'profiles; IR:', R['acceptable']['n_ir'],
        '; both:', R['acceptable']['n_ir_and_acceptable'])
    gains = Uf - U0[:, None]
    sel = (C & ir).reshape(-1)
    scale = gains[:, sel].max(1) if sel.any() else gains[:, ir.reshape(-1)].max(1)
    scale = np.where(scale > 0, scale, 1.0)
    R['scale'] = {a: float(scale[i]) for i, a in enumerate(ACTORS)}

    # ---------------- WP6: exact strict core inside the acceptable region
    core_idx, info = core.strict_core(U, OWNER, C, log)
    R['core'] = dict(n_candidates=info['n_candidates'], n_efficient=info.get('n_efficient', 0),
                     n_core=int(len(core_idx)),
                     blocked={gname(G): n for G, n in info['blocked'].items()})
    log('strict core inside acceptable region:', len(core_idx), 'profiles')
    json.dump([int(x) for x in core_idx], open(os.path.join(OUT, 'core_acceptable.json'), 'w'))
    if len(core_idx) == 0:
        json.dump(R, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
        log('EMPTY CORE: stopping after core stage')
        return R
    Gn = gains[:, core_idx] / scale[:, None]                      # normalised gains on the core
    logn = np.where((Gn > 0).all(0), np.log(np.maximum(Gn, 1e-300)).sum(0), -np.inf)
    best_log = float(np.max(logn))
    srt = np.sort(Gn, axis=0)
    ind = {k: ev[k].reshape(-1)[core_idx] for k in 'QAP'}
    nC = len(core_idx)

    def pick(score):                                              # ties: largest Nash product
        top = np.flatnonzero(score >= score.max() - 1e-12)
        return int(core_idx[top[int(np.argmax(logn[top]))]])

    cand = {
        'nash': int(core_idx[int(np.argmax(logn))]),
        'leximin': int(core_idx[int(np.lexsort(tuple(srt[k] for k in reversed(range(N))))[-1])]),
        'deepest': pick(ev['slack'].reshape(-1)[core_idx]),
        'ambition': pick(np.minimum.reduce([ind[k] / ind[k].max() for k in 'QAP'])),
    }
    cp = np.array(np.unravel_index(core_idx, SHAPE))
    R['core']['lever_range'] = {f'{LEVERS[d][0]}.{LEVERS[d][1]}': [int(cp[d].min()), int(cp[d].max())] for d in range(D)}
    R['core']['indicator_range'] = {k: [float(ind[k].min()), float(ind[k].max())] for k in 'QAP'}

    # ---------------- WP4/WP8: robustness set. Which core profiles keep which property in each draw?
    rng = np.random.default_rng(seed + 1)
    IRm, ACm, COm = (np.zeros((n_theta, nC), bool) for _ in range(3))
    mask_core = np.zeros(NPROF, bool)
    mask_core[core_idx] = True
    facs, orient, failing, other_side = [], [], {}, 0
    for t in range(n_theta):
        p, fac = perturbed(rng)
        e2 = evaluate(p, light=True)
        U2 = e2['U']
        U2f = U2.reshape(N, -1)
        v2 = core.orientation(U2, OWNER)
        orient.append(len(v2) == 0)
        other_side += int(any(i != OWNER[d] for d, i, n, mx in v2))
        for k in sorted({f'{LEVERS[d][0]}.{LEVERS[d][1]}' for d, i, n, mx in v2 if i == OWNER[d]}):
            failing[k] = failing.get(k, 0) + 1
        IRm[t] = np.all(U2f[:, core_idx] >= U2f[:, [0]] - 1e-9, axis=0)
        ACm[t] = e2['acc'].reshape(N, -1)[:, core_idx].all(0)
        ck, _ = core.strict_core(U2, OWNER, mask_core.reshape(SHAPE))
        COm[t] = np.isin(core_idx, ck)                            # in the strict core of the perturbed game
        facs.append(fac)
    JOm = IRm & ACm & COm
    joint = JOm.mean(0)
    cand['robust'] = pick(joint)
    lead = 'robust'
    a_flat = cand[lead]
    a_star = prof(a_flat)
    pos = {int(f): j for j, f in enumerate(core_idx)}
    log('robustness set:', n_theta, 'draws | orientation holds in', float(np.mean(orient)),
        '| joint share over the core: min', float(joint.min()), 'max', float(joint.max()))

    # second pass over the same draws: over-fulfilment for the menu, blockers for the lead
    rng = np.random.default_rng(seed + 1)
    distinct = sorted(set(cand.values()))
    EQm = {f: [] for f in distinct}
    blockers = {}
    for t in range(n_theta):
        p, fac = perturbed(rng)
        U2 = evaluate(p, light=True)['U']
        for f in distinct:
            EQm[f].append(bool(COm[t, pos[f]] and core.over_fulfilment(U2, OWNER, prof(f)) == 0))
        if not COm[t, pos[a_flat]]:
            okc, Gb = core.in_strict_core(U2, OWNER, a_flat)
            if not okc:
                blockers[gname(Gb)] = blockers.get(gname(Gb), 0) + 1
    okl = JOm[:, pos[a_flat]]
    sens = {}
    if 0 < okl.sum() < n_theta:
        for k in PERTURB:
            lf = np.log([fc[k] for fc in facs])
            sens[k] = float(lf[~okl].mean() - lf[okl].mean())
    R['robustness'] = dict(
        n=n_theta, spread=0.25, factor_range=[1 / 1.25, 1.25],
        share_orientation=float(np.mean(orient)), draws_with_a_non_owner_harmed=other_side,
        owner_side_orientation_failures=dict(sorted(failing.items(), key=lambda kv: -kv[1])),
        base_core_profiles_still_acceptable_ir_core=dict(
            mean=float(JOm.sum(1).mean()), min=int(JOm.sum(1).min()), max=int(JOm.sum(1).max())),
        joint_share_over_core=dict(min=float(joint.min()), median=float(np.median(joint)), max=float(joint.max()),
                                   n_at_max=int((joint >= joint.max() - 1e-12).sum()),
                                   n_at_or_above_0_9=int((joint >= 0.9).sum())),
        lead_blockers=dict(sorted(blockers.items(), key=lambda kv: -kv[1])[:6]),
        lead_sensitivity=dict(sorted(sens.items(), key=lambda kv: -abs(kv[1]))[:6]))

    # ---------------- WP8: certificates at the base point
    def certificate(f, sample=0):
        a = prof(f)
        cert = dict(individually_rational=bool(np.all(gains[:, f] >= -1e-9)),
                    acceptable_to_all=bool(C.reshape(-1)[f]))
        ok, _ = core.in_strict_core(U, OWNER, f)
        cert['strict_core_by_direct_test'] = bool(ok)
        mg = core.margins(U, OWNER, f, scale)
        cert['max_margin_all_coalitions'] = float(max(mg.values()))
        contrib = {i for i in range(N) if a[DIMS[i]].any()}
        miss = {G: v for G, v in mg.items() if not contrib <= set(G)}
        tight = max(miss, key=miss.get)
        cert['contributors'] = [ACTORS[i] for i in sorted(contrib)]
        cert['tightest_coalition_missing_a_contributor'] = dict(coalition=gname(tight), margin=float(miss[tight]))
        ccfs = [mechanism.canonical(i, a) for i in range(N)]
        cert['registry_returns_profile'] = bool(np.array_equal(mechanism.outcome(ccfs), a))
        worse = core.over_fulfilment(U, OWNER, a)
        cert['coalitions_gaining_by_over_fulfilment'] = worse
        mism = profitable = 0
        if sample:                    # deviations to unconditional actions: registry rule against closed form
            rs = np.random.default_rng(seed)
            ua = Uf[:, f]
            for _ in range(sample):
                k = int(rs.integers(1, N + 1))
                Gd = sorted(rs.choice(N, k, replace=False).tolist())
                x = {i: np.array([rs.integers(0, SHAPE[d]) for d in DIMS[i]]) for i in Gd}
                cc = [mechanism.constant(i, x[i]) if i in Gd else ccfs[i] for i in range(N)]
                o = mechanism.outcome(cc)
                if not np.array_equal(o, mechanism.closed_form_deviation(a, Gd, x)):
                    mism += 1
                uo = Uf[:, int(np.ravel_multi_index(tuple(o), SHAPE))]
                if np.all(uo[Gd] >= ua[Gd] - 1e-9) and np.any(uo[Gd] > ua[Gd] + 1e-9):
                    profitable += 1
            cert['sampled_deviations'] = dict(n=sample, registry_vs_closed_form_mismatches=mism, profitable=profitable)
        cert['strictly_strong_equilibrium_certified'] = bool(
            ok and worse == 0 and cert['registry_returns_profile'] and mism == 0 and profitable == 0)
        return cert

    R['menu'], R['lead'] = {}, lead
    for kname, f in cand.items():
        j = pos[f]
        R['menu'][kname] = dict(
            flat=f, profile=describe(prof(f)), same_profile_as=[k for k, g in cand.items() if g == f and k != kname],
            gain={ACTORS[i]: float(gains[i, f]) for i in range(N)},
            norm_gain={ACTORS[i]: float(gains[i, f] / scale[i]) for i in range(N)},
            log_nash=float(logn[j]), Q=float(ind['Q'][j]), A=float(ind['A'][j]), P=float(ind['P'][j]),
            slack=float(ev['slack'].reshape(-1)[f]),
            robustness=dict(individually_rational=float(IRm[:, j].mean()), acceptable=float(ACm[:, j].mean()),
                            strict_core=float(COm[:, j].mean()), all_three=float(joint[j]),
                            equilibrium=float(np.mean(EQm[f]))),
            certificate=certificate(f, sample=20000 if kname == lead else 0))
        log(f'  {kname:9s}', list(prof(f)), 'robust:', R['menu'][kname]['robustness'],
            '| equilibrium certified:', R['menu'][kname]['certificate']['strictly_strong_equilibrium_certified'])
    log('lead candidate (most robust core profile):', describe(a_star))

    # ---------------- WP6: heuristic search against enumeration (Gate 1)
    runs = []
    core_set = set(int(x) for x in core_idx)
    for s in range(heur_seeds):
        S = Search(U, acc, scale, np.random.default_rng(1000 + s))
        t = time.time()
        res = S.run()
        if res['profile'] is None:
            runs.append(dict(seed=s, found=False, rounds=res['rounds'], cuts=res['cuts'], evals=res['evals']))
            continue
        f = int(np.ravel_multi_index(tuple(res['profile']), SHAPE))
        ln = float(np.log(np.maximum(gains[:, f] / scale, 1e-300)).sum())
        runs.append(dict(seed=s, found=True, in_core=f in core_set, acceptable=bool(C.reshape(-1)[f]),
                         log_nash=ln, gap=best_log - ln, same_as_enumeration=f == cand['nash'],
                         rounds=res['rounds'], cuts=res['cuts'], evals=res['evals'],
                         seconds=round(time.time() - t, 1)))
        log(f'  heuristic seed {s}:', {k: runs[-1][k] for k in ('in_core', 'gap', 'rounds', 'evals', 'seconds')})
    a_ok = all(r.get('found') and r['in_core'] and r['acceptable'] for r in runs)
    b_share = float(np.mean([bool(r.get('found')) and r['gap'] <= 0.01 for r in runs]))
    R['gate1'] = dict(runs=runs, all_in_core=a_ok, share_reaching_optimum=b_share,
                      passed=bool(a_ok and b_share >= 0.75),
                      mean_share_of_profiles_evaluated=float(np.mean([r['evals'] for r in runs]) / NPROF))
    log('Gate 1:', 'PASSED' if R['gate1']['passed'] else 'NOT PASSED', '| all in core:', a_ok,
        '| share reaching optimum:', b_share)

    # ---------------- WP2: linkage value
    link = dict(per_issue_gain={}, single_issue_core={})
    for iss in ISSUES:
        b = np.where(np.array(ISSUE_OF) == iss, a_star, 0)
        fb = int(np.ravel_multi_index(tuple(b), SHAPE))
        link['per_issue_gain'][iss] = {ACTORS[i]: float(gains[i, fb]) for i in range(N)}
    tot = np.array([sum(link['per_issue_gain'][iss][a] for iss in ISSUES) for a in ACTORS])
    link['additive_check_max_error'] = float(np.abs(tot - gains[:, a_flat]).max())
    link['actors_losing_on_some_issue'] = {iss: [a for a in ACTORS if link['per_issue_gain'][iss][a] < -1e-9]
                                           for iss in ISSUES}
    for iss in ISSUES:
        dims = [d for d in range(D) if ISSUE_OF[d] == iss]
        idx = tuple(slice(None) if ISSUE_OF[d] == iss else 0 for d in range(D))
        Uk = U[(slice(None),) + idx]
        ck, _ = core.strict_core(Uk, OWNER[dims], np.ones(Uk.shape[1:], bool))
        pk = np.array(np.unravel_index(ck, Uk.shape[1:]))
        sub = tuple(int(a_star[d]) for d in dims)
        link['single_issue_core'][iss] = dict(
            n=int(len(ck)),
            lever_max={f'{LEVERS[d][0]}.{LEVERS[d][1]}': int(pk[j].max()) for j, d in enumerate(dims)},
            a_star_part_in_core=bool(int(np.ravel_multi_index(sub, Uk.shape[1:])) in set(int(x) for x in ck)))
    # three separate single-issue deals (Nash-product point of each single-issue core) against the package
    sep = np.zeros(D, int)
    for iss in ISSUES:
        dims = [d for d in range(D) if ISSUE_OF[d] == iss]
        idx = tuple(slice(None) if ISSUE_OF[d] == iss else 0 for d in range(D))
        Uk = U[(slice(None),) + idx]
        ck, _ = core.strict_core(Uk, OWNER[dims], np.ones(Uk.shape[1:], bool))
        Ukf = Uk.reshape(N, -1)
        gk = (Ukf[:, ck] - Ukf[:, [0]]) / scale[:, None]
        lg = np.where((gk > 0).all(0), np.log(np.maximum(gk, 1e-300)).sum(0), -np.inf)
        sk = np.sort(gk, axis=0)
        j = int(np.argmax(lg)) if np.isfinite(lg).any() else int(np.lexsort(tuple(sk[k] for k in reversed(range(N))))[-1])
        sep[dims] = np.unravel_index(int(ck[j]), Uk.shape[1:])
        link['single_issue_core'][iss]['focal_rule'] = 'nash' if np.isfinite(lg).any() else 'leximin'
    fb = int(np.ravel_multi_index(tuple(sep), SHAPE))
    okb, Gb = core.in_strict_core(U, OWNER, fb)
    gb = gains[:, [fb]]
    dom = np.all(gains[:, core_idx] >= gb - 1e-9, axis=0) & np.any(gains[:, core_idx] > gb + 1e-9, axis=0)
    link['separate_deals'] = dict(
        profile=describe(sep), Q=float(ev['Q'].reshape(-1)[fb]), A=float(ev['A'].reshape(-1)[fb]),
        P=float(ev['P'].reshape(-1)[fb]),
        norm_gain={ACTORS[i]: float(gains[i, fb] / scale[i]) for i in range(N)},
        acceptable_to_all=bool(C.reshape(-1)[fb]), in_package_strict_core=bool(okb),
        blocked_by=None if okb else gname(Gb),
        package_core_profiles_better_for_all=int(dom.sum()),
        lead_better_for_all=bool(dom[pos[a_flat]]),
        lead_gain_minus_separate={ACTORS[i]: float(gains[i, a_flat] - gains[i, fb]) for i in range(N)})
    R['linkage'] = link
    log('linkage: losers per issue', link['actors_losing_on_some_issue'], '| separate deals in package core:', okb,
        '| core profiles better for all:', int(dom.sum()))

    # ---------------- WP7 and WP9: filings and briefs
    with open(os.path.join(OUT, 'filings.md'), 'w') as fh:
        fh.write('# Filings through the lead candidate (toy instance)\n\n'
                 'Canonical form. Illustrative text generated from the toy model; not a legal draft.\n')
        for i, a in enumerate(ACTORS):
            own = [lever_sentence(d, int(a_star[d])) for d in DIMS[i] if a_star[d] > 0]
            if not own:
                continue
            oth = [f'{LEVERS[d][0]} {LEVERS[d][1]} at level {int(a_star[d])} or above'
                   for d in range(D) if OWNER[d] != i and a_star[d] > 0]
            fh.write(f"\n## {ACTOR_INFO[a]['name']}\n\n"
                     f"Instrument: {ACTOR_INFO[a]['instrument']}.\n\n"
                     f"{ACTOR_INFO[a]['name']} will " + '; and '.join(own) + ',\n'
                     'provided the registry shows every other signatory at or above its listed level:\n\n'
                     + '\n'.join('- ' + o for o in oth) +
                     '\n\nIf the condition is not met, the liability under this filing is zero '
                     '(current policies continue).\n')
    with open(os.path.join(OUT, 'briefs.md'), 'w') as fh:
        fh.write('# Briefs per actor (toy instance)\n\nAll figures in the actor\'s own units; illustrative.\n')
        Qs, As, Ps = (float(ev[k].reshape(-1)[a_flat]) for k in ['Q', 'A', 'P'])
        for i, a in enumerate(ACTORS):
            give = [lever_sentence(d, int(a_star[d])) for d in DIMS[i] if a_star[d] > 0] or ['nothing']
            fh.write(f"\n## {ACTOR_INFO[a]['name']}\n\n"
                     f"- You give: {'; '.join(give)}. Own cost: {float(ev['cost'][a].reshape(-1)[a_flat]):.2f}.\n"
                     f"- Indicators move from 0 to: abatement index {Qs:.2f}, AI risk-reduction index {As:.2f}, "
                     f"pandemic protection {Ps:.2f}.\n"
                     f"- Your net gain over no deal: {gains[i, a_flat]:.2f} "
                     f"({100 * gains[i, a_flat] / scale[i]:.0f} % of your largest acceptable gain).\n"
                     f"- Gain by issue: " + ', '.join(f"{iss} {link['per_issue_gain'][iss][a]:+.2f}" for iss in ISSUES) + '.\n'
                     f"- Certificate: individually rational, acceptable to you, efficient, and no coalition "
                     f"can do better for all its members on its own.\n")
    with open(os.path.join(OUT, 'menu.md'), 'w') as fh:
        fh.write('# Menu of core profiles (toy instance)\n\nLevels per lever; shares are over the robustness set.\n\n')
        fh.write('| Lever | ' + ' | '.join(cand) + ' |\n|' + ' --- |' * (len(cand) + 1) + '\n')
        for d in range(D):
            fh.write(f'| {LEVERS[d][0]} {LEVERS[d][1]} | ' + ' | '.join(str(int(prof(f)[d])) for f in cand.values()) + ' |\n')
        for key in ('Q', 'A', 'P'):
            fh.write(f'| indicator {key} | ' + ' | '.join(f"{R['menu'][k][key]:.2f}" for k in cand) + ' |\n')
        for key in ('acceptable', 'strict_core', 'all_three', 'equilibrium'):
            fh.write(f'| share {key} | ' + ' | '.join(f"{100 * R['menu'][k]['robustness'][key]:.0f} %" for k in cand) + ' |\n')
        for i, a in enumerate(ACTORS):
            fh.write(f'| normalised gain {a} | ' + ' | '.join(f"{R['menu'][k]['norm_gain'][a]:.2f}" for k in cand) + ' |\n')
    json.dump(dict(base=BASE, provenance=PROVENANCE, perturbed=PERTURB,
                   levers=[dict(actor=a, lever=l, levels=n, issue=iss) for a, l, n, iss in LEVERS],
                   actors=ACTOR_INFO), open(os.path.join(OUT, 'params.json'), 'w'), indent=1)
    R['meta']['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
    log('done')
    return R


if __name__ == '__main__':
    main()
