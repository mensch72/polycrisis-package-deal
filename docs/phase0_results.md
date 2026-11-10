# Phase 0: toy instance, first increment

> Exported on 10 November 2026 from the Claude Doc https://claude.ai/artifact/JsCtfcFLRjq5FHe33x6biu (tab "Phase 0 results", revision 18). Every number below is asserted against the result files by `phase0/check_writeup.py`.

2026-11-10

## Result in brief

The toy instance has a non-empty core and yields a certified menu of five packages. The search heuristic matches full enumeration, but only after one repair. All numbers except the emission shares are invented for the test, so nothing follows for real actors.

| Question | Finding | Status |
| --- | --- | --- |
| Did the pipeline run end to end? | Yes, once and in minimal form: 8 actors, 3 issues, 12 levers, 1,990,656 profiles, 255 coalitions. | [model] |
| Is there a core? | 326 profiles are acceptable to all and in the strict core. | [model], full enumeration |
| What is on the menu? | Five core profiles: Nash product, leximin, deepest, most ambitious, most robust. | [model] |
| Which one leads? | The most robust. It keeps all properties in 143 of 150 parameter draws. The Nash-product point does so in 90. | [model] |
| Is the lead self-enforcing as a set of filings? | Yes. Step-function filings through it form a strictly strong equilibrium, by exhaustive check. | [model] |
| Does heuristic search match enumeration? | The criterion is met in 8 of 8 runs. The test was weak, so stress tests followed. The first blocking oracle failed them, the second passes. | Gate 1 awaits Jobst's sign-off |

**What failed or looks weak.**

1. The Gate 1 criterion was met without the coalitional refinement ever being used.
2. The first blocking oracle found 64 % of known blocks. The repaired one finds 98 %.
3. The profile first recommended, the Nash-product point, lost acceptability in 40 % of the draws.
4. The orientation test fails somewhere on the lattice in 42 % of the draws.
5. Linkage gives no Pareto improvement over three separate deals in this instance.
6. The learning rule leaves the acceptable region unless aspirations cap the filed functions.

**Changed after seeing results.** Two things were added post hoc and are marked below: the stress tests for Gate 1, and the choice of the lead by robustness. The Gate 1 criterion itself is unchanged.

## The instance

The instance is small enough to enumerate and combines three dilemmas of different type. Only the emission shares come from data.

| Actor | Stands for | Levers and levels |
| --- | --- | --- |
| USA | United States | climate 0 to 3, AI oversight 0 to 2 |
| CHN | China | climate 0 to 3, AI oversight 0 to 2 |
| EU | European Union | climate 0 to 3, finance for surveillance in low-income countries 0 to 2 |
| IND | India | climate 0 to 3, pathogen surveillance 0 to 1 |
| FEX | fossil-exporter bloc: Russia, Iran, Saudi Arabia, Iraq, UAE, Kuwait, Qatar | climate 0 to 3 |
| LIC | low-income country bloc | pathogen surveillance 0 to 2 |
| DEV | frontier AI developers | safety restraint 0 to 3 |
| MDB | multilateral development banks | finance for surveillance in low-income countries 0 to 2 |

Level 0 means that current policies continue. It is the no-deal reference a⁰. A climate level v is a further cut of v × 10 % of own 2025 emissions by 2035.

**Effect model.** Three indicators, all zero at a⁰:

```latex
Q = \sum_i e_i\, c_i, \qquad
A = \tfrac{1}{4}\min(o_{\mathrm{US}}, o_{\mathrm{CN}}) + \tfrac{1}{20}\,(o_{\mathrm{US}} + o_{\mathrm{CN}}) + \tfrac{1}{10}\, s_{\mathrm{D}}, \qquad
P = \tfrac{1}{2}\min(s_{\mathrm{L}},\ 1 + s_{\mathrm{I}})
```

Here c is a climate level, o an oversight level, and s a restraint or surveillance tier. Q is abatement in units of 10 % of world emissions in 2025, with emission shares eᵢ. A is an AI risk-reduction index and P a pandemic-protection index, both between 0 and 1.

