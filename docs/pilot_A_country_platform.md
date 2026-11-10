# Pilot A: a conditional-pledge registry for a country platform

10 November 2026, session 2. Track A of the roadmap, developed to the point where outside knowledge is
needed. Model numbers are asserted by `pilots/check_pilots.py`. Sourced facts carry their URL; the full
fact file with quotes is `data/sources/trackA_climate_facts.md`.

## Proposal in brief

Start with one existing partnership between a recipient country and a group of donors, not with national
pledges at large. The Just Energy Transition Partnerships (JETPs) are already package deals of this kind,
and their known weaknesses are the ones a registry addresses.

| Question | Answer |
| --- | --- |
| Who files? | One recipient government and five to ten donor governments or their finance institutions. |
| What is filed? | Recipient: mitigation and reform levels as a function of finance allocated. Donor: finance allocated as a function of the recipient's levels and of the other donors' allocations. |
| What does the registry do? | It computes the largest mutually feasible profile and publishes it with each actor's liability. |
| Why would they? | A filing is unilateral and conditional. Nobody pays before the others' conditions are met. |
| First case to work through | South Africa: it has the only public register of pledges and allocations by donor. |

## Why this partnership form

1. **Conditionality is already written into the deals.** Indonesia's 2022 joint statement makes net zero
   in the power sector "conditional on international support". The private half of the Indonesian and
   Vietnamese packages is "subject to" the public half
   ([EC statement](https://ec.europa.eu/commission/presscorner/api/documents?reference=STATEMENT/22/6892&language=en);
   [UK, political declaration](https://www.gov.uk/government/publications/vietnams-just-energy-transition-partnership-political-declaration/political-declaration-on-establishing-the-just-energy-transition-partnership-with-viet-nam)).
2. **Share rules exist in law.** The United States capped its Global Fund contribution at 33 % of the
   total, by statute until March 2025
   ([22 U.S.C. 7622](https://www.law.cornell.edu/uscode/text/22/7622)). That is a conditional commitment
   function in all but name.
3. **The weaknesses are coordination failures.** The United States withdrew from the South African
   partnership on 28 February 2025
   ([UK government](https://www.gov.uk/government/news/12-month-just-energy-transition-partnership-leaders-update-2025)).
   The partners do not make a joint offer, and each pledges through several institutions
   ([Carnegie, 2025](https://carnegieendowment.org/russia-eurasia/research/2025/10/the-just-energy-transition-partnership-crossroads)).
   Indonesia's targets were renegotiated after the deal was announced
   ([JETP secretariat](https://jetp-id.org/about/why-is-the-emissions-reduction-target-in-the-cipp-different-to-the-emissions-reduction-target-in-the-joint-statement)).
4. **The numbers are small enough.** South Africa's partner group has six members, and its register lists
   every pledge by instrument.

Not sourced, and therefore not claimed: that any government wants such a registry.

## Skeleton instance

The instance has the shape of the South African partnership. Only the pledge sizes are real.

| Actor | Lever | Sourced | Illustrative |
| --- | --- | --- | --- |
| South Africa | ambition tier 0 to 3 inside its 2030 range of 350 to 420 MtCO₂-eq; reform tier 0 to 2 | the range | costs, value of finance, budget, red line |
| Germany | thirds of its pledge of USD 2,898 million | pledge, grants of 338 | valuation, share cap |
| United Kingdom | thirds of USD 1,875 million | pledge, grants of 75 | valuation, share cap |
| European Union and EIB | thirds of USD 1,592 million | pledge, grants of 264 | valuation, share cap |
| France | thirds of USD 1,084 million | pledge, grants of 4 | valuation, share cap |

Pledges are from the partnership's own register at 30 June 2026
([JET PMU, Table 3](https://justenergytransition.co.za/wp-content/uploads/2026/11/JET-IP-Quarterly-Progress-Report-Q2-2026.pdf)),
which I re-read at the source. Denmark and the Netherlands are left out to keep the instance small.

**Assumed structure.** Finance counts at its grant-equivalent value. South Africa weighs that value
against the cost of ambition and reform. Each donor weighs the mitigation achieved against the
grant-equivalent it gives, and refuses to carry more than a set share of the total.

## What the skeleton shows

The pipeline runs end to end and yields a two-stage tower. None of this is a finding about the real actors.

| Step | Result |
| --- | --- |
| lattice | 3,072 profiles, 31 groups |
| acceptable to all; individually rational; both | 858; 498; 204 |
| strict core inside the acceptable region | 89, all of them equilibria |
| chain fixed in advance: South Africa, Germany, United Kingdom first | no tower: 12 first-stage core profiles, none acceptable |
| all 30 possible first coalitions [post hoc] | 19 have a tower; 3 have a first stage that does something |
| tower used [post hoc] | South Africa, Germany, United Kingdom and EU first, then France |

**Why the fixed chain fails.** With only two donors, the share caps cannot both hold. A burden-sharing
rule of the Global Fund kind blocks small first coalitions. That is a design lesson, whatever the numbers.

**The tower.** Stage 1: ambition 2, reform 1, about USD 3.6 billion allocated. Stage 2, with France:
ambition 3, reform 2, about USD 7.1 billion. The filing is a strictly strong equilibrium of the full game,
and tests T1 to T4 pass.

**Withdrawal.** If France files nothing, the registry returns stage 1. If any other actor files nothing,
it returns zero. A step filing protects only against the loss of late joiners.

**Which numbers matter.** The final outcome stays certified in 173 of 200 draws of the valuations. Changed
one at a time, two numbers tip it at a factor of 1.25: the value South Africa puts on grant-equivalent
finance, and its cost of ambition. The grant-equivalent weight of loans and Germany's share cap tip it at 1.5.

## Where outside knowledge is needed

The skeleton cannot go further on public documents alone.

1. **The four numbers above.** They need someone who knows the partnership's financing from inside or has
   studied it closely.
2. **The form of a filing.** Whether a finance ministry or a development bank could sign a schedule that
   depends on other donors' allocations, and under what instrument.
3. **The recipient's side.** Whether ambition tiers inside a pledged range are a meaningful lever, and what
   the real red lines are.
4. **Per-donor data for Indonesia and Viet Nam.** The investment plans could not be downloaded here.

Who to ask, with what, and how is in `docs/outreach_proposal.md`.

**Files.** `pilots/pilot_a.py`, `pilots/run_pilot.py`, `pilots/results/pilot_a*.json`,
`pilots/results/pilot_a_filings.md`, `outreach/brief_A.md`.
