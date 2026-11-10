"""Assert every number quoted in the write-up (docs/phase0_results.md) against the result files.

Usage: python3 check_writeup.py [results_dir]
"""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
R = json.load(open(os.path.join(OUT, 'results.json')))
G = json.load(open(os.path.join(OUT, 'gate1_stress.json')))
Dn = json.load(open(os.path.join(OUT, 'dynamics.json')))
X = json.load(open(os.path.join(OUT, 'extras.json')))
n_ok = 0


def chk(name, cond):
    global n_ok
    assert cond, name
    n_ok += 1


def r2(x):
    return round(x + 1e-12, 2)


M, rob, lk = R['menu'], R['robustness'], R['linkage']
n = rob['n']
# result in brief
chk('size', (R['meta']['n_actors'], R['meta']['n_levers'], R['meta']['n_profiles'], R['meta']['n_coalitions']) == (8, 12, 1990656, 255))
chk('core 326', R['core']['n_core'] == 326)
chk('five distinct candidates', len({m['flat'] for m in M.values()}) == 5 and R['lead'] == 'robust')
chk('lead 143 of 150', round(M['robust']['robustness']['all_three'] * n) == 143 and n == 150)
chk('nash 90 of 150', round(M['nash']['robustness']['all_three'] * n) == 90)
chk('nash loses acceptability in 40 %', r2(1 - M['nash']['robustness']['acceptable']) == 0.40)
chk('gate 1: 8 of 8', R['gate1']['passed'] and len(R['gate1']['runs']) == 8 and all(x['same_as_enumeration'] for x in R['gate1']['runs']))
chk('oracle 64 % and 98 %', r2(G['B1']['recall_first_version']) == 0.64 and r2(G['B1']['recall']) == 0.98)
chk('orientation fails in 42 %', r2(1 - rob['share_orientation']) == 0.42 and round(rob['share_orientation'] * n) == 87)
# checks before the search
s = R['sufficiency']
chk('orientation at base', R['orientation']['passed'] and
    {(v['lever'], v['actor']) for v in R['orientation_contested_variant']} == {('USA.ai_oversight', 'DEV'), ('CHN.ai_oversight', 'DEV')})
chk('climate target', r2(s['climate']['target']) == 1.30 and r2(s['climate']['max']) == 1.95 and s['climate']['veto'] == ['CHN']
    and s['climate']['minimal_groups'] == ['USA+CHN+EU', 'USA+CHN+IND', 'USA+CHN+FEX', 'CHN+EU+IND', 'CHN+EU+FEX', 'CHN+IND+FEX'])
chk('ai target', r2(s['ai']['target']) == 0.67 and s['ai']['minimal_groups'] == ['USA+CHN'] and s['ai']['veto'] == ['USA', 'CHN'])
chk('pandemic target', s['pandemic']['target'] == 1.0 and s['pandemic']['minimal_groups'] == ['IND+LIC'])
a = R['acceptable']
N = R['meta']['n_profiles']
chk('acceptable region', (a['n'], a['n_ir'], a['n_ir_and_acceptable']) == (12810, 82022, 3403))
chk('shares of lattice', r2(100 * a['n'] / N) == 0.64 and round(100 * a['n_ir'] / N, 1) == 4.1 and r2(100 * a['n_ir_and_acceptable'] / N) == 0.17)
chk('per actor 39 to 78 %', min(a['per_actor'], key=a['per_actor'].get) == 'CHN' and r2(a['per_actor']['CHN']) == 0.39
    and max(a['per_actor'], key=a['per_actor'].get) == 'MDB' and r2(a['per_actor']['MDB']) == 0.78)
# core, menu, certificates
c = R['core']
chk('enumeration', c['n_candidates'] == 3403 and c['n_efficient'] == 326 and list(c['blocked'].values()) == [3077] and len(c['blocked']) == 1)
lc = X['core_level_counts']
chk('shape of core', lc['USA.ai_oversight'] == [0, 326, 0] and lc['CHN.ai_oversight'] == [0, 326, 0] and lc['FEX.climate'][1] == 196
    and lc['IND.surveillance'][1] == 225 and lc['LIC.surveillance'][2] == 225
    and all(lc[k][3] == 0 for k in lc if k.endswith('.climate')))
ir = c['indicator_range']
chk('indicator ranges', [r2(v) for v in ir['Q']] == [0.51, 0.90] and [r2(v) for v in ir['A']] == [0.35, 0.55] and ir['P'] == [0.5, 1.0])
chk('six tie', rob['joint_share_over_core']['n_at_max'] == 6 and rob['joint_share_over_core']['n_at_or_above_0_9'] == 9)
table = {  # lever rows of the menu table: nash, leximin, deepest, ambition, robust
    'USA.climate': [2, 1, 2, 2, 2], 'EU.climate': [1, 1, 1, 2, 1], 'FEX.climate': [0, 0, 0, 1, 0],
    'IND.surveillance': [1, 1, 0, 1, 1], 'LIC.surveillance': [2, 2, 1, 2, 2], 'DEV.ai_safety': [1, 1, 1, 2, 1],
    'MDB.finance_lic': [1, 2, 2, 1, 2]}