Climate is an aggregate-effort game. AI safety is mostly a weakest link between the two states' oversight. Pandemic protection is a weakest link between surveillance in LIC and in India, with finance as a side channel.

**Preferences.** Utilities are in each actor's own units and are never compared across actors:

```latex
u_i(a) \;=\; d_i\,Q + \alpha_i\,A + \pi_i\,P \;-\; \mathrm{cost}_i(a_i) \;+\; x_i(a)
```

Costs are quadratic in climate, oversight and restraint levels, and linear in surveillance tiers and finance tranches. The term xᵢ is a positional concern for USA and CHN: 0.15 lost per oversight level ahead of the other, and gained per level behind. For LIC it is 0.25 received per finance tranche.

**Aspirations.** They filter candidate profiles and are not traded off against gains.

| Actor | A profile is acceptable if |
| --- | --- |
| USA | its oversight level is not above China's, and its own cost is at most 0.9 |
| CHN | its oversight level is not above that of the United States, and its own cost is at most 0.9 |
| EU | Q is at least 0.5, and its own cost is at most 0.8 |
| IND | its own cost is at most 0.6 |
| FEX | its own cost is at most 0.4 |
| LIC | its cost net of finance received is at most 0.3 |
| DEV | its own cost is at most 0.35 |
| MDB | it gives finance only where P is at least 0.5 |

**Provenance.**

| Parameters | Status | Source |
| --- | --- | --- |
| emission shares eᵢ | sourced | EDGAR (2026), greenhouse gases without LULUCF, year 2025: China 29.51 %, United States 11.11 %, India 8.33 %, EU27 5.78 %, the seven FEX states 10.33 % |
| benefit weights, costs, index weights, budgets | illustrative | set by Claude on 10 November 2026; full list in `params.json` |

The illustrative values were chosen so that each issue is a social dilemma and every lever passes the orientation test at the base point. That choice flatters the theorems. The robustness set below is less polite.

## Checks before the search

Three checks ran before any search: the orientation test, sufficient groups, and the acceptable region.

**Orientation test (WP3).** At the base point every lever is costly to its owner and weakly beneficial to all others, on the whole lattice [model]. The instance then has the structure that the theorems of Heitzig (2025) assume. The equilibrium results below do not lean on them, because they are checked by enumeration. In a variant where developers bear a compliance cost of 0.10 per level of state oversight, both oversight levers harm DEV. Contested levers thus appear as soon as a regulated party is itself a signatory.

**Sufficient groups (WP1).** The target is two thirds of each indicator's largest value, and full protection for P.

| Issue | Target | Minimal sufficient groups | In every sufficient group |
| --- | --- | --- | --- |
| climate | Q at least 1.30 of at most 1.95 | USA+CHN+EU, USA+CHN+IND, USA+CHN+FEX, CHN+EU+IND, CHN+EU+FEX, CHN+IND+FEX | CHN |
| AI | A at least 0.67 of at most 1 | USA+CHN | USA, CHN |
| pandemic | P equal to 1 | IND+LIC | IND, LIC |

**Acceptable region (WP4 and WP6, stage 1).** The joint filter is what bites.

| Set | Profiles | Share of the lattice |
| --- | --- | --- |
| acceptable to all, C | 12,810 | 0.64 % |
| individually rational | 82,022 | 4.1 % |
| both | 3,403 | 0.17 % |

Taken alone, each actor accepts between 39 % (CHN) and 78 % (MDB) of all profiles.

## Core, menu and certificates

Inside C, every efficient and individually rational profile is in the strict core, and five of these 326 profiles form the menu.

**Enumeration (WP6).** Of the 3,403 candidates, 3,077 are Pareto-dominated. The other 326 survive every one of the 254 proper coalitions. Blocking profiles were not required to be acceptable, which is the conservative choice.

**Shape of the core.** Both states' AI oversight is at level 1 in all 326 profiles. Full pandemic protection holds in 225 of them. FEX contributes level 1 in 196, and no profile contains a climate level 3. The indicators range over Q 0.51 to 0.90, A 0.35 to 0.55, and P 0.5 to 1.

