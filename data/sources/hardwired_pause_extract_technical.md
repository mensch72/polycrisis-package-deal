# Extract from "The Feasibility of a Hardwired Pause of Frontier AI Training" (v1.0.2): technical sections

Ranges read in full (character offsets in `hp/paper.txt`): 76062–125061 (§3.2, §3.3), 146623–216479 (§4, §5),
222803–298474 (§6.2, §6.3, §6.4), 308310–372157 (§7; §8 starts at 372157). Not read: §1, §2, §3.1, §3.4–3.6, §6.1, §6.5, §8, §9,
except two sentences of §6.5 looked up for item G3 and two search hits at 61534 and 129988, all marked "outside my ranges".

Conventions. Every quote is verbatim and was machine-checked against the file; the number after it, written (@N), is the character offset
of its first character. Mathematical notation is garbled by the HTML conversion (each symbol appears twice, e.g.
"F E F_{E}"); where a quote contains such notation it is copied as it stands and marked [garbled]. Text outside quotation
marks is my summary. "Not found in my ranges" means exactly that.

---

## A. Actors

### A1. States

| Actor | Role the report gives it | Quote |
|---|---|---|
| United States, China | The two key parties; all ledgers are computed for them; both must take part in the census voluntarily | "The core of our feasibility analysis concerns the U.S. and China, two leading powers that are not members of the same coalition" (@94122) ; "voluntary participation of both the U.S. and China would likely be essential, as well as participation of other states such as Singapore and Malaysia, where many of the companies that supplied China with diverted stock reside" (@187081) |
| Singapore, Malaysia, Taiwan, UAE | Jurisdictions of resellers and data-centre operators that the census must cover | "would need to include resellers and data center operators in jurisdictions outside the U.S. and China including Singapore, Malaysia, Taiwan, and the UAE" (@110456) |
| "Host states" | Any state hosting licensed hardware; responsible for enforcement and inspector access; need not have ratified | "host states would be restricted to states that have agreed to abide by the terms of the treaty (e.g. signatories) but not necessarily restricted to states parties" (@107394) ; "with host states responsible for enforcement and inspector access" (@112079) |
| Small states (example: Luxembourg) | May get smaller allowances | "allowances might vary by state; e.g., Luxembourg might have less allowance than the U.S. or China" (@94023) |
| "Neutral states" | Possible hosts of scientific preserves | "either by locating them in neutral states unlikely to participate in a breakout, or giving treaty monitors the ability to quickly and permanently incapacitate the chips" (@296957) |
| Taiwan, South Korea (economic) | Receive the GDP effect of chip imports | "Spending on imports raises Taiwanese and Korean GDP, not U.S. GDP." (@310785) |

The EU appears in my ranges only as a jurisdiction with e-waste rules (offset ≈193300), not as a party. The sentence naming
"the EU, Japan, and South Korea" as US allies stands at 129988, outside my ranges (§3.4).

### A2. Supply-chain chokepoints: which state or firm controls which step (§5.2, §5.3.1)

| Step | Holder as the report states it | Quote |
|---|---|---|
| EUV lithography | Netherlands, ASML: monopoly | "The Netherlands’ ASML has a dominant market position in the production of DUV and a monopoly over the more advanced EUV." (@176034) |
| Immersion DUV lithography | ASML (NL), Nikon (JP); new Chinese entrant Yuliangsheng | "The Dutch company ASML is the only vendor for EUV machines and, until 2026, ASML and Nikon were the only two for immersion DUV machines" (@181869) ; "A new market entrant, Yuliangsheng in China, reportedly expects to produce 12 DUV machines at the 28nm node" (@182023) |
| High-precision optics, mirrors | Germany, Zeiss: sole producer | "The Germany-based company Zeiss is the only producer of some of the necessary mirrors and optical components" (@176929) |
| EUV coater/developer | Japan, Tokyo Electron | "the Japan-based Tokyo Electron has a nearly complete monopoly over coater/developer equipment used in EUV lithography" (@177107) |
| Leading-edge foundry and packaging | Taiwan, TSMC; some TSMC capacity in Arizona | "TSMC possesses the most advanced foundries and packaging processes, as well as several other key components for the production of compute." (@177558) |
| Second-tier foundries | South Korea (Samsung), China (SMIC, which works with Huawei on Ascend) | "both South Korea’s Samsung and China’s SMIC are capable of producing high quality, if not as advanced, AI relevant chips" (@177843) |
| Chip design and software stack | United States, Nvidia (CUDA); AMD | "Epoch AI estimates that over 60% of global AI compute capacity comes from Nvidia's chips" (@178409) |
| High-bandwidth memory (HBM) | South Korea, SK hynix (offshoring part to the US) | "HBM in particular has attracted increased attention ( Freed et al. 2026 ) , particularly given the significant role that South Korea’s SK hynix has in its development." (@179932) |
| Refined rare earths | China | "In 2024, 91% of the global supply of refined magnet rare earths was refined in mainland China" (@174829) |
| High-purity quartz | United States, Spruce Pine (North Carolina) | "the small town of Spruce Pine in North Carolina, which accounts for an “overwhelmingly” large portion of the global supply of the material" (@175195) |
| Whole chain | Nobody | "no state currently has a fully indigenous supply chain, and it would be profoundly difficult for any state to create one—especially without other states taking notice" (@180306) |

The report itself notes: "Many of these bottlenecks are not located within the United States or China, but are rather part of a global distributed supply chain." (@174249)

### A3. Firms, by role

