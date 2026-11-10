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
