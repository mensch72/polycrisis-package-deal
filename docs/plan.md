# Polycrisis package deal — work plan

> Exported on 10 November 2026 from the Claude Doc https://claude.ai/artifact/JsCtfcFLRjq5FHe33x6biu (main tab, revision 35). The two diagrams are omitted. The status log continues in `STATUS.md`.
>
> Changed in this repository after the export: the section "Bounded rationality and diplomatic knowledge", one row in "Objections and risks", and thirteen references.

Nov 10, 2026 · @Jobst

## Framing and architecture

The deal is a public registry of unilateral but mutually conditional commitments, one per signatory, whose joint outcome a fixed rule computes. A recommender proposes a focal package with stability certificates. What binds is each signatory's own filed commitment, never our estimate of their values.

**Reading of the task (assumption).** This is a research-and-design programme without a mandate from any actor. Its outputs are a method, a knowledge base, a draft deal with certificates, and a platform. The team is one AI working in sessions, as set out in the next section, so the plan states order and gates, not dates.

**Formal objects.**

| Symbol | Meaning | Built in |
| --- | --- | --- |
| N | actors who can sign | WP1 |
| K | issues | WP2 |
| Aᵢ | lever space of actor i, partially ordered so that larger means a larger concession | WP3 |
| a⁰ = 0 | no-deal reference profile (the disagreement point) | WP5, WP6 |
| y = F(a, ω) | outcome indicators under uncertainty ω | WP5 |
| ≽ᵢ | actor i's own preference over profiles, possibly incomplete, induced by own indicators, own beliefs and an aspiration set | WP4 |
| cᵢ : A₋ᵢ → Aᵢ | conditional commitment function (CCF), weakly increasing | WP7 |

The registry applies one rule to the filed profile c. It selects the largest mutually feasible action profile (Heitzig, 2025):

```latex
\ell(c) \;=\; \sup\{\, a \in A \;:\; a_i \le c_i(a_{-i}) \ \text{for all } i \in N \,\}
```

**Target properties of the deal.**

1. Individually rational and acceptable: every actor weakly prefers ℓ(c) to a⁰, and ℓ(c) lies inside its aspiration set.
2. Efficient: no profile is weakly preferred by all and strictly by some.
3. Core: no group G has a profile a′ with a′ = 0 outside G that all its members weakly prefer to ℓ(c) and one of them strictly prefers. This is the strict core.
4. Self-enforcing: c is a strictly strong Nash equilibrium of the commitment game, and compliance is a renegotiation-proof equilibrium of the repeated implementation game.
5. Reachable: far-sighted actors get from the status quo to the deal by individually profitable steps, and the full deal is absorbing.
6. Robust: 1 to 5 hold on a stated set Θ of preference and belief profiles.

**Why this is tractable.** For costly positive externality problems, the outcomes of strictly strong equilibria of the CCF mechanism are exactly the strict-core profiles, and simple step-function CCFs sustain them \[proved: Heitzig, 2025, Theorems 2 and A1\]. Properties 2, 3 and the static half of 4 therefore reduce to one task: exhibit a core profile a\* of the modelled game. WP6 searches for a\*, WP7 writes the CCFs through a\*, WP8 certifies it.

The theorem does not give three things: the truth of the model, compliance over time, and reachability. Validation (WP8), liability redistribution after shortfalls (WP7) and far-sighted coalition-formation analysis (WP8) cover them.

*[Diagram omitted in this export: architecture · 3 layers, the actors, 2 feedback paths]*

Estimates flow down as advice. Binding content enters only through the actors' filings, and their corrections flow back into the knowledge base.

**Tags used below.** \[proved\] is a theorem in a cited paper. \[model\] holds in the model to be built. \[open\] is unresolved. \[assumption\] is a planning choice that can be changed.

## Team and operating mode

The team is one AI, Claude, working in sessions that Jobst starts or schedules. Jobst sets direction, signs off each gate, and is the only channel to the outside world.

| Matter | Arrangement |
| --- | --- |
| Can do alone | desk research on public sources, data extraction, modelling, search, certificates, drafting, software, simulated pilots |
| Cannot do alone | expert elicitation, legal review, role-play with people, any contact with actors, publishing |
| Substitutes | language-model personas for elicitation and pilots, as priors only and scored for robustness; legal questions are listed, not answered |
| Continuity | a session keeps no memory of earlier work, so all state lives in this doc, the code and the data files; every session ends with a status-log entry |
| Checking | no second person exists, so checks are full enumeration where the instance allows, machine-checkable certificates, and a fresh session that re-runs the work without seeing how it was produced |
| External actions | none without Jobst's instruction: no repository, post, message or scheduled run is created unasked |

**Consequences for the gates.** Gates 1 to 3 can be passed by the team alone. Gate 4 changes from a completed legal review to a list of legal questions for counsel. Gate 5 runs with model-agent delegations first, and a pilot with people needs participants beyond the team.

**What limits progress.** Working time is not the main constraint. Access to non-public knowledge, to people and to a mandate is. Each session also has bounded working memory, so the work is cut into increments that end in files.

## WP1 Signatories

Anyone who controls a verifiable lever and can bind a successor may sign. States sign rather than governments, and firms rather than CEOs. NGOs mostly act as guarantors, and armed groups sign unilateral restraint deeds only.

| Class | Why it matters | How it can commit | Main caveat |
| --- | --- | --- | --- |
| States | most regulatory, fiscal and military levers | treaty, or a domestic statute that contains the CCF | government turnover; the deal must lie in each domestic win-set (Putnam, 1988) |
| Sub- and supranational polities (EU, federal states, cities) | own levers where the centre is blocked | own legislation, compacts | limited competences |
| Intergovernmental bodies (IAEA, WHO, IMF, development banks) | inspection, escrow, lending terms | mandate from their members | act through member majorities, so mostly guarantors |
| Firms and state-owned enterprises (frontier AI developers, chip and cloud suppliers, fossil producers, DNA synthesis, insurers) | direct control of technical levers | contracts enforceable by courts or arbitration | CEOs are agents; competition law may bar joint restraint without state cover \[open\] |
| Individuals with personal control (personalist rulers, controlling shareholders, large philanthropists) | sometimes the real decision-maker | personal undertaking, or guarantee for their entity | the commitment ends with their tenure |
| Civil society (NGOs, unions, religious bodies, academies, standards bodies) | information, certification, litigation, legitimacy | pledge to monitor or endorse | few material levers |
| Armed non-state actors and de facto authorities | territory, ceasefires, access | unilateral deed with third-party monitoring, as in Geneva Call's Deeds of Commitment (Bongard and Somer, 2011) | legal bars on dealing with listed groups; must not reward threat capacity |
| Stakeholders without levers (future generations, non-humans, unrepresented publics) | they bear the outcomes | not signatories; trustees speak for them in WP4 | who appoints the trustee |

Conditional pledges and non-state signatories both have precedents. States already file conditional pledges under the Paris Agreement (Pauw et al., 2020). Twenty AI companies signed the [Frontier AI Safety Commitments](https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024), which tie development and deployment to risk thresholds.

**Selection method.**

1. Seed: for each issue k, list the actors whose levers move its indicators.
2. Sufficiency: a group S is sufficient for k if some profile with a = 0 outside S reaches the target set of k. Minimal sufficient groups are the critical-mass clubs. An actor in all of them holds a veto.
3. Blockers: add outsiders who can undo the gains by leakage or substitution.
4. Currency holders: add actors who own cheap-to-give items that others want (WP2).
5. Capacity screen: a legal identity that outlives its leaders, observable levers, a ratification path.
6. Roles: signatory, guarantor (verifier, escrow agent, depositary) or represented stakeholder.
7. Granularity: 30 to 50 blocs in version 1, splitting a bloc only where results are sensitive to it \[assumption\].

