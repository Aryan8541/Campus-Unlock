# Shoolini University Online — Detail Page Content
*(Shoolini Centre for Online and Distance Education / SCDOE)*

> Sourced from Shoolini's own official domain (shooliniuniversity.com) plus many aggregators (CollegeBatch, CollegesGyan, Shiksha, CollegeDunia, CareerBracket, EduCollege, AdmissionsPao) and a detailed Careers360 forum answer citing an exact UGC file reference number. Two real conflicts here — one very one-sided, one genuinely uncertain.

---

## Hero

- **Name:** Shoolini University Online
- **City / State:** Solan, Himachal Pradesh
- **Type:** Private University (established by an Act of the Government of Himachal Pradesh)
- **Tagline:** *Research-focused university offering UGC-DEB approved online degrees*

## About

Shoolini University is a private, research-focused university in Solan, Himachal Pradesh, established by a specific Himachal Pradesh state act. Its Centre for Online and Distance Education (SCDOE) offers UGC-DEB approved online undergraduate and postgraduate programs in management, computer applications, and commerce, drawing on the parent university's strong research reputation (11 research centers, 100+ laboratories, 1,500+ patents filed, per one source).

## Highlights

- **Established year is very strongly disputed against your DB** — see flags, this is nearly as one-sided as the VGU case
- NIRF rank **69th** (university category, 2025) — corroborated by 2 independent sources
- Strong, well-documented research output: 1,500+ patents filed, 11 research centers (single source, but specific)
- "Pay After Placement" MBA option claimed as "India's first" (single source, distinctive claim worth verifying)
- Faculty/mentor network drawing from IIMs, IITs, and international institutions (careful: this describes mentors, not recruiters — see Placements section)

## Approvals & Accreditations — ⚠️ genuinely mixed evidence on NAAC grade

| Approval | Status | Source confidence |
|---|---|---|
| UGC recognition | ✅ Yes — with exact file reference (F No. 8-1/2010(CCP)-1/PU, dated 7.2.2011) | Very high — cited precisely in a detailed, sourced forum answer pointing to the university's own recognitions page |
| UGC-DEB | ✅ Approved | High — consistent everywhere |
| **NAAC** | **Genuinely disputed — not a clear majority like VGU's case** | Mixed: 7+ aggregator sources say A+; **one detailed, specific source (Shiksha) explicitly states "NAAC accreditation with a B+ grade."** Notably, **Shoolini's own official recognitions page doesn't state a specific letter grade at all** — it only says "NAAC accreditation" without specifying A+, B+, or otherwise. That official silence, combined with one clear dissenting claim, means I can't resolve this the way I could for VGU (where the official site loudly and repeatedly claimed A+). This one is a genuine open question, not a likely data error. |
| AICTE | ✅ Approved (recognized private university list) | High — confirmed via the same detailed forum answer with file reference |
| ISO certified | Yes (9001:2015) | Confirmed on official domain |

## Rankings

Well-corroborated multi-year trajectory, similar in kind to UPES's real historical data:

| Year / Ranking body | Rank |
|---|---|
| NIRF 2025 (University category) | **69th** — agreed by 2 independent sources |
| NIRF 2024 | 70th overall, 92nd engineering, 30th pharmacy |
| NIRF 2023 | Top 100 band (vague); pharmacy 41st, engineering 101-150 band (per one detailed source) |
| Business Today 2023 (MBA category) | 88th — different ranking body, not NIRF |
| QS Asia 2024 | 39th (Southern Asia) |
| QS World 2024 / 2026 | 771-780 / 503rd |

⚠️ Your DB has `ranking: 45` — this doesn't match any of the several well-corroborated recent figures above (all cluster in the 65-101+ range depending on year/category). Worth updating, though which specific number to use depends on which year/category your `ranking` field is meant to represent.

## Programs, Fees & Eligibility

| Program | Duration | Eligibility | Notes |
|---|---|---|---|
| Online MBA (incl. Executive MBA) | 2 years | Graduation in any discipline | "Pay After Placement" option claimed (single source) |
| Online BBA | 3 years | Class 12 pass | — |
| Online BCA / MCA | 3 / 2 years | Standard IT eligibility | — |
| Online B.Com / M.Com / MA | Varies | Varies | — |

