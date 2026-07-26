# SRM Institute of Science and Technology Online — Detail Page Content
*(SRM Online — official online education venture of SRMIST)*

> Sourced from the **official UGC-DEB government regulatory filing** (deb.ugc.ac.in, direct application PDF), SRMIST's own official domains (srmist.edu.in, srmtrichy.edu.in), Wikipedia, and multiple aggregators (CollegeBatch, CollegeVidya, APS Admission Panel, ApnaAdvantage, PujaEducation). Second official government filing found in this batch (after UPES) — this time it confirms the aggregator consensus rather than contradicting it.

---

## Hero

- **Name:** SRM Institute of Science and Technology Online
- **City / State:** Kattankulathur (Chennai), Tamil Nadu
- **Type:** Deemed University (Section 3, UGC Act 1956) — Category I status with Graded Autonomy
- **Tagline:** *NAAC A++ accredited online degrees from a deemed university with 40 years of academic history*

## About

SRM Institute of Science and Technology (SRMIST), founded in 1985 as SRM Engineering College, gained deemed-university status in 2002. Its name officially reverted from "SRM University" to "SRM Institute of Science and Technology" in 2017, following a UGC order requiring the change (worth noting since many sources — and casual usage — still refer to it as "SRM University"). SRM Online is its digital education arm, offering UGC-DEB and AICTE approved undergraduate and postgraduate programs.

## Highlights

- **NAAC A++, the highest possible grade** — confirmed by the official UGC-DEB government filing (score 3.55) *and* unanimous across every aggregator and official SRM domain checked
- Deemed University, UGC Category I status with Graded Autonomy — one of only 3 Tamil Nadu universities with this distinction (per SRM's own official site)
- 172+ total online programs across UG, PG, diploma, and certificate levels
- Dedicated "Online Career Service Track (OCST)" for placement support — a specific, named internal program, not just generic marketing language
- Students can pursue one full-time (offline) and one online degree simultaneously, per general UGC guidelines (a UGC-wide policy, not an SRM-specific perk)

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC (Section 3, deemed university) | ✅ Yes | Very high — confirmed by the official government filing and Wikipedia |
| UGC-DEB | ✅ Approved | High — consistent everywhere |
| **NAAC** | **A++ (Score 3.55, per the official government filing)** | **Very high — unanimous across every source, backed by primary regulatory documentation.** Minor internal note: SRM's own Trichy-campus page cites 3.58 for what appears to be the same 2018-2023 cycle — a small discrepancy between two official SRM sub-domains, though it doesn't change the letter grade either way. |
| AICTE | ✅ Approved | High — multiple sources |
| UGC Category I / Graded Autonomy | ✅ Yes | High — confirmed on official SRM domain |

## Rankings

Real historical data from the official government filing, similar to the UPES case:

| Source | Year | NIRF Rank |
|---|---|---|
| Official UGC-DEB filing | (unlabeled early year) | 58 |
| Official UGC-DEB filing | 2021 | 53 |
| One aggregator (APS Admission Panel) | 2024 | 12 (University category) |

This reads as a plausible continued-improvement trajectory (58 → 53 → ... → 12), similar to what I found for UPES — but the "12th in 2024" figure is aggregator-only, not confirmed by an official filing (the government PDF I retrieved only covers up through 2021-22). Worth confirming the current rank against nirfindia.org directly before publishing. Since your DB's `ranking` field is currently empty for this entry, there's nothing existing to conflict with either way.

## Programs, Fees & Eligibility

| Program | Duration | Eligibility | Notes |
|---|---|---|---|
| Online MBA | 2 years | Graduation in any discipline | — |
| Online MCA | 2 years | Bachelor's with relevant background | — |
| Online BBA | 3 years | Class 12 pass | — |
| Online BCA | 3 years | Class 12 pass with Math background | — |
| Online M.Com | 2 years | Graduation in any discipline | — |

⚠️ **No specific fee figures found** — sources describe fees as "affordable" and "lower than campus options" without quoting numbers.

No entrance exam required for online admissions (per one source) — consistent with the pattern found across nearly every UGC-DEB online program in this project.

## Admission Process

Standard online application, eligibility-based, no entrance exam. Document upload and verification, followed by LMS access.

## Documents Required

**This is the first university in this entire batch where a source actually confirmed a specific document list**, rather than me falling back on the generic assumed set:
- Mark sheets of qualifying exams
- Photograph
- Aadhaar or other government-recognized ID

*(Still worth confirming this is the complete/current list against the official portal, but it's a real sourced answer rather than an assumption for once.)*

## Scholarships

No specific SRM Online scholarship (name, amount, eligibility) was found in any source reviewed. Leaving empty rather than inventing one:

```python
# No verified SRM-specific scholarship found. Leave university_id-linked
# scholarships empty unless/until real data is sourced.
```

## Placements

No package figures or specific recruiter names were found in any source — genuinely nothing to withhold or flag as suspicious here, unlike some earlier universities in this batch.

- `placement_support`: **True** — the "Online Career Service Track (OCST)" is a specific, named program, more concrete than generic "placement assistance" language.
- `highest_package` / `average_package`: leave `None` — no figure found.
- `top_recruiters`: leave empty — no company names found in any source.

## Learning Methodology

- LMS with personalized learning dashboard
- Recorded video lectures, live sessions, assignments, online proctored exams
- Regular curriculum updates aligned with industry needs

## FAQs

```python
faqs = [
    {
        "question": "Is SRM Online's degree valid and recognized?",
        "answer": "Yes. SRM Online programs are UGC-DEB and AICTE approved, and SRM Institute of Science and Technology is a deemed university with a NAAC A++ accreditation — the highest grade possible.",
    },
    {
        "question": "Can I pursue an SRM Online degree alongside a full-time program?",
        "answer": "Per UGC guidelines, students are permitted to pursue one full-time (offline) degree and one online degree simultaneously — this is a general UGC policy, not specific to SRM.",
    },
    {
        "question": "Is SRM University the same as SRM Institute of Science and Technology?",
        "answer": "Yes. The institution was known as SRM University until 2017, when it officially reverted to SRM Institute of Science and Technology following a UGC order. Many people still refer to it informally as SRM University.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** SRM Online — NAAC A++ UGC-DEB Approved Online Degrees | CampusUnlock
- **Meta description:** Explore SRM Online's NAAC A++ accredited, UGC-DEB and AICTE approved MBA, MCA, BBA, and BCA programs from a deemed university with 40 years of academic history.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC grade is the most confidently-verified fact found in this batch** — official government filing (3.55) matches every other source unanimously. Safe to seed with high confidence.
2. **Minor internal SRM discrepancy** (3.55 vs 3.58 for the same accreditation cycle, across two official SRM sub-domains) — doesn't affect the letter grade, low priority.
3. **NIRF ranking trajectory is plausible but the most recent figure (12th, 2024) is aggregator-only** — the official filing I found only covers through ~2021-22. Confirm the current rank before publishing.
4. **Established year (1985) and deemed-university status (2002) are unanimous** — clean new-fact population, no DB conflict since the field was empty.
5. **Name-history note**: many sources still say "SRM University" informally — your DB already uses the correct current legal name, which is good.
