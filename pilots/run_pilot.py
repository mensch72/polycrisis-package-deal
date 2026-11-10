"""Pilot skeletons (roadmap M3): run one pilot instance through the pipeline, exactly, by enumeration.

Usage: python3 run_pilot.py pilot_a | pilot_b

A pilot module offers ACTORS, LEVERS, SHAPE, D, OWNER, DIMS, BASE, PROVENANCE, PERTURB, CHAIN, INDICATORS,
evaluate(p) and describe(a), like phase0/instance2.py. Preference and cost parameters in these modules are
ILLUSTRATIVE until people with knowledge of the actors have corrected them. No output says anything about
a real actor. The purpose is to fix the format of a filing and to rank the numbers experts must supply.

Concept: towers under condition (ii'), adopted by Jobst on 10 November 2026 (docs/phase0_towers.md).
A stage outcome b_k is admissible iff it is in the strict core of its stage game and no group inside the
stage coalition gains by over-fulfilling; both are tested directly.

Selection rule, fixed before the first run of any pilot: over all two-stage towers (b_1, b_2) along the
module's CHAIN with b_1 acceptable to the first coalition and b_2 acceptable to all: the largest smallest
normalised gain over a0 at b_2 among all actors, then the largest sum of these gains, then the smallest
flat indices of b_2 and b_1.
Tests on the selected tower, fixed before the first run (they test the software, as in phase0/run_tower.py):
  T1 registry returns b_2, and b_1 on the old members' levers if the newcomers file zero.
  T2 no group inside a stage coalition has a profitable deviation inside its stage box.
  T3 in the full game, no profitable deviation has an outcome at or above b_1.
  T4 every group with a profitable deviation in the full game mixes newcomers and earlier members.
Descriptive outputs without pass mark: withdrawal table, robustness share over perturbed illustrative
parameters, and the ranking of those parameters by how strongly they separate failing from passing draws.
"""
import importlib
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phase0'))
import core
import tower

name = sys.argv[1]
M = importlib.import_module(name)
ACTORS, LEVERS, SHAPE, D, OWNER, DIMS, BASE = M.ACTORS, M.LEVERS, M.SHAPE, M.D, M.OWNER, M.DIMS, M.BASE
N = len(ACTORS)
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
N_DRAWS, SPREAD, SEED = 200, 0.25, 5


def log(*a):
    print(f'[{time.time() - T0:6.1f}s]', *a, flush=True)


def gname(G):
    return '+'.join(ACTORS[i] for i in G)


def flat(a):
    return int(np.ravel_multi_index(tuple(int(x) for x in a), SHAPE))


def certified(U, acc, f):
    """Individually rational, acceptable to all, in the strict core, no gain by over-fulfilment."""
    Uf = U.reshape(N, -1)
    a = np.array(np.unravel_index(f, SHAPE))
    return bool(np.all(Uf[:, f] >= Uf[:, 0] - 1e-9) and acc.reshape(N, -1)[:, f].all()
                and core.in_strict_core(U, OWNER, f)[0] and core.over_fulfilment(U, OWNER, a) == 0)