**The menu (WP6, stages 3, 6 and 7).** Each candidate maximises a different criterion over the core.

| Candidate | Criterion |
| --- | --- |
| Nash product | product of normalised gains |
| Leximin | smallest normalised gain, then the next smallest |
| Deepest | smallest relative slack to any aspiration limit |
| Most ambitious | smallest of the three indicators, each relative to its largest value on the core |
| Most robust | share of the robustness set in which the profile stays individually rational, acceptable and in the strict core |

Gains are normalised per actor by its largest gain among individually rational, acceptable profiles. Ties are broken by the Nash product. Six profiles tie as most robust.

| Lever or measure | Nash product | Leximin | Deepest | Most ambitious | Most robust (lead) |
| --- | --- | --- | --- | --- | --- |
| USA climate | 2 | 1 | 2 | 2 | 2 |
| EU climate | 1 | 1 | 1 | 2 | 1 |
| FEX climate | 0 | 0 | 0 | 1 | 0 |
| IND surveillance | 1 | 1 | 0 | 1 | 1 |
| LIC surveillance | 2 | 2 | 1 | 2 | 2 |
| DEV restraint | 1 | 1 | 1 | 2 | 1 |
| MDB finance | 1 | 2 | 2 | 1 | 2 |
| Q | 0.66 | 0.55 | 0.66 | 0.82 | 0.66 |
| A | 0.45 | 0.45 | 0.45 | 0.55 | 0.45 |
| P | 1 | 1 | 0.5 | 1 | 1 |
| smallest normalised gain | 0.55 (USA) | 0.58 (IND) | 0.31 (USA) | 0.39 (FEX) | 0.55 (USA) |
| normalised gain of FEX | 0.92 | 0.90 | 0.68 | 0.39 | 0.92 |
| stays acceptable, share of draws | 60 % | 95 % | 100 % | 19 % | 95 % |
| stays in the strict core, share of draws | 100 % | 100 % | 33 % | 100 % | 100 % |
| keeps all properties, share of draws | 60 % | 95 % | 33 % | 19 % | 95 % |

Identical in all five: USA and CHN oversight 1, CHN climate 1, EU finance 2, IND climate 1. The lead was the Nash-product point in the first run. It is now the most robust candidate [changed post hoc]. The two differ only in MDB finance.

**Certificates at the base point.** All five candidates pass all four checks [model].

| Check | Method |
| --- | --- |
| individually rational and acceptable to all | evaluation of the profile |
| in the strict core | direct test against all 255 coalitions, by code separate from the enumeration |
| the registry returns the profile | rule ℓ applied to step-function filings through the profile |
| no group gains by over-fulfilling | enumeration over all 255 groups |

The second and fourth check together establish a strictly strong equilibrium of the commitment game. The reason is a case distinction. Suppose all others file step functions through a profile a\* and a group G deviates. If some member ends below its level in a\*, all others fall to zero. Then G gains only if it blocks a\* in the core sense. Otherwise the others stay at a\*, and G gains only by over-fulfilling. The distinction needs only that filings are weakly increasing, which the mechanism requires. It does not need the orientation test, so the check stays valid in draws where that test fails.

**Stability depth of the lead.** Groups that contain every contributor can reproduce the lead, so their blocking margin is zero by construction. Among all other groups the best placed is everyone except DEV and FEX. Its best own profile leaves its worst-off member 0.094 normalised units below the lead.

**Software test.** 20,000 random group deviations to unconditional actions were run through the registry rule. The outcome matched the closed form each time, and none was profitable.

## Gate 1: heuristic search against enumeration

The criterion fixed before the first run is met, but that run never tested the coalitional refinement. Stress tests were therefore added, and both are reported.

**Criterion, written into the code before the first run.** Pass if (a) every heuristic run returns a profile that enumeration confirms as acceptable and in the strict core, and (b) at least 75 % of the runs reach the enumerated optimum of the Nash product.

**Result.** All 8 runs return the enumerated optimum. Each needed one round and no cut, and looked up 41,000 to 44,000 distinct profiles, about 2 % of the lattice.

