"""Assert every number quoted in docs/phase0_towers.md against results2/tower_*.json and against the text."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results2')
T2 = json.load(open(os.path.join(OUT, 'tower_instance2.json')))
TC = json.load(open(os.path.join(OUT, 'tower_contested.json')))
TR = json.load(open(os.path.join(OUT, 'tower_relaxed.json')))
DOC = ' '.join(open(os.path.join(HERE, '..', 'docs', 'phase0_towers.md')).read().split())
n_ok = 0


def chk(name, cond, *quoted):
    global n_ok
    assert cond, name
    for q in quoted:
        assert q in DOC, f'{name}: not in the write-up: {q!r}'
    n_ok += 1


def r2(x):
    return round(x + 1e-12, 2)


b = T2['bases']
chk('triangle', T2['tower'] is None and sorted(T2['harmed']) == ['CHN', 'EU', 'USA']
    and sorted(b['coalitions_that_form_a_cpep_from_zero']) == ['CHN', 'EU', 'USA']
    and (b['n_profiles'], b['n_leaving_a_cpep_for_all'], b['of_these_with_an_inactive_actor']) == (46656, 64, 0),
    'All 3 actors are harmed', 'only the 3 single actors form a CPEP', 'Of the 46,656 profiles, 64 leave a proper CPEP')
b = TC['bases']
s1 = TC['with_aspirations']['stages'][0]
n1, n2 = TC['without_aspirations']['stages']
chk('contested chain and counts', TC['harmed'] == ['DEV'] and len(TC['chain'][0]) == 7 and len(TC['chain'][1]) == 8
    and (b['n_leaving_a_cpep_for_all'], b['n_profiles']) == (221184, 1990656)
    and (s1['n_core'], s1['n_core_acceptable'], s1['n_candidates']) == (4621, 142, 0)
    and not TC['with_aspirations']['found'] and n1['n_candidates'] == 870 and not TC['aspiration_filter_used'],
    '| profiles that leave a proper CPEP for all eight | 221,184 of 1,990,656 |',
    '| strict core of the first stage, seven actors | 4,621 |', '| of these, acceptable to the seven | 142 |',
    '| of these, leaving a proper CPEP for the last stage | 0 |', '| without aspirations: first-stage candidates | 870 |')
t = TC['tower']
chk('tower without aspirations', n1['profile']['USA.ai_oversight'] == 2 and n1['profile']['CHN.ai_oversight'] == 2
    and (r2(t['indicators']['Q']), r2(t['indicators']['A']), t['indicators']['P']) == (.85, .70, 1.0)
    and (n2['box_profiles'], n2['n_core']) == (1296, 1) and not n2['nontrivial']
    and round(100 * t['final_norm_gain_over_a0']['DEV']) == -53 and not t['final_acceptable_to_all'],
    'oversight 2 in both states, Q 0.85, A 0.70, P 1', 'has 1,296 profiles and a strict core of one', 'holds −53 %')
og = TC['original_game']
chk('tests and original game', all(TC[k]['passed'] for k in ('T1', 'T2', 'T3', 'T4'))
    and (og['n_deviations'], og['n_groups'], og['groups_with_profitable_deviation']) == (7909199, 255, 4)
    and og['minimal_groups'] == ['USA+CHN+EU+IND+LIC+DEV'] and round(og['largest_margin']['margin'], 3) == .017
    and og['largest_margin']['outcome']['USA.ai_oversight'] == 1 and og['largest_margin']['outcome']['CHN.ai_oversight'] == 1,
    'All 7,909,199 unconditional deviations of all 255 groups', '4 groups can gain', 'everyone except FEX and MDB',
    'gains 0.017', '4 of 255 groups can still gain, by a margin of at most 0.017')
ph = TC['all_first_stage_candidates_post_hoc']
chk('all candidates', (ph['n_candidates'], ph['n_with_nontrivial_last_stage'], ph['n_where_newcomers_end_at_or_above_a0']) == (870, 15, 0)
    and round(100 * ph['best_final_norm_gain_of_a_newcomer']) == -43,
    '15 allow a last stage that adds something', 'Its best result is −43 %', 'in every one of the 870 towers')
chk('relaxed counts', (TR['n_first_stage'], TR['n_first_stage_with_a_second'], TR['n_pairs'], TR['n_pairs_nontrivial'],
                       TR['n_pairs_all_at_or_above_a0']) == (142, 125, 169, 75, 150),
    '| acceptable first-stage core profiles | 142 |', '| of these, with an admissible last stage | 125 |',
    '| towers (pairs of outcomes), acceptable to all | 169 |', '| of these, with a last stage that adds something | 75 |',
    '| of these 169, with every actor at or above no deal | 150 |', 'there are 169 two-stage towers')
rt = TR['tower']
g = rt['final_norm_gain_over_a0']
chk('relaxed tower', rt['final'] == rt['stage1'] and rt['final']['USA.ai_oversight'] == 1 and rt['final']['CHN.ai_oversight'] == 1
    and rt['final']['DEV.ai_safety'] == 0 and (r2(rt['indicators']['Q']), r2(rt['indicators']['A']), rt['indicators']['P']) == (.82, .35, 1.0)
    and min(g, key=g.get) == 'DEV' and round(100 * g['DEV']) == 20 and not rt['last_stage_is_proper_cpep']
    and all(TR[k]['passed'] for k in ('T1', 'T2', 'T3', 'T4')) and TR['original_game']['strictly_strong_equilibrium']
    and TR['original_game']['groups_with_profitable_deviation'] == 0,
    'oversight 1 in both states, Q 0.82, A 0.35, P 1', 'DEV holds 20 %', 'the filing is a strictly strong equilibrium')
print(f'all {n_ok} checks passed against {OUT}')
