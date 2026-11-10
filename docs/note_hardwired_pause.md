# Note: the "hardwired pause" report and this programme

10 November 2026, session 2. Written at Jobst's request. Model numbers are asserted by
`pilots/check_pilots.py`.

**What I read.** The executive summary in full, the section on game theory (2.3), the transition phases
and exit conditions (3.4, 3.5), the list of authors, and passages found by keyword. I did not read the
whole report, which runs to about half a million characters. Technical claims about chips are the
report's, not checked by me.

**Conflict of interest.** Claude is built by Anthropic, whose training the proposed pause would stop.

## Result in brief

The report and this programme fit together like two halves. It shows how a pause could be verified once
states are willing. Our mechanism is about how conditional willingness becomes a commitment without anyone
moving first. I propose to make it the lead variant of track B.

| Question | Answer |
| --- | --- |
| What is it? | Fithian, Holliday and the Working Group on AI Pause Feasibility (2026): a working paper by 26 listed authors on whether a pause of frontier AI training for a decade or more is feasible. |
| What does it claim? | Feasible, if states are willing: stop making training-capable chips, phase out the existing stock, replace it with inference-only chips, and verify by a census and monitoring. |
| What does it assume? | "Pause-willingness": leaders would prefer pausing if confident that others pause or that defection is detected in time. |
| What does it leave open? | How willingness that is conditional on others turns into an agreement, in what order, and with what stability against groups. |
| What can we add? | Exactly that: conditional filings, a stability test against all groups, and a staged entry. |

## Where the two meet

1. **Its premise is a conditional commitment function.** "I pause if the others do" is the canonical filing
   of our mechanism. The report models the situation as a stag hunt or a repeated Prisoner's Dilemma and
   stops at the statement that cooperation can be an equilibrium. It does not say how the players get there.
2. **It supplies what our theorems assume.** The plan's weakest point is that liabilities are taken as
   binding (objection "Binding liabilities are assumed"). Hardware-level verification with public signals
   is a concrete answer for one issue.
3. **Its levers are the kind WP3 asks for.** They are observable, countable and ordered: production stopped
   or not, share of chips declared, retained stock from about 100 % down to 25 % of a breakout threshold.
   The report's second historical lesson says the same: agreements "focus on observable, verifiable units".
4. **Its phases are a tower.** Phase 1 begins "as soon as the U.S. and China agree"; the states that
   control supply-chain chokepoints follow; most others come later.
5. **Its actors are states.** The competition-law problem that blocks track B among developers does not
   arise when governments commit and firms are bound by statute.
6. **Its levers are contested.** A pause costs chip suppliers their orders and may entrench leading firms,
   as the report notes. That is a pre-CPEP, which is why condition (ii′) matters here.

## A skeleton of the entry problem

Three actors: the United States, China, and the supplier states as one bloc. The levers and the order of
entry are taken from the report. Every preference number is invented.

| Step | Result |
| --- | --- |
| lattice | 256 profiles, 7 groups |
| contested levers | each lead state's pause harms the supplier bloc |
| strict core inside the acceptable region | 1 profile, an equilibrium |
| tower along the report's order | stage 1: both lead states pause and draw down; stage 2: suppliers stop production and join the census |
| first coalitions with a first stage that does something [post hoc] | only the two lead states together |
| stability | strictly strong equilibrium of the full game; tests T1 to T4 pass |
| withdrawal | suppliers out: back to stage 1; either lead state out: back to zero |

**One structural point.** In the skeleton, the gain from training on while the rival pauses can be tripled
without breaking the certificate. At that value the stage game is a Prisoner's Dilemma, not a stag hunt.
Mutually conditional filings do not need the benign case. They need the filings to bind, and that is what
the report's verification is for.

**What this does not show.** Anything about real governments, or that a pause is desirable. The skeleton
has one core profile on a tiny lattice, so it tests the format, not the method.

## Consequences proposed

1. **Track B gets two variants.** B1, developers' safeguards: nearer, but legally delicate and hard to
   verify. B2, states and hardware: far from a pilot we could host, but verifiable, legally clean, and
   supported by a detailed public study. B2 becomes the worked case for the theory note and the method paper.
2. **The first outside contact for track B changes.** Holliday and Fithian are academics with a public
   feedback channel, and their group holds three kinds of expertise the roadmap needs later: an
   experimental economist (Shachar Kariv), a former arms-control negotiator (Rose Gottemoeller), and an
   author already cited in the plan (David Krueger). What we can offer them is a companion analysis of
   entry, which their report lacks.
3. **The plan gains a concrete answer on bindingness** for one issue, and a reason to treat "verifiable by
   construction" as a selection criterion for levers.
4. **Linkage.** The report's palatability features, such as scientific preserves and the distribution of
   inference-only chips across borders, are natural linkage currencies for a wider package.

## Open

1. Read the remaining sections, above all the quantitative ledger (6) and the actors' perspectives (8.5).
2. A richer skeleton: private developers as actors bound by their home states, other states with compute,
   noisy detection, and an exit condition.
3. The repeated-game enforcement of the report against the linear-compensation device of WP7.

**Source.** Fithian, W., Holliday, W.H. and the Working Group on AI Pause Feasibility (2026) *The
Feasibility of a Hardwired Pause of Frontier AI Training*. Working paper, version 1.0.2, 26 October 2026.
[hardwired-pause.ai/paper](https://hardwired-pause.ai/paper) (retrieved 10 November 2026). No DOI or arXiv
number found.
