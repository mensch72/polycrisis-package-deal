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

    sh run_all.sh        # deletes phase0/results and recomputes everything, about 15 minutes on two cores

Needs Python 3 with numpy (tested with Python 3.13, numpy 2.5). All random seeds are fixed.
The last step, `check_writeup.py`, fails loudly if any number quoted in the write-up no longer matches.

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
