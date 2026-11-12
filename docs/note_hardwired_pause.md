# Note: the "hardwired pause" report and this programme

12 November 2026, session 2. Second version, after reading the rest of the report as Jobst asked. Model
numbers are asserted by `pilots/check_pilots.py`.

**What was read, and how.** Myself: sections 1, 2.3, 3.1, 3.2.3, 3.4 to 3.6, 6.1, 6.5, 8.3, 8.5.2 and 9, and
the executive summary. Through a research sub-session that extracted 234 quotes with character offsets:
sections 3.2, 3.3, 4, 5, 6.2 to 6.4 and 7 (`data/sources/hardwired_pause_extract_technical.md`); the jurisdictions the
report names, with their roles, are compiled in `data/sources/hardwired_pause_actors.md`; of that
extract I read the numbers, asymmetries, sequencing and its checks of my earlier statements. Not read
beyond keyword passages: 2.1, 2.2, 8.1, 8.2, 8.4 and 8.5.1. Technical claims about chips are the report's.

**Conflict of interest.** Claude is built by Anthropic, whose training the proposed pause would stop.

## Result in brief

The first version of this note stands in substance, and three of its statements were wrong in detail. The
report leaves open exactly the question our mechanism answers, and it supplies numbers on which a model of
that question can stand.

| Question | Answer |
| --- | --- |
| What is it? | Fithian, Holliday and the Working Group on AI Pause Feasibility (2026): a working paper by 26 listed authors on whether a pause of frontier AI training for a decade or more is feasible. |
| What does it claim? | Feasible, if states are willing: stop making training-capable chips, phase out the stock, replace it with inference-only chips, and keep each state's training capacity below two thresholds. |
| What does it assume? | "Pause-willing futures": each leader has some terms under which they would pause if confident that others pause under those terms. |
| What does it leave open? | Whether one set of terms is acceptable to all; how the parties get there; the response to a state that breaks out; what coalitions can do. |
| What can we add? | Conditional filings in the report's own units, a test for terms acceptable to all and stable against every group, and a staged entry. |

## Corrections to the first version

1. **The "100 % to 25 %" is an allowance, not a stock.** Each state's ledger of training capacity must stay
   below an allowance times a threshold. The allowance could "start close to 100% at entry into force and
   fall gradually to 25%". The first version called this retained stock. The skeleton had the same error.
2. **Not every lever is observable.** Hidden chips ("dark compute") are unobservable by definition and enter
   as a negotiated estimate. Every ledger term is a count times negotiated discount factors. The breakout
   threshold itself is "a matter of negotiation and trust more than one of estimation".
3. **The chokepoint holders are more than the three named.** The report lists the Netherlands, Germany,
   Japan, Taiwan and South Korea, and for other inputs China and the United States themselves. The census
   also needs Singapore, Malaysia and the United Arab Emirates early.

## Where the two meet

1. **The open question is ours.** The report says pause-willingness "does not assume that there is a single
   set of terms that would provide the requisite confidence and be acceptable to all parties". Whether such
   terms exist is, in our words, whether the acceptable region contains a core profile.
2. **Its only reciprocal mechanism is a conditional commitment in prose.** On recovering hidden chips, states
   "could agree to produce some number of chips conditional on others doing the same". Nothing computes it.
3. **Entry is expected to be informal.** A near-term pause "would most likely be initially implemented as an
   informal agreement", with a treaty years later. Unilateral conditional filings need no treaty.
4. **It supplies what our theorems assume.** The plan takes liabilities as binding. The ledgers, the census
   and the control of fabrication are a concrete way to make them so for one issue.
5. **The binding constraints are asymmetric.** For the United States it is breakout capacity from its large
   fleet. For China it is covert capacity from hidden chips. Each holds the lever the other needs.
6. **Its phases are a tower,** and its levers are contested: a pause costs suppliers their orders.
7. **A state's breakout has no modelled response.** If it happened, "the treaty would likely have already
   failed". Commitments about how coalitions would respond are named as an input and not analysed.
