## Unverified or conflicting

### Conflicts between sources

- **Date of the US withdrawal.** UK government (Dec 2025): "withdrew from the JETP on 28 February 2025". DIRCO's statement is dated 6 March 2025. Carnegie says the commitments were rescinded "on March 5"; CSIS says "On March 6". Likely letter date versus announcement date; not resolved.
- **South Africa pledge totals differ by source and date.** UK, March 2025: "$12.8bn total". UK, Dec 2025: IPG $10bn / $12.4bn with other bilaterals / $13.7bn with MDBs. JET PMU, 30 June 2026: Table 3 grand total 13,177 pledged and 7,276 allocated (USD mn), while the report text gives an "inclusive" total of USD 14.382bn including private-sector and local DFI commitments. The Dec 2025 "IPG $10bn" does not match the PMU's IPG sub-total of 7,794 mn six months later; the definitions (what counts as IPG, treatment of CIF/ACT money) were not reconciled.
- **Size of the US share in South Africa.** UK: $56m grants + $1bn DFC. PMU Table 2 (original 2021 pledge): 20.15 grants + 1,000 commercial = 1,020.15 mn. News reports cite $1.5bn and $1.56bn (search snippets only, pages not fetched).
- **Indonesia targets attributed to the wrong document.** CSIS (13 Mar 2025) attributes the 290 Mt cap and 34% renewables to the CIPP. The primary texts show these are the November 2022 Joint Statement targets; the CIPP has 250 Mt and 44%, on-grid only.
- **jetp-id.org is stale on leadership.** Its "About JETP" text (retrieved today) still says Japan and the United States "are co-leaders of the partnership". German embassy, BMZ and Antara say Germany and Japan co-lead since early 2025.
- **Senegal lead.** BMZ factsheet (March 2025): "Lead: Germany, France". Carnegie (Oct 2025): "France (chair)". Not resolved.
- **Senegal headline.** EUR 2.5bn in the EC release; Carnegie gives "$2.7 billion" (same package in dollars, presumably).
- **Viet Nam headline.** USD 15.5bn in the Political Declaration; USD 15.8bn in the RMP statement (IPG part rose from 7.75 to 8.08).
- **Bangladesh NDC date.** Climate Watch gives 29 Sep 2025 (`submission_date`) and 24 Sep 2025 (`2025_date`).
- **Morocco.** Climate Watch flags "no economy-wide GHG target (for 2035)" while its own summary text says "across the economy". Same flag for Indonesia.
- **Global Fund cap.** The codified text limits the 33% rule to 25 March 2025; KFF says it is "not in place unless Congress includes it in appropriations". Whether a current appropriations act restates it was not checked.

### Could not verify (what was tried)

- **Indonesia per-donor pledges and grant/loan split.** They are in the CIPP (jetp-id.org PDF). Download stalls at 98,304 bytes on every attempt (HTTP/2 and HTTP/1.1, resume tried 12 times). Only the EU (about USD 2.5bn incl. EIB EUR 1bn) and UK (USD 1bn guarantee) figures from press releases are verified. The US share in Indonesia ("over $2 billion" in a search snippet) is unverified.
- **Indonesia Progress Report 2025** (1 Dec 2025): exists, contents not read (linked file not reachable). No verified 2026 disbursement figure. Reported figures of "$19.53 billion committed" and "over $6 billion in progress" (Mining Weekly, Nov 2025) could not be fetched (HTTP 403).
- **Viet Nam per-donor pledges and instrument split.** The RMP was not fetched. Search snippets (Böll, Vietnam Briefing) give grants of about USD 302–322m and concessional loans of about USD 2.75bn; not verified. Norway's page and both EEAS pages (July and October 2025, incl. a reported EUR 430m package) returned HTTP 403; UNDP returned 403. "Over 7 billion USD mobilised" (VietnamPlus, July 2025): page fetched but figure not found in the text.
- **Viet Nam: US share and what happened to it.** No primary figure found.
- **Senegal investment plan** (vie-publique.sn): not fetched; the instrument split rests on the Rosa-Luxemburg-Stiftung brief, which is a secondary and partisan source. The "less than EUR 1bn mobilised" figure is a news report of an official's remark.
- **Indonesia Joint Statement on coal:** the clause on a freeze of new coal plants was not extracted; only the peak, renewables and retirement clauses are quoted.
- **South Africa coal phase-down numbers** (plant decommissioning schedule and its delays): not collected.
- **Section 2, exact condition wording** not obtained for Indonesia (Second NDC), South Africa, Viet Nam, Nigeria (2035 split) and Thailand (Third NDC). Climate Watch's `M_Con*` conditionality indicators are listed in its indicator catalogue but were not returned by the endpoints tried (`/api/v1/data/ndc_content`, `/api/v1/ndcs?indicators=`, `?category=mitigation`).
- **Viet Nam and Egypt 2035 NDCs.** Climate Watch shows none on 10 Nov 2026. Not cross-checked against the UNFCCC registry (page not readable by curl). Climate Action Tracker pages agree in substance but may lag.
- **India's NDC date** (24 Apr 2026) and the **Philippines'** (8 Sep 2026) are after my training data; they rest on Climate Watch alone.
- **COP30 and country platforms.** Only the Mutirão decision was searched. Search snippets say that "thirteen new national platforms and one regional platform" were launched around COP30 and that country platforms featured in the Baku to Belém Roadmap report; neither was verified (the roadmap document URL tried returned an empty body; the C2ES summary returned 404).
- **COP31 presidency.** The UNFCCC page confirms place and dates only. Presidency roles rest on the Australian government release and one news report. Türkiye's own COP31 site was not fetched.
- **Global Fund, US pledges with an explicit match.** Seventh replenishment (USD 6bn, "$1 for every $2") and eighth replenishment (USD 4.6bn, Nov 2025): Global Fund news URL returned 404, results.org 403. Not verified.
- **UK 2016 Global Fund pledge** (GBP 200m private-sector match window) and **Japan's GCF condition**: search snippets only.
- **IDA:** no formal matching pledge found; not searched in depth.
- **People not verified.** Shikha Bhasin (fourth author of the conditional-NDC paper): the IDOS page is a former-staff record; CEEW returned 403; current affiliation unknown. William Nordhaus: only a Yale search-results page was reached ("Sterling Professor Emeritus"); no page read on his climate-club work. Scott Barrett (Columbia, 403), Urs Fischbacher (404), Axel Ockenfels (page reached at the Max Planck Institute for Behavioral Economics, but role and relevance text not extracted), Saliem Fakir (African Climate Foundation, 404). The relevance lines for Gächter, Tavoni, Dannenberg and Kesternich rest only on what their pages say; no specific paper on conditional contribution mechanisms was opened.
- **Pauw et al. (2020)** itself was not opened and its DOI was not verified in this session.