**Why this says little.** Inside C every efficient, individually rational profile is already in the core. The blocking oracle therefore had nothing to find.

**Stress tests [added post hoc].** They use the same instance without the aspiration filter. There, enumeration finds 21,490 efficient, individually rational profiles, of which proper coalitions block 1,841. The pass marks were fixed before each test ran.

| Test | Pass mark | First oracle | Second oracle |
| --- | --- | --- | --- |
| B1: find a block for 300 profiles known to be blocked | at least 95 % | 191 of 300, failed | 294 of 300, passed |
| B1 on a hold-out sample of 300 further blocked profiles, drawn after the repair | at least 95 % | not run | 300 of 300, passed |
| invalid blocks reported; false alarms on 200 core profiles | none | not run | 0 and 0 |
| B2: best core point for each actor, 8 actors × 3 seeds | all in the core, 75 % at the optimum | not run | 24 of 24 in the core and at the optimum |

**The repair.** The first oracle searched over levers for a fixed family of coalitions. The second enumerates all profiles of coalitions with up to three members, and otherwise searches over membership and levers together.

**Limits.**

1. The second oracle missed 6 of 300 blocks in one sample. A heuristic certificate therefore says that no block was found, not that none exists.
2. B2 needed a cut in only 3 of 24 runs, so constraint generation is still lightly tested.
3. The search reads utilities from a table precomputed for the whole lattice. The 2 % counts look-ups and says nothing about run time at scale.
4. Recall can be measured only where ground truth exists.

**Reading.** Gate 1 is met on the toy, by its own criterion and by the added tests. How the oracle scales to forty actors is [open] and is carried into the scale-up phases. The sign-off is Jobst's.

## Linkage and robustness

Linkage reshapes the set of stable outcomes without improving on issue-by-issue deals for everyone. For the lead, robustness is limited by aspirations, not by blocking.

**Gains by issue at the lead (WP2).** In each actor's own units, relative to no deal.

| Actor | Climate | AI | Pandemic |
| --- | --- | --- | --- |
| USA | −0.17 | +0.25 | +0.50 |
| CHN | +0.10 | +0.16 | +0.50 |
| EU | +0.23 | +0.36 | +0.44 |
| IND | +0.44 | +0.225 | +0.20 |
| FEX | +0.10 | +0.18 | +0.30 |
| LIC | +0.66 | +0.135 | +0.60 |
| DEV | +0.03 | +0.19 | +0.20 |
| MDB | +0.26 | +0.09 | +0.30 |

USA is the only actor that loses on an issue. Its gains on AI and pandemic protection pay for its climate effort.

**Package against separate deals.** The single-issue cores were computed without the aspiration filter.

| Measure | Issue by issue | Package |
| --- | --- | --- |
| core profiles | climate 3, AI 3, pandemic 14 | 326 inside C |
| largest Q in the core | 0.55 | 0.90 |
| largest A and largest P in the core | 0.55 and 1 | 0.55 and 1 |

Of the 126 combinations of single-issue core profiles, 56 are in the package core when aspirations are ignored. 33 are acceptable to all, and 11 are both. Linkage therefore adds stable outcomes with more abatement. It also removes 70 combinations, which groups can block once they trade across issues.

Three separate deals, each at its own Nash-product point, give exactly the leximin candidate. It is in the package core, and no core profile is better for everyone. Against it, the lead costs USA 0.26 and gives every other actor between 0.01 and 0.11 more.

**Reading.** The package does not dominate separate deals here. It adds stable outcomes with more abatement, paid for by the actor that loses on climate. Which core point results is a distributional question for the actors (WP10). The toy is also too benign to show linkage as a necessity, since every issue has a deal of its own.

**Robustness set (WP6, stage 6).** It has 150 draws. Each benefit weight and cost is multiplied by an independent log-uniform factor between 0.8 and 1.25. Emission shares, index weights and budgets stay fixed.

