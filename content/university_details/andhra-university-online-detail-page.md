# Andhra University Online — Detail Page Content

> Sourced from Andhra University's own domains (andhrauniversity.edu.in, andhrauniversityonline.in, onlineausde.andhrauniversity.edu.in) plus multiple independent aggregators (CampusIQ, Careers360, Samarth Edu, DistanceEducationSchool, Vidyarishi, AdmissionDIY, BoostMyTalent, Collegedunia) and Deccan Chronicle / Shiksha (for the parent Andhra University, Visakhapatnam). Where sources disagreed, flagged rather than picked — see **⚠️ Flags** at the end.

---

## Hero

- **Name:** Andhra University Online
- **City / State:** Visakhapatnam, Andhra Pradesh
- **Type:** Public State University (established 1926 under the Madras Act; not a deemed or private university)
- **Tagline:** *UGC-DEB approved, NAAC A++ accredited online degrees from one of India's oldest state universities*

## About

Andhra University Online is the online-learning arm of Andhra University, a public state university in Visakhapatnam established in 1926. The university runs its online programs through a dedicated portal (onlineausde.andhrauniversity.edu.in), separate from its older, legacy School/Directorate of Distance Education (est. 1972), which still runs its own distance-mode offerings — see flag on this distinction. Andhra University Online currently focuses on a smaller set of UGC-DEB approved online degrees in commerce, arts, management, and computer applications.

## Highlights

- UGC-DEB approved — consistent across every source reviewed
- NAAC A++ accredited (most-cited figure; one source gives a CGPA of 3.60 — see flags on the specific score)
- AICTE approval also claimed by some sources for MBA/MCA — see flags, not universally corroborated
- Compact, focused catalog (roughly 6–8 online programs) rather than a large multi-program catalog
- Merit-based admission, no entrance exam for the online mode
- Education loan / EMI option via a third-party lending partner (CampusCredit™ by CosmosIQ) mentioned on one aggregator only — not an official Andhra University Online feature, flagged accordingly

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC-DEB | ✅ Approved | High — consistent everywhere |
| NAAC | ✅ A++ | High — cited by nearly every source; one cites a CGPA score of 3.60 specifically (not corroborated elsewhere) |
| AICTE | Mixed | Medium — cited by some aggregators (e.g., for MCA/MBA), not mentioned by others; AICTE approval is unusual for a purely online/distance program, so this needs direct verification |
| WES / international recognition | Not found | — no source claims this for the online arm specifically |

## Rankings

⚠️ **No online-arm-specific ranking found anywhere.** All NIRF figures found are for the *parent, on-campus* Andhra University, and none should be conflated with the online programs:
- NIRF 2025: Overall rank 41, University category rank 23, State Public University category rank 4 (Careers360, Shiksha)
- NIRF 2024: Overall rank 41 (up from 76 the prior year), University category rank 25, 7th among "newly established state universities" (Deccan Chronicle)
- These figures fluctuate year to year across sources and refer to the whole university (engineering, sciences, etc.), not the online degree programs

Recommend leaving any `ranking` field for the online arm unset, or clearly labeling any published figure as "parent university, not online-program-specific" — same caution as Amity's flagged ranking mismatch.

## Programs, Fees & Eligibility

| Program category | Duration | Eligibility | Fees |
|---|---|---|---|
| UG (BA, B.Com) | 3 years | Class 12 pass | Conflicting figures — see flag |
| PG (MBA, MCA, M.Com, MA Sociology) | 2 years | Graduation in relevant/any discipline (varies by program), min. 50% marks | Conflicting figures — see flag |

⚠️ **Fee figures conflict significantly across sources** and none is confirmed against the official fee page:
- One aggregator: total UG/PG fees "starting ~₹15,000"
- Another (Careers360): total fees ₹19,700–₹28,100 across 2–3 year UG/PG programs
- Another: ₹31,000–₹45,000 for UG & PG online courses
- Another: ₹50,000–₹70,000 for the "whole course"
- MBA specifically: ₹14,300/semester (one source), ₹16,300/semester (another), or a stated total of ₹62,200 across 4 semesters (a third) — these do not reconcile with each other
- Separately, the older/legacy distance-mode MBA (School of Distance Education, est. 1972) is quoted at a flat ₹35,000 total — this appears to be a *different, older program* from the current Online AUSDE portal and should not be conflated with it

Recommend pulling exact current fees directly from onlineausde.andhrauniversity.edu.in per program before publishing any number.

## Admission Process