order = ['nash', 'leximin', 'deepest', 'ambition', 'robust']
for lever, vals in table.items():
    chk('menu ' + lever, [M[k]['profile'][lever] for k in order] == vals)
for lever, v in {'USA.ai_oversight': 1, 'CHN.climate': 1, 'CHN.ai_oversight': 1, 'EU.finance_lic': 2, 'IND.climate': 1}.items():
    chk('identical ' + lever, all(M[k]['profile'][lever] == v for k in order))
chk('menu Q', [r2(M[k]['Q']) for k in order] == [0.66, 0.55, 0.66, 0.82, 0.66])
chk('menu A', [r2(M[k]['A']) for k in order] == [0.45, 0.45, 0.45, 0.55, 0.45])
chk('menu P', [M[k]['P'] for k in order] == [1, 1, 0.5, 1, 1])
mins = [(min(M[k]['norm_gain'], key=M[k]['norm_gain'].get), r2(min(M[k]['norm_gain'].values()))) for k in order]
chk('smallest gains', mins == [('USA', 0.55), ('IND', 0.58), ('USA', 0.31), ('FEX', 0.39), ('USA', 0.55)])
chk('FEX gains', [r2(M[k]['norm_gain']['FEX']) for k in order] == [0.92, 0.90, 0.68, 0.39, 0.92])
chk('acceptable shares', [round(100 * M[k]['robustness']['acceptable']) for k in order] == [60, 95, 100, 19, 95])
chk('core shares', [round(100 * M[k]['robustness']['strict_core']) for k in order] == [100, 100, 33, 100, 100])
chk('joint shares', [round(100 * M[k]['robustness']['all_three']) for k in order] == [60, 95, 33, 19, 95])
chk('nash and robust differ only in MDB finance',
    [k for k in M['nash']['profile'] if M['nash']['profile'][k] != M['robust']['profile'][k]] == ['MDB.finance_lic'])
for k in order:
    ce = M[k]['certificate']
    chk('certificate ' + k, ce['individually_rational'] and ce['acceptable_to_all'] and ce['strict_core_by_direct_test']
        and ce['registry_returns_profile'] and ce['coalitions_gaining_by_over_fulfilment'] == 0
        and ce['strictly_strong_equilibrium_certified'])
ce = M['robust']['certificate']
chk('depth', ce['tightest_coalition_missing_a_contributor']['coalition'] == 'USA+CHN+EU+IND+LIC+MDB'
    and round(ce['tightest_coalition_missing_a_contributor']['margin'], 3) == -0.094 and ce['max_margin_all_coalitions'] == 0.0)
chk('software test', ce['sampled_deviations'] == dict(n=20000, registry_vs_closed_form_mismatches=0, profitable=0))
chk('seven contributors', ce['contributors'] == ['USA', 'CHN', 'EU', 'IND', 'LIC', 'DEV', 'MDB'])
# gate 1
runs = R['gate1']['runs']
chk('one round, no cut', all(x['rounds'] == 1 and x['cuts'] == 0 for x in runs))
chk('look-ups', round(min(x['evals'] for x in runs), -3) == 41000 and round(max(x['evals'] for x in runs), -3) == 44000
    and round(100 * R['gate1']['mean_share_of_profiles_evaluated']) == 2)
chk('stress variant', (G['n_efficient'], G['n_blocked'], G['n_core']) == (21490, 1841, 19649))
chk('B1', (G['B1']['detected_by_first_version'], G['B1']['detected'], G['B1']['n']) == (191, 294, 300)
    and G['B1']['invalid_blocks'] == 0 and G['B1']['false_alarms_on_200_core_profiles'] == 0)
chk('B1 hold-out', (G['B1_holdout']['detected'], G['B1_holdout']['n']) == (300, 300))
b2 = G['B2']['runs']
chk('B2', len(b2) == 24 and G['B2']['all_in_core'] and G['B2']['share_reaching_optimum'] == 1.0 and sum(x['cuts'] > 0 for x in b2) == 3)
# linkage
want = {'USA': (-0.17, 0.25, 0.50), 'CHN': (0.10, 0.16, 0.50), 'EU': (0.23, 0.36, 0.44), 'IND': (0.44, 0.225, 0.20),
        'FEX': (0.10, 0.18, 0.30), 'LIC': (0.66, 0.135, 0.60), 'DEV': (0.03, 0.19, 0.20), 'MDB': (0.26, 0.09, 0.30)}