- On average 102 of the 326 base-core profiles keep all properties in a draw. The range is 12 to 278.
- Nine profiles keep them in at least 90 % of the draws. The best six reach 143 of 150.
- The lead fails in 7 draws, each time on LIC's net-cost budget. Failing draws have a higher surveillance cost for LIC and a lower value of finance.
- The lead stays in the strict core, and its filings stay a strictly strong equilibrium, in all 150 draws.
- The deepest candidate shows the opposite pattern. It is always acceptable but leaves the strict core in 100 of 150 draws.

**Orientation test across the set.** It holds on the whole lattice in 87 of 150 draws. All failures are on the owner's side: in some region the owner gains from raising its own lever. This affects USA oversight in 31 draws, IND surveillance in 25, DEV restraint in 16 and CHN climate in 1. No lever ever harms a non-owner. In the failing draws the premise of the theorems does not hold, which is why equilibrium was checked directly.

## Filings, briefs, updating and compliance

WP7, WP9 and WP10 ran in generated or simulated form. The outputs show format and behaviour and are not drafts.

**Filings (WP7).** Seven actors get a step-function filing through the lead. FEX contributes nothing there and files nothing. An excerpt from `filings.md`:

> United States will cut own 2025 emissions by a further 20 % by 2035, relative to current policies; and license and evaluate frontier models, provided the registry shows every other signatory at or above its listed level. […] If the condition is not met, the liability under this filing is zero (current policies continue).

Step functions are the simplest filings and the most brittle: one shortfall anywhere sets every liability to zero. Indifference-curve filings, which degrade gradually, are not yet generated [open].

**Briefs (WP9).** Each actor gets its own page in its own units. An excerpt from `briefs.md`:

> You give: cut own 2025 emissions by a further 20 % by 2035, relative to current policies; license and evaluate frontier models. Own cost: 0.60. […] Your net gain over no deal: 0.58 (55 % of your largest acceptable gain). Gain by issue: climate -0.17, ai +0.25, pandemic +0.50.

**Updating (WP10).** The learning rule of Heitzig (2025, Theorem 3) was run in a discrete form. The theorem covers a single continuous good, so this is a test outside its scope. Each actor's levers were ordered into one ladder, which leaves 155,520 profiles. From all-zero filings and in random order, each actor once files the indifference-curve function through its favourite feasible point.

| Variant | Distinct outcomes in 200 orders | Acceptable to all | In the strict core of the full game | FEX contributes | Mean Q |
| --- | --- | --- | --- | --- | --- |
| rule as published | 137 | 1 % | 70.5 % | 63 % | 1.02 |
| aspirations cap each actor's filing | 62 | 95 % | 67.5 % | 58 % | 0.72 |

Under the published rule every outcome lies in the weak core of the ladder game, and every actor gains whatever its place in the order. The outcomes are more ambitious than the lead, whose Q is 0.66. But the rule knows nothing of aspirations and lands outside C. With caps, 95 % of the outcomes lie inside C, and about two thirds are core profiles. EU's climate floor cannot be written as a cap on its own action. It needs a filing that is conditional on the outcome [open].

**Compliance (WP7).** A first-order calculation gives the compensation factor that linear compensation (Heitzig, Lessmann and Zou, 2011) needs on the climate part of the lead. It assumes continuous levels, shortfalls counted in abatement units, and one actor falling short once. The discount factor is δ = 0.9, and n = 4 actors have positive targets.

```latex
\alpha_i \;\ge\; \frac{1 - b_i/m_i}{\delta\,(1 - 1/n)}, \qquad b_i = d_i\,e_i, \qquad m_i = 2\,k_i\,c_i^{\ast}
```

Here bᵢ is the marginal benefit and mᵢ the marginal cost of actor i's own abatement step at its target. The values are 1.34 for USA, 0.99 for CHN, 1.27 for EU and 1.11 for IND, so α must be at least 1.34 [model, first order]. The theorem is proved for a single good, and the other two issues are not covered [open].

## What the toy taught, and what is open

The first increment yields seven lessons for the plan and leaves seven items open in Phase 0.

**Coverage of the work packages.**

