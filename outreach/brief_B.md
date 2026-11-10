# Conditional safety commitments among frontier AI developers: a two-page brief

*Draft for Jobst to edit and send. Research proposal; no developer has asked for this. Disclosure: drafts
and computations are produced with Claude, an AI system built by Anthropic, one of the developers concerned.*

**The problem.** Developers publish safety frameworks, and several say in them that what they can do
depends on what rivals do. One reserves the right to lower safeguards if a rival releases without
comparable ones. Another says some mitigations work only if all relevant organisations adopt them. A third
separates what it does alone from what it recommends for the industry and cannot promise alone. These
clauses are prose, mostly point downwards, and cannot be computed.

**The idea.** Each developer files one public, conditional commitment, alone: "we will apply safeguard
level x above our current framework, provided the levels filed by the other developers are at or above
theirs". A fixed rule computes the largest set of levels that satisfies every filed condition. Nobody
moves unless the others' conditions are met, and a filing can be withdrawn with notice. The mechanism and
its equilibrium properties are in Heitzig (2025),
[doi:10.3390/g16060058](https://doi.org/10.3390/g16060058).

**What is new.**

1. The dependence on rivals becomes an explicit function that points upwards as well as downwards.
2. Before anyone files, the method tests whether a package is stable against any developer or group.
3. Filings can be stepped, so that a small group can start and others join.

**A worked skeleton.** We modelled five stylised developers, not named companies, with invented numbers. If
risk is largely set by the weakest link, two leading developers gain nothing by moving alone, all five can
move one tier together, and the package collapses if any one of them stays out. The numbers are
placeholders. The dependence on the least willing developer is structural.

**The legal question, which comes first.** A Congressional Research Service note of 28 September 2026 says
a unilateral commitment carries no risk under Section 1 of the Sherman Act, and a coordinated pause the
highest. Our filings are unilateral, public and withdrawable, but each is conditional on what rivals file.

**What we would like from you.** Thirty minutes, on three questions:

1. Is a public registry of mutually conditional, unilateral commitments an agreement or a concerted
   practice, in the United States and in the EU?
2. Which design features move it towards the safe side: conditions on published levels and not on named
   rivals, no private communication, a public body as registrar, a business review letter?
3. Who else should read this before it goes near a developer?

**Who we are.** Jobst Heitzig leads the work and checks every draft. Nothing here is a finding about any company.