def main():
    ev = M.evaluate(BASE)
    U, acc = ev['U'], ev['acc']
    Uf = U.reshape(N, -1)
    gains = Uf - Uf[:, [0]]
    C = acc.all(0).reshape(-1)
    ir = np.all(gains >= -1e-9, axis=0)
    scale = gains[:, C & ir].max(1) if (C & ir).any() else gains[:, ir].max(1)
    scale = np.where(scale > 0, scale, 1.0)
    R = dict(pilot=name, n_actors=N, n_levers=D, n_profiles=int(np.prod(SHAPE)), n_groups=2 ** N - 1,
             chain=M.CHAIN, scale={a: float(scale[i]) for i, a in enumerate(ACTORS)})
    viol = core.orientation(U, OWNER)
    R['orientation'] = dict(passed=len(viol) == 0, violations=[
        dict(lever=f'{LEVERS[d][0]}.{LEVERS[d][1]}', actor=ACTORS[i]) for d, i, n, mx in viol])
    R['regions'] = dict(acceptable=int(C.sum()), individually_rational=int(ir.sum()), both=int((C & ir).sum()))
    core_idx, info = core.strict_core(U, OWNER, acc.all(0))
    P = np.array(np.unravel_index(core_idx, SHAPE)).T
    eq = np.array([core.over_fulfilment(U, OWNER, p) == 0 for p in P], bool) if len(P) else np.zeros(0, bool)
    R['core'] = dict(n_efficient=info.get('n_efficient', 0), n_core=int(len(core_idx)), n_equilibria=int(eq.sum()))
    log('regions', R['regions'], '| core', R['core'], '| orientation passed:', R['orientation']['passed'])

    # ---- towers under (ii') along the chain
    chain = [[ACTORS.index(a) for a in S] for S in M.CHAIN]
    I1, newc = chain[0], [i for i in chain[1] if i not in chain[0]]
    zeroD = np.zeros(D, int)
    Uk, dims, owner_k, sub = tower.stage_game(U, OWNER, I1, zeroD)
    ck, _ = core.strict_core(Uk, owner_k, np.ones(sub, bool))
    b1s = []
    for x in ck:
        b1 = tower.to_full(x, dims, sub, zeroD, D)
        if acc.reshape(N, -1)[I1, flat(b1)].all() and not tower.stage_deviations(U, SHAPE, OWNER, I1, zeroD, b1):
            b1s.append(b1)
    pairs = []
    for b1 in b1s:
        U2, d2, o2, s2 = tower.stage_game(U, OWNER, range(N), b1)
        c2, _ = core.strict_core(U2, o2, np.ones(s2, bool))
        for x in c2:
            b2 = tower.to_full(x, d2, s2, b1, D)
            f2 = flat(b2)
            if C[f2] and core.over_fulfilment(U, OWNER, b2) == 0:
                g = gains[:, f2] / scale
                pairs.append((float(g.min()), float(g.sum()), -f2, -flat(b1)))
    R['towers'] = dict(n_first_stage_core=int(len(ck)), n_first_stage_admissible=len(b1s), n_towers=len(pairs),
                       n_nontrivial=sum(p[2] != p[3] for p in pairs),
                       n_all_at_or_above_a0=sum(bool(np.all(gains[:, -p[2]] >= -1e-9)) for p in pairs))
    log('towers', R['towers'])
    if not pairs:
        R['tower'] = None
        json.dump(R, open(os.path.join(OUT, f'{name}.json'), 'w'), indent=1)
        log('no tower')
        return
    mn, sm, nf2, nf1 = max(pairs)
    f1, fm = -nf1, -nf2
    b1 = np.array(np.unravel_index(f1, SHAPE))
    bm = np.array(np.unravel_index(fm, SHAPE))
    stages = [(set(I1), b1), (set(range(N)), bm)]
    ind = lambda f: {k: float(ev[k].reshape(-1)[f]) for k in M.INDICATORS}
    R['tower'] = dict(
        stage1=M.describe(b1), final=M.describe(bm), nontrivial=bool(f1 != fm),
        stage1_indicators=ind(f1), final_indicators=ind(fm),
        stage1_norm_gain={ACTORS[i]: float(gains[i, f1] / scale[i]) for i in range(N)},
        final_norm_gain={ACTORS[i]: float(gains[i, fm] / scale[i]) for i in range(N)},
        final_certified_in_full_game=certified(U, acc, fm))
    zero = np.zeros((1, D), int)
    old = np.array([OWNER[d] not in newc for d in range(D)])
    t1 = bool(np.array_equal(tower.registry(stages, SHAPE, OWNER, set(), zero)[0], bm)
              and np.array_equal(tower.registry(stages, SHAPE, OWNER, set(newc), zero)[0][old], b1[old]))
    t2 = [tower.stage_deviations(U, SHAPE, OWNER, I1, zeroD, b1), tower.stage_deviations(U, SHAPE, OWNER, range(N), b1, bm)]
    earlier, newcomers = set(I1), set(newc)
    old_lev = np.array([OWNER[d] in earlier for d in range(D)])
    groups, inside = {}, 0
    for G in core.coalitions(N):
        dv = tower.all_devs(SHAPE, OWNER, G)
        out = tower.registry(stages, SHAPE, OWNER, set(G), dv)
        pm = tower.profitable(U, SHAPE, G, out, fm)
        if pm.any():
            groups[G] = int(pm.sum())
            inside += int(np.all(out[pm][:, old_lev] >= b1[old_lev], axis=1).sum())
    R['tests'] = dict(T1=t1, T2=all(len(x) == 0 for x in t2), T3=inside == 0,
                      T4=all(set(G) & newcomers and set(G) & earlier for G in groups))
    R['full_game'] = dict(groups_with_profitable_deviation=len(groups), groups=[gname(G) for G in groups],
                          strictly_strong_equilibrium=len(groups) == 0)
    log('tests', R['tests'], '| groups that can still gain:', len(groups))

    # ---- withdrawal table: what the registry returns if one actor files nothing
    wd = {}
    for i in range(N):
        o = tower.registry(stages, SHAPE, OWNER, {i}, zero)[0]
        fo = flat(o)
        wd[ACTORS[i]] = dict(outcome=M.describe(o), indicators=ind(fo), falls_to=('zero' if fo == 0 else 'stage 1' if fo == f1 else 'other'),
                             norm_gain={ACTORS[j]: float(gains[j, fo] / scale[j]) for j in range(N)})
    R['withdrawal'] = wd

    # ---- robustness of the final outcome and ranking of the illustrative parameters
    rng = np.random.default_rng(SEED)
    ok, facs = [], []
    for _ in range(N_DRAWS):
        p = dict(BASE)
        f = {}
        for k in M.PERTURB:
            f[k] = float(np.exp(rng.uniform(-np.log(1 + SPREAD), np.log(1 + SPREAD))))
            p[k] = BASE[k] * f[k]
        e2 = M.evaluate(p)
        ok.append(certified(e2['U'], e2['acc'], fm))
        facs.append(f)
    ok = np.array(ok)
    sens = {}
    if 0 < ok.sum() < N_DRAWS:
        for k in M.PERTURB:
            lf = np.log([f[k] for f in facs])
            sens[k] = float(lf[~ok].mean() - lf[ok].mean())
    R['robustness'] = dict(n=N_DRAWS, spread=SPREAD, n_perturbed_parameters=len(M.PERTURB), final_stays_certified=int(ok.sum()),
                           ranking=[dict(parameter=k, shift=v) for k, v in sorted(sens.items(), key=lambda kv: -abs(kv[1]))[:8]])
    log('robustness: certified in', int(ok.sum()), 'of', N_DRAWS, '| top parameters', [r['parameter'] for r in R['robustness']['ranking'][:5]])

    # ---- [post hoc] added after the first pilot run, in which all 200 draws stayed certified and the ranking
    # was empty: tipping factors. For each illustrative parameter alone, the smallest factor on a fixed grid,
    # upwards and downwards, at which the final outcome is no longer certified.
    GRID = [1.1, 1.25, 1.5, 2.0, 3.0]
    tip = {}
    for k in getattr(M, 'TIPPING', M.PERTURB):
        up = down = None
        for fct in GRID:
            if up is None:
                p = dict(BASE); p[k] = BASE[k] * fct
                e2 = M.evaluate(p)
                if not certified(e2['U'], e2['acc'], fm):
                    up = fct
            if down is None:
                p = dict(BASE); p[k] = BASE[k] / fct
                e2 = M.evaluate(p)
                if not certified(e2['U'], e2['acc'], fm):
                    down = fct
        tip[k] = dict(up=up, down=down)
    order = sorted(tip, key=lambda k: min(x for x in (tip[k]['up'], tip[k]['down'], 99) if x is not None))
    R['tipping_post_hoc'] = dict(grid=GRID, n_parameters=len(tip), n_that_tip_within_grid=sum(1 for k in tip if tip[k]['up'] or tip[k]['down']),
                                 ranking=[dict(parameter=k, **tip[k]) for k in order if tip[k]['up'] or tip[k]['down']])
    log('[post hoc] tipping:', [(r['parameter'], r['up'], r['down']) for r in R['tipping_post_hoc']['ranking'][:8]])

    # ---- the filing, in words
    with open(os.path.join(OUT, f'{name}_filings.md'), 'w') as fh:
        fh.write(f'# Filings of the selected tower ({name})\n\nNested step form. Generated from illustrative numbers; not a draft.\n')
        for i, a in enumerate(ACTORS):
            fh.write(f'\n## {M.ACTOR_INFO[a]}\n\n')
            lines = []
            for k, (members, b) in enumerate(stages):
                if i not in members or not b[DIMS[i]].any():
                    continue
                own = '; '.join(M.lever_sentence(d, int(b[d])) for d in DIMS[i] if b[d] > 0)
                oth = ', '.join(sorted(M.ACTOR_INFO[ACTORS[j]] for j in members if j != i))
                lines.append((k, own, oth))
            if not lines:
                fh.write('Files nothing.\n')
            for k, own, oth in reversed(lines):
                fh.write(f'- Step {k + 1}: will {own}, provided the registry shows each of {oth} at or above its step-{k + 1} level.\n')
            if lines:
                fh.write('- Otherwise the liability under this filing is that of the highest step whose condition holds, or zero.\n')
    json.dump(dict(base=BASE, provenance=M.PROVENANCE, perturbed=M.PERTURB,
                   levers=[dict(actor=a, lever=l, levels=n, issue=iss) for a, l, n, iss in LEVERS]),
              open(os.path.join(OUT, f'{name}_params.json'), 'w'), indent=1)
    R['runtime_seconds'] = round(time.time() - T0, 1)
    json.dump(R, open(os.path.join(OUT, f'{name}.json'), 'w'), indent=1)
    log('done')


if __name__ == '__main__':
    main()
