# GLA University Online — Detail Page Content

> Sourced from GLA's own online platforms (glaonline.com, glaonline.in) plus multiple independent aggregators (CollegeVidya, BoostMyTalent, Samarth Edu, AdmissionDIY, HikeEducation, EducationMitra, TopGradLearning, CollegeDunia, CollegeDekho) and Wikipedia (for the parent GLA University, Mathura). Where sources disagreed, flagged rather than picked — see **⚠️ Flags** at the end.

---

## Hero

- **Name:** GLA University Online
- **City / State:** Mathura, Uttar Pradesh
- **Type:** Private University (per Wikipedia's infobox; UGC-affiliated, not deemed) — established year is genuinely disputed, see flag
- **Tagline:** *UGC-DEB approved, NAAC A+ accredited online degrees from a private university in Mathura*

## About

GLA University Online is the online-learning arm of GLA University (Ganeshi Lal Agrawal University), a private university in Mathura, Uttar Pradesh, delivered through the university's Centre for Distance and Online Education — one source dates this specific online/distance wing's launch to 2022, separate from the parent university's much older founding. GLA Online offers a compact catalog of five online programs: B.Com, BBA, BCA, MBA, and MCA.

## Highlights

- UGC-DEB approved (recognized under UGC 12(B) and 2(f), per one source) and AICTE approved — consistent across sources
- NAAC A+ accredited (most current sources); one older source (CollegeVidya) rates it plain 'A' — likely an outdated figure but not confirmed
- WES recognition cited by one source, not corroborated elsewhere
- A university-branded marketing page (glaonline.in) claims "90% placement rate, 3000+ hiring partners" — a striking, high-confidence-sounding figure that directly conflicts with other sources (see flags); treat the 90%/3000+ figures with real skepticism given they appear only on what looks like a promotional landing page, not the main official CDOE site
- ⚠️ **Direct contradiction on scholarships found between two GLA-branded domains** — see flag; this is unusual and worth resolving carefully

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC-DEB | ✅ Approved | High — consistent everywhere |
| NAAC | Mostly A+ | Medium-high — most sources say A+; one says plain 'A' |
| AICTE | ✅ Approved | High — consistent across sources |
| WES | Claimed | Low — single-source claim, not corroborated |

## Rankings

- NIRF 2025 Overall: 101–150 band (multiple sources agree)
- NIRF Pharmacy category: cited as both 48th and 53rd by two different sources — a minor but real conflict, likely reflecting different years (2024 vs. 2025) rather than a genuine discrepancy
- NIRF MBA-specific ranking: cited as both 54th (two sources, for different years — 2025 and 2026) — internally consistent
- ⚠️ As with every other university researched, none of these rankings are confirmed as specific to the online programs

## Programs, Fees & Eligibility

| Program category | Duration | Eligibility | Fees |
|---|---|---|---|
| UG (BBA, BCA, B.Com) | 3 years | Class 12 pass | Conflicting figures — see flag |
| PG (MBA, MCA) | 2 years | Bachelor's degree, min. 50% marks for MBA (MCA appears to require only a passing grade, per one source) | Conflicting figures — see flag |

⚠️ **Fee figures conflict, most sharply for MCA**:
- MBA: ₹97,000 total (two independent sources) vs. "around ₹1.1 lakh" (a third) — these are reasonably close and can be treated as roughly consistent
- MCA: ₹87,000 total (BoostMyTalent) vs. ₹43,500 total (AdmissionDIY) — almost exactly a 2x difference, a genuine unresolved conflict
- BBA: ₹91,000 (one source)
- BCA: ₹91,000 (one source) — note this figure is identical to the BBA figure from the same source, which may indicate a templated/generic figure rather than a program-specific one
- B.Com: ₹64,000 (one source)

Recommend verifying all figures directly against glaonline.com before publishing.

## Admission Process

1. Apply online via the official portal (glaonline.com)
2. Pay the non-refundable application fee (cited as both ₹1,000 and ₹1,500 by different sources — minor conflict)
3. Admission is merit-based (Class 12 marks for UG; graduation marks for PG)
4. Submit required documents
5. Fee payment, with installment/EMI options and no-cost EMI via financial-service partners, per the official site
6. Enrollment confirmation and LMS access

## Documents Required

⚠️ **Not explicitly itemized** by any source reviewed — same caveat as the other universities in this batch. Standard expected set, not verified specifically for GLA Online:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

⚠️ **Direct, sharp contradiction found here, unlike any other university in this research batch.** The university's own domain, glaonline.com, states in an FAQ: *"No. Currently, GLA Online does not offer merit-based scholarships... one-time fee payment carries special benefits [instead]."* Meanwhile, two independent third-party aggregators (BoostMyTalent and AdmissionDIY) both state GLA University Online "provides scholarships and fee benefits to eligible students." This isn't a minor figure disagreement — it's a flat contradiction on whether a scholarship program exists at all, and it comes from what appears to be the university's own official FAQ page versus third-party marketing content.

```python
# CONTRADICTION: glaonline.com's own FAQ explicitly denies offering
# merit-based scholarships (offering only a one-time-payment fee benefit
# instead). Two independent third-party aggregators claim scholarships
# ARE offered. Given the direct conflict with what appears to be the
# university's own official statement, do NOT list a scholarship program
# for GLA Online without confirming directly with the university first.
# Leaving university_id-linked scholarships empty pending that confirmation.
```

## Placements

⚠️ **Placement figures vary enormously and don't reconcile**:
- A GLA-branded marketing page (glaonline.in) claims "90% placement rate, 3000+ hiring partners"
- A separate aggregator (Samarth Edu) states "a placement record of over 75%... for academic session 2023-24," with an average package of ₹6.5 LPA
- Neither figure is confirmed against what looks like the primary CDOE site (glaonline.com), and the 3000+ hiring-partner figure in particular is far larger than any comparable claim found for any other university in this entire research batch (the next-highest was 500+ for SMU) — this warrants real skepticism rather than being taken at face value
- Named recruiters cited: Microsoft, Amazon, TCS, Capgemini, Infosys, Wipro, HCL, Samsung, Flipkart, Reliance, DHL — a long list, but not clearly distinguished between on-campus and online-program-specific recruitment in any source

- `placement_support`: **True** — described across multiple sources, though the specific numbers are unreliable.
- `highest_package` / `average_package`: leave `None` — the one specific figure found (₹6.5 LPA average) is not corroborated and conflicts with the "90%" marketing claim's implied strength.
- `top_recruiters`: leave empty, or use with low confidence — no source clearly confirms these are online-program-specific rather than generic on-campus recruiter lists.

## Learning Methodology

- 100% online delivery via a "digital platform" with live sessions, recorded video lectures, e-study materials, quizzes, and assignments
- Guest lectures from industry experts, on-the-job training opportunities, and group projects mentioned by one source — these sound more like on-campus-style program descriptions and are not clearly confirmed as actually delivered to fully-online students

## FAQs

```python
faqs = [
    {
        "question": "Is a GLA University Online degree valid and recognized?",
        "answer": "Yes. GLA University Online is UGC-DEB approved, and the university holds NAAC A+ accreditation (some older sources cite a plain 'A' grade, likely outdated).",
    },
    {
        "question": "Does GLA University Online offer scholarships?",
        "answer": "This is currently unclear. The university's own FAQ page states no merit-based scholarships are offered, while some third-party sources claim scholarships are available. Confirm directly with the university before assuming eligibility for a scholarship.",
    },
    {
        "question": "What programs does GLA University Online offer?",
        "answer": "GLA University Online offers five programs: B.Com, BBA, BCA, MBA, and MCA, each with several specialization options.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source; scholarship language deliberately omitted given the unresolved contradiction above)*

- **Meta title:** GLA University Online — UGC-DEB Approved Online Degrees | CampusUnlock
- **Meta description:** Explore GLA University Online's UGC-DEB approved, NAAC A+ accredited MBA, MCA, BBA, BCA, and B.Com programs from a private university in Mathura.

---

## ⚠️ Flags — things to double-check before publishing

1. **Scholarship contradiction is the top priority here**: the university's own site denies offering merit scholarships; two independent aggregators say scholarships exist. Resolve this directly with GLA before publishing anything about scholarships.
2. **Placement statistics are wildly inconsistent** ("90% / 3000+ hiring partners" on one GLA-branded page vs. "75%... ₹6.5 LPA average" on a third-party aggregator) — the 3000+ figure is far outside the range seen for any comparable university in this research batch and should be treated with particular skepticism.
3. **MCA fee conflicts by roughly 2x** (₹87,000 vs. ₹43,500) — needs direct verification.
4. **Established year is genuinely disputed**: sources variously cite 1988, 1991, 1998, and 2010 (the last being when UGC granted university status, per Wikipedia) — a wider spread than any other university in this or the prior research batch. Needs careful disambiguation between "founding of the parent trust/college" and "grant of university status."
5. **BBA and BCA fees are identical (₹91,000) in the same source** — possibly a templated/non-program-specific figure rather than an accurate breakdown; worth double-checking against the official fee page.
6. Application fee cited as both ₹1,000 and ₹1,500 — minor conflict, worth a quick check.
