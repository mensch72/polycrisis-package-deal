"""Audit, part 2: robustness set, orientation test, linkage numbers, stability depth.

Uses the audit's own model and core test (audit_core.py). The 150 parameter draws are regenerated with
the original sampling function (instance.perturbed, generator seed 1), because the claim under test is
about those draws. Float comparisons use eps = 1e-9 as in the original; near-ties are counted.

Usage: python3 -I audit_robust.py <repo>/phase0
"""
import sys, json, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from audit_core import (inst, BASE, ACT, LEV, SHAPE, OWN, COALS, SUB, model, blocked_by, strict_core)

PH = sys.argv[1]
EPS = 1e-9
core = np.array(json.load(open(PH + '/results/core_acceptable.json')))
R0 = json.load(open(PH + '/results/results.json'))
P = np.array(np.unravel_index(core, SHAPE)).T
nC = len(core)
STR = np.array([int(np.prod(SHAPE[d + 1:])) for d in range(len(SHAPE))])


def orientation(U):
    """Owner weakly prefers less, everyone else weakly prefers more, along every lever, everywhere."""
    Ug = U.reshape((8,) + SHAPE)
    bad_owner, bad_other = set(), set()
    for d in range(len(LEV)):
        for i in range(8):
            dU = np.diff(Ug[i], axis=d)
            if i == OWN[d] and (dU > EPS).any():
                bad_owner.add(d)
            if i != OWN[d] and (dU < -EPS).any():
                bad_other.add(d)
    return bad_owner, bad_other


def over_fulfil(U, a):
    """True iff some group gains (all weakly, one strictly) by raising own levers above a, others at a."""
    f0 = int(a @ STR)
    for G in COALS:
        rng = [range(a[d], n) if OWN[d] in G else (a[d],) for d, (_, _, n) in enumerate(LEV)]
        dv = np.array(list(itertools.product(*rng)))
        if len(dv) == 1:
            continue
        fl = dv @ STR
        d = U[np.ix_(list(G), fl)] - U[list(G), f0][:, None]
        if (np.all(d >= -EPS, axis=0) & np.any(d > EPS, axis=0)).any():
            return True
    return False


R = {}
# ---- base point: orientation, contested variant, stability depth, linkage
mf = model(BASE, exact=False)
U = mf['U']
R['orientation_base'] = [sorted(x) for x in orientation(U)]
Uc = U.copy()
lv = mf['levels']
Uc[6] = Uc[6] - 0.10 * (lv[1] + lv[3])
R['orientation_contested'] = [[LEV[d][:2] for d in sorted(x)] for x in orientation(Uc)]

gain = U - U[:, [0]]
C = mf['acc'].all(0)
IR = np.all(gain >= -EPS, axis=0)
norm = gain[:, C & IR].max(1)
lead = np.array([R0['menu']['robust']['profile'][f'{a}.{n}'] for a, n in
                 [(l[0], dict(c='climate', o='ai_oversight', f='finance_lic', s='surveillance')[l[1]]
                   if not (l[0] == 'DEV') else 'ai_safety') for l in LEV]])
fl = int(lead @ STR)
contrib = {OWN[d] for d in range(len(LEV)) if lead[d] > 0}
best = (-9, None)
for G in COALS:
    if contrib <= set(G):
        continue
    d = (U[np.ix_(list(G), SUB[G])] - U[list(G), fl][:, None]) / norm[list(G)][:, None]
    m = float(d.min(0).max())
    if m > best[0]:
        best = (m, [ACT[i] for i in G])
R['lead_tightest_group_missing_a_contributor'] = best
R['lead_gain'] = {a: round(float(gain[i, fl]), 4) for i, a in enumerate(ACT)}
R['lead_ngain'] = {a: round(float(gain[i, fl] / norm[i]), 4) for i, a in enumerate(ACT)}

# single-issue games: other issues' levers at 0; strict core without aspiration filter
ISS = dict(climate=[0, 2, 4, 6, 8], ai=[1, 3, 10], pandemic=[5, 7, 9, 11])
parts = {}
for iss, dims in ISS.items():
    rng = [range(n) if d in dims else (0,) for d, (_, _, n) in enumerate(LEV)]
    prof = np.array(list(itertools.product(*rng)))
    fls = prof @ STR
    ir = np.all(U[:, fls] >= U[:, [0]] - EPS, axis=0)
    cand = fls[ir]
    alive = np.ones(len(cand), bool)
    for G in COALS:
        sub = np.intersect1d(SUB[G], fls)          # coalition moves only this issue's levers
        ug = U[np.ix_(list(G), sub)]
        uc = U[np.ix_(list(G), cand)]
        dd = ug[:, :, None] - uc[:, None, :]
        alive &= ~(np.all(dd >= -EPS, axis=0) & np.any(dd > EPS, axis=0)).any(0)
    parts[iss] = np.array(np.unravel_index(cand[alive], SHAPE)).T
    R.setdefault('single_issue_core', {})[iss] = dict(
        n=int(alive.sum()), max_indicator=float(mf[dict(climate='Q', ai='A', pandemic='P')[iss]][cand[alive]].max()))
