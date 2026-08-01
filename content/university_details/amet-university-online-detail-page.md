# AMET University Online — Detail Page Content
*(AUOL — AMET University Online Learning)*

> Sourced from AMET's own official domains (ametuniv.ac.in, and what appears to be a genuine dedicated online portal, auol.in) plus Wikipedia and multiple aggregators (CollegeDekho, CollegeBatch, CollegeDunia, Dial4College, Eduquanta, WingEducations, EntranceZone). AMET has a genuinely distinctive institutional identity — India's only deemed university dedicated exclusively to maritime education — which shows up consistently and helps cross-check other claims.

---

## Hero

- **Name:** AMET University Online (Academy of Maritime Education and Training)
- **City / State:** Chennai (Kanathur, East Coast Road), Tamil Nadu
- **Type:** Deemed-to-be University (Section 3, UGC Act 1956) — **confirms your DB's existing "Deemed University" classification correctly**
- **Tagline:** *India's only maritime-focused deemed university, now offering UGC-entitled online business degrees*

## About

AMET (Academy of Maritime Education and Training) is India's first and only deemed-to-be university dedicated exclusively to maritime education, established in 1993 with just 14 cadets in a marine engineering diploma program. Its Centre for Distance and Online Education (CDOE), branded as AUOL (AMET University Online Learning), extends this identity into online business programs — notably including a BBA with a Shipping specialization, a genuinely distinctive offering that reflects the parent university's real character rather than a generic catalog.

## Highlights

- **India's only deemed university exclusively for maritime education** — well-corroborated, genuine institutional distinctiveness
- Sole Indian member of the International Association of Maritime Universities (IAMU)
- DG Shipping approval and IMO STCW Convention compliance for maritime programs
- **Online BBA specifically offers a Shipping specialization** — a distinctive, institutionally-authentic program choice, alongside more standard HR, Finance, and Supply Chain Management tracks
- Unusually low, specific online program fees found (see Programs section) — notably lower than most universities in this project

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC (Section 3, deemed university) | ✅ Yes | High — consistent everywhere |
| AICTE | ✅ Approved | High — consistent |
| AIU member | ✅ Yes | High — confirmed by 2 sources |
| DEB (Distance Education Bureau) | ✅ Approved | Medium — confirmed by one source specifically for CBCS-based distance courses |
| **NAAC** | **Likely A (2021 cycle)** | Medium-high — two independent sources agree on the exact same accreditation date (13 September 2021), which is stronger evidence than most date claims in this project, though they disagree on the validity period (one says 5 years, one says 1 year). One older/less-specific source says grade "B" instead — possibly an earlier cycle or a simple error. |

## Rankings

Only program-specific NIRF figures were found (Marine Engineering: 201st; overall university: 251-300 band, 2022) — no confirmed figure specifically for the online business catalog. Since your DB's `ranking` field is empty, nothing existing to conflict with, but these figures describe on-campus maritime programs, not the online BBA/MBA/B.Com catalog.

## Programs, Fees & Eligibility

**Genuinely distinctive, clearly-confirmed online catalog** directly from what appears to be AMET's official online portal:

| Program | Duration | Specializations | Fee (per source) |
|---|---|---|---|
| Online BBA | 3 years | Shipping, HR Management, Finance, Supply Chain Management | **₹9,000/semester** |
| Online B.Com | 3 years | Commerce, Accounting & Finance, Logistics, Computer Applications, Digital Marketing | **₹7,000/semester** |
| Online MBA | 2 years | Not itemized in the source | Not specified |

⚠️ These fee figures are notably specific (exact rupee amounts, not vague ranges) but single-sourced — still worth confirming against the current official fee page, though the specificity is a good sign compared to most fee claims in this project.

## Admission Process

Standard online application via the AUOL portal; no detailed step-by-step found.

## Documents Required

⚠️ **Not explicitly itemized** by any source — standard expected set, same caveat as previous universities:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

One source mentions AMET "assisting deserving students for scholarships given by various Government Departments" — vague, and describes the general/on-campus university, not confirmed for the online catalog specifically:

```python
# UNVERIFIED for the online division — general government-department
# scholarship assistance is mentioned for AMET broadly, not confirmed as
# online-specific terms. Leave university_id-linked scholarships empty
# unless/until real online-specific data is sourced.
```

## Placements

⚠️ **Important distinction to maintain here.** Sources give genuinely specific, institutionally-plausible maritime recruiters — **Shipping Corporation of India, Maersk, MSC, Evergreen, MOL, Anglo-Eastern** — but these are explicitly for **on-campus Marine Engineering and Nautical Science programs**, not the online BBA/MBA/B.Com catalog. A separate "93% placement or further study within six months" claim on the official site is general marketing language for the university overall, not online-specific.

- `placement_support`: AUOL's own page confirms "a dedicated placement cell to assist students with job opportunities" specifically for online graduates — **True**, with reasonable confidence since this is genuinely scoped to the online division.
- `highest_package` / `average_package`: leave `None` — the ~₹4 LPA figure found is for on-campus Marine Engineering, not the online catalog.
- `top_recruiters`: leave empty for the online-specific record — the maritime shipping companies named are for on-campus maritime programs, not the online business catalog. Don't conflate the two.

## Learning Methodology

- Delivered via online learning platform with video lectures, live sessions, and interactive materials
- Centre for Distance and Online Education (CDOE) manages program delivery

## FAQs

```python
faqs = [
    {
        "question": "Is AMET University Online the same as AMET's maritime programs?",
        "answer": "No. AMET University Online (AUOL) offers business programs — BBA, B.Com, and MBA — distinct from AMET's on-campus maritime engineering and nautical science programs, though the university is the same deemed institution.",
    },
    {
        "question": "Does AMET University Online offer any maritime-specific specializations?",
        "answer": "Yes. The Online BBA includes a Shipping specialization, alongside HR Management, Finance, and Supply Chain Management tracks — reflecting AMET's institutional identity as India's only maritime-focused deemed university.",
    },
    {
        "question": "Is AMET a deemed university?",
        "answer": "Yes. AMET (Academy of Maritime Education and Training) is a Deemed-to-be University under Section 3 of the UGC Act, 1956 — India's only deemed university dedicated exclusively to maritime education.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** AMET University Online — UGC-Entitled Online BBA, B.Com & MBA | CampusUnlock
- **Meta description:** Explore AMET University's UGC-entitled online BBA, B.Com, and MBA programs — including a distinctive Shipping specialization from India's only maritime-focused deemed university.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC grade needs verification**, but with unusually specific evidence to check against: two sources agree precisely on a 13 September 2021 accreditation date and "A" grade, but disagree on the validity period (5 years vs. 1 year) — worth confirming both the grade and the actual current validity directly.
2. **Established year has minor variance** (1992 vs. 1993) and the deemed-university-status grant year has a real conflict (2005 vs. 2007 between two sources) — neither is a major concern, but worth noting rather than picking one silently.
3. **Don't conflate on-campus maritime placement data with the online business catalog** — the well-corroborated shipping-company recruiter list is for a completely different program set than what's actually offered online.
4. **The online fee figures (₹9,000 and ₹7,000 per semester) are unusually low compared to every other university in this project** — worth double-checking these are current and complete (not missing additional charges), given how much lower they are than typical figures found elsewhere.
