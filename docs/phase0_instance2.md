# Phase 0: second instance and contested variant

10 November 2026, session 2. Step 1 of the open list. Every number below is asserted against the result
files by `phase0/check_writeup2.py`, which also checks that the number stands in this text.

## Result in brief

Both fallbacks ran, and both have a defect. A contested lever also breaks the step from core to
equilibrium. All numbers except the emission shares are invented for the test.

| Question | Finding | Status |
| --- | --- | --- |
| Is there an instance with an empty core? | Yes: 3 actors, 2 issues, 9 levers, 46,656 profiles, 7 coalitions. No profile is in the strict core, with or without aspirations. | [model], full enumeration |
| Does the search report emptiness? | Yes, in 8 of 8 runs. Each excluded every candidate with 4 cuts. | E1 passed |
| What does the fallback by blocking margin return? | One profile with margin 0.165. Every pair blocks it, and it is Pareto-dominated. | [model] |
| What does the fallback by issue set return? | The climate issue alone has 7 core profiles. In the package game its focal deal has margin 0.479. | [model] |
| Does the search work when coalitions block? | In the contested variant of the first instance it meets the Gate 1 criterion in 8 of 8 runs, with 15 cuts each. | G1c passed |
| Is the profile it returns self-enforcing? | No. It is in the strict core, yet USA and CHN gain by over-fulfilling. | [model] |

**What failed or looks weak.**

1. In the contested variant only 150 of 399 core profiles are equilibria of step-function filings.
   The search returned one of the other 249.
2. The margin fallback returns a profile that the grand coalition can improve on.
3. The issue-set fallback is worse than the margin fallback unless the dropped levers are really unavailable.
4. No empty core was found on the eight-actor lattice. The second instance is a purpose-built triangle.
5. With three actors the blocking oracle is exact. E1 therefore tests the master search and the cuts only.

**Changed after seeing results.** Two additions are post hoc and marked below: the margin fallback
restricted to efficient candidates, and the count of core profiles that are equilibria.

## The second instance

Three actors can grant each other preferential access, and each grant harms the third. That makes
every access lever contested and empties the core.

| Actor | Levers and levels |
| --- | --- |
| USA | access for CHN 0 to 2, access for EU 0 to 2, climate 0 to 3 |
| CHN | access for EU 0 to 2, access for USA 0 to 2, climate 0 to 3 |
| EU | access for USA 0 to 2, access for CHN 0 to 2, climate 0 to 3 |

Access stands for markets, technology or critical minerals, a linkage currency of WP2.

```latex
u_i(a) \;=\; d_i\,Q \;-\; k_i\,c_i^2 \;+\; b\,r_i \;-\; g\,s_i \;-\; h\,t_i ,
\qquad Q = \sum_j e_j\, c_j
```

Here rᵢ counts access levels received, sᵢ those granted, and tᵢ those exchanged between the other two.
The values are b = 0.30, g = 0.10 and h = 0.18. A pair gains b − g = 0.20 per level each from a swap,
and costs the third 2h = 0.36. Since h lies between (b − g)/2 and b − g, a swap among all three still
pays a little, but any pair does better alone.

**Aspirations.** Each actor accepts a profile if its own cost is within budget (USA 0.60, CHN 0.90,
EU 0.60) and at most 2 access levels are exchanged between the other two.

**Provenance.** Emission shares are from EDGAR (2026), as in the first instance. All other values are
illustrative, set by Claude on 10 November 2026. They were chosen after a short scan so that the access
issue has an empty core, the climate issue has a core, the package has none, and no lever pays for itself.

**Checks before the search.**

- Orientation test: all 6 access levers fail it, each harming the third actor by 0.18 per level. No lever
  fails on the owner's side.
- Acceptable region: 4,527 profiles are acceptable to all, 2,448 are individually rational, 548 are both.

## The core is empty

No candidate survives, and the two code paths agree.

- Of the 548 candidates, 542 are Pareto-dominated. The other 6 are blocked by pairs: 3 by USA+CHN and
  3 by USA+EU.
- Without the aspiration filter, 204 profiles are efficient and individually rational. All are blocked.
- E3, fixed before the run: `core.strict_core` returns nothing, and `fallbacks.strict_blockers` finds a
  blocking group for each of the 548 candidates. Passed.

