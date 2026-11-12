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
# ---- pilot B2 (version 2) and the note on the hardwired-pause report
import sys
import numpy as np
sys.path.insert(0, HERE)
import pilot_b2 as M2
B2 = json.load(open(os.path.join(HERE, 'results', 'pilot_b2.json')))
P2 = json.load(open(os.path.join(HERE, 'results', 'pilot_b2_params.json')))['base']
NB, OL = txt('docs', 'note_hardwired_pause.md'), txt('outreach', 'outline_B2.md')
chk('B2 sourced inputs', (P2['alpha'], P2['stockB.USA'], P2['stockB.CHN'], P2['gain']) == (.25, .20, .018, .57)
    and (P2['dark0.USA'], P2['dark1.USA'], P2['dark2.USA'], P2['dark0.CHN'], P2['dark1.CHN'], P2['dark2.CHN'])
    == (.047, .0094, .0011, .16, .018, .0011), NB, '57 % a year')
k = np.log(10) / np.log(1 + P2['gain'])
tab = [[round(float(k * min(P2['cap'], M2.headroom(P2, 'USA', np.array(2), np.array(d)), M2.headroom(P2, 'USA', np.array(2), np.array(d)),
                              M2.headroom(P2, 'CHN', np.array(cc), np.array(3)))), 1) for cc in range(3)] for d in range(4)]
rows = ['| United States keeps its whole fleet at home | 0.5 | 0.5 | 0.5 |', '| keeps half | 1.0 | 2.0 | 2.0 |',
        '| keeps a tenth | 1.0 | 5.6 | 5.6 |', '| keeps a residual | 1.0 | 5.8 | 10.2 |']
for doc in (NB, OL):
    chk('durability table', tab == [[0.5, 0.5, 0.5], [1.0, 2.0, 2.0], [1.0, 5.6, 5.6], [1.0, 5.8, 10.2]], doc, *rows)
cn_home = round(float(k * min(P2['cap'], M2.headroom(P2, 'USA', np.array(2), np.array(3)), M2.headroom(P2, 'CHN', np.array(2), np.array(0)))), 1)
chk('China fleet at home caps durability', cn_home == 5.8, NB, 'caps durability at 5.8 years')
t = B2['tower']
rg = B2['regions']
tipped = {r['parameter'] for r in B2['tipping_post_hoc']['ranking']}
full = {'USA.pause': 1, 'USA.census': 2, 'USA.drawdown': 3, 'CHN.pause': 1, 'CHN.census': 2, 'CHN.drawdown': 3}
chk('B2 skeleton', (B2['n_profiles'], B2['n_groups'], rg['acceptable'], rg['individually_rational'], rg['both'],
                    B2['core']['n_core'], B2['core']['n_equilibria']) == (2304, 7, 318, 49, 39, 2, 2)
    and B2['tower_chain'] == 'fixed' and B2['chain'][0] == ['USA', 'CHN']
    and t['stage1'] == dict(full, **{'SUP.production_stop': 0, 'SUP.monitoring': 0})
    and t['final'] == dict(full, **{'SUP.production_stop': 1, 'SUP.monitoring': 1})
    and round(t['stage1_indicators']['YEARS']) == 5 and round(t['final_indicators']['YEARS']) == 10
    and B2['chain_scan_post_hoc']['first_coalitions_with_a_nontrivial_first_stage'] == ['USA+CHN']
    and B2['full_game']['strictly_strong_equilibrium'] and all(B2['tests'].values())
    and B2['withdrawal']['SUP']['falls_to'] == 'stage 1' and B2['withdrawal']['USA']['falls_to'] == 'zero'
    and B2['withdrawal']['CHN']['falls_to'] == 'zero' and 'G' not in tipped and 3.0 in B2['tipping_post_hoc']['grid'], NB,
    '| lattice | 2,304 profiles, 7 groups |', '| 318; 49; 39 |', '| 2 profiles, both equilibria |',
    'about 5 years after stage 1, about 10 after stage 2', 'only the two lead states together',
    'suppliers out: back to stage 1; either lead state out: back to zero', 'can be tripled without breaking the certificate')
chk('B2 in the outline', True, OL, 'if the suppliers leave, the outcome falls back to the first stage; if a lead state leaves, to nothing',
    'tripled', 'the two lead states first, the suppliers on top')
x_mutual = P2['a.USA'] * 0.5 - P2['f.USA']      # value of a bare mutual pause at half durability, illustrative
chk("B2 tripled gain makes a Prisoner's Dilemma", P2['G'] < x_mutual < 3 * P2['G'], NB, "the stage game is a Prisoner's Dilemma, not a stag hunt")
print(f'all {n_ok} checks passed')