8. **Its actors are states.** The competition-law problem of variant B1 does not arise.

## What the report's numbers imply before any preference is assumed

Durability can be read off the report's ledger. Take headroom as the orders of magnitude by which training
efficiency may improve before a ledger exceeds its allowance, and convert at the report's 57 % a year.
With every other lever at its most cooperative level, two levers decide it [derived from the report's
illustrative values]:

| Years of durability | China conceals | China cooperates a little | China cooperates fully |
| --- | --- | --- | --- |
| United States keeps its whole fleet at home | 0.5 | 0.5 | 0.5 |
| keeps half | 1.0 | 2.0 | 2.0 |
| keeps a tenth | 1.0 | 5.6 | 5.6 |
| keeps a residual | 1.0 | 5.8 | 10.2 |

China's own fleet, if left at home, caps durability at 5.8 years, so the last cell needs its drawdown too.
Neither state can buy durability alone. That is the report's asymmetry as a table, and it is the natural
subject of a pair of conditional filings: fleet moved out against census cooperation.

## Skeleton, version 2

Three actors: the United States, China, and the chokepoint jurisdictions as one bloc. The ledger rule,
thresholds, stocks, census scenarios and order of entry are the report's. Every preference number, and the
effect of the suppliers' levers, is invented.

| Step | Result |
| --- | --- |
| lattice | 2,304 profiles, 7 groups |
| acceptable to all; individually rational; both | 318; 49; 39 |
| strict core inside the acceptable region | 2 profiles, both equilibria |
| tower along the report's order | stage 1: both lead states pause, cooperate fully and draw down; stage 2: suppliers stop production and accept monitoring |
| durability | about 5 years after stage 1, about 10 after stage 2 |
| first coalitions with a first stage that does something [post hoc] | only the two lead states together |
| stability | strictly strong equilibrium of the full game; tests T1 to T4 pass |
| withdrawal | suppliers out: back to stage 1; either lead state out: back to zero |

**One structural point.** The gain from training on while the rival pauses can be tripled without breaking
the certificate. At that value the stage game is a Prisoner's Dilemma, not a stag hunt. Conditional filings
do not need the benign case. They need to bind, and binding is what the report's verification is for.

**What this does not show.** Anything about real governments, or that a pause is desirable. The halving of
durability without the suppliers is my assumption, so the "5 years" is not the report's number.

## Decisions and consequences

On 11 November 2026 Jobst decided: B2 is the lead variant of track B; Wesley Holliday, whom he knows well,
is the first contact; and the rest of the report is read before anything goes out. That reading is done,
to the extent stated at the top.

1. What goes to Holliday is `outreach/email_B2.md` with the two-page outline `outreach/outline_B2.md`.
2. The group holds expertise the roadmap needs later: an experimental economist (Shachar Kariv), a former
   arms-control negotiator (Rose Gottemoeller), and an author already cited in the plan (David Krueger).
   Its July workshop ran tabletop exercises, a possible test bed for a registry.
3. The report's code is public, so a joint analysis can use its ledger directly.
4. The report's inducements, such as scientific preserves and shared inference capacity, are linkage
   currencies for a wider package.

## Open

1. Read the sections not yet read, above all 8.4 and 8.5.1.
2. Graded entry: filings on the allowance schedule itself, shrinking as the other side's census advances.
3. Hidden chips as an unobservable lever: what a filing can condition on when the level is an estimate.
4. Developers and other chip-holding states as actors; strategic reserves as insurance next to filings.
5. The report's repeated-game enforcement against the linear-compensation device of WP7.

**Source.** Fithian, W., Holliday, W.H. and the Working Group on AI Pause Feasibility (2026) *The
Feasibility of a Hardwired Pause of Frontier AI Training*. Working paper, version 1.0.2, 26 October 2026.
[hardwired-pause.ai/paper](https://hardwired-pause.ai/paper) (retrieved 10 and 12 November 2026). No DOI or
arXiv number found.
