# Status log

Newest entry last. Every session ends with an entry: what ran, what failed, what changed, what is open.

## 10 November 2026, session 1 (Claude, chat session)

- Work plan written, then revised for a one-AI team (`docs/plan.md`).
- Phase 0, first increment: a toy instance with 8 actors and 3 issues ran through all ten work
  packages. It has 326 core profiles, a certified menu of five, and a lead candidate that keeps all
  properties in 143 of 150 parameter draws (`docs/phase0_results.md`).
- Gate 1: the criterion is met in 8 of 8 runs. Stress tests were added afterwards. The first
  blocking oracle failed them (191 of 300 known blocks found), and the repaired one passes
  (294 of 300, and 300 of 300 on a hold-out sample). Jobst's sign-off is pending.
- Changed after seeing results: the stress tests, and the choice of the lead by robustness instead
  of the Nash product.
- Checked: a run from scratch reproduced every result file, and `phase0/check_writeup.py` passes
  with 82 assertions. Not checked by anyone other than the session that wrote it.
- Not yet done in Phase 0: instances with an empty core, with a contested lever, and with an issue
  that has no deal of its own; budgets in the robustness set; far-sighted formation; MaxParC over
  the menu; an independent checker; a fresh-session audit.
- Open decisions for Jobst: Gate 1 sign-off; whether further increments run as scheduled sessions.
- Handover: this repository was assembled at the end of the session so that work can continue in
  Claude Code. The proposed first task is the audit, step 0 in `CLAUDE.md`.

## 10 November 2026, session 2 (Claude, Claude Code session)

- The zip from session 1 was imported unmodified into this repository, on branch
  `claude/something-from-d7fvox`. The repository was empty before.
- Step 0, audit of the first increment: done, report in `audit/AUDIT.md`. Nothing in `phase0/` or
  `docs/` was changed.
- Ran: `run_all.sh` from a clean copy, and an independent checker written before reading `core.py`
  (`audit/`: own model in exact arithmetic, own strict core, own registry rule).
- Outcome: every result file reproduced, apart from run times. The checker agrees on all core,
  equilibrium, robustness and linkage numbers. The emission shares match the EDGAR page.
- Failed or weak: nothing failed. Seven findings on method and wording are listed in the report.
  The largest: on 500 fresh draws the deepest candidate stays in the strict core in 46.6 % of
  draws, against 33 % reported from 150. The lead holds at 96.4 %.
- Added post hoc by the audit: the fresh-draw test.
- Not audited: the learning rule and the compensation formula against the papers, the references,
  and the Markdown exports against the Claude Doc.
- Claude Doc: not edited. It still says that no repository exists.
- Open decisions for Jobst: Gate 1 sign-off; the four proposals at the end of `audit/AUDIT.md`;
  whether further increments run as scheduled sessions.
- Later in the same session, on Jobst's instruction to start working: step 1 of the open list.
  - New: `phase0/instance2.py` (3 actors, contested access levers, empty core), `phase0/fallbacks.py`,
    `phase0/run_instance2.py`, `phase0/run_contested.py`, `phase0/check_writeup2.py`,
    `docs/phase0_instance2.md`. `run_all.sh` now runs them too. `README.md` and `CLAUDE.md` updated.
  - Pass marks E1 to E3 and G1c were committed before the first run of each runner. All four passed.
  - Weak or failed: in the contested variant the search meets the Gate 1 criterion, but the profile it
    returns is not an equilibrium; only 150 of 399 core profiles are. The margin fallback returns a
    Pareto-dominated profile. The issue-set fallback gives a deal with margin 0.479 in the package game,
    against 0.165 for the margin fallback. No empty core was found on the eight-actor lattice.
  - Changed after seeing results, and labelled post hoc: the margin fallback restricted to efficient
    candidates, and the count of core profiles that are equilibria.
  - Not done: robustness set for the second instance, heuristic for the smallest margin, far-sighted
    fallback. The audit proposals were not acted on.
  - Claude Doc: not edited. It lacks the audit, the second instance and the repository.
  - Open decisions for Jobst, added: the two at the end of `docs/phase0_instance2.md`.
- Later again, on Jobst's request for bounded rationality and diplomatic knowledge:
  - `docs/plan.md` gained the section "Bounded rationality and diplomatic knowledge" (design rules,
    where diplomatic knowledge enters, a table of data sources, method, status), one row in
    "Objections and risks", and thirteen references. All thirteen DOIs were checked against Crossref
    today. The Claude Doc does not have these changes.
  - `phase0/run_instance2.py` gained an exploration without pass mark: stability of the second
    instance by group size, by inertia threshold, and with the USA–CHN channel removed. The write-up
    has a section on it, with assertions.
  - A first reading of that result was wrong and the text assertion caught it: the profile with the
    smallest margin under the channel restriction is not the margin fallback but one that favours EU.
  - Not built: the safe-filing check, quantal response, loss aversion, error rates. No dataset was
    downloaded.
  - `run_all.sh` was rerun from a clean state after the last code change.
- Last part of the session, on Jobst's three remarks:
  - Pushing: `CLAUDE.md` now has the rule to commit and push after every unit and before long runs.
  - Towers in a pre-CPEP: `phase0/tower.py`, `run_tower.py`, `run_tower_relaxed.py`, `check_towers.py`,
    `docs/phase0_towers.md`. Tests T1 to T4 were pushed before the first run and passed. Under condition
    (ii): no tower in the triangle; in the contested variant none with aspirations, and without them a
    tower whose last stage adds nothing and which leaves DEV below no deal. In the original game 4 of
    255 groups can still gain, by at most 0.017. Under the relaxed (ii′), which is Claude's proposal and
    post hoc: 169 acceptable towers, and the selected one is a strictly strong equilibrium.
  - Weak: only chains of two coalitions and step filings. The selected towers have trivial last stages.
    Three readings of the definition await Jobst's confirmation.
  - Plan: "Strategy and roadmap" replaces "Sequencing and gates" (horizons, candidate pilots, who does
    what, milestones M0 to M6 with venues, decisions). "Beyond CPEPs: towers" added to the framing. The
    reading of the task, item 3 of the WP3 method and three risk rows changed. Gates 2 and 3 are
    restated, because their earlier wording was in a diagram the export omitted. The Claude Doc has
    none of this.
  - `run_all.sh` includes the tower runners and was rerun from a clean state.
