# Hardwired-pause report: which jurisdictions it names, and in what role

Compiled by Claude on 12 November 2026 from Fithian, Holliday et al. (2026), working paper v1.0.2,
https://hardwired-pause.ai/paper. It closes a gap that Jobst found: the technical extract
(`hardwired_pause_extract_technical.md`, section A1) covers only sections 3.2, 3.3, 4 to 7, and the
report names its participating jurisdictions in section 3.1, outside those ranges.

Every quote was machine-checked against the report's text on 12 November 2026. The number after a quote
is its character offset in the plain-text conversion used for the extract.

## Initial participants (section 3.1)

| Jurisdiction | Quote |
| --- | --- |
| United States, China, European Union (especially Germany and the Netherlands), United Kingdom, Taiwan, South Korea, Japan | "We assume that participating jurisdictions would initially include (at least) the United States, China, the European Union (especially Germany and the Netherlands), the United Kingdom, Taiwan" (@61926) … "South Korea, and Japan—jurisdictions that currently enjoy nearly a collective global monopoly on both cutting-edge AI chip manufacturing and frontier model training" (@62124) |
| Singapore, Malaysia, Indonesia, Thailand, Vietnam, United Arab Emirates, Saudi Arabia | "Other especially high-value signatories include nations like Singapore, Malaysia, Indonesia, Thailand, Vietnam, the United Arab Emirates and Saudi Arabia" (@62290) |
| Taiwan, status | "its formal status in a treaty would potentially be contested by the People’s Republic of China" (@63300) |

## Order of entry (sections 3.1, 3.4.2)

| Step | Quote |
| --- | --- |
| United States and China first | "could be implemented immediately by the U.S. and China alone" (@61449) |
| allies and partners next | "with a handful of allies and partners joining shortly thereafter" (@61516) |
| named allies with chokepoints | "recruit additional U.S. allies such as the EU, Japan, and South Korea, which control supply chain chokepoints" (@129964) |
| then the rest | "Adding the other supplier monopoly states would buy more time until it were possible to induce most other states to join" (@131175) |

## Chokepoints by jurisdiction (section 5.2)

| Jurisdiction | Chokepoint | Quote |
| --- | --- | --- |
| Netherlands | lithography machines (ASML) | "The Netherlands’ ASML has a dominant market position in the production of DUV and a monopoly over the more advanced EUV" (@176034) |
| Germany | mirrors and optics (Zeiss) | "The Germany-based company Zeiss is the only producer of some of the necessary mirrors and optical components" (@176929) |
| Japan | coater and developer equipment (Tokyo Electron) | "the Japan-based Tokyo Electron has a nearly complete monopoly over coater/developer equipment used in EUV lithography" (@177107) |
| Taiwan | leading-edge foundry and packaging (TSMC) | "TSMC possesses the most advanced foundries and packaging processes" (@177558) |
| South Korea | high-bandwidth memory (SK hynix) | "particularly given the significant role that South Korea’s SK hynix has in its development" (@180008) |
| nobody | the whole chain | "no state currently has a fully indigenous supply chain" (@180306) |

Further rows (United States: chip design, quartz; China: rare earths, second-tier foundry) are in section A2
of the technical extract.

## What the report does not give

- A role for the United Kingdom beyond its place in the list of initial participants.
- The European Union as an actor with levers of its own. Outside that list it appears as "the EU" among US
  allies, and its AI Office as a lesson in institution-building (@144326).
- Preferences or red lines of any of these jurisdictions. Section 8.5 covers the United States and China only.

## How the skeleton uses this

`pilots/pilot_b2.py`, version 3, has three supplier actors: `EUR` for the Netherlands and Germany, `EAS` for
Japan and South Korea, `TWN` for Taiwan. Version 2 lumped them into one bloc. The grouping is a modelling
choice of mine and not the report's view. The United Kingdom and the second group of signatories are not
in the skeleton at all.
