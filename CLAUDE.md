# Polycrisis package deal

Research-and-design programme led by Jobst Heitzig: design a self-enforcing package deal for the
global polycrisis. The deal is a public registry of unilateral but mutually conditional commitments
(CCF mechanism; Heitzig, 2025, https://doi.org/10.3390/g16060058). A recommender proposes focal
packages with stability certificates. The team is one AI working in sessions. Jobst sets direction,
signs off each gate, and is the only channel to the outside world.

## Read first

1. `STATUS.md`: what was done last and what is open. Add an entry at the end of every session.
2. `docs/plan.md`: the work plan with ten work packages (WP1 to WP10), phases, gates, objections and references.
3. `docs/phase0_results.md`: write-up of the first increment of Phase 0.
4. `README.md`: files, conventions, how to reproduce.

## State on 10 November 2026

- Phase 0 is a toy instance with 8 actors, 3 issues and 12 levers, small enough for full enumeration.
  Its first increment ran all ten work packages once, in minimal form. Code is in `phase0/`,
  results in `phase0/results/`.
- Gate 1 (heuristic search matches enumeration): the criterion is met. Stress tests were added
  afterwards and pass after one repair of the blocking oracle. Jobst has not signed off yet.
- Nobody has checked this increment except the session that wrote it.
- Every number except the emission shares is illustrative. No result says anything about real actors.

## Next steps, in proposed order (Jobst decides)

0. Audit the first increment as an independent reviewer. Suggested: write your own strict-core and
   equilibrium checker from the definitions in `docs/plan.md` before reading `phase0/core.py`,
   run `sh run_all.sh`, compare, and report discrepancies before changing anything.
1. A second instance with an empty core or a contested lever, to exercise the fallbacks.
2. A third instance in which one issue has no deal of its own, to test linkage as a necessity.
3. Budgets and index weights in the robustness set.
4. The far-sighted formation path and absorbing states (WP8), and internal-and-external stability (WP6).
5. MaxParC over the menu, and a model-agent pilot (WP10).
6. Beliefs in the effect model, so that the no-betting test has something to test.
7. An independent checker for the certificates, published with them.

Also open: the case distinction behind the equilibrium certificate (`docs/phase0_results.md`,
section "Core, menu and certificates") is a prose argument, checked by enumeration only. WP8 asks
for mechanism-level statements to be machine-checked in a proof assistant.

## Rules of work

- External actions need Jobst's instruction: no publishing, posting, messaging, contact with actors,
  new repositories or scheduled runs unasked. Commit and push as Jobst directs.
- Tag claims: [proved] is a theorem in a cited paper, [model] holds in our model, [open] is
  unresolved, [assumption] is a planning choice. Do not claim what the files do not support.
- Fix pass marks before running a test, and write them into the code. A test or selection rule
  added after seeing results is labelled post hoc, in the code and in the write-up. Never edit a
  criterion that was fixed earlier, such as the Gate 1 criterion in `phase0/run_phase0.py`.
- Check by full enumeration wherever the instance allows. Certify equilibrium directly where the
  orientation test fails. Keep an enumerable instance in the test suite at every scale-up.
- Every number in a write-up gets an assertion in `phase0/check_writeup.py`. Before reporting, run
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

`docs/plan.md` and `docs/phase0_results.md` were exported from it on 10 November 2026. In this
repository the Markdown files are the working copies. If a session cannot edit the Claude Doc,
list in `STATUS.md` what changed, so that the doc can be brought up to date.