⚠️ **No specific fee figures found** — only "affordable fee structure" marketing language across sources.

## Admission Process

1. Visit the official portal (apply.shoolinionline.com)
2. Register and log in via mobile number
3. Fill details and pay a **₹500 application fee** (single source)
4. Complete document submission and verification

## Documents Required

⚠️ **Not explicitly itemized** by any source — standard expected set, same caveat as previous universities:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

No specific Shoolini Online scholarship (name, amount, eligibility) was found in any source reviewed. Leaving empty rather than inventing one:

```python
# No verified Shoolini-specific scholarship found. Leave university_id-linked
# scholarships empty unless/until real data is sourced.
```

## Placements

⚠️ **Important distinction to get right here.** One source lists "mentors from IIMs, IITs, HSBC, Stanford University, and ISB" — these are described as **faculty/mentor affiliations, not recruiters**. Don't let this get miscategorized as a recruiter list if this data gets processed later. Separately, on-campus collaborations with KPMG, LIBF, ICT Academy, and NHRDN are mentioned (CollegeDunia) — but for the **overall/on-campus university**, not confirmed specifically for the online division.

- `placement_support`: **True** — described consistently, including a distinctive "Pay After Placement" MBA option (single-sourced, but specific enough to be worth verifying rather than dismissing).
- `highest_package`: ⚠️ One source cites ₹42 LPA — but this is for the **overall/on-campus university**, not confirmed as an online-program figure. Do not use this for the online division's `highest_package` without separate confirmation.
- `average_package`: One online-specific source cites **₹5-12 LPA** — single-sourced, treat as unconfirmed.
- `top_recruiters`: leave empty — the specific names found (IIMs, IITs, HSBC, Stanford, ISB; separately KPMG, LIBF, ICT Academy, NHRDN) are either mentor affiliations or on-campus-specific, not verified online-division recruiters.

## Learning Methodology

- Live weekend sessions, recorded lectures, value-added courses
- 24/7 LMS access
- Faculty/mentor network from top institutions (see caveat above — mentors, not recruiters)

## FAQs

```python
faqs = [
    {
        "question": "Is a Shoolini University Online degree valid?",
        "answer": "Yes. Shoolini University Online programs are UGC-DEB approved, making the degree valid for jobs and further study, at par with on-campus programs.",
    },
    {
        "question": "What is Shoolini University's NIRF ranking?",
        "answer": "Shoolini University was ranked 69th in the University category in NIRF 2025, continuing an improving trend from recent years.",
    },
    {
        "question": "Is Shoolini University research-focused?",
        "answer": "Yes. Shoolini University has a strong research reputation, with over 1,500 patents filed and 11 dedicated research centers across its campus.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** Shoolini University Online — UGC-DEB Approved, NIRF-Ranked Degrees | CampusUnlock
- **Meta description:** Explore Shoolini University Online's UGC-DEB approved MBA, BBA, and MCA programs from a research-focused university ranked 69th in NIRF 2025.

---

## ⚠️ Flags — things to double-check before publishing

1. **Established year — nearly as one-sided a conflict as VGU's.** Your DB has `2015`. **Nine independent sources — including Shoolini's own official domain and a precisely-cited UGC file reference — all say the university was set up in 2009.** No source anywhere supports 2015. This looks like a near-certain data error worth prioritizing alongside the VGU NAAC fix.
2. **NAAC grade — genuinely uncertain, unlike most conflicts in this batch.** Your DB currently says A+, matching the majority of aggregators. But one specific, detailed source says B+, and — notably — Shoolini's own official recognitions page avoids stating a letter grade at all, which is unusual for a university with a genuinely good grade to advertise. I'd treat this as worth a direct check with Shoolini rather than trusting either side confidently.
3. **Ranking conflict:** DB has `45`; well-corroborated recent figures (69-70, 2024-2025) don't match. Worth updating, but pin down which specific year/category your field should represent first.
4. **Don't conflate on-campus and online-specific placement/package figures** — the ₹42 LPA highest package and several named recruiters found in sources are for the overall university, not confirmed for the online division specifically.
