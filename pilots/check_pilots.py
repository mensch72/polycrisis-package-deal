"""Assert every model number quoted in the pilot notes and briefs against pilots/results and against the texts."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'results', 'pilot_a.json')))
B = json.load(open(os.path.join(HERE, 'results', 'pilot_b.json')))
PA = json.load(open(os.path.join(HERE, 'results', 'pilot_a_params.json')))['base']
txt = lambda *p: ' '.join(open(os.path.join(HERE, '..', *p)).read().split())
DA, DB = txt('docs', 'pilot_A_country_platform.md'), txt('docs', 'pilot_B_frontier_ai.md')
BA, BB = txt('outreach', 'brief_A.md'), txt('outreach', 'brief_B.md')
n_ok = 0


def chk(name, cond, doc, *quoted):
    global n_ok
    assert cond, name
    for q in quoted:
        assert q in doc, f'{name}: not in the text: {q!r}'
    n_ok += 1


r2 = lambda x: round(x + 1e-12, 2)
# ---- pilot A
chk('A pledges', (PA['S.DEU'], PA['S.GBR'], PA['S.EU'], PA['S.FRA'], PA['G.DEU'], PA['G.GBR'], PA['G.EU'], PA['G.FRA'])
    == (2898, 1875, 1592, 1084, 338, 75, 264, 4), DA,
    'USD 2,898 million', 'grants of 338', 'USD 1,875 million', 'grants of 75', 'USD 1,592 million', 'grants of 264',
    'USD 1,084 million', 'grants of 4')
rg, co, tw = A['regions'], A['core'], A['towers']
chk('A counts', (A['n_profiles'], A['n_groups'], rg['acceptable'], rg['individually_rational'], rg['both'], co['n_core'],
                 co['n_equilibria']) == (3072, 31, 858, 498, 204, 89, 89), DA,
    '| lattice | 3,072 profiles, 31 groups |', '| 858; 498; 204 |', '| 89, all of them equilibria |')
sc = A['chain_scan_post_hoc']
chk('A chains', (tw['n_first_stage_core'], tw['n_first_stage_admissible'], tw['n_towers']) == (12, 0, 0)
    and A['chain'][0] == ['ZAF', 'DEU', 'GBR'] and (sc['n_first_coalitions'], sc['n_with_a_tower'], sc['n_with_a_nontrivial_first_stage']) == (30, 19, 3)
    and A['chain_used'][0] == ['ZAF', 'DEU', 'GBR', 'EU'], DA,
    'no tower: 12 first-stage core profiles, none acceptable', '| 19 have a tower; 3 have a first stage that does something |',
    'South Africa, Germany, United Kingdom and EU first, then France')
t = A['tower']
chk('A tower', (t['stage1']['ZAF.ambition'], t['stage1']['ZAF.reform'], t['final']['ZAF.ambition'], t['final']['ZAF.reform']) == (2, 1, 3, 2)
    and round(t['stage1_indicators']['F'], 1) == 3.6 and round(t['final_indicators']['F'], 1) == 7.1
    and all(A['tests'].values()) and A['full_game']['strictly_strong_equilibrium'], DA,
    'Stage 1: ambition 2, reform 1, about USD 3.6 billion', 'ambition 3, reform 2, about USD 7.1 billion', 'strictly strong equilibrium')
chk('A tower in brief', True, BA, 'about USD 3.6 billion allocated', 'about USD 7.1 billion', 'a first step among four parties')
w = A['withdrawal']
chk('A withdrawal', w['FRA']['falls_to'] == 'stage 1' and all(w[k]['falls_to'] == 'zero' for k in ('ZAF', 'DEU', 'GBR', 'EU')), DA,
    'If France files nothing, the registry returns stage 1', 'it returns zero')
tp = {r['parameter']: r for r in A['tipping_post_hoc']['ranking']}
chk('A sensitivity', A['robustness']['final_stays_certified'] == 173 and A['robustness']['n'] == 200
    and tp['rho']['down'] == 1.25 and tp['ca']['up'] == 1.25 and tp['conc']['down'] == 1.5 and tp['smax.DEU']['down'] == 1.5
    and sum(1 for r in tp.values() if min(x for x in (r['up'], r['down'], 99) if x) <= 1.25) == 2, DA,
    '173 of 200 draws', 'two numbers tip it at a factor of 1.25', 'tip it at 1.5')
# ---- pilot B
rg, co, tw = B['regions'], B['core'], B['towers']
sc = B['chain_scan_post_hoc']
chk('B counts', (B['n_profiles'], B['n_groups'], rg['acceptable'], rg['individually_rational'], rg['both'], co['n_core'],
                 co['n_equilibria'], tw['n_towers']) == (248832, 31, 12858, 143, 143, 55, 55, 92)
    and (sc['n_with_a_tower'], sc['n_with_a_nontrivial_first_stage']) == (30, 11) and B['tower_chain'] == 'fixed', DB,
    '| lattice | 248,832 profiles, 31 groups |', '| 12,858; 143; 143 |', '| 55, all of them equilibria |',
    '| towers along the fixed chain, A and B first | 92 |', '| all have a tower; 11 have a first stage that does something |')
t = B['tower']
f = t['final']
chk('B tower', not any(t['stage1'].values()) and all(f[f'{a}.safeguards'] == 1 for a in 'ABCDE')
    and [f[f'{a}.access'] for a in 'ABCDE'] == [2, 2, 1, 1, 0] and all(B['tests'].values())
    and B['full_game']['strictly_strong_equilibrium'] and all(v['falls_to'] == 'zero' for v in B['withdrawal'].values()), DB,
    'A and B do nothing alone; all five then move together', 'Every developer adds one safeguard tier',
    'access at tier 2, C and D at tier 1, E none', 'If any one developer files nothing, the registry returns zero')
chk('B tower in brief', True, BB, 'all five can move one tier together', 'collapses if any one of them stays out')
tp = B['tipping_post_hoc']['ranking']
chk('B sensitivity', B['robustness']['final_stays_certified'] == 200 and min(min(x for x in (r['up'], r['down'], 99) if x) for r in tp) == 2.0, DB,
    '200 of 200 draws', 'no number tips it below a factor of 2')
print(f'all {n_ok} checks passed')