**Threat rule.** In variable-threat bargaining the disagreement point is the outcome of chosen threats (Nash, 1953). A deal benchmarked that way would pay for threat capacity. Gains are therefore measured against a threat-free reference.

**Output.** Actor registry v1: class, role, levers, commitment instrument, verifier, internal veto players. WP1 to WP3 iterate until adding an actor or issue changes the achievable set by less than a set tolerance.

## WP2 Issues

Issues are chosen by stakes, tractability and linkage value. Each is typed by its game structure, because the type decides which form of commitment can work.

**Seed list.** Game types follow Barrett (2007). Types and critical actors are working hypotheses for WP5 to test.

| Issue | Game type | Critical actors | Example levers |
| --- | --- | --- | --- |
| AI safety and control | mutual restraint; weakest link for securing model weights | frontier developers, their home states, chip and cloud suppliers | capability thresholds, evaluations, compute reporting, liability |
| Climate change | aggregate effort | large emitters, fossil exporters, finance providers | emission paths, carbon prices, finance, technology transfer |
| Nuclear weapons and nuclear safety | mutual restraint; weakest link for material security | nuclear-armed states, IAEA | arsenals and postures, fissile-material controls, inspections |
| Biological weapons and dual-use research | mutual restraint; weakest link | states with high-containment labs, synthesis providers | verification, order screening, research oversight |
| Pandemic prevention | weakest link for surveillance; single best effort for countermeasures | all states; states and firms with R&D capacity | surveillance, sample and data sharing, surge finance |
| Terrorism and armed conflict | weakest link; mutual restraint | states, de facto authorities, financial hubs | financing controls, ceasefires, denial of safe havens |
| Poverty and debt | aggregate effort | donors, creditors including private ones, development banks | concessional finance, debt relief, market access |
| Biodiversity, land and oceans | aggregate effort | megadiverse states, commodity importers, traders | protected areas, deforestation-free trade, fishery subsidies |

Further candidates: antimicrobial resistance, cyber and information integrity, outer space, critical minerals, migration, financial stability and tax, food and water, solar geoengineering governance, and the gradual loss of human influence over AI-run systems (Kulveit et al., 2025).

**Linkage currencies.** A second list holds items that cost the giver little and matter much to the receiver. Examples are seats and voting shares in international bodies, recognition, sanctions relief, market and technology access, and security guarantees. They enter the lever catalogue like any other lever.

**Method.**

