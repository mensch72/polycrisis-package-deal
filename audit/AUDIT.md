# Audit of the Phase 0 first increment

10 November 2026, session 2 (Claude, fresh session). Step 0 of `CLAUDE.md`. Nothing in `phase0/` or
`docs/` was changed. This folder is new.

## Result in brief

No reported number is wrong. Seven findings concern method and wording, and one of them puts an
error bar on a reported share.

| Check | Outcome |
| --- | --- |
| Clean rerun of `run_all.sh` in a copy | every result file identical, apart from run times; 82 assertions pass |
| Independent model, exact arithmetic | utilities agree to 9 × 10⁻¹⁶, acceptability masks identical |
| Independent strict core | same 326 profiles; same counts 12,810 / 82,022 / 3,403 / 3,077 |
| Independent equilibrium test | no profitable group deviation at any of the 326 core profiles |
| Variant without aspiration filter | same 21,490 / 1,841 / 19,649, and the same core set |
| Robustness set, same 150 draws | same 143 of 150, six-way tie, nine at 90 %, mean 101.62, range 12 to 278 |
| Orientation test | passes at base; holds in 87 of 150 draws; same four owner-side counts |
| Linkage numbers | same 3 / 3 / 14, 126 / 56 / 33 / 11, same separate-deals profile and differences |
| Stability depth of the lead | same group and margin, −0.094 |
| Emission shares | all five match the EDGAR page, retrieved today |

## What was done

The checker was written from `docs/plan.md` and the model description in `docs/phase0_results.md`
before `core.py`, `mechanism.py`, `search.py` and `run_phase0.py` were read. It shares only the
parameter values and, for the robustness set, the sampling function with the original.

- `audit_core.py`: own model with utilities as exact integers (scaled by 12 × 10⁸), so no tolerance
  enters at the base point. Own strict-core test over all 255 coalitions. Own registry rule.
- `audit_robust.py`: orientation test, stability depth, single-issue cores, and the 150 draws.
- `audit_extra.py`: the lead under the registry rule, fresh draws, normaliser variants.
- `results/`: the three output files.

Run from this folder: `python3 -I audit_core.py ../phase0`, then the other two in the same way.
`audit_extra.py` takes the results folder of a rerun as an optional second argument.

**Equilibrium test.** For the five menu profiles, every joint deviation of every group to constant
filings was run through the registry rule by fixed-point iteration, 7.9 million deviations per
profile. None is profitable [model]. Constants suffice, by this argument. Let a deviation c′ of G
lead to the outcome a. Replace c′ by the constants a_G and let b be the new outcome. Then b ≥ a,
since a stays feasible. Also b_G = a_G ≤ c′_G(a₋G) ≤ c′_G(b₋G), since c′ is weakly increasing. So b
is feasible under c′, hence b ≤ a. The iteration also confirmed the closed form on which the
original certificate rests. For the other 321 core profiles the closed form was used.

## Findings

1. **Robustness shares carry sampling error, and one is off by more than that.** [post hoc test,
   added by this audit; no pass mark, an estimate] The lead was chosen as the best of 326 on the
   draws that then report its share. On 500 fresh draws the menu gives:

   | Candidate | Reported, 150 draws | Fresh, 500 draws | 95 % interval, fresh |
   | --- | --- | --- | --- |
   | Nash product | 60 % | 63.4 % | 59 to 68 % |
   | Leximin | 95 % | 96.4 % | 94 to 98 % |
   | Deepest | 33 % | 46.6 % | 42 to 51 % |
   | Most ambitious | 19 % | 19.0 % | 16 to 23 % |
   | Most robust (lead) | 95 % | 96.4 % | 94 to 98 % |

   The selection did not flatter the lead. The share for the deepest candidate did move, by about
   three standard errors. The write-up quotes all shares without intervals.

2. **`check_writeup.py` does not read the write-up.** It compares the result files with constants
   typed into the script. An edit to the text would pass unnoticed. Model parameters quoted in the
   text have no assertion at all: shares, index weights, budgets, the 0.15 and 0.25, the 0.10 of the
   contested variant. I compared them by reading, and they match. "Every number below is asserted"
   overstates this.

3. **"Fixed before the first run" cannot be verified.** The repository starts with one import
   commit. The order of criterion and result is on record only in docstrings. From here on, the
   commit history can carry it.

4. **Two rows of the stress table test less than they seem to.** The oracle returns a block only
   after verifying it. "No invalid blocks" and "no false alarms" therefore hold by construction.
   The three B2 runs with a cut are the three seeds for LIC, with one cut each. That is one case
   of constraint generation, not three. The write-up's own limit 2 points the same way.

5. **"Largest acceptable gain" means acceptable to all.** The normaliser is the largest gain among
   individually rational profiles inside C. The briefs say "your largest acceptable gain". With
   acceptability to the actor alone the scales are larger, for USA 1.31 against 1.06. The choice
   moves the leximin point, the smallest normalised gains and the margin of −0.094. It does not
   move the core or the Nash-product point.

6. **Stale or loose sentences.**
   - `docs/phase0_results.md` and the status log in `docs/plan.md` say that no repository exists.
   - The Gate 1 criterion in the code allows a gap of 0.01 in the log Nash product. The write-up
     says "reach the enumerated optimum". All eight runs hit it exactly, so nothing turns on it.
   - "By code separate from the enumeration": `in_strict_core` sits in the same file as
     `strict_core` and shares its helpers. The audit checker is now the separate code.

7. **Not audited.**
   - Whether `dynamics.py` implements the learning rule of Heitzig (2025, Theorem 3) as published.
     The publisher's page returned 403 to this session, and I did not look further.
   - The compensation formula against Heitzig, Lessmann and Zou (2011). I re-derived the
     first-order condition myself and it gives the same formula; that is not a check of the paper.
   - `search.py` and `dynamics.py` were read and rerun, not re-implemented.
   - The references in `docs/plan.md`, and the Markdown exports against the Claude Doc.

## Observations that are not discrepancies

- The leximin candidate is one of the six that tie at 143 of 150. The tie-break by Nash product
  picks the lead.
- Three core profiles tie on the ambition criterion.
- In no draw is a base-core profile in the strict core without being individually rational, so
  the owner-side orientation failures do not disturb the count.
- The strict core without the aspiration filter contains exactly 326 profiles acceptable to all.
  Filtering before or after the core test gives the same set here.
- The rerun took about 20 minutes on this machine, with other jobs running.

## For Jobst to decide

Nothing found here contradicts the Gate 1 statement in the write-up. Its caveats stand, and
finding 4 adds to them. Proposed, none done:

1. Quote robustness shares with intervals, or raise the number of draws.
2. Make `check_writeup.py` parse the numbers out of the Markdown file.
3. Correct the sentences under finding 6 and the wording under finding 5.
4. Keep this checker as the start of step 7, the independent checker for certificates.
