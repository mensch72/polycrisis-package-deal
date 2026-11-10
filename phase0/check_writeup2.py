"""Assert every number quoted in docs/phase0_instance2.md against the result files in results2/.

Each check has two parts: the result files give the value, and the quoted strings stand in the text.
Usage: python3 check_writeup2.py [results_dir]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results2')
R = json.load(open(os.path.join(OUT, 'results.json')))
K = json.load(open(os.path.join(OUT, 'contested.json')))
PAR = json.load(open(os.path.join(OUT, 'params.json')))['base']
DOC = ' '.join(open(os.path.join(HERE, '..', 'docs', 'phase0_instance2.md')).read().split())
n_ok = 0


def chk(name, cond, *quoted):
    global n_ok
    assert cond, name
    for q in quoted:
        assert q in DOC, f'{name}: not in the write-up: {q!r}'
    n_ok += 1


def r2(x):
    return round(x + 1e-12, 2)


def r3(x):
    return round(x + 1e-12, 3)


m, f1, f3 = R['meta'], R['fallback1'], R['fallback3']
chk('size', (m['n_actors'], m['n_levers'], m['n_profiles'], m['n_coalitions']) == (3, 9, 46656, 7),
    '3 actors, 2 issues, 9 levers, 46,656 profiles, 7 coalitions')
chk('parameters', (PAR['b'], PAR['g'], PAR['h']) == (.30, .10, .18) and r2(PAR['b'] - PAR['g']) == .20 and r2(2 * PAR['h']) == .36,
    'b = 0.30, g = 0.10 and h = 0.18', 'b − g = 0.20', '2h = 0.36')
chk('aspirations', (PAR['B.USA'], PAR['B.CHN'], PAR['B.EU']) == (.60, .90, .60) and {PAR['X.USA'], PAR['X.CHN'], PAR['X.EU']} == {2},
    'USA 0.60, CHN 0.90, EU 0.60', 'at most 2 access levels')
o = R['orientation']
chk('orientation', len(o['contested']) == 6 and all(r2(c['largest']) == .18 for c in o['contested']) and o['owner_side'] == [],
    'all 6 access levers fail it', 'by 0.18 per level')
a = R['acceptable']
chk('regions', (a['n'], a['n_ir'], a['n_ir_and_acceptable']) == (4527, 2448, 548),
    '4,527 profiles are acceptable to all, 2,448 are individually rational, 548 are both')
c = R['core']
chk('core empty', c['n_core'] == 0 and c['n_efficient'] == 6 and c['blocked'] == {'USA+CHN+EU': 542, 'USA+CHN': 3, 'USA+EU': 3},
    '542 are Pareto-dominated', 'The other 6 are blocked by pairs: 3 by USA+CHN and 3 by USA+EU')
w = R['core_without_aspirations']
chk('core empty without aspirations', (w['n_ir'], w['n_efficient'], w['n_core']) == (2448, 204, 0),
    '204 profiles are efficient and individually rational. All are blocked.')
chk('E3', R['E3']['passed'] and R['E3']['candidates_without_blocker'] == 0, 'for each of the 548 candidates. Passed.')
e1 = R['E1']
chk('E1', e1['passed'] and len(e1['runs']) == 8 and all(x['rounds'] == 5 and x['cuts'] == 4 for x in e1['runs'])
    and e1['runs_that_excluded_every_candidate'] == 8, 'All 8 runs returned none', '5 rounds and 4 cuts',
    'Each excluded every candidate with 4 cuts')
ev = [x['evals'] for x in e1['runs']]
chk('E1 look-ups', (min(ev), max(ev)) == (12746, 13634) and round(100 * min(ev) / 46656) == 27 and round(100 * max(ev) / 46656) == 29,
    '12,746 to 13,634 distinct profiles, 27 to 29 %')
md = f1['margin_distribution']
chk('margin range', (r3(md['min']), r3(md['max']), r3(md['median'])) == (.165, .661, .439) and f1['n_minimisers'] == 1,
    'from 0.165 to 0.661, with median 0.439', 'One profile with margin 0.165')
p = f1['profile']
chk('fallback profile', [p[k] for k in ('USA.access_CHN', 'USA.access_EU', 'CHN.access_EU', 'CHN.access_USA', 'EU.access_USA',
                                         'EU.access_CHN', 'USA.climate', 'CHN.climate', 'EU.climate')] == [2, 0, 0, 0, 1, 1, 1, 2, 1],
    '| USA access for CHN, for EU | 2, 0 |', '| CHN access for EU, for USA | 0, 0 |', '| EU access for USA, for CHN | 1, 1 |',
    '| climate USA, CHN, EU | 1, 2, 1 |')
chk('fallback measures', r2(f1['Q']) == .76 and [r2(f1['norm_gain'][k]) for k in ('USA', 'CHN', 'EU')] == [.47, .59, .13]
    and r3(f1['eps']) == .165 and f1['coalitions_gaining_by_over_fulfilment'] == 3,
    '| Q | 0.76 |', '| 0.47, 0.59, 0.13 |', '| blocking margin in the package game | 0.165 |', '| groups that gain by over-fulfilling | 3 |')
mg = f1['margins']
chk('margins', [r3(mg[k]) for k in ('CHN+EU', 'USA+EU', 'USA+CHN', 'USA+CHN+EU')] == [.165, .145, .072, .026]
    and all(mg[k] < 0 for k in ('USA', 'CHN', 'EU'))
    and set(f1['strict_blockers']) == {'USA+CHN', 'USA+EU', 'CHN+EU', 'USA+CHN+EU'} and not f1['pareto_efficient'],
    'CHN+EU 0.165, USA+EU 0.145, USA+CHN 0.072, grand coalition 0.026', 'all three pairs, and the grand coalition')
e2 = R['E2']
chk('E2', e2['passed'] and e2['n_deviations'] == 50652 and e2['registry_vs_closed_form_mismatches'] == 0
    and e2['no_single_actor_deviates'] and f1['registry_returns_profile']
    and e2['groups_with_profitable_deviation'] == {'USA+CHN': 3, 'USA+EU': 15, 'CHN+EU': 16, 'USA+CHN+EU': 1},
    'All 50,652 joint deviations', 'USA+CHN with 3 deviations, USA+EU with 15, CHN+EU with 16, and the grand coalition with 1')
pe = R['fallback1_efficient_post_hoc']
q = pe['profile']
chk('efficient fallback', pe['n_efficient_candidates'] == 6 and r3(pe['eps']) == .220 and r2(pe['Q']) == .70
    and [q[k] for k in ('USA.access_CHN', 'USA.access_EU', 'CHN.access_EU', 'CHN.access_USA', 'EU.access_USA', 'EU.access_CHN',
                        'USA.climate', 'CHN.climate', 'EU.climate')] == [2, 1, 0, 0, 1, 2, 1, 2, 0]
    and [r2(pe['norm_gain'][k]) for k in ('USA', 'CHN', 'EU')] == [.04, .71, .44]
    and set(pe['strict_blockers']) == {'USA+CHN', 'USA+EU', 'CHN+EU'} and pe['coalitions_gaining_by_over_fulfilment'] == 1,
    '| 2, 0 | 2, 1 | 0, 0 |', '| 1, 1 | 1, 2 | 0, 0 |', '| 1, 2, 1 | 1, 2, 0 | 1, 1, 1 |', '| 0.76 | 0.70 | 0.46 |',
    '| 0.04, 0.71, 0.44 |', '| 0.165 | 0.220 | 0.479 |', '| 3 | 1 | not computed |', '0.220 against 0.165')
for key, row in {'access': (729, 9, 1, 0, 0), 'climate': (64, 9, 7, 7, 7), 'access+climate': (46656, 2448, 204, 0, 0)}.items():
    v = f3[key]
    chk('sub-package ' + key, (v['n_profiles'], v['n_ir'], v['n_efficient'], v['n_core'], v['n_core_in_C']) == row)
chk('sub-package rows in text', True, '| access | 729 | 9 | 1 | 0 | 0 |', '| climate | 64 | 9 | 7 | 7 | 7 |',
    '| access and climate | 46,656 | 2,448 | 204 | 0 | 0 |', 'The climate issue alone has 7 core profiles')
npt = f3['climate']['nash_point']
chk('climate-only deal', f3['subpackage_with_core'] == 'climate' and [npt['profile'][k] for k in ('USA.climate', 'CHN.climate', 'EU.climate')] == [1, 1, 1]
    and sum(npt['profile'].values()) == 3 and r2(npt['Q']) == .46 and [r2(npt['norm_gain'][k]) for k in ('USA', 'CHN', 'EU')] == [.30, .14, .47]
    and r3(npt['margin_in_package_game']) == .479 and set(npt['blockers_in_package_game']) == {'USA+CHN', 'USA+EU', 'CHN+EU', 'USA+CHN+EU'}
    and 2.5 < npt['margin_in_package_game'] / f1['eps'] < 3,
    '| 0.30, 0.14, 0.47 |', 'There its margin is 0.479, almost three times', 'its focal deal has margin 0.479')
# contested variant
chk('kappa', K['kappa'] == .20 and {(v['lever'], v['actor']) for v in K['orientation']['violations']} ==
    {('USA.ai_oversight', 'DEV'), ('CHN.ai_oversight', 'DEV')} and all(r2(v['largest']) == .17 for v in K['orientation']['violations']),
    'compliance burden of 0.20 per level', 'up to 0.17 per level')
kc = K['core']
chk('contested core', (kc['n_candidates'], kc['n_efficient'], kc['blocked_by_proper_coalitions'], kc['n_core']) == (1351, 833, 434, 399)
    and max((n, G) for G, n in kc['blocked'].items() if G.count('+') < 7) == (276, 'USA+CHN+EU+IND+LIC+MDB'),
    '1,351 candidates', '833 of them are efficient', 'proper coalitions block 434', 'has 399 profiles', 'with 276 profiles')
g = K['G1c']
evs = [x['evals'] for x in g['runs']]
chk('G1c', g['passed'] and len(g['runs']) == 8 and all(x['same_as_enumeration'] and x['rounds'] == 16 and x['cuts'] == 15 for x in g['runs'])
    and round(min(evs), -3) == 93000 and round(max(evs), -3) == 102000 and round(100 * g['mean_share_of_profiles_evaluated']) == 5,
    'in 8 of 8 runs, with 15 cuts each', '16 rounds and 15 cuts', '93,000 to 102,000', 'about 5 % of the lattice')
kn = K['nash']
ce = kn['certificate']
chk('returned profile', kn['profile']['USA.ai_oversight'] == 0 and kn['profile']['CHN.ai_oversight'] == 0 and kn['profile']['DEV.ai_safety'] == 2
    and (r2(kn['Q']), r2(kn['A']), kn['P']) == (.95, .20, 1.0) and ce['strict_core_by_direct_test'] and ce['individually_rational']
    and ce['acceptable_to_all'] and ce['coalitions_gaining_by_over_fulfilment'] == 32 and not ce['strictly_strong_equilibrium_certified'],
    'Q 0.95, A 0.20 and P 1', '32 groups gain this way')
ph = K['over_fulfilment_post_hoc']
ne = ph['nash_among_equilibria']
chk('equilibria among core', (ph['core_profiles_that_are_equilibria'], ph['core_profiles']) == (150, 399)
    and ph['minimal_groups_gaining_at_nash'] == ['USA+CHN'] and ph['equilibria_with_any_oversight'] == 150
    and ph['core_profiles_with_any_oversight'] == 150 and 399 - 150 == 249
    and ne['profile']['USA.ai_oversight'] == 1 and ne['profile']['CHN.ai_oversight'] == 1 and ne['profile']['DEV.ai_safety'] == 0
    and r2(ne['A']) == .35 and round(100 * ne['norm_gain']['DEV']) == 16,
    '150 of 399 core profiles are equilibria', '150 of the 399 core profiles are equilibria', 'one of the other 249',
    'exactly the 150 that already contain oversight', 'with A 0.35', 'DEV keeps 16 %', 'USA+CHN is the only minimal one')
print(f'all {n_ok} checks passed against {OUT}')
