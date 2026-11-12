# Pilot B: conditional safety commitments among frontier AI developers

10 November 2026, session 2. Track B of the roadmap, developed to the point where outside knowledge is
needed. Model numbers are asserted by `pilots/check_pilots.py`. Sourced facts carry their URL; the full
fact file with quotes is `data/sources/trackB_ai_facts.md`.

**Conflict of interest.** Claude is built by Anthropic, one of the developers this pilot concerns. Its
documents are quoted below next to those of others. Jobst should have the framing of this track checked
by someone with no tie to any developer.

**Two variants.** This note covers B1, commitments among developers. Variant B2, commitments among states
on chip production and stocks, follows the "hardwired pause" report and is in `docs/note_hardwired_pause.md`.
B2 avoids the competition-law question. Jobst made it the lead variant on 11 November 2026.

## Proposal in brief

Developers already publish safety frameworks whose strength depends on what rivals do, but only in prose
and mostly downwards. A registry would let each state that dependence as an explicit function, upwards as
well, and would compute the joint outcome.

| Question | Answer |
| --- | --- |
| Who files? | Developers with a published frontier safety framework: twelve are on METR's list. |
| What is filed? | Safeguard and evaluation-access levels above the current framework, as a function of the levels others file. |
| What does the registry do? | It computes the largest mutually feasible profile and publishes it. |
| Why would they? | Each filing is unilateral. Nobody moves unless the others' conditions are met. |
| First obstacle | Competition law: whether mutually conditional public filings count as an agreement. |

## Why now

1. **The conditional clauses exist.** OpenAI's Preparedness Framework, version 2, lets it lower safeguards
   if another developer releases a comparable system "without instituting comparable safeguards", under
   three conditions ([§4.3](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf)).
   Google DeepMind writes that some mitigations work "only if all relevant organizations provide similar
   levels of protection" ([Frontier Safety Framework 3.1](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf)).
   Anthropic's Responsible Scaling Policy, version 3.4, separates what it does alone from industry-wide
   recommendations it "cannot commit to following ... unilaterally", and lists "competitor-contingent
   commitments" in an appendix ([policy](https://cdn.sanity.io/files/4zrzovbb/website/0bacdc8440ea96e62a8766d99ebe1d4eea6d5f3a.pdf)).
   I re-read that passage at the source.
2. **The public debate has reached coordination.** An essay by Anthropic's chief executive in September
   2026 proposed pacing in three steps: unilateral, industry-wide with government mediation or antitrust
   waivers, then global ([essay](https://darioamodei.com/post/we-must-pace-the-frontier)). That is a tower.
3. **The legal line is being drawn.** A Congressional Research Service note of 28 September 2026 says a
   unilateral commitment carries no risk under Section 1 of the Sherman Act, while a coordinated pause
   carries the highest. It also reports a class action filed on 18 September 2026
   ([CRS Legal Sidebar LSB11485, mirror](https://www.everycrsreport.com/reports/LSB11485.html)).
4. **Floors exist.** The EU's Code of Practice for general-purpose AI has 22 full signatories, and
   California's SB 53 was signed on 29 September 2025
   ([Commission](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai);
   [Governor of California](https://www.gov.ca.gov/2025/09/29/governor-newsom-signs-sb-53-advancing-californias-world-leading-artificial-intelligence-industry/)).
   The registry would sit above them.

A registry of conditional filings lies between the two poles of the CRS note. Each filing is unilateral,
but its condition refers to rivals. Where that falls in law is the first question for an outsider.

## Skeleton instance

Five stylised developers, not named companies. Every number is illustrative.

| Actor | Stands for | Levers |
| --- | --- | --- |
| A, B | the two developers with the most detailed frameworks | safeguard tier 0 to 3; evaluator access 0 to 2 |
| C, D | two further frontier developers | the same |
| E | a developer that releases model weights openly | the same |

**Assumed structure.** Industry-wide risk reduction has a weakest-link part, an average part and an access
part. A tier costs its owner, more so if it stands above its rivals. Developers A to D accept at most one
tier above the least strict of the other three. That red line mirrors the clauses quoted above.

## What the skeleton shows

The pipeline runs end to end. None of this is a finding about any company.

| Step | Result |
| --- | --- |
| lattice | 248,832 profiles, 31 groups |
| acceptable to all; individually rational; both | 12,858; 143; 143 |
| strict core inside the acceptable region | 55, all of them equilibria |
| towers along the fixed chain, A and B first | 92 |
| selected tower | A and B do nothing alone; all five then move together |
| all 30 possible first coalitions [post hoc] | all have a tower; 11 have a first stage that does something |

**The selected outcome.** Every developer adds one safeguard tier. A and B give evaluators access at tier
2, C and D at tier 1, E none. The filing is a strictly strong equilibrium, and tests T1 to T4 pass.

**Withdrawal.** If any one developer files nothing, the registry returns zero. With a weakest-link risk,
the deal is only as firm as its least willing member. Here that member is the open-weights developer.

**Which numbers matter.** The outcome stays certified in 200 of 200 draws. Changed one at a time, no
number tips it below a factor of 2. The skeleton is robust to its own invented numbers, which says the
structure matters more than the values.

## Where outside knowledge is needed

1. **Law, first.** Whether a public registry of mutually conditional, unilateral safety commitments is an
   agreement or concerted practice under US and EU competition law, and what design keeps it on the safe
   side. Candidates from the literature: filings that refer to published levels and not to named rivals,
   no private communication, a public body as registrar, or a business review letter.
2. **The structure.** Whether the weakest-link assumption and the two levers describe what developers
   could verifiably commit to. This needs people who study the frameworks.
3. **Verification.** What an outside evaluator can confirm. Without it a filed level is a statement.
4. **A developer's view.** Only after the first two.

Who to ask, with what, and how is in `docs/outreach_proposal.md`.

**Files.** `pilots/pilot_b.py`, `pilots/run_pilot.py`, `pilots/results/pilot_b*.json`,
`pilots/results/pilot_b_filings.md`, `outreach/brief_B.md`.