combos = np.array([a + b + c for a in parts['climate'] for b in parts['ai'] for c in parts['pandemic']])
cf = combos @ STR
ok_core, _ = strict_core(U, cf, eps=EPS)
R['combos'] = dict(n=len(cf), in_package_core=int(ok_core.sum()), acceptable=int(C[cf].sum()),
                   both=int((ok_core & C[cf]).sum()), both_in_core_list=int(np.isin(cf, core).sum()))
# separate deals at each issue's Nash-product point
sep = np.zeros(len(LEV), int)
for iss in ISS:
    g = (U[:, parts[iss] @ STR] - U[:, [0]]) / norm[:, None]
    sep += parts[iss][int(np.argmax(np.where((g > 0).all(0), np.log(np.maximum(g, 1e-300)).sum(0), -np.inf)))]
fs = int(sep @ STR)
dom = np.all(gain[:, core] >= gain[:, [fs]] - EPS, axis=0) & np.any(gain[:, core] > gain[:, [fs]] + EPS, axis=0)
R['separate_deals'] = dict(profile=sep.tolist(), in_core_list=bool(fs in set(core.tolist())),
                           core_profiles_better_for_all=int(dom.sum()),
                           lead_minus_sep={a: round(float(gain[i, fl] - gain[i, fs]), 4) for i, a in enumerate(ACT)})
print(json.dumps(R, indent=1), flush=True)

# ---- robustness set
rng = np.random.default_rng(R0['meta']['seed'] + 1)
n = R0['robustness']['n']
IRm, ACm, COm, EQm, IRs = (np.zeros((n, nC), bool) for _ in range(5))
orient_ok, owner_fail, other_fail, near = 0, {}, 0, 0
lic_fail = other_acc_fail = 0
jl = int(np.flatnonzero(core == fl)[0])
MENU_J = sorted({int(np.flatnonzero(core == v['flat'])[0]) for v in R0['menu'].values()})
for t in range(n):
    p, fac = inst.perturbed(rng)
    m = model(p, exact=False)
    U2 = m['U']
    bo, bx = orientation(U2)
    orient_ok += not (bo or bx)
    other_fail += bool(bx)
    for d in bo:
        owner_fail[LEV[d][0] + '.' + LEV[d][1]] = owner_fail.get(LEV[d][0] + '.' + LEV[d][1], 0) + 1
    IRm[t] = np.all(U2[:, core] >= U2[:, [0]] - EPS, axis=0)
    ACm[t] = m['acc'][:, core].all(0)
    COm[t], _ = strict_core(U2, core, eps=EPS)        # full definition, all 255 coalitions incl. singletons
    for k in MENU_J:
      if COm[t, k]:
        EQm[t, k] = not over_fulfil(U2, P[k])
    if t < 3 or t % 25 == 0:
        from audit_core import equilibrium
        assert (not equilibrium(U2, P[jl].tolist(), eps=EPS, closed=True)) == bool(EQm[t, jl]), 'decomposition differs'
    a_l = m['acc'][:, fl]
    lic_fail += int(not a_l[5]); other_acc_fail += int(not np.delete(a_l, 5).all())
    if t % 10 == 9:
        print('draw', t + 1, 'lead ok so far', int((IRm & ACm & COm)[:t + 1, jl].sum()), flush=True)
JO = IRm & ACm & COm
joint = JO.sum(0)
R['robust'] = dict(
    orientation_holds=int(orient_ok), draws_non_owner_harmed=int(other_fail), owner_fail=owner_fail,
    per_draw_surviving=dict(mean=float(JO.sum(1).mean()), min=int(JO.sum(1).min()), max=int(JO.sum(1).max())),
    best=int(joint.max()), n_at_best=int((joint == joint.max()).sum()), n_ge_90pct=int((joint >= 0.9 * n).sum()),
    lead=dict(joint=int(joint[jl]), core=int(COm[:, jl].sum()), eq=int(EQm[:, jl].sum()),
              acc=int(ACm[:, jl].sum()), ir=int(IRm[:, jl].sum()), lic_fail=lic_fail, other_acc_fail=other_acc_fail),
    core_without_IR_vs_a0=int((COm & ~IRm).sum()),
    menu_core_but_not_equilibrium=int((COm & ~EQm)[:, MENU_J].sum()))
menu = {}
for k, v in R0['menu'].items():
    j = int(np.flatnonzero(core == v['flat'])[0])
    menu[k] = dict(acc=int(ACm[:, j].sum()), core=int(COm[:, j].sum()), all3=int(JO[:, j].sum()),
                   eq=int(EQm[:, j].sum()), ir=int(IRm[:, j].sum()))
R['robust']['menu'] = menu
np.save('results/joint_counts.npy', joint)
json.dump(R, open('results/audit_robust.json', 'w'), indent=1, default=str)
print(json.dumps(R['robust'], indent=1))