**Search (E1).** The pass mark was fixed before the run: no heuristic run may return a profile. All 8
runs returned none. Each took 5 rounds and 4 cuts and left no candidate unexcluded. They looked up
12,746 to 13,634 distinct profiles, 27 to 29 % of this small lattice.

## Fallback 1: smallest blocking margin

The rule returns a unique profile, but not one anybody should sign as it stands.

The selection rule was fixed before the run: smallest margin among individually rational, acceptable
profiles, ties broken by the Nash product. Over the 548 candidates the margin ranges from 0.165 to
0.661, with median 0.439.

| Lever or measure | Margin fallback | Among efficient candidates [post hoc] | Climate-only deal |
| --- | --- | --- | --- |
| USA access for CHN, for EU | 2, 0 | 2, 1 | 0, 0 |
| CHN access for EU, for USA | 0, 0 | 0, 0 | 0, 0 |
| EU access for USA, for CHN | 1, 1 | 1, 2 | 0, 0 |
| climate USA, CHN, EU | 1, 2, 1 | 1, 2, 0 | 1, 1, 1 |
| Q | 0.76 | 0.70 | 0.46 |
| normalised gain USA, CHN, EU | 0.47, 0.59, 0.13 | 0.04, 0.71, 0.44 | 0.30, 0.14, 0.47 |
| blocking margin in the package game | 0.165 | 0.220 | 0.479 |
| groups that block | all three pairs, and the grand coalition | all three pairs | all three pairs, and the grand coalition |
| groups that gain by over-fulfilling | 3 | 1 | not computed |

**Margins at the fallback profile.** CHN+EU 0.165, USA+EU 0.145, USA+CHN 0.072, grand coalition 0.026.
Each single actor's margin is negative, so the profile is individually rational with room to spare.

**Mechanism at the fallback profile (E2).** All 50,652 joint deviations to unconditional actions were
run through the registry rule. The rule matched its closed form each time. No single actor gains by
deviating, so the filings are a Nash equilibrium. The groups that gain are exactly the blockers:
USA+CHN with 3 deviations, USA+EU with 15, CHN+EU with 16, and the grand coalition with 1. That is what
the certificate logic predicts. Passed.

**Defect.** The margin objective does not see Pareto dominance when the dominating gain is small.
Restricting the rule to the 6 efficient candidates removes that, at the price of a larger margin, 0.220
against 0.165 [post hoc]. Which rule the plan should adopt is a decision for Jobst.

## Fallback 3: a different issue set

Dropping the access issue restores a core on paper only.

| Sub-package | Profiles | Individually rational | Efficient | Strict core | Strict core inside C |
| --- | --- | --- | --- | --- | --- |
| access | 729 | 9 | 1 | 0 | 0 |
| climate | 64 | 9 | 7 | 7 | 7 |
| access and climate | 46,656 | 2,448 | 204 | 0 | 0 |

The climate deal at its Nash-product point has every actor at level 1. It is stable if access grants
cannot be made at all. If pairs can still strike access deals outside the registry, the right test is
the package game. There its margin is 0.479, almost three times that of the margin fallback.

**Reading.** Linkage destroys the zone of agreement here, as Sebenius (1983) warns: climate alone has a
core and the package has none. Taking an issue off the table helps only if its levers leave with it.
Far-sighted stability, the second fallback of the plan, is not implemented yet [open].

## Bounded coordination and diplomatic channels [exploration]

Stability of the second instance depends sharply on who can coordinate with whom. This section was
added on Jobst's request after the tests above. It has no pass mark. The plan section "Bounded
rationality and diplomatic knowledge" gives the concepts.

The 548 candidates were re-tested against restricted families of groups. The channel graph is an
illustrative assumption: USA and CHN have no bilateral channel, and a group can coordinate only if it
is connected.

| Groups that can coordinate | Candidates no such group blocks | Smallest margin |
| --- | --- | --- |
| all 7 groups | 0 | 0.165 |
| groups of at most two | 0 | 0.165 |
| groups connected by a channel (no USA+CHN) | 0 | 0.026 |
| single actors only | 548 | not applicable |

**Inertia.** Suppose actors move only for a normalised gain above a threshold. No candidate is stable
below a threshold of 0.165. At 0.20 one candidate is stable, at 0.25 there are 10, and at 0.30 there are 56.

**Reading.**