| WP | Exercised in the toy | Not yet |
| --- | --- | --- |
| WP1 | actor list set by hand; sufficient groups | authority and sufficiency of real actors |
| WP2 | three issues with game types; linkage in both directions | an issue without a deal of its own |
| WP3 | 12 levers; orientation test at base, in a contested variant and across the robustness set | generalised mechanism for contested levers |
| WP4 | aspirations as filters; own units; per-actor normalisation | any elicitation; budgets in the robustness set |
| WP5 | parameter file with provenance; one sourced series | everything else |
| WP6 | enumeration, menu, heuristic search, stress tests, robustness | empty-core fallback; far-sighted concepts; internal-and-external stability |
| WP7 | step-function filings; compensation factor to first order | indifference-curve filings; legal questions |
| WP8 | certificates by exhaustive check, at base and across the set | reachability; no-betting test; independent checker; back-test |
| WP9 | briefs per actor | everything else |
| WP10 | learning rule with and without aspiration caps | MaxParC over the menu; model-agent pilot |

**Lessons for the plan.**

1. Choose among core points by robustness as well as by a fairness criterion. Stages 3 and 6 of WP6 should run as one step. This is already applied here.
2. Aspiration files are the most consequential data. C is 0.64 % of the lattice, and every robustness failure of the lead is an aspiration failure. WP4 deserves priority over effect data.
3. Run the orientation test across the robustness set, and certify equilibrium directly where it fails.
4. A blocking oracle must search over coalition membership, and its recall must be measured. Keep an enumerable instance in the test suite at every scale-up.
5. Report linkage in both directions: the outcomes it adds and the outcomes it removes.
6. Aspirations must enter the filings themselves, or updating leaves the acceptable region.
7. Show contributions by likely free-riders on the menu. FEX contributes in 196 of the 326 core profiles but in only one of the five candidates.

**Open in Phase 0, in proposed order.**

1. A second instance with an empty core or a contested lever, to exercise the fallbacks.
2. A third instance in which one issue has no deal of its own, to test linkage as a necessity.
3. Budgets and index weights in the robustness set.
4. The far-sighted formation path and absorbing states (WP8), and internal-and-external stability (WP6).
5. MaxParC (Heitzig, Simmons and Constantino, 2025) over the menu, and a model-agent pilot (WP10).
6. Beliefs in the effect model, so that the no-betting test has something to test.
7. An independent checker for the certificates, and a fresh-session audit of this increment.

**Decisions for Jobst.**

1. Gate 1: sign off, or name a further test.
2. Home for the code: a repository, or the text bundle now kept with this doc. No repository exists.
3. Whether further increments should run as scheduled sessions. None is scheduled.

**Files.** Code, logs and result files went to Jobst as a zip in the chat on 10 November 2026. `README.md` lists every file, and `run_all.sh` recomputes all results in about 15 minutes. A run from scratch reproduced every result file. The script check_writeup.py asserts each number quoted in this tab against those files, 82 assertions in all. A text bundle of the same files is stored with this doc as asset c73bfcab8ebe97d3c427f8fde79760b2. Its header says how to restore the folder.

**Sources.**

- EDGAR (2026) *GHG emissions of all world countries – 2026 Report*. European Commission, Joint Research Centre. [edgar.jrc.ec.europa.eu/report_2026](https://edgar.jrc.ec.europa.eu/report_2026) (retrieved 10 November 2026).
- Heitzig, J. (2025) 'Provision of public goods via unilateral but mutually conditional commitments—mechanism, equilibria, and learning', *Games*, 16(6), 58. [doi:10.3390/g16060058](https://doi.org/10.3390/g16060058)
- Heitzig, J., Lessmann, K. and Zou, Y. (2011) 'Self-enforcing strategies to deter free-riding in the climate change mitigation game and other repeated public good games', *Proceedings of the National Academy of Sciences*, 108(38), pp. 15739–15744. [doi:10.1073/pnas.1106265108](https://doi.org/10.1073/pnas.1106265108)
- Heitzig, J., Simmons, F.W. and Constantino, S.M. (2025) 'Fair group decisions via non-deterministic proportional consensus', *Social Choice and Welfare*, 64, pp. 345–371. [doi:10.1007/s00355-024-01524-3](https://doi.org/10.1007/s00355-024-01524-3)