1. Apply online via the official portal (andhrauniversityonline.in or onlineausde.andhrauniversity.edu.in)
2. Pay the non-refundable application fee (₹1,000 per most sources)
3. Select program and complete the registration form
4. Upload required documents
5. Fee payment (semester-wise or annual, per one source; installment/EMI options not confirmed on an official page)
6. Enrollment confirmation, LMS access provided

## Documents Required

⚠️ **Not explicitly confirmed on an official Andhra University Online page** — same caveat as Amity. Standard expected set, compiled from aggregators, not verified specifically for AU Online:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Transfer/migration certificate
- Government photo ID
- Passport-size photograph

## Scholarships

One aggregator (BoostMyTalent) explicitly states: *"No scholarship information is officially mentioned for the online division."* No other source contradicts this. Leaving this empty rather than inventing one — same approach as Amity:

```python
# No verified Andhra University Online-specific scholarship found. Leave
# university_id-linked scholarships empty unless/until real data is sourced.
# Note: the parent campus university does offer general scholarships
# (e.g., state government schemes, UGC fellowships) but these are not
# confirmed as available to online-mode students specifically.
```

## Placements

⚠️ **Nearly all placement data found (top recruiters, packages, hiring-partner counts) is for the on-campus/regular Andhra University — not the online arm specifically.** No source gives placement statistics, hiring-partner counts, or package figures for Andhra University Online students. One aggregator explicitly notes dedicated EMI/placement infrastructure is "not officially highlighted" for the online division.

- `placement_support`: Leave unset / **False** — no source confirms dedicated placement infrastructure for the online programs specifically, unlike Amity where multiple independent sources described genuine online-specific career support.
- `highest_package` / `average_package`: leave `None` — all figures found (e.g., ₹12 LPA highest, ₹4 LPA average) are for the on-campus university.
- `top_recruiters`: leave empty — recruiter names found (IBM, HDFC Bank, Accenture, Infosys, etc.) are for on-campus placements, not confirmed for the online arm.

## Learning Methodology

- 100% online delivery via LMS
- Online examinations, described as a mix of MCQs, short and long answer questions, and assignments
- No mention of live/recorded session split, international faculty, or an AI learning assistant in any source reviewed — leaving these unconfirmed rather than assuming Amity-style features apply here too

## FAQs

```python
faqs = [
    {
        "question": "Is an Andhra University Online degree valid and recognized?",
        "answer": "Yes. Andhra University Online is UGC-DEB approved, and the university is NAAC A++ accredited. Online degrees are treated as equivalent to regular mode degrees for employment purposes.",
    },
    {
        "question": "Is Andhra University a private or deemed university?",
        "answer": "No. Andhra University is a public state university, established in 1926, and is not a deemed-to-be or private university.",
    },
    {
        "question": "What programs does Andhra University Online offer?",
        "answer": "Andhra University Online offers a focused set of UG and PG programs, including BA, B.Com, MA (Sociology), M.Com, MBA, and MCA.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** Andhra University Online — UGC-DEB Approved Online Degrees | CampusUnlock
- **Meta description:** Explore Andhra University Online's UGC-DEB approved, NAAC A++ accredited BA, B.Com, MBA, and MCA programs from one of India's oldest state universities.

---

## ⚠️ Flags — things to double-check before publishing

1. **Fee figures conflict heavily** across at least five sources, ranging from "starting ₹15,000" to "₹50,000–₹70,000 total," with MBA-specific figures also disagreeing (₹14,300 vs ₹16,300 per semester vs ₹62,200 total). None is confirmed against the official fee page — do not publish a single figure without verifying directly.
2. **Two distinct online/distance programs may be getting conflated**: the newer "Online AUSDE" portal (onlineausde.andhrauniversity.edu.in) versus the older School of Distance Education (est. 1972, ₹35,000 flat MBA fee). Confirm which one is being profiled before publishing.
3. **No ranking, placement statistic, or hiring-partner count found anywhere is specific to the online arm** — all such figures found in research pertain to the on-campus university and should not be attributed to Andhra University Online.
4. **AICTE approval** is claimed by some sources (notably for MBA/MCA) but not corroborated by others — worth confirming directly, as AICTE approval alongside a purely online/distance delivery mode is unusual and worth double-checking.
5. **NAAC A++ with a CGPA of 3.60** is cited by exactly one source; the grade itself (A++) is well-corroborated but the specific score is not.
6. Established year (1926), UGC-DEB approval, and public-state-university status are well-corroborated and consistent — no changes needed there.
