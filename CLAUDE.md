# Polycrisis package deal

Research-and-design programme led by Jobst Heitzig: design a self-enforcing package deal for the
global polycrisis. The deal is a public registry of unilateral but mutually conditional commitments
(CCF mechanism; Heitzig, 2025, https://doi.org/10.3390/g16060058). A recommender proposes focal
packages with stability certificates. The team is one AI working in sessions. Jobst sets direction,
signs off each gate, and is the only channel to the outside world.

## Read first

1. `STATUS.md`: what was done last and what is open. Add an entry at the end of every session.
2. `docs/plan.md`: the work plan with ten work packages (WP1 to WP10), phases, gates, objections and references.
3. `docs/phase0_results.md`, `docs/phase0_instance2.md` and `docs/phase0_towers.md`: write-ups of Phase 0 so far.
   `docs/pilot_A_country_platform.md`, `docs/pilot_B_frontier_ai.md`, `docs/outreach_proposal.md`: the pilots.
   `audit/AUDIT.md`: audit of the first increment.
4. `README.md`: files, conventions, how to reproduce.

## State on 10 November 2026, after session 2

- Aim, as revised by Jobst: real-world use. The realistic outcome is one small pilot registry with real
  filings, reached through milestones M0 to M6 in `docs/plan.md`, section "Strategy and roadmap". That
  section also says what Claude does alone, what needs Jobst, and when other people come in.
- Phase 0, first instance: 8 actors, 3 issues and 12 levers. Write-up `docs/phase0_results.md`. Audited
  by a fresh session (`audit/AUDIT.md`): no number was wrong; seven findings await Jobst's decision.
- Gate 1: the criterion is met, and so are the stress tests after one repair of the blocking oracle.
  Jobst has not signed off yet.
- Step 1 (`docs/phase0_instance2.md`): a second instance with contested levers and an empty core, and a
  contested variant of the first. Both fallbacks have a defect. With a contested lever, a strict-core
  profile need not be an equilibrium.
- Towers in a pre-CPEP, Jobst's proposal (`docs/phase0_towers.md`): implemented and tested for chains
  of two coalitions with step filings. Under his condition (ii) no acceptable tower exists on the toys.
  Under the relaxed (ii′) the selected tower is a strictly strong equilibrium of the original game.
  Jobst adopted (ii′) and confirmed the three readings listed in that file. Still open: whether every
  stage must be individually rational against a⁰ for all actors.
- Pilot tracks (`docs/pilot_A_country_platform.md`, `docs/pilot_B_frontier_ai.md`): developed to the
  point where outside knowledge is needed. Each has a sourced fact file in `data/sources/`, a skeleton
  instance in `pilots/` with illustrative preferences, and a two-page brief in `outreach/`.
  Track B has two variants: B1 among developers, and B2 among states, shaped on the "hardwired pause"
  report of Fithian, Holliday et al. (`docs/note_hardwired_pause.md`). Jobst made B2 the lead variant on
  11 November 2026; Wesley Holliday, whom he knows well, is the first contact.
  `docs/outreach_proposal.md` proposes whom Jobst should ask first. Nothing has been sent. Claude is
  built by Anthropic, a party to track B; that is disclosed in the track's documents.
- The plan section "Bounded rationality and diplomatic knowledge" exists; only a first exploration is
  in code. The datasets it names have not been downloaded.
- Nobody has checked step 1 or the tower work except the session that wrote them.
- Every number except the emission shares is illustrative. No result says anything about real actors.

## Next steps (Jobst decides; the order is that of the plan's roadmap)

0. Jobst's open decisions: the three in `docs/outreach_proposal.md`; Gate 1; individual rationality against a⁰ at every tower stage; when the repository
   becomes public; the audit proposals; the two decisions in `docs/phase0_instance2.md`.
1. A fresh-session audit of step 1 and of the tower code.
2. Towers with longer chains, a search over chains, and a look-ahead selection rule.
3. The search oracle extended to over-fulfilment, and a heuristic for the smallest margin.
4. A scaling test of search and certificates on synthetic instances with 20 to 40 actors (start of M2).
5. A first draft of the theory note on pre-CPEPs and towers (M1), marked as draft.
6. Pilots: fill the gaps listed in the fact files (per-donor data for Indonesia and Viet Nam, statute
   texts); correct the skeletons once outside answers arrive. No contact by Claude.
7. Still open from the first list: an instance in which one issue has no deal of its own; budgets in the
   robustness set; far-sighted formation; MaxParC and a model-agent pilot; beliefs for the no-betting
   test; the stability table and safe-filing check of the bounded-rationality section.

Also open: the case distinction behind the equilibrium certificate (`docs/phase0_results.md`,
section "Core, menu and certificates") is a prose argument, checked by enumeration only. WP8 asks
for mechanism-level statements to be machine-checked in a proof assistant.

## Rules of work

- Commit and push to the working branch after every completed unit of work, and before any long run.
  A session can end without warning at a spending limit; nothing may be left unpushed.
- External actions need Jobst's instruction: no publishing, posting, messaging, contact with actors,
  new repositories or scheduled runs unasked.
- Tag claims: [proved] is a theorem in a cited paper, [model] holds in our model, [open] is
  unresolved, [assumption] is a planning choice. Do not claim what the files do not support.
- Fix pass marks before running a test, and write them into the code. A test or selection rule
  added after seeing results is labelled post hoc, in the code and in the write-up. Never edit a
  criterion that was fixed earlier, such as the Gate 1 criterion in `phase0/run_phase0.py`.
- Check by full enumeration wherever the instance allows. Certify equilibrium directly where the
  orientation test fails. Keep an enumerable instance in the test suite at every scale-up.
- Every number in a write-up gets an assertion in a `check_*.py` script, which from now on also checks
  that the number stands in the text. Before reporting, run
  `sh run_all.sh` from a clean state. Do not edit files in `phase0/results/` by hand.
- Every parameter carries provenance: sourced, with URL and retrieval date, or illustrative, with
  who set it. Never present invented data as sourced.
- Utilities are in each actor's own units and are never compared across actors. Aspirations filter
  candidate profiles and are not traded off against gains. Blocking profiles are not filtered.
- Report failures and weak tests as prominently as successes.
- If a URL Jobst gives cannot be fetched, stop and tell him instead of working around it.
- Follow Jobst's instructions literally and completely. State objections separately. Do not
  re-propose options he has rejected.

## Writing conventions

- Brief and to the point. Maths where it helps. No flattery. A little British humour, only a little.
- British spelling, as in the existing documents.
- In documents: the first sentence of a section states its point, sentences stay under about
  25 words, display formulas are LaTeX, inline maths is plain Unicode.
- Game theory: "response" and "best response", not "reply". Gender-neutral language.
- Do not use the words "honest", "honestly", "straightforward", "load-bearing", "race" or "racial".
- No "Dr." before names. Cite papers Harvard-style with a DOI link, or an arXiv link where no DOI
  exists. Verify every identifier before citing it.

## Where the plan lives

The plan and the Phase 0 write-up are also a Claude Doc:
https://claude.ai/artifact/JsCtfcFLRjq5FHe33x6biu

`docs/plan.md` and `docs/phase0_results.md` were exported from it on 10 November 2026.
`docs/phase0_instance2.md`, `docs/phase0_towers.md` and `audit/AUDIT.md` exist only in this repository. In this
repository the Markdown files are the working copies. If a session cannot edit the Claude Doc,
list in `STATUS.md` what changed, so that the doc can be brought up to date.