1. Harvest candidates from existing agendas and assessments, starting with the [Pact for the Future](https://digitallibrary.un.org/record/4061879) (UN resolution 79/1, 2024) and the polycrisis literature (Lawrence et al., 2024).
2. Build the ontology: issue, indicators, and for each indicator the boundary of its acceptable region, in the sense of a safe operating space (Heitzig et al., 2016).
3. Type each issue's game. Record the existing regime and its gap.
4. Map causal couplings between issues as a cross-impact matrix, using the mechanisms of crisis entanglement in Lawrence et al. (2024).
5. Score each candidate on stakes, tractability by the listed levers, and linkage value.

**Linkage value.** For a candidate package x, let gᵢₖ be actor i's gain over a⁰ on issue k.

```latex
\underbrace{g_{ik} \ge 0 \quad \forall\, i,k}_{\text{issue by issue}}
\qquad \text{versus} \qquad
\underbrace{\textstyle\sum_{k} g_{ik} \ge 0 \quad \forall\, i}_{\text{package}}
```

With additively separable gains the package condition is weaker. It helps where relative saliences differ across actors, since each can concede on what matters less to them. Without separability, adding an issue can also shrink or destroy the zone of agreement (Sebenius, 1983), so linkage value is computed in WP6, not assumed.

**Output.** Issue ontology v1: indicators, boundaries, game type, critical actors, regime gap, couplings, currencies. Version 1 holds 8 to 12 issues, and the first end-to-end test uses three \[assumption\].

## WP3 Control variables

Each actor gets a short catalogue of levers. Every lever is oriented so that more of it costs its owner and is weakly welcome to everyone else, because that is the structure the CCF theorems need.

**Lever archetypes.**

| Actor class | Lever archetypes |
| --- | --- |
| States and other polities | regulate; tax, spend and transfer; abstain (moratoria, postures); disclose and admit inspectors; share technology, samples and data; vote and recognise; open markets |
| Firms | safety thresholds and practices; audit access; non-deployment; licensing and supply terms |
| Finance | lending terms, underwriting, divestment, escrow |
| Intergovernmental bodies | inspection, certification, fund management |
| Civil society | monitoring, certification, litigation, endorsement |
| Armed non-state actors | ceasefire, access, renunciation of specific means |

**Catalogue fields.**

| Field | Used for |
| --- | --- |
| Domain: binary, up to five ordered levels, or a parametrised time path | search (WP6) |
| Baseline and feasible range | disagreement point and feasibility |
| Own cost and indicators moved | preferences (WP4) and world model (WP5) |
| Observability: public, inspectable, self-reported or hidden | verification (WP7) |
| Reversibility and lag | enforcement and exit rules (WP7) |
| Legal instrument and internal approver | ratification constraint (WP1) |

**Method.**

1. Derive each actor's levers from the issue ontology and the currency list.
2. Orientation test: the owner weakly prefers less, every other actor weakly prefers more. Levers that pass fall under the proved results (Heitzig, 2025).
3. Levers that fail have a contested direction, such as the speed of technology diffusion. Split or re-parametrise them, or route them to the generalised mechanism for arbitrary games \[open; in preparation as a postscriptum to Heitzig, 2025\].
4. Add side payments as levers. A transfer from i to j costs i and benefits j. It passes the test unless third actors hold relative-gains concerns (WP4).
5. Choose the committed quantity by attribution: an action where outcomes depend on others or on chance, an outcome where it is observable and the actor's own.
6. Add state-contingent levers of the form "if indicator X crosses level z, then action Y". They let actors with different forecasts agree, subject to the betting caveat in WP4.

**Output.** Lever catalogue v1 with about ten levers per actor \[assumption\], each flagged pass or fail on orientation and classed by observability.

## WP4 Evaluative dimensions and rough preferences

Each actor is described in its own terms: own indicators, own beliefs, and an aspiration set of acceptable outcomes. No common welfare function is built at any point.

**Representation tiers.** A tier is escalated only where the recommended package is sensitive to it.

| Tier | Content | Source |
| --- | --- | --- |
| T0 | per issue: position, salience, red lines (data model of Thomson et al., 2006) | documents, votes, experts |
| T1 | aspiration set: the acceptable region in the actor's own indicators (Dima et al., 2025) | stated targets and red lines |
| T2 | trade-offs inside the region, as weights or a partial order; risk and time attitudes | structured elicitation |
| T3 | evaluation supplied and filed by the actor | participation (WP10) |

**Acceptability.** Let yᵢ be actor i's own indicator vector and Pᵢ its own beliefs.

```latex
a \ \text{acceptable to } i \iff \mathbb{E}_{P_i}\!\big[\, y_i(a,\omega) \,\big] \in \mathcal{A}_i ,
\qquad
\mathcal{C} = \{\, a \in A : a \ \text{acceptable to every } i \,\}
```

Risk limits fit this form, because a probability is the expectation of an event indicator. Inside its region an actor's preference is at least monotone: less own concession and more from others is weakly better. The first question for WP6 is whether C is non-empty.

**Decision paradigms.** Actors may also differ in how they decide. Even in a two-option thought experiment, optimal control, welfare economics, responsibility-based and safe-operating-space approaches disagree on the right choice (Heitzig, Barfuss and Donges, 2018). The aspiration-set format takes no side.

**Sources for rough preferences.**

- Stated: official positions, pledges, reservations, strategies, corporate filings.
- Revealed: UN General Assembly votes (Bailey, Strezhnev and Voeten, 2017), budgets, ratification records, past deals.
- Surveyed: publics and experts.
- Simulated: language-model personas as priors only, to be checked against the three sources above.

**Five separations to keep.**

1. Values and beliefs. A package that all prefer only because their forecasts differ is a bet. Each candidate is tested for one shared belief under which every actor still gains (Gilboa, Samuelson and Schmeidler, 2014).
2. Outcomes, actions and process. Sovereignty costs, face and credit attach to actions and procedure, not to outcomes.
3. Absolute and relative gains. Rivals may judge their gain against the other's (Grieco, 1988).
4. Actor and constituents. Domestic veto players enter as a ratification constraint on the package, not as an averaged preference (Putnam, 1988).
5. Known and unknown. Preferences may be incomplete. The CCF results are stated for partial orders \[proved: Heitzig, 2025, Appendices A and B\].

**Robustness set.** Each actor gets an ensemble of plausible aspiration sets and beliefs. Their product is Θ, the set on which WP6 and WP8 must hold.

**Validation.** Back-predict known positions and outcomes of past negotiations. Compare stated with revealed preferences and report the gaps.

**Output.** One preference file per actor, tiered, with provenance and uncertainty.

## WP5 Data

The knowledge base is an open, versioned graph of actors, issues, levers, indicators, effect models and preferences. Contested entries are kept side by side with their source, not averaged.

| Component | Content | Main sources |
| --- | --- | --- |
| Registries | actors, issues, levers, indicators (WP1 to WP3) | official statistics, treaty and voting records, corporate filings |
| Baselines | current values and no-deal projections per indicator | scientific assessments, specialised trackers, published scenarios |
| Effect models F | reduced-form emulators from levers to indicators, with uncertainty and cross-issue coupling | sectoral models, assessment reports, expert elicitation |
| Preferences | tiered files from WP4 | documents, votes, surveys, elicitation |

**Method.**

1. Schema first. Every entry carries source, date, uncertainty and a "who says" field.
2. Extraction by language-model-assisted reading of primary documents. Each value keeps a link to its passage. A sample is coded twice, by independent sessions, and the agreement rate reported.
3. Effect models: one emulator per issue, calibrated to existing assessments, plus coupling terms from the cross-impact matrix. A modular host such as copan:CORE (Donges et al., 2020) keeps modules exchangeable. A climate-economy module can start from RICE-N (Zhang et al., 2022).
4. Deep uncertainty: for AI, nuclear and engineered-pandemic risks, store ranges and sets of priors, never single point estimates. Keep each actor's own beliefs.
5. Harmonise units, time grid and baseline scenarios only. Discount rates, monetisation and risk weights stay actor-specific.
6. Fix the reference profile a⁰ at a date before the exercise becomes public. Actors who expect to bargain soon under-invest beforehand (Harstad, 2012).
7. Treat no-deal forecasts as performative, since publishing them changes behaviour. Report them as self-consistent, set-valued forecasts (Heitzig, 2026b).
8. Governance: open licence, versioned releases, and a correction channel for the actors themselves, which feeds WP10.

**Output.** Knowledge base v1 and a data descriptor.

**Open.** Access rules for entries whose detail could be misused, such as fine-grained maps of who can pressure whom.

## WP6 Search

The search looks for a core profile a\* inside the jointly acceptable region C. By the CCF theorem such a profile is efficient and can be sustained in strong equilibrium. Where the core is empty, the search returns the profile with the smallest blocking margin.

**Size.** With 40 actors, 10 levers each and 4 levels per lever there are 4^400 ≈ 6.7 × 10^240 profiles. There are 2^40 − 1 ≈ 1.1 × 10^12 coalitions and about 1.6 × 10^35 coalition structures. Enumeration is out, so the search exploits structure.

**Objective.** Let ũᵢ be actor i's gain over a⁰, normalised by its own largest acceptable gain \[model\]. The blocking margin of a group G at a profile a, and the target, are

```latex
e(G,a) \;=\; \max_{a' \in A,\ a'_{-G} = 0}\ \ \min_{i \in G}\ \big[\tilde u_i(a') - \tilde u_i(a)\big],
\qquad
a^\ast \in \arg\min_{a \in \mathcal{C}}\ \max_{G \subseteq N}\ e(G,a)
```

Singletons give individual rationality and G = N gives efficiency. The maximum is never negative, because G = N can choose a′ = a, and it is zero exactly on the weak core. The strict core required by the theorems is then checked at the candidate. The normalisation is per actor, so no interpersonal comparison enters. Actors known only ordinally enter through blocking tests instead of margins.

**Stages.**

1. Feasibility. Test whether C is non-empty. If it is empty, report the smallest sets of aspirations that cannot hold together. That finding is a result in itself.
2. Screening. Per issue, compute who gains and who loses from efficient single-issue agreements. The losers define who must be compensated on what.
3. Focal profiles. Inside C, compute scale-free candidates: the Nash product of normalised gains (Nash, 1950), their leximin, and the profile deepest inside C, which maximises the smallest margin to any actor's boundary.
4. Coalitional refinement by constraint generation. An oracle searches for a blocking pair (G, a′). If it finds one, the constraint is added and the candidate re-solved. Coalition families are tried in order: singletons, pairs, issue clubs from WP1, blocs, complements of single actors, then heuristic search over general G.
5. Mechanism in the loop. File the CCFs through a\* in a simulator and let model agents update them, using the learning rule of Heitzig (2025) and generic learners. Check that a\* is absorbing and record which other core points are reached.
6. Robustness. Re-run on the ensemble Θ. Rank data entries by how often they flip the result, and send the top ones back to WP4 and WP5.
7. Menu. Return three to seven structurally different candidates with certificates. The choice among core points is distributional and belongs to the actors (WP10). Sharing keys on offer include equal normalised gains and degrees of responsibility for the risk (Heitzig and Hiller, 2020).

**Test beds for stage 5.** A conditional commitment mechanism has already run in the AI4ClimateCooperation challenge (Heitzig et al., 2023), whose simulator is RICE-N (Zhang et al., 2022). Language-model agents reach high welfare under conditional-contribution mechanisms while following brittle policies (Rengert, Heitzig and Asano, 2026). Stage 5 therefore scores adaptation and robustness, not welfare.

**Outsider response.** The core above lets outsiders fall to zero when G deviates. Canonical CCFs produce exactly that response \[proved: Heitzig, 2025\]. It is the analogue of individually best-responding outsiders in the core of Chander and Tulkens (1997). Results are also reported under the internal-and-external stability test used by Barrett (1994), which lets remaining members re-optimise after one leaves, and under far-sighted concepts (WP8).

**Empty core.** Fall back, in order, to the smallest blocking margin, to far-sighted stability (WP8), and to a different issue set or currency list (WP2).

**Output.** A menu of candidates with certificates, and a ranked list of the data gaps that matter. The toy instance with eight actors has 2^8 − 1 = 255 coalitions, so full enumeration gives ground truth for the heuristics.

## WP7 Drafting the package deal

The draft is a set of filings, not one treaty text. Each signatory files a conditional commitment function through the recommended profile a\*. A short common protocol fixes the rule, verification, the response to shortfalls, and updating.

| Part | Content | Draws on |
| --- | --- | --- |
| A. Protocol | the rule ℓ, the registry and its depositary, lever definitions and measurement | Heitzig (2025) |
| B. Filings | one CCF per signatory, in the legal form its class allows: statute, board resolution with contract, deed, mandate | WP1, WP3 |
| C. Verification annex | per lever: indicator, data source, verifier, tolerance band | WP3, WP5 |
| D. Shortfall response | liability redistribution, cross-issue reciprocity, deposits, club measures | below |
| E. Change rules | accession, withdrawal with notice, scheduled re-solving, contingency clauses | WP10 |

**Filing forms.** The canonical filing through a\* is a single step:

```latex
c_i^{a^\ast}(a_{-i}) \;=\; \begin{cases} a_i^\ast & \text{if } a_j \ge a_j^\ast \ \text{for all } j \ne i,\\[2pt] 0 & \text{otherwise.} \end{cases}
```

In words: i implements its listed levels provided the registry shows every other signatory at or above its listed levels. The indifference-curve filing instead commits i to the largest own action that leaves it no worse off than at a\*, whatever the others do. Both sustain a core profile in strong equilibrium \[proved: Heitzig, 2025, Theorem A1\].

The indifference-curve form is the default where preferences are continuous, because it shrinks liabilities gradually when someone falls short. The 1978 Bonn summit package, re-expressed as eight conditional commitments, is the worked template for binary levers (Heitzig, 2025, Appendix A).

**Shortfall response.** The theorem treats liabilities as binding. Where they are not, four devices apply, in this order of preference.

1. Liability redistribution by linear compensation. With shortfall dᵢ(t) = max{0, ℓᵢ(t) − aᵢ(t)} and mean shortfall d̄(t), next-period liabilities are

   ```latex
   \ell_i(t+1) \;=\; a_i^\ast + \alpha\,\big[\,d_i(t) - \bar d(t)\,\big]
   ```

   Total liabilities stay constant. The strategy is strongly renegotiation-proof and a strong Nash equilibrium in every subgame \[proved for one public good with public monitoring, equal marginal costs and common discounting: Heitzig, Lessmann and Zou, 2011\]. Vector levers and noisy monitoring are \[open\].
2. Cross-issue reciprocity. A violation on one issue is answered on another, which pools incentive constraints across issues (Bernheim and Whinston, 1990). Maggi (2016) separates this enforcement linkage from negotiation and participation linkage.
3. Deposits held in escrow and refunded on compliance (Gerber and Wichardt, 2009).
4. Club measures against non-participants, such as trade measures (Nordhaus, 2015), where reciprocity is too weak.

Side payments are conditioned inside the CCFs and not offered separately. Binding offers of strategy-contingent side payments alone do not always lead to efficient outcomes (Jackson and Wilkie, 2005).

**Change rules.** Any actor may file at any time, and ℓ is recomputed. A larger filing never lowers anyone's liability \[proved: Heitzig, 2025, Lemma A2\]. Filings can be withdrawn with notice. In the carbon-market linking model, reversibility shortened the formation path, because agreements that would later be terminated were not signed at all (Heitzig and Kornek, 2018).

**Drafting procedure.** One neutral text is revised against each party's criticism, with no competing drafts, as in the single negotiating text of Raiffa (1982). Here the text is generated from a\* and revised whenever filings or data change.

**Output.** Protocol text, filing templates per actor class, verification annex, and a machine-readable schema for CCFs.

## WP8 Proving that it is a good deal

"Good deal" is split into three kinds of evidence: theorems about the mechanism, checkable certificates about the instance, and empirical validation of the model. Only the first two are proofs.

| Property | Evidence | Tool | Status |
| --- | --- | --- | --- |
| Liabilities exist and are unique | theorem | the largest feasible profile exists (Heitzig, 2025, Lemma A2) | \[proved\] |
| Individually rational and acceptable | certificate per actor and per element of Θ | evaluation of a\* with each actor's own indicators and beliefs | \[model\] |
| Efficient and in the core | certificate: no blocking pair in the coalition family searched, with margin ε | constraint generation (WP6); full enumeration for small n | \[model\]; complete only for small n |
| Filed CCFs form a strictly strong, hence coalition-proof, Nash equilibrium | theorem, given the row above and the orientation test | Heitzig (2025), Theorem A1; concept of Bernheim, Peleg and Whinston (1987) | \[proved\] for levers that pass the test |
| Compliance is self-enforcing and renegotiation-proof | theorem, plus an estimate of the compensation factor α each actor needs | Heitzig, Lessmann and Zou (2011) | \[proved\] for one good; \[open\] beyond |
| Reachable and absorbing | equilibrium analysis of the formation process | Konishi and Ray (2003); Heitzig and Kornek (2018); Heitzig (2026a) | \[model\] |
| Far-sightedly stable | membership in the largest consistent set or a farsighted stable set | Chwe (1994); Ray and Vohra (2015) | \[model\] |
| Not a bet | certificate: one shared belief under which all still gain | Gilboa, Samuelson and Schmeidler (2014) | \[model\] |
| Robust | stress tests: remove each actor and each pair, perturb Θ, change governments | recomputation of ℓ and of all certificates | \[model\] |

**Reachability.** In the process of nested binding agreements, a grand state once reached is absorbing, and arrival can fail only by cycling among non-grand states \[proved: Heitzig, 2026a\]. A grand state is reached almost surely when distributional stakes are smaller than each actor's share of the efficiency gain. The necessary conditions for a given candidate cycle can be checked by linear programming. WP8 checks these conditions on the instance.

**Formalisation.** Mechanism-level statements are machine-checked in a proof assistant. Instance-level certificates are published as data with an independent checker, so anyone can re-verify them without trusting the search.

**Validation.** The pipeline is back-tested on past package deals. The first case is the 1978 Bonn summit, already encoded as conditional commitments (Heitzig, 2025, Appendix A). The test asks whether the historical package is a core profile under reconstructed preferences, and whether deals that later collapsed are flagged.

**Limits.** Certificates are relative to the effect model F and the set Θ. Under private information no mechanism for bilateral trade is at once efficient, individually rational, incentive-compatible and budget-balanced (Myerson and Satterthwaite, 1983). Actors can therefore gain by misreporting to the recommender. The registry itself asks only for commitments, never for preferences.

**Output.** A certificate bundle per candidate, the proof scripts, and a validation report.

## WP9 Communicating and promoting

Promotion rests on one property of these filings: a filing through an individually rational profile cannot leave its author worse off than no deal, provided liabilities are met. Early movers therefore bear no risk, and each public filing brings the others' conditions closer. The property follows from the monotonicity assumptions, for levers that pass the orientation test.

1. Tailored briefs. Each actor gets a short brief generated from its own certificate: what it gains in its own indicators, what it gives, who else must move. No brief claims more than its certificate.
2. Explorer. A public site lets anyone vary assumptions and watch the package and the certificates change. It doubles as the correction channel of WP5.
3. Cascade plan. Outreach is ordered by filing thresholds, as in a threshold model of collective behaviour (Granovetter, 1978). Actors who gain most and risk least file first, and the far-sighted path from WP8 gives the order.
4. Carriers. Middle powers, cities, firms, funders and academies carry the first filings. Informal expert channels precede official ones.
5. Framing. The deal is presented as unilateral, withdrawable with notice, and binding only if others move. Aspiration sets are presented as each actor's own, never as a common yardstick.
6. Red team. Before release, an independent review checks each brief for misuse, for instance being read as a map of pressure points or as recognition of a listed group.

**Output.** Brief generator, explorer site, outreach sequence, papers.

## WP10 Participation and updating (optional)

Participation needs no extra machinery. The registry already accepts filings from the actors themselves, so the recommender's estimates are replaced, actor by actor, by what the actors file.

**Three ways in, by rising commitment.**

1. Correct: an actor edits its own entries in the knowledge base.
2. Consult: it files aspirations privately and receives a recommendation computed with them.
3. Commit: it files a CCF publicly.

**No imposed value system.** The binding layer takes commitments only. The advisory layer uses each actor's own indicators and aspiration set. Where aggregation is unavoidable it is scale-free (Nash, 1950) or approval-based.

**Choosing among candidates.** Actors rate each candidate on the menu with a willingness to approve that depends on how many others approve, as in MaxParC (Heitzig, Simmons and Constantino, 2025). If all rate some candidate positively, one such candidate wins for sure. The method's chance element is its fallback when no such candidate exists. Whether a treaty can replace the lottery by proportional shares of divisible items is \[open\].

**Negotiation by updating.** Actors take turns. Each picks its favourite point on the others' current offers and responds with its indifference-curve CCF through that point. Starting from all-zero filings, one round of such updates ends in the core \[proved for the single-good case: Heitzig, 2025, Theorem 3\]. No chair is needed.

**Commitment devices to compare.** Delegation to a mediator who acts for those who opt in (Monderer and Tennenholtz, 2009). Conditional programs (Tennenholtz, 2004; Kalai et al., 2010). Conditional contribution mechanisms (Reischmann and Oechssler, 2018; Oechssler, Reischmann and Sofianos, 2022). Instructions to delegates under which every principal is guaranteed to be no worse off (Oesterheld and Conitzer, 2022).

**Deliberation aids.** In experiments, AI-mediated drafting helped groups find common ground (Tessler et al., 2024). It is used for the wording of clauses and briefs, not for the binding numbers.

**Updating.** Re-solving runs on a fixed schedule and after material data changes. Releases are versioned. A filing stays valid until withdrawn. A change of a\* arrives as a proposed amendment that each actor accepts by re-filing.

**Stakeholders without levers.** Trustees or citizens' assemblies supply aspiration sets that enter the acceptable region. Whether these act as hard constraints or only as flags is \[open\].

**Privacy.** Aspirations filed for consultation stay private. Only CCFs are public.

**Pilot.** Before any real actor is approached, model-agent delegations play the process on the toy instance. Role-play with people follows once participants are available.

## Bounded rationality and diplomatic knowledge

Two layers cut across the work packages. One keeps the deal sound when actors do not optimise. The other
feeds in what diplomats know about relationships and constraints. Added on 10 November 2026 at Jobst's
request. A first toy exploration is in `docs/phase0_instance2.md`.

**Why.** The theorems describe actors who compute best responses and can coordinate in any group. Real
actors satisfice (Simon, 1955), make errors, weigh losses more than gains (Kahneman and Tversky, 1979),
and are not unitary. Groups without a working relationship can coordinate neither a deal nor a deviation.

**Bounded rationality: design rules** \[assumption\].

| Limit of the actor | Response in the design | Where |
| --- | --- | --- |
| Cannot foresee the filings of others | Safe filings. A filing through an individually rational profile cannot leave its author worse off than no deal, for levers that pass the orientation test (WP9). The certificate checks this by enumeration. The standard is that of obviously strategy-proof mechanisms (Li, 2017): safety must show without contingent reasoning. | WP7, WP8 |
| Cannot evaluate complex functions | A complexity budget for filings: steps or ladders with few conditions, in the actor's own indicators. | WP7, WP9 |
| Optimises only roughly | Stability with a margin. Certificates report the smallest loss of any deviating group, and deviation probabilities under logit quantal response (McKelvey and Palfrey, 1995) for a range of precisions. | WP6, WP8 |
| Moves only for a noticeable gain | Stability is reported as a function of an inertia threshold. | WP6 |
| Cannot coordinate in large groups | Stability is reported by group size, next to stability against all groups. | WP8 |
| Errs in implementation | Gradual filings and liability redistribution, so that one shortfall does not void the deal. Expected loss is reported for a range of error rates. | WP7 |
| Weighs losses more than gains | Loss-averse variants of each preference file enter Θ. Losses on single issues are shown in the briefs. | WP4, WP9 |
| Learns by trial, not by deduction | Stage 5 of WP6 runs generic learners and model agents, and scores adaptation. | WP6, WP10 |
| Is not unitary | Internal veto players enter as a ratification constraint. | WP1, WP4 |

**Rule of caution.** Each of these limits can make a deal look more stable than it is. A certificate that
relies on one states it, and gives the result without it alongside.

**Diplomatic knowledge: where it enters.**

| Kind of knowledge | Formal object it changes | Where |
| --- | --- | --- |
| Relationships: alliance, rivalry, recognition, sanctions, dependence | the family of groups that can coordinate, as in games on graphs (Myerson, 1977); relative-gains terms between rivals | WP1, WP4, WP6, WP8 |
| Red lines and non-negotiables | aspiration sets | WP4 |
| Existing obligations and legal bars | lever catalogue: barred levels, instrument, approver | WP3 |
| Linkage taboos and customary linkages | admissible issue sets | WP2 |
| Who cannot be seen to sign with whom | filing form: filings are unilateral, and conditions refer to registry levels, not to named counterparts | WP7 |
| Ratification rules and domestic veto players | ratification constraint | WP1, WP4 |
| Sequence, face and credit | cascade order | WP9 |
| Compliance record | priors on compliance; size of compensation factor and deposits | WP7 |

**Is there data?** Yes for formal ties between states, mostly by pair and year. Little exists for firms
and armed groups, and tacit knowledge is in no dataset.

| Knowledge | Source | Limit |
| --- | --- | --- |
| Alliances and their obligations | ATOP (Leeds et al., 2002) | coded treaty texts; states only |
| Disputes and rivalry | Militarized Interstate Disputes (Palmer et al., 2022); UCDP/PRIO armed conflict (Gleditsch et al., 2002) | events, not intentions |
| Voting affinity | UN General Assembly ideal points (Bailey, Strezhnev and Voeten, 2017) | one dimension |
| Sanctions | Global Sanctions Data Base (Felbermayr et al., 2020) | announced measures, not their bite |
| Trade agreements | DESTA (Dür, Baccini and Elsig, 2014) | design, not use |
| Environmental agreements | IEADB (Mitchell et al., 2020) | membership and text |
| Membership of intergovernmental bodies | Correlates of War IGO data (Pevehouse et al., 2020) | formal membership |
| Domestic veto players | political constraint index (Henisz, 2002) | coarse |
| Negotiating positions and salience | DEU (Thomson et al., 2006) | EU legislation only |

None of these has been downloaded yet. Versions, coverage years and licences are checked at extraction
(WP5). Tacit knowledge covers who trusts whom, what is negotiable in private, and what would cost face.
It needs practitioners, whom the team cannot reach alone. Document reading and language-model personas
stand in as priors only, and the correction channel of WP10 replaces them over time.

**Method.**

1. Add a relationship layer to the knowledge base: a typed, dated multigraph on the actors, each edge with source and "who says".
2. Derive the family of groups connected by a working channel. Run WP6 and WP8 with all groups and with this family, and report both.
3. Enter each constraint as a filter with provenance. Rank constraints by how often they flip the result, as for data entries in WP6.
4. Give every certificate a stability table: by group size, by inertia threshold, by logit precision, by error rate.
5. Keep the relationship layer under the access rules of WP5. It is a map of pressure points.

**Status.** Explored on the second toy instance: stability by group size, by threshold and with one
channel removed. Not yet built: the safe-filing check, quantal response, loss-averse variants, error
rates, and any real relationship data \[open\].

## Sequencing and gates

Phase 0 exercises all ten work packages on a small instance before anything is scaled. Each later phase starts only when the gate before it is passed.

*[Diagram omitted in this export: roadmap · 6 phases, 5 gates]*

**Dependencies.** WP1 to WP3 iterate to closure. WP4 and WP5 feed WP6. WP6 and WP8 run as one loop. WP7 needs a certified candidate. WP9 and WP10 start with the registry prototype.

**Papers along the way.** A method paper after Phase 0, the data descriptor after Phase 1, a certified case study after Phase 2.

**Pace.** With a one-AI team, progress is counted in sessions, not months. Phase 0 started on 10 November 2026.

## Objections and risks

The plan above implements the request as stated. These are the points where it may fail to deliver, each with the current response.

| Objection | Why it matters | Response or status |
| --- | --- | --- |
| Proof is model-relative | Certificates hold for the effect model F and the set Θ only. A wrong model or preference file voids them. | Validation, the robustness set, and actors' own filings in place of estimates. |
| The core may be empty | Likely once relative-gains concerns or contested levers enter. | Smallest blocking margin, far-sighted stability, or a smaller issue set. |
| Binding liabilities are assumed | The static theorem presumes fulfilment. Linear compensation is proved for one good with public monitoring. | \[open\] for vector levers, noisy monitoring and unequal discounting. Devices 2 to 4 of WP7 are the fallback. |
| Contested levers | Central levers may fail the orientation test, for instance where an ally dislikes a protector's disarmament. | Needs the generalised mechanism \[open\]. |
| Strategic misreporting | Actors can shift the focal point by misstating aspirations. | The registry takes no preferences. The recommender returns a menu and reports sensitivity to each actor's file. |
| Bets | A package may rest on contradictory forecasts. | No-betting test, with contingent clauses flagged. |
| Linkage fragility and complexity | A package ties issues together, so failure can spread. Transaction and information costs grow with issues and parties (Sebenius, 1983; Maggi, 2016). | Indifference-curve filings degrade gradually. Linkage value is computed. The start is three issues. |
| Legitimacy | Nobody mandated the exercise. Listing an actor may be read as recognition. | Roles are kept separate from recognition. Participation layer and red team. |
| Paying for restraint | Rewarding restraint can invite a build-up of what is to be restrained. | Threat-free reference fixed at an earlier date. No transfer for withdrawing a threat. |
| Misuse of the knowledge base | It maps red lines and pressure points. | Access rules, aggregated publication, policy-level content only. |
| Scale | One deal for everything may be less attainable than several overlapping conditional deals. | The rule ℓ is computed over whatever is filed, so partial packages work. Phase 0 tests this first. |
| Assumed limits flatter the deal | Bounded coordination, inertia and missing channels all enlarge the set of stable outcomes. | The result without the assumption is always reported alongside. |
| One-AI team | No second person checks the work, so an error of mine can pass unnoticed. The team has no access to people or to non-public knowledge. | Full enumeration on small instances, published certificates, fresh-session audits, and Jobst's sign-off at each gate. |

## Status log

Specification and results of the toy instance are in the tab Phase 0 results.

**10 November 2026, session 1 (Claude).**

- Plan revised for a one-AI team: Team and operating mode, the gates, the roadmap and the risk table.
- Phase 0, first increment: a toy instance with 8 actors and 3 issues ran through all ten work packages. It has 326 core profiles, a certified menu of five, and a lead candidate that keeps all properties in 143 of 150 parameter draws.
- Gate 1: the criterion is met in 8 of 8 runs. Stress tests were added afterwards. The first blocking oracle failed them, and the repaired one passes. Jobst's sign-off is pending.
- Changed after seeing results: the lead is chosen by robustness, not by the Nash product.
- Not yet done in Phase 0: instances with an empty core and with an issue that has no deal of its own, far-sighted formation, MaxParC over the menu, an independent checker, and a fresh-session audit.
- State: code, logs and results went to Jobst as a zip in the chat. A text bundle of the same files is stored with this doc as asset c73bfcab8ebe97d3c427f8fde79760b2. Its header says how to restore the folder. No repository and no scheduled run exist.
- The next session restores the code from that asset and starts from the open list in the tab Phase 0 results.

## References

Identifiers were checked on 10 November 2026 against Crossref, arXiv, publisher pages or the PDFs in the project.

- Bailey, M.A., Strezhnev, A. and Voeten, E. (2017) 'Estimating dynamic state preferences from United Nations voting data', *Journal of Conflict Resolution*, 61(2), pp. 430–456. [doi:10.1177/0022002715595700](https://doi.org/10.1177/0022002715595700)
- Barrett, S. (1994) 'Self-enforcing international environmental agreements', *Oxford Economic Papers*, 46(Supplement 1), pp. 878–894. [doi:10.1093/oep/46.Supplement\_1.878](https://doi.org/10.1093/oep/46.Supplement_1.878)
- Barrett, S. (2007) *Why Cooperate? The Incentive to Supply Global Public Goods*. Oxford: Oxford University Press. [doi:10.1093/acprof:oso/9780199211890.001.0001](https://doi.org/10.1093/acprof:oso/9780199211890.001.0001)
- Bernheim, B.D., Peleg, B. and Whinston, M.D. (1987) 'Coalition-proof Nash equilibria I. Concepts', *Journal of Economic Theory*, 42(1), pp. 1–12. [doi:10.1016/0022-0531(87)90099-8](https://doi.org/10.1016/0022-0531%2887%2990099-8)
- Bernheim, B.D. and Whinston, M.D. (1990) 'Multimarket contact and collusive behavior', *RAND Journal of Economics*, 21(1), pp. 1–26. [doi:10.2307/2555490](https://doi.org/10.2307/2555490)
- Bongard, P. and Somer, J. (2011) 'Monitoring armed non-state actor compliance with humanitarian norms: a look at international mechanisms and the Geneva Call Deed of Commitment', *International Review of the Red Cross*, 93(883), pp. 673–706. [doi:10.1017/S1816383112000197](https://doi.org/10.1017/S1816383112000197)
- Chander, P. and Tulkens, H. (1997) 'The core of an economy with multilateral environmental externalities', *International Journal of Game Theory*, 26(3), pp. 379–401. [doi:10.1007/BF01263279](https://doi.org/10.1007/BF01263279)
- Chwe, M.S.-Y. (1994) 'Farsighted coalitional stability', *Journal of Economic Theory*, 63(2), pp. 299–325. [doi:10.1006/jeth.1994.1044](https://doi.org/10.1006/jeth.1994.1044)
- Dima, S., Fischer, S., Heitzig, J. and Oliver, J. (2025) 'Non-maximizing policies that fulfill multi-criterion aspirations in expectation', in Freeman, R. and Mattei, N. (eds) *Algorithmic Decision Theory. ADT 2024*. Lecture Notes in Computer Science, vol. 15248. Cham: Springer, pp. 113–127. [doi:10.1007/978-3-031-73903-3\_8](https://doi.org/10.1007/978-3-031-73903-3_8)
- Donges, J.F., Heitzig, J., Barfuss, W., Wiedermann, M., Kassel, J.A., Kittel, T., Kolb, J.J., Kolster, T., Müller-Hansen, F., Otto, I.M., Zimmerer, K.B. and Lucht, W. (2020) 'Earth system modeling with endogenous and dynamic human societies: the copan:CORE open World–Earth modeling framework', *Earth System Dynamics*, 11(2), pp. 395–413. [doi:10.5194/esd-11-395-2020](https://doi.org/10.5194/esd-11-395-2020)
- Dür, A., Baccini, L. and Elsig, M. (2014) 'The design of international trade agreements: introducing a new dataset', *Review of International Organizations*, 9(3), pp. 353–375. [doi:10.1007/s11558-013-9179-8](https://doi.org/10.1007/s11558-013-9179-8)
- Felbermayr, G., Kirilakha, A., Syropoulos, C., Yalcin, E. and Yotov, Y.V. (2020) 'The global sanctions data base', *European Economic Review*, 129, 103561. [doi:10.1016/j.euroecorev.2020.103561](https://doi.org/10.1016/j.euroecorev.2020.103561)
- Gerber, A. and Wichardt, P.C. (2009) 'Providing public goods in the absence of strong institutions', *Journal of Public Economics*, 93(3–4), pp. 429–439. [doi:10.1016/j.jpubeco.2008.10.006](https://doi.org/10.1016/j.jpubeco.2008.10.006)
- Gilboa, I., Samuelson, L. and Schmeidler, D. (2014) 'No-betting-Pareto dominance', *Econometrica*, 82(4), pp. 1405–1442. [doi:10.3982/ECTA11281](https://doi.org/10.3982/ECTA11281)
- Gleditsch, N.P., Wallensteen, P., Eriksson, M., Sollenberg, M. and Strand, H. (2002) 'Armed conflict 1946–2001: a new dataset', *Journal of Peace Research*, 39(5), pp. 615–637. [doi:10.1177/0022343302039005007](https://doi.org/10.1177/0022343302039005007)
- Granovetter, M. (1978) 'Threshold models of collective behavior', *American Journal of Sociology*, 83(6), pp. 1420–1443. [doi:10.1086/226707](https://doi.org/10.1086/226707)
- Grieco, J.M. (1988) 'Anarchy and the limits of cooperation: a realist critique of the newest liberal institutionalism', *International Organization*, 42(3), pp. 485–507. [doi:10.1017/S0020818300027715](https://doi.org/10.1017/S0020818300027715)
- Harstad, B. (2012) 'Climate contracts: a game of emissions, investments, negotiations, and renegotiations', *Review of Economic Studies*, 79(4), pp. 1527–1557. [doi:10.1093/restud/rds011](https://doi.org/10.1093/restud/rds011)
- Heitzig, J. (2025) 'Provision of public goods via unilateral but mutually conditional commitments—mechanism, equilibria, and learning', *Games*, 16(6), 58. [doi:10.3390/g16060058](https://doi.org/10.3390/g16060058)
- Heitzig, J. (2026a) 'Does the grand coalition form? Persistence, arrival, and the role of the sharing rule in a dynamic process of nested binding agreements'. arXiv preprint. [arXiv:2608.17766](https://arxiv.org/abs/2608.17766)
- Heitzig, J. (2026b) 'Unbiased canonical set-valued oracles via lattice theory'. arXiv preprint. [arXiv:2606.26418](https://arxiv.org/abs/2606.26418)
- Heitzig, J., Barfuss, W. and Donges, J.F. (2018) 'A thought experiment on sustainable management of the Earth system', *Sustainability*, 10(6), 1947. [doi:10.3390/su10061947](https://doi.org/10.3390/su10061947)
- Heitzig, J. and Hiller, S. (2020) 'Degrees of individual and groupwise backward and forward responsibility in extensive-form games with ambiguity, and their application to social choice problems'. arXiv preprint. [arXiv:2007.07352](https://arxiv.org/abs/2007.07352)
- Heitzig, J., Kittel, T., Donges, J.F. and Molkenthin, N. (2016) 'Topology of sustainable management of dynamical systems with desirable states: from defining planetary boundaries to safe operating spaces in the Earth system', *Earth System Dynamics*, 7(1), pp. 21–50. [doi:10.5194/esd-7-21-2016](https://doi.org/10.5194/esd-7-21-2016)
- Heitzig, J. and Kornek, U. (2018) 'Bottom-up linking of carbon markets under far-sighted cap coordination and reversibility', *Nature Climate Change*, 8(3), pp. 204–209. [doi:10.1038/s41558-018-0079-z](https://doi.org/10.1038/s41558-018-0079-z)
- Heitzig, J., Lessmann, K. and Zou, Y. (2011) 'Self-enforcing strategies to deter free-riding in the climate change mitigation game and other repeated public good games', *Proceedings of the National Academy of Sciences*, 108(38), pp. 15739–15744. [doi:10.1073/pnas.1106265108](https://doi.org/10.1073/pnas.1106265108)
- Heitzig, J., Oechssler, J., Pröschel, C., Ragavan, N. and Lo, Y.L. (2023) 'Improving international climate policy via mutually conditional binding commitments'. arXiv preprint. [arXiv:2307.14267](https://arxiv.org/abs/2307.14267)
- Heitzig, J., Simmons, F.W. and Constantino, S.M. (2025) 'Fair group decisions via non-deterministic proportional consensus', *Social Choice and Welfare*, 64, pp. 345–371. [doi:10.1007/s00355-024-01524-3](https://doi.org/10.1007/s00355-024-01524-3)
- Henisz, W.J. (2002) 'The institutional environment for infrastructure investment', *Industrial and Corporate Change*, 11(2), pp. 355–389. [doi:10.1093/icc/11.2.355](https://doi.org/10.1093/icc/11.2.355)
- Jackson, M.O. and Wilkie, S. (2005) 'Endogenous games and mechanisms: side payments among players', *Review of Economic Studies*, 72(2), pp. 543–566. [doi:10.1111/j.1467-937X.2005.00342.x](https://doi.org/10.1111/j.1467-937X.2005.00342.x)
- Kahneman, D. and Tversky, A. (1979) 'Prospect theory: an analysis of decision under risk', *Econometrica*, 47(2), pp. 263–291. [doi:10.2307/1914185](https://doi.org/10.2307/1914185)
- Kalai, A.T., Kalai, E., Lehrer, E. and Samet, D. (2010) 'A commitment folk theorem', *Games and Economic Behavior*, 69(1), pp. 127–137. [doi:10.1016/j.geb.2009.09.008](https://doi.org/10.1016/j.geb.2009.09.008)
- Konishi, H. and Ray, D. (2003) 'Coalition formation as a dynamic process', *Journal of Economic Theory*, 110(1), pp. 1–41. [doi:10.1016/S0022-0531(03)00004-8](https://doi.org/10.1016/S0022-0531%2803%2900004-8)
- Kulveit, J., Douglas, R., Ammann, N., Turan, D., Krueger, D. and Duvenaud, D. (2025) 'Gradual disempowerment: systemic existential risks from incremental AI development'. arXiv preprint. [arXiv:2501.16946](https://arxiv.org/abs/2501.16946)
- Lawrence, M., Homer-Dixon, T., Janzwood, S., Rockström, J., Renn, O. and Donges, J.F. (2024) 'Global polycrisis: the causal mechanisms of crisis entanglement', *Global Sustainability*, 7, e6. [doi:10.1017/sus.2024.1](https://doi.org/10.1017/sus.2024.1)
- Leeds, B.A., Ritter, J.M., Mitchell, S.M. and Long, A.G. (2002) 'Alliance Treaty Obligations and Provisions, 1815–1944', *International Interactions*, 28(3), pp. 237–260. [doi:10.1080/03050620213653](https://doi.org/10.1080/03050620213653)
- Li, S. (2017) 'Obviously strategy-proof mechanisms', *American Economic Review*, 107(11), pp. 3257–3287. [doi:10.1257/aer.20160425](https://doi.org/10.1257/aer.20160425)
- Maggi, G. (2016) 'Issue linkage', in Bagwell, K. and Staiger, R.W. (eds) *Handbook of Commercial Policy*, vol. 1B. Amsterdam: North-Holland, pp. 513–564. [doi:10.1016/bs.hescop.2016.04.017](https://doi.org/10.1016/bs.hescop.2016.04.017)
- McKelvey, R.D. and Palfrey, T.R. (1995) 'Quantal response equilibria for normal form games', *Games and Economic Behavior*, 10(1), pp. 6–38. [doi:10.1006/game.1995.1023](https://doi.org/10.1006/game.1995.1023)
- Mitchell, R.B., Andonova, L.B., Axelrod, M., Balsiger, J., Bernauer, T., Green, J.F., Hollway, J., Kim, R.E. and Morin, J.-F. (2020) 'What we know (and could know) about international environmental agreements', *Global Environmental Politics*, 20(1), pp. 103–121. [doi:10.1162/glep_a_00544](https://doi.org/10.1162/glep_a_00544)
- Monderer, D. and Tennenholtz, M. (2009) 'Strong mediated equilibrium', *Artificial Intelligence*, 173(1), pp. 180–195. [doi:10.1016/j.artint.2008.10.005](https://doi.org/10.1016/j.artint.2008.10.005)
- Myerson, R.B. (1977) 'Graphs and cooperation in games', *Mathematics of Operations Research*, 2(3), pp. 225–229. [doi:10.1287/moor.2.3.225](https://doi.org/10.1287/moor.2.3.225)
- Myerson, R.B. and Satterthwaite, M.A. (1983) 'Efficient mechanisms for bilateral trading', *Journal of Economic Theory*, 29(2), pp. 265–281. [doi:10.1016/0022-0531(83)90048-0](https://doi.org/10.1016/0022-0531%2883%2990048-0)
- Nash, J.F. (1950) 'The bargaining problem', *Econometrica*, 18(2), pp. 155–162. [doi:10.2307/1907266](https://doi.org/10.2307/1907266)
- Nash, J. (1953) 'Two-person cooperative games', *Econometrica*, 21(1), pp. 128–140. [doi:10.2307/1906951](https://doi.org/10.2307/1906951)
- Nordhaus, W. (2015) 'Climate clubs: overcoming free-riding in international climate policy', *American Economic Review*, 105(4), pp. 1339–1370. [doi:10.1257/aer.15000001](https://doi.org/10.1257/aer.15000001)
- Oechssler, J., Reischmann, A. and Sofianos, A. (2022) 'The conditional contribution mechanism for repeated public goods – the general case', *Journal of Economic Theory*, 203, 105488. [doi:10.1016/j.jet.2022.105488](https://doi.org/10.1016/j.jet.2022.105488)
- Oesterheld, C. and Conitzer, V. (2022) 'Safe Pareto improvements for delegated game playing', *Autonomous Agents and Multi-Agent Systems*, 36(2), 46. [doi:10.1007/s10458-022-09574-6](https://doi.org/10.1007/s10458-022-09574-6)
- Palmer, G., McManus, R.W., D'Orazio, V., Kenwick, M.R., Karstens, M., Bloch, C., Dietrich, N., Kahn, K., Ritter, K. and Soules, M.J. (2022) 'The MID5 dataset, 2011–2014: procedures, coding rules, and description', *Conflict Management and Peace Science*, 39(4), pp. 470–482. [doi:10.1177/0738894221995743](https://doi.org/10.1177/0738894221995743)
- Pauw, W.P., Castro, P., Pickering, J. and Bhasin, S. (2020) 'Conditional nationally determined contributions in the Paris Agreement: foothold for equity or Achilles heel?', *Climate Policy*, 20(4), pp. 468–484. [doi:10.1080/14693062.2019.1635874](https://doi.org/10.1080/14693062.2019.1635874)
- Pevehouse, J.C.W., Nordstrom, T., McManus, R.W. and Jamison, A.S. (2020) 'Tracking organizations in the world: the Correlates of War IGO Version 3.0 datasets', *Journal of Peace Research*, 57(3), pp. 492–503. [doi:10.1177/0022343319881175](https://doi.org/10.1177/0022343319881175)
- Putnam, R.D. (1988) 'Diplomacy and domestic politics: the logic of two-level games', *International Organization*, 42(3), pp. 427–460. [doi:10.1017/S0020818300027697](https://doi.org/10.1017/S0020818300027697)
- Raiffa, H. (1982) *The Art and Science of Negotiation*. Cambridge, MA: Belknap Press of Harvard University Press. ISBN 978-0-674-04813-3. No DOI.
- Ray, D. and Vohra, R. (2015) 'The farsighted stable set', *Econometrica*, 83(3), pp. 977–1011. [doi:10.3982/ECTA12022](https://doi.org/10.3982/ECTA12022)
- Reischmann, A. and Oechssler, J. (2018) 'The binary conditional contribution mechanism for public good provision in dynamic settings — theory and experimental evidence', *Journal of Public Economics*, 159, pp. 104–115. [doi:10.1016/j.jpubeco.2018.02.009](https://doi.org/10.1016/j.jpubeco.2018.02.009)
- Rengert, M., Heitzig, J. and Asano, Y. (2026) 'Cooperation is not competence – conditional commitments in LLM public-good games'. Poster, Trustworthy AI for Good (AI4GOOD) Workshop at NeurIPS 2026. No DOI. [neurips.cc/virtual/2026/165274](https://neurips.cc/virtual/2026/165274)
- Sebenius, J.K. (1983) 'Negotiation arithmetic: adding and subtracting issues and parties', *International Organization*, 37(2), pp. 281–316. [doi:10.1017/S002081830003438X](https://doi.org/10.1017/S002081830003438X)
- Simon, H.A. (1955) 'A behavioral model of rational choice', *Quarterly Journal of Economics*, 69(1), pp. 99–118. [doi:10.2307/1884852](https://doi.org/10.2307/1884852)
- Tennenholtz, M. (2004) 'Program equilibrium', *Games and Economic Behavior*, 49(2), pp. 363–373. [doi:10.1016/j.geb.2004.02.002](https://doi.org/10.1016/j.geb.2004.02.002)
- Tessler, M.H., Bakker, M.A., Jarrett, D., Sheahan, H., Chadwick, M.J., Koster, R., Evans, G., Campbell-Gillingham, L., Collins, T., Parkes, D.C., Botvinick, M. and Summerfield, C. (2024) 'AI can help humans find common ground in democratic deliberation', *Science*, 386(6719), eadq2852. [doi:10.1126/science.adq2852](https://doi.org/10.1126/science.adq2852)
- Thomson, R., Stokman, F.N., Achen, C.H. and König, T. (eds) (2006) *The European Union Decides*. Cambridge: Cambridge University Press. [doi:10.1017/CBO9780511492082](https://doi.org/10.1017/CBO9780511492082)
- Zhang, T., Williams, A., Phade, S., Srinivasa, S., Zhang, Y., Gupta, P., Bengio, Y. and Zheng, S. (2022) 'AI for global climate cooperation: modeling global climate negotiations, agreements, and long-term cooperation in RICE-N'. arXiv preprint. [arXiv:2208.07004](https://arxiv.org/abs/2208.07004)

**Other sources.**

- Department for Science, Innovation and Technology (2024) *Frontier AI Safety Commitments, AI Seoul Summit 2024*. London: UK Government. [gov.uk](https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024)
- United Nations General Assembly (2024) *The Pact for the Future*. Resolution A/RES/79/1, adopted 22 September 2024. [digitallibrary.un.org/record/4061879](https://digitallibrary.un.org/record/4061879)
