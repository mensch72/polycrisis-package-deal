# Polycrisis package deal

Work plan, code and results for designing a self-enforcing package deal for the global polycrisis,
built on unilateral but mutually conditional commitments. Started on 10 November 2026 by Claude for
Jobst Heitzig. Not yet reviewed by a second person.

## Layout

| Path | Content |
| --- | --- |
| `CLAUDE.md` | briefing for a new session: state, next steps, rules of work, writing conventions |
| `STATUS.md` | status log, one entry per session |
| `docs/plan.md` | the work plan: ten work packages, phases, gates, objections, references |
| `docs/phase0_results.md` | write-up of the first increment of Phase 0 |
| `docs/phase0_instance2.md` | write-up of the second instance and the contested variant (step 1) |
| `docs/phase0_towers.md` | towers in a pre-CPEP: definitions as implemented, tests, assessment |
| `docs/pilot_A_country_platform.md`, `docs/pilot_B_frontier_ai.md` | design notes of the two pilot tracks |
| `docs/outreach_proposal.md` | whom to involve first, with what, on which channel; nothing sent |
| `pilots/` | pilot skeleton instances, generic runner, results, assertion script |
| `data/sources/` | sourced fact files for the pilots, with URLs and quotes, collected 10 November 2026 |
| `outreach/` | two-page briefs and email drafts for Jobst to edit and send |
| `audit/` | independent audit of the first increment: report, checker, outputs |
| `phase0/` | code and results of the Phase 0 toy instance |
| `run_all.sh` | recomputes every Phase 0 result from a clean state |
| `log_*.txt` | console output of the last full run |

## Phase 0 toy instance

A toy instance with 8 actors, 3 issues and 12 levers (1,990,656 action profiles, 255 coalitions),
small enough for full enumeration. It exercises the plan's pipeline once: orientation test,
sufficient groups, acceptable region, strict core, a menu of five core profiles with certificates,
heuristic search against enumeration (Gate 1), linkage value, robustness set, generated filings
and briefs, an updating process, and a compliance probe.

Only the emission shares are sourced (EDGAR, GHG emissions of all world countries, 2026 report,
year 2025, excluding LULUCF; https://edgar.jrc.ec.europa.eu/report_2026). Every other number is
illustrative and was chosen so that each issue is a social dilemma and every lever passes the
orientation test at the base point. No conclusion about real actors follows from the results.

## Reproduce

    sh run_all.sh        # deletes phase0/results and results2, recomputes everything, about 20 minutes on two cores

Needs Python 3 with numpy (tested with Python 3.13, numpy 2.5). All random seeds are fixed.
`check_writeup.py` and `check_writeup2.py` fail loudly if a number quoted in a write-up no longer matches.
`check_writeup2.py` also checks that each number stands in the text; `check_writeup.py` does not yet.

## Files in `phase0/`

| File | Content |
| --- | --- |
| `instance.py` | actors, levers, parameters with provenance, effect model, utilities, aspirations |
| `core.py` | exact checks by enumeration: orientation test, strict core, blocking margins, sufficient groups, over-fulfilment |
| `mechanism.py` | registry rule (largest mutually feasible profile) and step-function CCFs |
| `search.py` | heuristic search by constraint generation; two versions of the blocking oracle |
| `run_phase0.py` | main pipeline; states the Gate 1 criterion fixed before the first run |
| `gate1_stress.py` | stress tests of the search on the variant without aspiration filter |
| `dynamics.py` | learning rule on ladders, with and without aspiration caps; linear-compensation probe |
| `extras.py` | supporting numbers quoted in the write-up (failing aspirations, core composition, single-issue cores) |
| `check_writeup.py` | asserts every number quoted in `docs/phase0_results.md` against the result files |
| `results/results.json` | all numbers of the main pipeline |
| `results/gate1_stress.json` | stress-test numbers |
| `results/dynamics.json` | learning and compliance numbers |
| `results/extras.json` | supporting numbers |
| `results/params.json` | parameter file with provenance |
| `results/menu.md` | the menu of core profiles |
| `results/filings.md`, `results/briefs.md` | generated filings and briefs for the lead candidate |
| `results/core_acceptable.json` | flat indices of the core profiles inside the acceptable region |
| `instance2.py` | second instance: 3 actors, 2 issues, 9 levers, contested access levers, empty core |
| `fallbacks.py` | smallest blocking margin, strict blockers, cores of sub-packages; exact, for any lever grid |
| `run_instance2.py` | second instance through core, both fallbacks, registry rule and search; tests E1 to E3 |
| `run_contested.py` | first instance with a compliance burden on developers; search test G1c |
| `check_writeup2.py` | asserts every number quoted in `docs/phase0_instance2.md`, against files and text |
| `tower.py` | towers of coalitions and filings in a pre-CPEP: stage games, nested step filings, registry rule |
| `run_tower.py` | builds and tests a tower under Jobst's condition (ii); argument `contested` or `instance2` |
| `run_tower_relaxed.py` | the same under the relaxed condition (ii′), on the contested variant |
| `check_towers.py` | asserts every number quoted in `docs/phase0_towers.md`, against files and text |
| `results2/tower_*.json` | results of the tower runners |
| `results2/results.json`, `results2/contested.json`, `results2/params.json` | results of the two runners |

## Second instance and contested variant

The second instance has three actors who can grant each other preferential access. Each grant harms
the third, so the access levers are contested and the core is empty. The contested variant adds a
compliance burden on developers to the first instance. `mechanism.py` and `search.py` read their
instance from the module name `instance`; `run_instance2.py` puts `instance2` under that name.

## Conventions

- A profile is a vector of 12 lever levels; level 0 is "current policies continue" (the no-deal reference).
- Utilities are in each actor's own units. Gains are normalised per actor by that actor's largest
  gain among individually rational, acceptable profiles. Nothing is compared across actors.
- Aspirations filter the candidate profiles. Blocking profiles are not filtered (conservative).
- Strict core: no coalition G has a profile with non-members at level 0 that all members weakly
  prefer and one strictly prefers.

## Known limits

- The instance was built to pass the orientation test at the base point; it fails somewhere on the
  lattice in a large share of the perturbed parameter draws (see `results/results.json`, robustness).
- The heuristic search reads utilities from a table precomputed for all profiles. The count of
  profiles it looks up says nothing about run time on an instance where no such table exists.
- The learning rule and the linear-compensation probe are tests outside the cases covered by the
  theorems in Heitzig (2025, https://doi.org/10.3390/g16060058) and Heitzig, Lessmann and Zou (2011,
  https://doi.org/10.1073/pnas.1106265108).
