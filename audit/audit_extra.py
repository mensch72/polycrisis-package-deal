"""Audit, part 3: (a) full group-deviation test of the lead through the registry rule itself,
(b) out-of-sample robustness of the menu on fresh draws, (c) normaliser variants,
(d) the audit's no-filter core against the original cache.

The lead was selected as the best of 326 profiles on the same 150 draws on which its share is reported.
Pass mark for (b), fixed before running: none; it is an estimate, reported with a 95 % Wilson interval.
Fresh draws: instance.perturbed with numpy default_rng(20261110), 500 draws.

Usage: python3 -I audit_extra.py <repo>/phase0 [rerun_results_dir]
"""
import sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from audit_core import inst, BASE, ACT, SHAPE, model, strict_core, equilibrium
PH = sys.argv[1]
EPS = 1e-9
R0 = json.load(open(PH + '/results/results.json'))
R = {}
m = model(BASE, exact=True)
lead = np.array(np.unravel_index(R0['menu']['robust']['flat'], SHAPE))
R['lead_equilibrium_violations_registry_iteration'] = equilibrium(m['U'], lead.tolist())
# (c) normaliser: largest gain among profiles IR for all and acceptable to ALL (used) vs acceptable to the actor only
U = m['U'] / m['uscale']; g = U - U[:, [0]]; IR = np.all(g >= 0, axis=0); C = m['acc'].all(0)
R['normaliser_acceptable_to_all'] = {a: round(float(g[i, IR & C].max()), 4) for i, a in enumerate(ACT)}
R['normaliser_acceptable_to_self'] = {a: round(float(g[i, IR & m['acc'][i]].max()), 4) for i, a in enumerate(ACT)}
# (d)
if len(sys.argv) > 2:
    z = np.load(sys.argv[2] + '/cache_core_no_aspirations.npz')
    mine = np.load('results/core_nofilter_idx.npy')
    R['nofilter_core_same_set_as_original'] = bool(np.array_equal(np.sort(mine), np.sort(z['core_idx'])))
print(json.dumps(R, indent=1), flush=True)
# (b)
menu = {k: v['flat'] for k, v in R0['menu'].items()}
fl = np.array(list(menu.values()))
rng = np.random.default_rng(20261110)
n = 500
ok = np.zeros((n, len(fl)), bool); acc = ok.copy(); co = ok.copy()
for t in range(n):
    p, _ = inst.perturbed(rng)
    mm = model(p, exact=False)
    U2 = mm['U']
    ir = np.all(U2[:, fl] >= U2[:, [0]] - EPS, axis=0)
    acc[t] = mm['acc'][:, fl].all(0)
    co[t], _ = strict_core(U2, fl, eps=EPS)
    ok[t] = ir & acc[t] & co[t]
    if t % 50 == 49: print('fresh draw', t + 1, ok[:t + 1].sum(0).tolist(), flush=True)
def wilson(k, n, z=1.96):
    ph = k / n; d = 1 + z * z / n; c = ph + z * z / (2 * n); h = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 3), round((c + h) / d, 3)]
R['fresh_draws'] = {k: dict(all_three=int(ok[:, j].sum()), acceptable=int(acc[:, j].sum()), strict_core=int(co[:, j].sum()),
                            n=n, wilson95=wilson(int(ok[:, j].sum()), n)) for j, k in enumerate(menu)}
json.dump(R, open('results/audit_extra.json', 'w'), indent=1)
print(json.dumps(R['fresh_draws'], indent=1))