| Role | Names in my ranges | Quote |
|---|---|---|
| Chip designers (training-capable) | Nvidia, AMD, Huawei (Ascend) | "Nvidia is the world's largest supplier of advanced AI training chips." (@178339) |
| Inference-only / specialised chip makers | Taalas (being acquired by AMD), Etched, Groq, Cerebras; Google (TPU, "Frozen" chip), OpenAI (Jalapeño); academic HNLPU design | "The hardware company Taalas, which AMD has agreed to acquire ( AMD 2026 ) , specializes in making chips of this type" (@156493) |
| Foundries | TSMC, Samsung, SMIC | see A2 |
| Equipment and optics makers | ASML, Nikon, Zeiss, Tokyo Electron, Yuliangsheng | see A2 |
| Memory makers | SK hynix | see A2 |
| Largest chip owners / cloud operators | Google, Microsoft, Amazon, Meta, Oracle, xAI, CoreWeave; also neoclouds, Tesla, Apple, ByteDance (China); colocation centres such as QTS | "78% measured in H100e as of year-end 2025, are owned by seven large American companies" (@207448) ; "Google, Microsoft, Amazon, Meta, Oracle, xAI, and CoreWeave." (@208270) |
| AI developers | OpenAI, Anthropic (named as the incumbents most likely to be entrenched); Z.ai, MiniMax (fast followers); Google | "entrench market power with the incumbent AI developers who have the most dominant market positions today, especially OpenAI and Anthropic" (@360993) |
| Shell companies, traders, diversion resellers | Unnamed, in Singapore, Malaysia and elsewhere; offered amnesty | "granting amnesty to shell companies and their customers for diversion around U.S. export controls or Chinese customs, conditional on producing retrospective records" (@110162) |
| Financial actors exposed | Nvidia shareholders (Vanguard, BlackRock, Fidelity, Geode, State Street), private credit funds, insurers, pension funds, banks | "the vast majority of private credit finance is provided by institutional investors, including pension funds and insurance companies" (@317803) |

### A4. Regulated roles created by the treaty (proposed)

| Role | Obligation | Quote |
|---|---|---|
| Licensed hardware operator | Holds every governed chip at a known data centre; routine inspections; licence depends on compliance record | "Each hardware system under treaty governance could be placed in the care of a licensed hardware operator at a known data center, residing in a host state" (@106964) |
| Licensed inference provider | Buys inference through a monitored API; subject to per-provider caps | "cap the total number of H100e units licensed per inference provider and host state" (@82695) |
| AI company (submits models) | Submits models and weight hashes by the deadline; design option: barred from operating hardware, compelled to license models | "AI companies (companies submitting whitelisted models) could be ineligible to apply for hardware operation or inference provision licenses" (@112814) |
| Licensed fab; lithography-machine factories | Register new chips at manufacture; attested wafer logs | "new hardware would enter by registration at the time of its manufacture at a licensed fab" (@108455) |
| Hardware owners (pre-pause) | Declare chips to the census; register or sell | "A census could require declaration of accelerators by current hardware owners" (@109702) |

### A5. Institutions

| Institution | Status | Role | Quote |
|---|---|---|---|
| "Treaty authorities" / "treaty governing authorities" / "interim treaty authorities" | Proposed | Certify ledgers, issue licences, keep the whitelist, run routers and preserves, buy and auction chips, insurer of last resort | "The treaty authority’s primary lever for balancing these two inequalities for each state would be limiting the total number of licenses granted to each state" (@94329) |
| Internationally operated router and recomputation server | Proposed | Verification of transitional inference | "All encrypted traffic from outside the data center would pass through an internationally-operated router machine" (@115210) |
| Scientific preserves | Proposed | Data centres run by treaty authorities | "data centers operated by treaty authorities and dedicated to common-good scientific applications such as medical research or healthcare provision" (@105275) |
| Chemical Weapons Convention | Existing, as precedent | Model for inspection protocols | "Inspection protocols could be modeled on precedents from the Chemical Weapons Convention" (@116034) |
| National intelligence, local law enforcement | Existing | Detect covert facilities and private evasion | "without detection by the combined efforts of local law enforcement, state intelligence agencies, and treaty authorities" (@255671) |
| Federal Reserve; bank, insurance and financial regulators | Existing | Buffer and monitor the economic shock (§7.1) | "Bank regulators should closely monitor bank lending to private credit firms and limit concentrated exposures to this sector." (@321666) |
| De-whitelisting insurance fund | Proposed | Compensates MSIC owners; treaty authority as last resort | "The treaty authority could serve as the insurer of last resort." (@356399) |

---

## B. Levers

Unit throughout: H100e. "A commonly used and intuitive unit of hardware arithmetic throughput is the H100-equivalent (H100e) , taken as 989 TFLOP/s" (@78563).
Inference capacity is measured in "inference-H100e".

The report's own master lever is the number of licences per state, under two ledger inequalities (see C2):
"each term in a given ledger could be adjusted until the inequality is satisfied, with the important exception of the term for dark compute" (@94609).