1. Removing one channel does not restore a core, but it cuts the smallest margin from 0.165 to 0.026.
   The profile that achieves this is a different one, and it favours the broker. EU holds 91 % of its
   largest acceptable gain there, USA 9 % and CHN 19 %. Among connected groups only the grand coalition
   blocks it. If USA and CHN could talk after all, they would block it with a margin of 0.471.
2. Against single actors every candidate holds. The whole difficulty lies in pairs.
3. A missing channel and a threshold are optimistic assumptions. A certificate that relies on either
   must say so, and the unrestricted result must be reported next to it.

## Contested variant of the first instance

The search handles real blocking, and the result shows why a core certificate is not enough.

**Variant.** Developers bear a compliance burden of 0.20 per level of state AI oversight. The value was
chosen after a scan: at 0.10 no proper coalition blocks inside C. Both oversight levers now harm DEV, by
up to 0.17 per level. Everything else is the first instance.

**Enumeration.** 1,351 candidates are individually rational and acceptable. 833 of them are efficient,
and proper coalitions block 434 of those. The strict core inside C has 399 profiles. The busiest
blocker is everyone except FEX and DEV, with 276 profiles.

**Search (G1c).** The criterion is that of Gate 1 and was fixed before the run. All 8 runs returned the
enumerated Nash-product point. Each took 16 rounds and 15 cuts and looked up 93,000 to 102,000
profiles, about 5 % of the lattice. This is the first run in which constraint generation did real work.

**The returned profile is not self-enforcing.** It has no state oversight, DEV restraint at level 2,
Q 0.95, A 0.20 and P 1. It passes the direct core test. But USA and CHN together gain by adding
oversight on top of their filings. The step functions of the others cannot answer that, because nobody
falls below a listed level. 32 groups gain this way, and USA+CHN is the only minimal one.

**How common this is [post hoc].** 150 of the 399 core profiles are equilibria. They are exactly the 150
that already contain oversight. The best of them by Nash product has both states at oversight 1 and DEV
at restraint 0, with A 0.35. DEV keeps 16 % of its largest acceptable gain there.

**Reading.** With a contested lever, the strict core admits profiles that leave a harmful lever unused.
The mechanism cannot hold them, because filings must be weakly increasing and so cannot forbid
over-fulfilment. The certificate pipeline caught this through its over-fulfilment check. The search did
not, since its oracle looks for core blocks only. The generalised mechanism for contested levers stays
[open].

## Lessons and what is open

**Lessons for the plan.**

1. The search oracle must test over-fulfilment as well as blocking whenever the orientation test fails.
2. The margin fallback should either be restricted to efficient profiles or report dominance next to
   the margin.
3. The issue-set fallback needs a statement of whether dropped levers stay available outside the registry.
4. Report the blocking groups with every fallback profile. Here the filings are safe against single
   actors and unsafe against every pair.

**Open.**

1. A heuristic for the smallest margin. The fallback here is by enumeration only.
2. An oracle that also searches over-fulfilment deviations.
3. A robustness set for the second instance.
4. An empty core on the eight-actor lattice. A scan over a compliance burden and a relative-gains term
   between USA and CHN found none. That scan is not in the result files.
5. Far-sighted stability as the second fallback (step 4 of the open list).

**Decisions for Jobst.**

1. Whether the margin fallback is restricted to efficient profiles.
2. Whether G1c counts towards Gate 1, given that the returned profile is not an equilibrium.

**Files.** `phase0/instance2.py`, `phase0/fallbacks.py`, `phase0/run_instance2.py`,
`phase0/run_contested.py`, `phase0/check_writeup2.py`, results in `phase0/results2/`. The runners were
committed with their pass marks before their first run.

**Sources.**

- EDGAR (2026) *GHG emissions of all world countries – 2026 Report*. European Commission, Joint Research Centre. [edgar.jrc.ec.europa.eu/report_2026](https://edgar.jrc.ec.europa.eu/report_2026) (retrieved 10 November 2026).
- Heitzig, J. (2025) 'Provision of public goods via unilateral but mutually conditional commitments—mechanism, equilibria, and learning', *Games*, 16(6), 58. [doi:10.3390/g16060058](https://doi.org/10.3390/g16060058)
- Sebenius, J.K. (1983) 'Negotiation arithmetic: adding and subtracting issues and parties', *International Organization*, 37(2), pp. 281–316. [doi:10.1017/S002081830003438X](https://doi.org/10.1017/S002081830003438X)
