# Phase 0: towers in a pre-CPEP

10 November 2026, session 2. Jobst's proposal of the same day, tested on the two toys with contested
levers. Every number below is asserted against the result files and against this text by
`phase0/check_towers.py`.

## Result in brief

The idea works for nested contests and not for cyclic ones, and its condition (ii) is stricter than it
needs to be. A relaxed version gives a strictly strong equilibrium of the original game in the toy.

| Question | Finding | Status |
| --- | --- | --- |
| Does a tower exist in the triangle of the second instance? | No. Every actor is harmed by some lever, and only single actors form a CPEP. | [model] |
| Does one exist in the contested variant of the first instance? | Not with aspirations. Without them, yes, but its last stage adds nothing and DEV ends below no deal. | [model] |
| Is that tower stable in the original game? | Nearly: 4 of 255 groups can still gain, by a margin of at most 0.017. | [model], T1 to T4 passed |
| Does a relaxed condition help? | Yes. With (ii′) there are 169 two-stage towers inside the acceptable region. The selected one is a strictly strong equilibrium of the original game. | [model], post hoc |

**What failed or looks weak.**

1. Under (ii) as stated, no acceptable first-stage profile leaves a proper CPEP for the last stage.
2. Under (ii), DEV ends below its no-deal utility in every one of the 870 towers.
3. The selection rule is stage by stage and picked a first stage after which nothing can be added.
4. Under (ii′) the selected tower also has a trivial last stage. The towers describe who joins when, not yet a path of rising ambition.
5. Only chains of two coalitions were tried, and only step filings.

## Definitions as implemented

A pre-CPEP keeps the costly levers of a CPEP and drops the requirement that others welcome them.

Jobst's definition: coalitions I₁ ⊆ … ⊆ I_m = I and filings c₁ ≤ … ≤ c_m = c such that, for every k,
(i) c_k is zero outside I_k and ignores actors outside I_k, and (ii) the game of I_k, with outsiders at
a⁰ and members of I_(k−1) held at or above b(c_(k−1)), is a proper CPEP in which c_k is a strong
equilibrium. Three readings were needed [assumption, for Jobst to confirm]:

- "Proper CPEP for I_k" is tested on the members' utilities only. Outsiders may be harmed.
- Gains at stage k are measured from b(c_(k−1)), the bottom of the stage box.
- The filing is a nested step function: actor i is liable for its level in b_k if every other member
  of I_k is at or above b_k, for the largest such k, and for nothing otherwise.

**Chain rule, fixed before the run.** I₁ is everyone not harmed by a contested lever at the base point,
and I₂ = I.

## What can be said in general

For step towers with two stages, three properties follow from (i) and (ii). They were also confirmed by
enumeration (T1 to T4).

1. **Graceful degradation.** If the newcomers of the last stage file nothing, the registry returns
   b₁, not zero.
2. **Stability inside the last box.** No group gains by a deviation whose outcome keeps the earlier
   members at or above b₁. Such a deviation is one of the last stage game, where c is a strong equilibrium.
3. **Only mixed groups can upset it.** A group of earlier members alone cannot gain: if one of them
   falls below b₁, everyone else falls to zero, and b₁ is in the strict core of the first stage, while
   b₂ is weakly better than b₁ for each of them. A group of newcomers alone stays inside the box.

So c is a Nash equilibrium, and a strong equilibrium once the first stage cannot be undone. What remains
is renegotiation: a group with members of both stages may prefer to take an earlier stage back. Whether
the three properties extend to longer chains by induction is [open].

## Strict condition (ii)

**Triangle.** All 3 actors are harmed by some lever. From zero, only the 3 single actors form a CPEP.
Of the 46,656 profiles, 64 leave a proper CPEP for all three, and in each of them every actor is already
active. No tower exists.

**Contested variant.** DEV is the only harmed actor, so the chain is the other seven, then all eight.