for act, w in want.items():
    got = [lk['per_issue_gain'][iss][act] for iss in ('climate', 'ai', 'pandemic')]
    chk('gain by issue ' + act, all(abs(g - x) < 0.0051 for g, x in zip(got, w)))
chk('only USA loses', lk['actors_losing_on_some_issue'] == {'climate': ['USA'], 'ai': [], 'pandemic': []})
chk('single-issue cores', [lk['single_issue_core'][i]['n'] for i in ('climate', 'ai', 'pandemic')] == [3, 3, 14])
im = X['indicator_max']
chk('largest indicators', r2(im['Q']['single_issue_core']) == 0.55 and r2(im['Q']['package_core']) == 0.90
    and r2(im['A']['single_issue_core']) == 0.55 and r2(im['A']['package_core']) == 0.55
    and im['P']['single_issue_core'] == 1.0 and im['P']['package_core'] == 1.0)
cb = X['combinations_of_single_issue_core_profiles']
chk('combinations', (cb['n'], cb['in_package_strict_core_ignoring_aspirations'], cb['acceptable_to_all'],
                     cb['in_package_core_inside_acceptable_region']) == (126, 56, 33, 11))
sd = lk['separate_deals']
chk('separate deals', sd['profile'] == M['leximin']['profile'] and sd['in_package_strict_core']
    and sd['package_core_profiles_better_for_all'] == 0)
d = sd['lead_gain_minus_separate']
chk('lead against separate', r2(d['USA']) == -0.26 and r2(min(v for k, v in d.items() if k != 'USA')) == 0.01
    and r2(max(d.values())) == 0.11)
# robustness
chk('factor range', rob['factor_range'] == [0.8, 1.25])
bc = rob['base_core_profiles_still_acceptable_ir_core']
chk('base core per draw', round(bc['mean']) == 102 and (bc['min'], bc['max']) == (12, 278))
chk('lead failures', X['lead_draws_not_acceptable'] == 7 and X['lead_failing_aspirations_by_actor'] == {'LIC': 7})
sens = rob['lead_sensitivity']
chk('sensitivity', sens['kL.LIC'] > 0 and sens['r.LIC'] < 0 and list(sens)[:2] == ['kL.LIC', 'r.LIC'])
chk('lead core and equilibrium', M['robust']['robustness']['strict_core'] == 1.0 and M['robust']['robustness']['equilibrium'] == 1.0
    and rob['lead_blockers'] == {})
chk('deepest leaves core', round((1 - M['deepest']['robustness']['strict_core']) * n) == 100 and M['deepest']['robustness']['acceptable'] == 1.0)
chk('orientation failures', rob['owner_side_orientation_failures'] ==
    {'USA.ai_oversight': 31, 'IND.surveillance': 25, 'DEV.ai_safety': 16, 'CHN.climate': 1} and rob['draws_with_a_non_owner_harmed'] == 0)
# updating and compliance
L, Cp = Dn['learning'], Dn['learning_capped']
chk('ladders', Dn['ladder_profiles'] == 155520 and Dn['orientation_on_ladders'])
chk('published rule', (L['n_orders'], L['distinct_outcomes']) == (200, 137) and L['share_acceptable'] == 0.01
    and L['share_full_strict_core'] == 0.705 and r2(L['share_fex_contributes']) == 0.63 and r2(L['mean_Q']) == 1.02
    and L['share_ladder_weak_core'] == 1.0 and set(L['share_with_positive_gain_by_position_in_order']) == {1.0})
chk('capped rule', Cp['distinct_outcomes'] == 62 and Cp['share_acceptable'] == 0.95
    and Cp['share_in_core_inside_acceptable_region'] == 0.675 and Cp['share_full_strict_core'] == 0.675
    and r2(Cp['share_fex_contributes']) == 0.58 and r2(Cp['mean_Q']) == 0.72
    and Cp['constraints_not_usable_as_caps'] == ['EU: climate progress at or above floor'])
al = Dn['linc_probe']['alpha_min']
chk('compensation factor', [r2(al[k]) for k in ('USA', 'CHN', 'EU', 'IND')] == [1.34, 0.99, 1.27, 1.11]
    and Dn['linc_probe']['delta'] == 0.9 and Dn['linc_probe']['n'] == 4)
# lessons
chk('FEX on the menu', sum(M[k]['profile']['FEX.climate'] > 0 for k in order) == 1)
# brief quoted in the write-up
brief = open(os.path.join(OUT, 'briefs.md')).read()
chk('brief excerpt', 'Own cost: 0.60.' in brief and 'Your net gain over no deal: 0.58 (55 % of your largest acceptable gain).' in brief
    and 'Gain by issue: climate -0.17, ai +0.25, pandemic +0.50.' in brief)
print(f'all {n_ok} checks passed against {OUT}')