| # | Lever | Owner | Unit / scale | Binary or graded | Verification | Report's wording |
|---|---|---|---|---|---|---|
| B1 | Halt production of training-capable accelerators | States with fabs; fabs; designers | Chips or H100e produced per period; the type boundary is a treaty-set throughput threshold | Binary in the text (a "halt"); the definition of "training-capable" is a graded threshold | Lithography census, attested wafer logs, wafer/chip reconciliation, sampling of dies | "enforce the mandate that training-capable accelerator production be halted during Phase 1" (@121192) ; "This is what makes stopping the production of training-capable hardware an essential element of a hardwired pause" (@278586) |
| B2 | Pause frontier training; compute ceiling C_T and parameter ceiling N_T | States (law), AI developers | FLOPs per model; parameters per model | Binary per model; ceilings are graded and adjustable | Denial of compute before the fact; parameter count after the fact | "while a parameter ceiling is more enforceable after the fact, training FLOPs are easier to deny to evaders before the fact" (@85704) |
| B3 | Declare models near the ceiling | AI developers | Parameters above a licensing floor N_L | Binary | Declaration | "could require declaration to treaty authorities, with graduated penalties for noncompliance" (@87083) |
| B4 | Submit models for the whitelist by a deadline, with a hash of weights | AI developers; states decide | Per model | Binary per model | Hash checked against deployed weights | "developers submitting closed-weight models could be required to submit a cryptographic hash of a complete description of the architecture and weights" (@98617) |
| B5 | Whitelist, de-whitelist, re-whitelist a model; approve fine-tunes | Treaty authorities / participating states | Per model | Binary per model, reversible | n/a (authority's own act) | "a model for which a critical jailbreak is discovered could be de-whitelisted, possibly followed by re-whitelisting contingent on inference providers deploying it with required external constraints" (@97614) |
| B6 | Global accelerator census: declare and register pre-pause chips | States (records, subpoenas), owners | H100e registered; equivalently the missing stock K_M(s) | Graded (coverage) | Cross-checks of tax, customs, sales, power and rental records; inspections; satellite archives | "a global accelerator census attempting, as far as possible, to account for every pre-pause accelerator unit" (@108902) |
| B7 | Furnish records, admit inspectors to commercial data centres | States | Not quantified; feeds the negotiated dark-compute estimate | Graded | Observed by counterparties | "A state’s willingness to furnish data on request, to permit inspector visits to commercial data centers, and generally to assure other parties of its accounting transparency would likely be a factor in the negotiated estimate." (@111189) |
| B8 | Buybacks, bounties, amnesty | States | Money; the report gives an illustrative budget of $1T | Graded | n/a | "offering generous buybacks and bounties for tips leading to the discovery of undeclared accelerators" (@110049) |
| B9 | Licences for transitional inference on training-capable chips | Treaty authority grants; state and operator hold | H100e licensed per provider and host state | Graded (count) | International router, sampled recomputation, power reconciliation | "interim commercial allocation of training-capable hardware to transitional inference service by licensed inference providers while the market awaited sufficient inference-only hardware to replace it" (@103759) |
| B10 | Licences for inference-only chips; cap on residual training factor ϕ | Treaty authority; states; chip makers | inference-H100e; ϕ = training H100e per inference-H100e | Graded | Hardware audit, certified bound | "the number of licenses for a given state could be reduced if the state had insufficient headroom on its covert evasion or overt breakout ledger" (@286466) |
| B11 | Sovereign fleet (kept training-capable, for national security) | Each state | H100e; reference size El Capitan, 46k H100e | Graded | Negotiated case by case; power monitoring, telemetry, whistleblower protection lower the charge | "each state could be allowed a licensed sovereign fleet of training-capable accelerators, with registered and tracked chips, for use on specific sensitive national security workloads" (@104819) |
| B12 | Strategic reserve: powered-off chips under seal on own territory | Each state | H100e; counts in full against the breakout ledger, zero against the evasion ledger | Graded | Periodic inspection and counting of seals | "store licensed strategic reserves of powered-off training-capable hardware under seal in monitored facilities within their own territory" (@105463) ; "verification could rely on periodic inspection and counting to check that hardware remains under seal in its purported location" (@117911) |
| B13 | Place chips in internationally governed scientific preserves, possibly in neutral states | States, owners; treaty authorities operate | H100e | Graded | Declared, logged, replayable workloads; kill ability | "all workloads would be declared by named, vetted participants, and could be logged and replayable on demand by treaty authorities" (@116595) |
| B14 | Sell chips to licensed operators or to treaty authorities | Owners | H100e | Graded | Registration | "either register their chips under the treaty or sell their chips to licensed hardware operators, or to treaty authorities, which could sell them back to hardware operators at auction" (@104433) |
| B15 | On-chip location attestation; re-registration on transfer; produce or surrender silent chips | Operators; host states enforce | Per chip | Binary per chip | Latency-based location | "Chips that unexpectedly moved or fell silent would have to be produced for inspection or surrendered to authorities" (@111783) |
| B16 | Verified destruction at end of life | Operators | Per chip | Binary per chip | Witnessed | "The only approved way for hardware to exit treaty governance would be verified destruction at the end of its life." (@108546) |
| B17 | Register and track lithography machines (EUV, ArF-immersion DUV) and other tools | States with fabs; vendors | Machines, by serial number | Binary per machine | Vendor delivery records; attested per-wafer logs; satellite, off-gassing, substation metering | "any unaccounted-for machine could be charged to host states’ ledgers as continuously producing dark compute until they were located and accounted for" (@123043) |
| B18 | Monitor declared fabs: wafer counts, die sampling, consumables | Fabs; host states | Wafers, dies, kilograms of photoresist | Graded (sampling rate) | Reconciliation and random inspection | "reconciling the number of silicon wafers coming in, the number of logged wafer prints, and the number of chips coming out" (@124454) |
| B19 | Refrain from full indigenisation of the supply chain | United States, China | Not quantified | Binary in spirit | Lens accounting by ASML and Zeiss; intelligence | "we would recommend to pause-willing leaders of the U.S. and China that they not pursue full indigenization, since succeeding in that pursuit could destabilize the treaty" (@183425) |
| B20 | Lens accounting | ASML, Zeiss (Netherlands, Germany) | Lenses | Binary per lens | Vendor replacement and return | "Any failed lens should be replaced by the vendor and returned to its nation of origin." (@182735) |
| B21 | Domestic safeguards that lower the political discount π: criminalisation, whistleblower protection, inspections, power monitoring | States | Enters as π_E between 0 and 1 | Graded | Accepted or not by counterparties | "If a state can persuade other parties to accept that no more than 20% of a facility could plausibly be marshalled toward covert training without a significant likelihood of detection" (@271757) |
| B22 | Limit consumer GPUs per holder | States | Cards per actor | Graded | Domestic law | "states parties might consider passing laws limiting the number of consumer GPUs held by any one actor" (@293359) |
| B23 | Bar AI companies from hardware and inference licences; compulsory model licensing at regulated rates | States / treaty | Per firm | Binary | Licensing | "a mandate for AI companies to license their models to inference providers at regulated rates" (@113086) |
| B24 | Compulsory de-whitelisting insurance for MSIC operators | Operators | Premium on book value | Graded | Licence condition | "require firms to buy insurance covering losses from de-whitelisting as a condition of their license to serve inference with MSICs" (@355885) |
| B25 | Incremental recovery of hidden chips, conditional on others | States | Chips produced | Graded, in increments | Mutual observation | "they could agree to produce some number of chips conditional on others doing the same" (@200546) |
| B26 | Moving transitional chips to new data centres (offshore / neutral custody) | United States in the example | Share of the transitional fleet ("half") | Graded | n/a here | Outside my ranges (§6.5.2, offset ≈305400). In my ranges only the preserves in neutral states (B13). |

Not found in my ranges: any lever framed as an export-control commitment by chokepoint states towards third parties; any explicit
"offshore custody" rule (see B26).

---

## C. Numbers

### C1. Thresholds, illustrative values for a pause at year-end 2026 (Table 3.1, offset ≈84000; derivations in §6.2)

The table row text, verbatim [garbled]: "F E F_{E} Fleet threshold for covert evasion at present-day utilization 6.4M H100e F B F_{B} Fleet threshold for overt breakout at present-day utilization 180M H100e" (@88709)

| Symbol | Value | Meaning | Quote |
|---|---|---|---|
| C_F | 2 × 10^27 FLOPs | Training budget of the frozen frontier | "we estimate a frontier level of roughly" (@229071) (followed by the garbled value "2 × 10 27 F L O P s" and "at year-end 2026") |
| C_T | 2 × 10^24 FLOPs (β_T = 0.001) | Treaty compute ceiling | "we suggest keeping C T C_{T} three orders of magnitude below C F C_{F}" (@252664) [garbled] |
| N_T | 13B parameters | Treaty parameter ceiling | "N T N_{T} Treaty parameter ceiling 13B parameters" (@88419) [garbled] |
| C_E | 2 × 10^28 FLOPs (β_E = 10) | Budget for strategically relevant covert evasion | "which would correspond to a mid-2028 model on the present race trajectory" (@243298) |
| C_B | 2 × 10^29 FLOPs (β_B = 100) | Budget for strategically decisive overt breakout | "suppose that negotiators at the time of the pause think a bullish defector would be confident that superintelligence will arrive by the end of 2029" (@248402) |
| F_E | 6.4M H100e | Covert evasion fleet threshold, horizon T_E = 5 years | "we estimate initial covert evasion fleet threshold" (@224324) ; "we adopt a strategic time horizon of" (@241888) (then "T E = 5 T_{E} = 5 years") |
| F_B | 180M H100e | Overt breakout fleet threshold, horizon T_B = 2 years | "We adopt 180M H100e as our illustrative value going forward but, in practice, we expect a realized choice of" (@251744) ; "we adopt a breakout time horizon of" (@250239) (then "T B = 2 T_{B} = 2 years") |
| F_P | 150k H100e (up to 1.2M) | Aggregate private evasion fleet that would undermine the treaty, under the worked example V(x) = 100/x | "amounting to billions of dollars of installed hardware" (@255526) ; "this gives 1.2M H100e, or tens of billions of dollars worth of hardware" (@256664) |

Sensitivity of F_E and F_B:
- Later pause date: "the same steps would yield F E = 14 M H 100 e" (@243993) [garbled] for a pause in mid-2027 with C_F = 4.2 × 10^27 (offset ≈243100).
- More bullish leader (decisive model by year-end 2028): β_B = 22, F_B = 36M H100e. With T_B = 1 year: "the previous two F B F_{B} values would change to 350M H100e and 73M H100e, respectively" (@251442) [garbled].
- F_B is declared a negotiated quantity: "a matter of negotiation and trust more than one of estimation" (@251872).
- F_E grows with a later pause, F_B may not: "guarding against covert evasion could be somewhat easier if a pause is implemented later" (@226010) ; "guarding against overt breakout could get more difficult, since every year of scaling brings us closer to any fixed capability level" (@226240).

Inputs to the thresholds: research overhead ρ_F = 6.3, ρ_E = 11, ρ_B = 12, ρ_P = 4.9; utilisation U_F = 0.21; blind-leap increment δ = 1/3;
frontier growth g = 4.5 per year. Quotes: "frontier AI companies spend only about 9.6% of their research compute budget on these final training runs" (@231725) ;
"we adopt the conservative value" (@235836) (then "U F = 0.21"); "Reproducing Epoch’s frontier plot gives an estimated 4.5x increment per year" (@229200).

### C2. Ledger rule and allowances

- Rule [garbled]: "held below the covert evasion fleet threshold times a fractional covert evasion allowance" (@93336) ; "certifying that it is below the breakout fleet threshold by an overt breakout allowance" (@93760). In plain form: L_E(s) ≤ α_E · F_E and L_B(s) ≤ α_B · F_B, with L(s) the sum over compute sources c of K(c, s).
- Illustrative allowance 25% for both: "we evaluate its headroom for a treaty that gives an allowance of 25% for both ledgers" (@273841).
- Capacity of a source = political discount × technical discount × raw capacity: "a political discount factor π \pi representing the fraction of hardware in that category that could plausibly be marshalled toward building frontier models" (@268940) [garbled] ; "a technical discount factor τ \tau representing the average sustained utilization that could realistically be achieved, relative to present-day frontier training" (@269165) [garbled].
- Schedule of allowances, 100% → 25%: outside my ranges, §6.5 at offset 301324: "they could start close to 100% at entry into force and fall gradually to 25% by the time one order of magnitude of training efficiency gains had been incorporated". See G3.

### C3. Stocks at year-end 2026 (Table 6.1, offset ≈225900; Table 5.1, offset ≈202300)

| Quantity | Value | Range shown | Quote |
|---|---|---|---|
| World stock Q | 47M H100e | 45–47M | "World accelerator stock Q Q 47M 45–47M" (@226833) [garbled] |
| In the United States Q_US | 35M H100e | 26–44M | "Located in the United States Q U S Q_{\mathrm{US}} 35M 26–44M" (@226872) [garbled] |
| In China Q_CN | 3.1M H100e | 2.6–4.5M | "Located in China Q C N Q_{\mathrm{CN}} 3.1M 2.6–4.5M" (@226934) [garbled] |
| US stock as share of F_B(0) | 20% | | "or 20% of F B ( 0 ) F_{B}(0) , and" (@275908) [garbled] |
| China stock as share of F_B(0) | 1.8% | | "or 1.8% of F B ( 0 ) F_{B}(0) . Thus, at the pause date, both breakout capacities would likely be below the allowance before discounting." (@276066) [garbled] |
| OpenAI's own fleet | 6.4M H100e (equal to F_E) | | "we project that OpenAI’s fleet at year-end 2026 will be 6.4M H100e, and China’s total fleet would be 3.1M H100e" (@243573) |
| Diverted stock in China | 990k H100e | | "Epoch AI estimates 660k H100e diverted over 2024-25" (@209246) ; "to arrive at 990k H100e" (@209384) |
| New capacity shipped | 2.9M H100e per month in Q4 2026 | | "roughly 2.9M H100e of new AI compute capacity shipped each month during Q4 2026, which is rising" (@168165) |
| Share of stock under three years old | over 95% | | "over 95% of the world stock by computing power is less than three years old" (@194115) |
| Ownership concentration | 78% with seven US firms | | see A3 |

### C4. What a thorough census would miss (§5.5, Table 5.1)

- Headline: "giving conservative estimates of 12k total H100e in the U.S. and 11k H100e in China" (@202621). That is about 0.03% of the US stock and 0.35% of the Chinese stock (my division, not in the text).
- Table totals, verbatim: "Total, United States 35M 190k 4.5k 35M — 7.5k 12k" (@203643) and "Total, China 3.1M 24k 1.7k 3.1M — 9.6k 11k" (@203961) (columns: stock, failed chips, failed chips missing, functional chips, missing fraction, functional missing, total missing).
- Missing fractions μ(h) of functional chips by holding type: publicly identifiable 0; on-books 0.19%; off-books (China only) 1.6%; informal 10%. Quotes: "Multiplying these numbers gives a conservative bound of" (@215348) (then "μ (On-books) ≤ 0.19 %"); "For publicly identifiable holdings, which are held by large businesses and public institutions, we assume negligible noncompliance." (@213354)
- Caveat: "it does not imply a prediction that the Phase 1 census necessarily would be thorough" (@201125).
- Dark-compute scenarios (§6.4.3), as share of F_E(0):

| Scenario | United States | China | Quote |
|---|---|---|---|
| High cooperation | ≤ 7.2k H100e, 0.11% | ≤ 6.8k H100e, 0.11% | "would stash no more than 20% of the total missing amount" (@281023) |
| Low cooperation | 5 × K_M, 0.94% | 10 × K_M, 1.8% | "we assume five times the missed quantity estimated in § 5.5.2 for the U.S., and ten times the missed quantity for China" (@283703) |
| Non-deniable concealment | 300k H100e, 4.7% | 1M H100e, 16% | "which would respectively be 4.7% and 16% of F E ( 0 ) F_{E}(0) , and 0.17% and 0.57% of F B ( 0 ) F_{B}(0) , if undiscounted" (@285611) [garbled] |

- Tipping size: "a million missing H100e units would approach 16% of" (@279503) (F_E).

### C5. Other ledger terms (§6.4), per state unless said otherwise

| Source | Covert evasion capacity K_E | Breakout capacity K_B | Discounts used | Quote |
|---|---|---|---|---|
| Transitional inference, US | ≤ 35k H100e, 0.55% of F_E | ≤ 35M, 20% of F_B | π_E = 0.001 | "If we assume pessimistically that 10% of hardware operators in the U.S. engage in treaty evasion" (@276693) |
| Transitional inference, China | ≤ 31k H100e | ≤ 3.1M, 1.8% of F_B | π_E = 0.01 (all operators, 1%) | "the Chinese government were able to covertly suborn all of its hardware operators into diverting 1% of their computing power" (@277263) |
| Inference-only fleet at ϕ = 10^-4 | ≤ 310 H100e, 0.0049% of F_E | ≤ 310k H100e, 0.18% of F_B | π_B = τ_B = 1 | "would allow each of the U.S. and China to replicate the estimated 31M H100e of global inference service one hundred times over with inference-only accelerators" (@287789) |
| Consumer GPUs | ≤ 3.0k H100e, 0.047% | ≤ 76k H100e, 0.043% | π_E ≤ 0.01, π_B ≤ 0.25, τ ≤ 0.1; raw 3M H100e | "it would be difficult to commandeer more than 25% of total consumer capacity toward a breakout program" (@291550) |
| Sovereign fleet (El Capitan, US) | ≤ 9.1k H100e, 0.14% | ≤ 46k H100e, 0.026% | π_E = 0.2, π_B = 1 | "the treaty could sustain a practice of allowing a number of supercomputers on the scale of El Capitan per state without threatening treaty thresholds, at least early on" (@295491) |
| Strategic reserve | 0 | full size | π_E = 0, π_B = τ_B = 1 | "thereby contributing nothing to a state’s covert evasion ledger" (@297906) |
| Scientific preserve | negligible | negligible if in neutral states or with kill ability | | "scientific preserves contribute negligibly to the U.S. or China’s covert evasion or overt breakout ledgers" (@297254) |

Exchange rate between breakout allowance and inference: "if a state wished to spend 1M H100e of its overt breakout allowance on an inference-only fleet, then it could serve 100M H100e worth of token demand on a fleet with average residual training factor below 0.01" (@287171).
Residual training factor example: "whose average residual training factor is" (@82204) (then "ϕ = 0.001 … would reduce that fleet’s training capacity by 99.9%"); the 10^-4 is "not an estimate or prediction but an illustrative value" (@288253).

### C6. Time to ramp inference-only hardware (§4.4)

- Phase 1 (design to production): "we might expect timelines of roughly 26 months or less for their Phase 1s" (@164869). With an existing platform: "“From the moment a previously unseen model is received, it can be realized in hardware in only two months”" (@163328) (Taalas' claim).
- Phase 2 (substitution): "then we obtain a rough estimate of 47M / 2.9M per month ≈ 16 months for Phase 2" (@168451).
- Together: "the world could transition through Phases 1 and 2 in less than 5 years, depending on the amount of R&D carried out in Phase 0" (@169328).
- The report stresses heterogeneity: "in reality there is no single Phase 1; instead, there are different Phase 1s for different hardware companies" (@163084).

### C7. Training efficiency gains (§6.3) and frontier growth

| Rate | Source cited | Quote |
|---|---|---|
| 2.7-fold per year (most extreme) | Ho et al. 2024 | "found that there had been annual 2.7-fold training efficiency gains" (@260482) |
| 45% per year | Gundlach et al. 2025 | "translating to an impressive but much less overwhelming 45% improvement per year" (@262664) |
| 57% per year, at fixed scale | Patel and Han 2026 | "found annual pretraining efficiency gains of 57% over the period 2019 to 2025" (@263473) |
| Frontier training compute, 4.5× per year | Epoch AI, replicated | see C1 |
| World AI compute, doubling about every seven months | You et al. 2026 | "global AI computing capacity has doubled roughly every seven months" (@173254) |

The report gives no rate for the paused world: "no one can predict what training efficiency gains would be after a pause" (@371482). Durability is stated in orders of magnitude of erosion:
high cooperation "It could comfortably survive two orders of magnitude of erosion due to training efficiency gains" (@282232); low cooperation
"the regime could survive one order of magnitude of training efficiency gains relatively comfortably" (@284225).

### C8. Verification and cost numbers

- Fab sampling: "a diversion of 1% of production in that line would be recognized within six months with 95% probability" (@185553) (2400 dies sampled per line per year, detection chance one in four).
- GEMM laundering through the token interface: "requiring more than 80,000 such machines to match the arithmetic throughput of a single H100" (@149169).
- Buyback budget: "implying an estimated total acquisition cost of $500B" (@197231) ; "this is less than a fourth of the roughly $4.5T that the U.S. government alone spent on Covid relief" (@197424).
- Tax incentives to have declared chips: "the tax deduction a business can claim for capital expenditures is worth over 21% of the purchase price" (@189449) (US); "is worth 13% of the price, along with an additional 15–25% from an enterprise tax deduction" (@189696) (China).
- Economics (§7): Mag7 thought experiment "falls by $6.5 trillion" (@313037); "is 0.6 percent of projected 2026 GDP, or about a quarter of projected 2026 GDP growth" (@313107); MSIC savings "Estimates for the savings term S S range from 60% to 95%" (@329212) [garbled]; stranded capital on de-whitelisting of the top model "Then the stranded capital cost is approximately $45B" (@353690); share of compute now spent on training "Anthropic and OpenAI are committing 62% of their combined compute resources to research, development, and training of new models" (@323570).

---

## D. Asymmetries

| # | Asymmetry | Quote |
|---|---|---|
| D1 | Stock: US 35M against China 3.1M H100e (about 11 to 1) | see C3 |
| D2 | The binding constraint differs. US: overt breakout capacity from its transitional fleet. China: covert evasion capacity from dark compute | "China’s covert evasion capacity from dark compute would pose a similar issue as the U.S.’s overt breakout capacity from transitional inference service" (@285828) |
| D3 | US has almost no headroom on the breakout ledger at 25% | "the breakout number leaves almost no headroom for a treaty with 25% allowance, and two doublings of training efficiency gains could bring" (@276213) |
| D4 | Concealment is judged easier in China | "In the U.S., it would likely be more difficult to conceal a large stock owing to the relatively greater difficulty of keeping secrets." (@283549) |
| D5 | Subornation of operators: 10% of US operators, all Chinese operators (pessimistic assumptions) | see C5 |
| D6 | China holds the diverted, partly off-books stock; the "off-books" holding type is estimated for China only | "We only estimate the third category in China because of the large quantity of diverted stock located there." (@206239) |
| D7 | Yet diverted chips are visible to the Chinese state | "demonstrating that most of the diverted stock has never been invisible to the Chinese government" (@195853) |
| D8 | Chips cost more in China | "where it has at times traded at two to three times the U.S. price, as a result of scarcity created by U.S. export controls" (@188287) |
| D9 | Production capacity | "China has nascent and growing capacity, but it continues to lag the United States" (@173519) |
| D10 | Whoever breaks out faces a rest of the world with the fuller supply chain | "or to resume racing against it, likely with a more complete hardware supply chain and therefore, eventually, a larger fleet" (@250056) |
| D11 | Legal constraints differ: US takings law, warrants, First Amendment; constitutional democracies face hurdles in commandeering hardware | "Under U.S. law, compulsory surrender may require just compensation" (@112146) ; "In constitutional democracies, at least, any such effort would require sufficient constitutional or statutory basis" (@291330) |
| D12 | Chokepoints: China holds rare earths; the Netherlands, Germany, Japan, Taiwan and South Korea hold the tools, optics, foundry and memory | see A2 |
| D13 | Small against large states: allowances may differ | see A1 (Luxembourg) |
| D14 | Economic exposure is concentrated in the US (Nvidia, Mag7, private credit); chip import spending accrues to Taiwan and Korea | see E |

Not found in my ranges: any asymmetry in energy, talent, or inference demand between the two states; any figure for a third state's stock.

---

## E. Who gains and who loses

### E1. Losers and costs

| Who | Effect | Quote |
|---|---|---|
| Nvidia | Loses dominance; costly pivot | "such a transition would be neither painless nor cost free, and the company would presumably not dominate that market as it does the market for general-purpose accelerators" (@316065) |
| "Mag7" shareholders | Share prices fall | "There would presumably be a drop in the lofty stock prices of the “Mag7,”" (@312310) |
| OpenAI, Anthropic (IPO candidates) | Delay, not abandonment | "But delay is more plausible than the more dire scenario of abandonment." (@313637) |
| Data-centre lenders, insurers, pension funds | Only if inference demand falls | "Only if declining data center revenues cause distress in debt markets and if that distress is allowed to infect institutional investors could the effects be seriously destabilizing." (@322722) |
| MSIC owners | Stranded capital if a model is de-whitelisted | "The firms that own and operate MSICs incur the losses when a model is de-whitelisted, which raises the worry that they will lobby heavily against any de-whitelisting." (@355665) |
| Users of low-demand models, small languages | Model may go unserved | "the loss may be greater for users for whom no model with an MSIC performs well in their native language" (@342735) |
| Individuals and businesses | New constraints | "the liberty to buy an unrestricted number of accelerator GPUs, to train AI models of unlimited size, or to operate chip fabs and data centers without being subject to inspections" (@359937) |
| Lagging AI labs | Not stated as losers in so many words; the text says they now spend more on catching up | "Other lagging AI labs with less market share and a strong desire to catch up to the frontier may currently devote an even larger fraction of their compute to training." (@323700) |
| States without a domestic industry | Not found in my ranges, beyond the Luxembourg allowance and "neutral states" as hosts of preserves | |

### E2. Gainers

| Who | Effect | Quote |
|---|---|---|
| Incumbent AI developers | Entrenched market power, rents | "granting long-term monopoly rents" (@113286) (footnote: "Or duopoly/oligopoly rents, if a small number of AI companies own the most powerful models at the time the treaty is enacted." (@113681)) |
| Owners of pre-pause chips | Profitable transitional inference; buybacks | "The transitional inference service during Phases 1-2 of the treaty (see Figure 1.1 ) would likely be highly profitable" (@196577) ; "compliance would be the most remunerative option for hardware owners" (@104741) |
| Makers of inference-only chips (Taalas/AMD and others) | New market | "The commercial advantages of MSICs over general-purpose hardware would correspondingly be greater in a world with a frozen whitelist" (@160270) |
| Consumers of inference | Lower token prices | "the principal near-term economic welfare effect of a pause could be an increase in consumer surplus from reduction of token prices as well as increased speed and supply" (@325110) |
| AI labs and cloud providers (margins) | Lower hardware and energy cost | "alleviate the pressure on AI labs/cloud service providers' margins, making it more conducive for them to agree on a pause" (@324531) |
| Macroeconomy | Limited damage | "frontier model restraints would do little to reduce economywide productivity growth below its current rate" (@312202) |

### E3. Side benefits offered to make the pause palatable

| Sweetener | For whom | Quote |
|---|---|---|
| Sovereign fleets | Each state's national security | "it does not appear that, in the immediately foreseeable future, a treaty would need to impose on strategically important assets like El Capitan" (@296322) |
| Strategic reserves | Each state's insurance | "This is what makes the strategic reserves an attractive, politically cheaper alternative to covertly hoarding a large reserve of chips." (@297971) |
| Scientific preserves | Common-good science | "Another palatability feature we discussed in § 3.3.1 was the option to create internationally governed scientific preserves." (@296490) |
| Exemptions for beneficial science | Medical research | "Models trained for beneficial scientific purposes such as medical research could potentially be granted exemptions" (@91225) |
| Buybacks, bounties, amnesty | Chip owners, diversion traders | see B8, A3 |
| More licences for cleaner ledgers | Any state | see F2 |
| Separation of AI companies from hardware; regulated model licensing | Constituencies opposed to monopoly rents | "could also potentially increase political palatability for constituencies that object to governments granting long-term monopoly rents" (@113185) |
| Continued growth of non-AI compute | Science, graphics | "to continue on a rapid growth trajectory even as the total training capacity for AI models dwindles" (@106733) |
| De-whitelisting insurance | MSIC operators | see B24 |

Not found in my ranges: any scheme to distribute inference-only chips or inference access to states without an industry; any side payment between states.

---

## F. Sequencing, conditionality, commitment, response to defection

### F1. Sequencing

- Phase 1 starts with the agreement and presupposes a provisional whitelist: "by the beginning of Phase 1, marked by the pause agreement, there is a provisional model whitelist" (@162375).
- Models are submitted before a deadline in Phase 0 or 1: "AI developers would submit above-threshold models to be considered for whitelisting by participating states or interim treaty authorities before a defined whitelist submission deadline" (@98361).
- Production halt in Phase 1 (B1). Census "as early as possible": "As early as possible, it would be important for governments to undertake a global accelerator census" (@108829).
- Interim arrangements may be informal: "During an interim agreement, arrangements could be based on informal participation." (@107612)
- The census may be slow and trust may grow stepwise: "It could also be that leaders gain greater confidence in each other over time, beginning with small measures and slowly finding ways to work together more closely." (@280158)
- Verification is weaker while being set up: "Both political discount factors would likely be higher during the stages when these methods were being set up." (@277690) Stopgap: "Whole-lab inspections as proposed by Choussat and Khoja ( 2026 ) could be a stopgap interim measure" (@277945).
- Residual training factor may start high and fall: "The maximum residual training factor could start relatively high in order to allow early designs to speed the transitional period, and it could decrease over time" (@82353).
- Problems to be solved in the first years: "Both problems would need to be resolved in the early years of the treaty, but the two states would likely have a few years." (@285980)
- Who must act before whom among states: not found in my ranges. The recruitment of allies after a US–China start is at 61534 and 129988, outside my ranges.

### F2. Conditionality built into the design

- Licences are conditional on the state's own ledger: "Because issuance of licenses would depend on satisfying these inequalities, states desiring more licenses would have an incentive to keep their ledgers clean" (@95103).
- Verification is traded against allowance, state by state: "they could be flexibly negotiated based on each state’s willingness to make concessions in each context, with larger compute sources requiring more rigorous verification measures than smaller ones" (@95560).
- More transparency lowers the charge on a sovereign fleet: "states would be charged less against their covert evasion ledger if they could show other parties some evidence that most of the sovereign fleet was not being used for illicit training" (@117300).
- Dark compute is charged to the host state: "Hardware lost to the regime would likely be presumed dark compute and charged to host states’ covert evasion and overt breakout ledgers at near-full training capacity." (@108661)
- Concealment costs licences: "any dark compute retained by a state would likely inflate the state’s covert evasion ledger and limit the issuance of licenses for other purposes, except to the extent that that state could credibly deny possession of it" (@198582).
- The one explicitly reciprocal mechanism in my ranges (hidden-stock recovery): "they could agree to produce some number of chips conditional on others doing the same" (@200546) ; "announce that they had done so in small increments so long as others appear to be doing the same" (@200763) ; "This process would be smoother if states parties all agreed on how many more chips ought to be recoverable from each party." (@200861)
- Peer pressure through comparison: "it would place additional pressure on states missing larger fractions of their pre-pause stock, by making large gaps in the census appear more incriminating" (@197849).
- Operator licences depend on compliance record (see A4). Amnesty is conditional on records (see A3). Re-whitelisting is conditional on guardrails (B5).

### F3. What reserves and allowances insure against

- Reserves insure against a rival's breakout and are recoverable on exit: "Because these strategic reserves would be recoverable in the event of a treaty exit, they would give states insurance against breakout by rivals." (@105681)
- They substitute for hidden stock: "they would be a cheaper form of insurance than a dark compute stockpile would" (@105906).
- Residual hidden stock as insurance is expected even under high cooperation: "but might stash a small, plausibly deniable number as insurance" (@280838).
- Allowances α are a safety margin for estimation error: "times a fractional covert evasion allowance" (@93382) … "to account for uncertainty" (@93450).
- The wide margin between C_T and C_F insures against capability proxies being poor: "preventing the training of new frontier models would require leaving a wide margin between the compute ceiling" (@85895).

### F4. Response to defection or withdrawal

- Breakout means failure; no enforcement response is modelled: "if and when a state broke out and resumed racing to build a strategically decisive model, the treaty would likely have already failed" (@247328).
- The implied response is that others resume: "before the rest of the world could react to stop it—or to resume racing against it" (@250004).
- Coalition responses are mentioned as an input, not specified: "The choice of breakout time might likewise be sensitive to the quantity of strategic reserves states are allowed, as well as expectations and possible commitments about how coalitions would respond to defection." (@251532)
- More stock means less credible commitment: "the more training-capable hardware states accumulate, the less credibly they can assure other states that they would not break out and race faster than before" (@278701).
- Thresholds are set by beliefs of the most bullish party: "conservative treaty provisions should base" (@247850) … "on the estimate of what a bullish would-be defector might believe" (@248053).
- Seizure of a preserve: monitors disable the chips (A1, "neutral states" quote).
- Graduated penalties exist only for firms and models (B3): "with graduated penalties for noncompliance" (@87132). Private violations: "the treaty would need to combine sufficient penalties with sufficiently credible detection to deter all but a few private actors" (@253358).
- Silent or moved chips: produce or surrender (B15). Unaccounted lithography machines: charged as continuous dark production (B17). Vulnerable inference-only hardware: "inference-only licenses would be recallable for retrofit and re-licensing once the jailbreak is patched" (@114032).
- Deterrent for firms comes from pause length: "shorter-duration pauses would likely require stronger enforcement measures to prevent illicit training" (@99493).
- Expected durability feeds back on investment: "if there is uncertainty about whether the pause will be upheld over the investment horizon, that would make flexible accelerators relatively more attractive" (@334962).
- Fallback if cooperation stays low: "longer-term durability would hinge on the success of detection-based fallback measures" (@284663).
- A graduated state-level response schedule, sanctions, or a withdrawal clause: not found in my ranges.

---

## G. Checks of the six statements

**G1. "It assumes willingness to pause and studies feasibility, not desirability or probability."** Supported in my ranges, with two qualifications.
- Support: "after all, this paper is a feasibility study for a different political program that would sharply bend it by government fiat" (@239393) ; "As these estimates apply to a hypothetical future, they necessarily reflect speculations about, e.g., how cooperative pause-willing states parties would be" (@273340) ; "Compliance would depend on political conditions we cannot foretell." (@279825)
- Qualification (a): §7 does weigh some consequences (economy, consumer surplus, concentration of power) and admits the welfare comparison is open: "this would have to be weighed against the expected welfare effects of continuing to advance AI capabilities, about which there is significant disagreement" (@325299). It also says "which would make pausing sooner a more robust approach to mitigating these risks" (@371643).
- Qualification (b): §8, by its own opening sentence, treats how willingness could arise: "we consider some of the conditions under which the present might evolve into a pause-willing future" (@372056) (offset just at the end of my ranges; §8 itself not read).
- Qualification (c): willingness is not assumed to be uniform. The report distinguishes degrees: "In some pause-willing futures, leaders could be ambivalent about the pause and unwilling to provide any transparency to rivals" (@279893) ; "Despite their pause-willingness, both states suspect the other of planning to cheat" (@283116).

**G2. "Its levers are observable, countable and ordered."** Partly contradicted. Countable and ordered: yes, nearly everything is in H100e. Observable: not all.
- Dark compute is unobservable by definition and enters as a negotiated estimate: "Because dark compute would by definition be ungoverned under the treaty" (@94749) ; "parties could arrive at a negotiated estimate based in part on compiling and reconciling the above data" (@111005).
- The ledgers are not counts but counts times negotiated discount factors: "the parties could negotiate means of estimating a total (undiscounted) existing capacity" (@269487).
- Sovereign fleets need not be verified: "the treaty ledger approach above would not necessarily require ruling out that any portion of their computing power were being used for training" (@117027).
- The thresholds themselves rest on beliefs: "a matter of negotiation and trust more than one of estimation" (@251872).
- A state can gain from being under-estimated: "except insofar as they could arrange for other states to underestimate how much dark compute they had" (@105985).
- Verification intensity is itself a (graded, negotiated) lever (F2).

**G3. "Retained training-capable stock would fall from about 100% to 25% of a breakout threshold."** Not supported as worded.
- In my ranges, 25% is the allowance α, the cap on a state's whole ledger as a fraction of the threshold, for both ledgers (C2).
- The US training-capable stock at the pause date is 20% of F_B(0), not 100% (C3); China's is 1.8%.
- The "100% → 25%" wording is in §6.5 (offset 301324, outside my ranges) and describes the schedule of the allowances, not the stock: "a schedule might require states to reduce them to 25% over a period of years … start close to 100% at entry into force and fall gradually to 25% by the time one order of magnitude of training efficiency gains had been incorporated". Since F_B(t) itself shrinks with efficiency gains, the cap in H100e falls by more than a factor of four over that period. Please re-read 300900–301500 before relying on this.
- The stock is also meant to go to near zero in commercial use: "inference-only accelerators would displace the majority of training-capable accelerators after a several-year-long transitional period" (@103395) ; residual uses are sovereign fleets, preserves, reserves.

**G4. "Phase 1 begins when the United States and China agree, and states controlling chokepoints (EU, Japan, South Korea, as US allies) are recruited next."** Not contradicted, but incomplete against §5.
- Phase 1 "marked by the pause agreement" (F1). The US–China start and the allies sentence are at 61534 and 129988, outside my ranges.
- §5.2 names chokepoint holders the statement omits: Taiwan (TSMC), and within the EU specifically the Netherlands (ASML) and Germany (Zeiss); also China itself (rare earths) and the United States (quartz, Nvidia). See A2.
- The census needs a different set again: Singapore, Malaysia, Taiwan, UAE (A1).
- Not "recruited next" but needed from the start for the census: "conducted with the cooperation of the U.S., China, and a small number of additional jurisdictions key to international semiconductor trade in Asia" (@186390).

**G5. "A pause may entrench leading firms."** Confirmed (§7.4, quote in A3), and extended to capture of the whitelisting body: "the body responsible for whitelisting models would potentially be vulnerable to industry capture" (@361158). Two counter-points in the report: the design option of B23, and that Nvidia would lose dominance (E1). The entrenchment named is of AI developers, not of chip firms.

**G6. "The report does not model how conditional willingness turns into an agreement or analyse stability against coalitions."** Confirmed for my ranges. No game model, no equilibrium analysis, no coalition analysis appears. What does appear, as prose only:
- Incentive arguments that compliance beats concealment for a single state (three costs of concealment, offset ≈199700): "concealing a hoard of dark compute would be more costly for a state in several respects" (@199366).
- One reciprocal, incremental mechanism (F2, hidden-stock recovery).
- Coalitions mentioned twice and set aside: "there might be per-coalition allowances in addition to per-state allowances" (@93942) ; and the F4 sentence on "possible commitments about how coalitions would respond to defection".
- A bilateral framing by assumption (A1, first quote).
- A recommendation that is itself a commitment problem (B19, indigenisation).