| Step | Count |
| --- | --- |
| profiles that leave a proper CPEP for all eight | 221,184 of 1,990,656 |
| strict core of the first stage, seven actors | 4,621 |
| of these, acceptable to the seven | 142 |
| of these, leaving a proper CPEP for the last stage | 0 |
| without aspirations: first-stage candidates | 870 |

The harm to DEV is linear in oversight. The last stage is therefore a proper CPEP only if both states
are already at oversight level 2, the top. No acceptable profile has that.

**The tower built without aspirations.** First stage: oversight 2 in both states, Q 0.85, A 0.70, P 1.
The last stage has 1,296 profiles and a strict core of one, the first-stage outcome itself. DEV adds
nothing and holds −53 % of its largest acceptable gain: it is worse off than without any deal.

**Stability in the original game.** All 7,909,199 unconditional deviations of all 255 groups were run
through the registry rule. 4 groups can gain. The only minimal one is everyone except FEX and MDB. Its
best deviation lowers oversight to 1, and its worst-off member gains 0.017 in normalised units.

**All 870 first-stage candidates [post hoc].** 15 allow a last stage that adds something. In none does
DEV end at or above its no-deal utility. Its best result is −43 %.

## Relaxed condition (ii′) [post hoc, Claude's proposal]

Dropping "proper CPEP" and testing the stage equilibrium directly is enough in the toy.

**(ii′)** c_k is a strong equilibrium of the stage game. For step filings this holds exactly if b_k is in
the strict core of the stage game and no group gains by over-fulfilling. That case distinction needs no
orientation.

| Step | Count |
| --- | --- |
| acceptable first-stage core profiles | 142 |
| of these, with an admissible last stage | 125 |
| towers (pairs of outcomes), acceptable to all | 169 |
| of these, with a last stage that adds something | 75 |
| of these 169, with every actor at or above no deal | 150 |

**The selected tower.** The rule was fixed before the run: largest smallest normalised gain over no deal.
It picks oversight 1 in both states, Q 0.82, A 0.35, P 1, and no restraint by DEV. DEV holds 20 % of its
largest acceptable gain, the smallest share of any actor. The last stage is not a proper CPEP. T1 to T4
pass. In the original game no group has a profitable deviation: the filing is a strictly strong equilibrium.

## Does the idea make sense?

Yes, with three qualifications.

1. **It fits nested contests.** A harmed party can join last if the harm is over, or bounded, by then.
   A cycle of harms, as in the triangle, has no first stage.
2. **Condition (ii) asks for too much.** It needs the contested lever exhausted before the victim joins.
   (ii′) keeps the stage logic and replaces the structural premise by a direct check. The price is that
   the theorems on CPEPs no longer do the work, so each instance needs its own certificate.
3. **The reference point moves.** Under (ii) a newcomer's gains are counted from a stage that may already
   have harmed it. The deal can then leave it below no deal, as it does for DEV. That clashes with the
   threat rule of WP1. Requiring every stage outcome to be individually rational against a⁰ for all
   actors, members or not, would repair it [open, for Jobst].

**What towers add beyond a certificate.** An implementation path, graceful degradation, and stability
that needs only irreversibility of earlier stages, not the full strong-equilibrium property.

## Open

1. Chains with more than two coalitions, and a search over chains.
2. A selection rule that looks ahead, so that later stages have something to add.
3. Indifference-curve filings in place of steps.
4. A proof of the three general properties for any number of stages.
5. Towers that add issues as well as actors.

**Files.** `phase0/tower.py`, `phase0/run_tower.py`, `phase0/run_tower_relaxed.py`,
`phase0/check_towers.py`, results in `phase0/results2/tower_*.json`. Runners and pass marks were
committed before their first run.

**Source.** Heitzig, J. (2025) 'Provision of public goods via unilateral but mutually conditional commitments—mechanism, equilibria, and learning', *Games*, 16(6), 58. [doi:10.3390/g16060058](https://doi.org/10.3390/g16060058)
