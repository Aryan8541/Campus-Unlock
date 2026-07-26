# NMIMS Online — Detail Page Content
*(NMIMS Global Access School for Continuing Education / NMIMS CDOE)*

> **Read this first:** every fact below is sourced from either NMIMS's own site (`online.nmims.edu`) or education-info aggregators (CollegeDekho, Careers360, PaGaLGuY, SelectYourUniversity, SearchUrCollege). Where sources genuinely disagreed, I've flagged it instead of picking a number — see **⚠️ Flags** at the end. Anything I couldn't verify at all (placement %, specific recruiters, scholarship amounts) is left blank rather than invented, per your standing rule on this project.

---

## Hero

- **Name:** NMIMS Online (NMIMS Global Access School for Continuing Education)
- **City / State:** Mumbai, Maharashtra
- **Type:** Deemed-to-be University (Section 3, UGC Act 1956) — online/distance arm of SVKM's NMIMS
- **Tagline:** *India's largest UGC-DEB approved online university for management education*

## About

NMIMS Online is the distance and online learning school of SVKM's NMIMS, a deemed-to-be university under Section 3 of the UGC Act, 1956. Originally launched as NGASCE (NMIMS Global Access School for Continuing Education), it now also operates as NMIMS CDOE (Centre for Distance and Online Education). It offers UGC-DEB approved undergraduate, postgraduate, diploma, and certificate programs — primarily in management, finance, and business analytics — aimed at working professionals who can't attend a full-time campus program.

## Highlights

- UGC-DEB approved, NAAC accredited
- Deemed-to-be University status (Section 3, UGC Act 1956)
- Online MBA/PGDM does not require CAT/NMAT/GMAT — admission is merit-based on prior academic marks
- 800+ hours of live faculty-led sessions (per NMIMS's own site)
- Dedicated digital library (journals, case studies, whitepapers)
- Career services offered specifically to online/distance students and alumni

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC-DEB | ✅ Approved | High — consistent across every source, including official site |
| UGC (Section 3, deemed university) | ✅ Yes | High — official + multiple aggregators |
| NAAC | ✅ Accredited | Grade conflicts — see ⚠️ Flags |
| AICTE | Not confirmed | No source mentioned this for the online arm specifically — leave unset, don't assume |
| AIU membership | Not confirmed | No direct citation found — leave unset |
| WES recognition | Not confirmed | No source mentioned this — leave unset |

## Rankings

⚠️ One aggregator (CampusIQ) cited **NIRF #22 (Management)** — I could not independently verify this against the official NIRF results portal, so I'm not confident enough to publish it as fact. Recommend confirming directly at nirfindia.org before adding a ranking number to the live page.

## Programs, Fees & Eligibility

*(Programs already following your existing `PROGRAM_DEFS` shape — duration/fees ranges below are what's publicly quoted; exact current fees should be pulled from the official fee page before publishing, since sources gave different ranges.)*

| Program | Duration | Eligibility | Publicly quoted fee range |
|---|---|---|---|
| Online MBA | 2 years | Graduation in any discipline | ₹1.2L – ₹2.0L (total program cost cited as ₹2.4L–₹4.0L by one source, ₹75K–₹200K/yr by another — **range varies by source, confirm exact figure**) |
| Online PGDM | 2 years | Graduation in any discipline | Similar range to MBA (not separately confirmed) |
| Online MBA – FinTech | 2 years | Graduation in any discipline | Not separately confirmed |
| Online BBA | 3 years | Class 12 pass | Not confirmed in sources reviewed |
| Online BCom | 3 years | Class 12 pass | Not confirmed in sources reviewed |
| PG Diploma / Diploma / Certificate (various) | Varies | Varies by program (Class 10/12/UG, depending on level) | Not confirmed in sources reviewed |

## Admission Process

1. Register on the official NMIMS Online portal
2. Fill application form and select program
3. Submit required documents (see below)
4. Pay program fee (EMI options available via third-party financing, per one aggregator — not confirmed on the official site, so I haven't stated specific EMI terms)
5. Confirmation and onboarding to the student portal

## Documents Required

⚠️ **Not explicitly confirmed** in any source I found — this is the standard set typically required by comparable UGC-DEB programs, not something I verified specifically for NMIMS. Confirm the actual checklist with NMIMS admissions before publishing:
- 10th and 12th mark sheets
- Graduation degree/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

No specific NMIMS Online scholarship program (name, amount, or eligibility criteria) turned up in any source I checked. Rather than invent one, I'm leaving this section empty — matching the real `Scholarship` model shape below for whenever real data is available:

```python
# No verified NMIMS-specific scholarship found. Leave university_id-linked
# scholarships empty for NMIMS unless/until real data is sourced — do NOT
# reuse the generic "Merit Scholarship" fallback as if it were NMIMS-specific.
```

## Placements

⚠️ One lower-tier aggregator (SelectYourUniversity) claimed "~85% placement" and named TCS/Deloitte as recruiters. This wasn't corroborated by any other source, including NMIMS's own site, so I'm **not** carrying it into `highest_package`, `average_package`, or `top_recruiters`. What I can confirm:

- `placement_support`: **True** — multiple independent sources (including the official site) describe dedicated career services for online students/alumni as a genuine, stated feature.
- `highest_package` / `average_package`: leave `None` — no reliable figure found.
- `top_recruiters`: leave empty — the only named companies came from one unverified aggregator.

## Learning Methodology

- 100% online delivery, live + recorded sessions
- 800+ hours of live lectures (per official site)
- KSA (Knowledge–Skill–Attitude) framework structuring the curriculum
- Digital library access (case studies, journals, whitepapers)
- Mobile app + web portal for content delivery

## FAQs

```python
faqs = [
    {
        "question": "Is the NMIMS Online degree equivalent to the on-campus degree?",
        "answer": "Yes. NMIMS Online programs are UGC-DEB approved, and the degree carries the same NMIMS University name as the on-campus program.",
    },
    {
        "question": "Do I need to take CAT, NMAT, or GMAT for the Online MBA?",
        "answer": "No. Admission to NMIMS Online's MBA/PGDM programs is merit-based on your prior academic marks — entrance exams are not required. (Note: this differs from NMIMS's on-campus MBA, which does require NMAT.)",
    },
    {
        "question": "Is NMIMS Online UGC approved?",
        "answer": "Yes. NMIMS Online programs are approved by the UGC's Distance Education Bureau (UGC-DEB), and NMIMS itself is a deemed-to-be university under Section 3 of the UGC Act, 1956.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** NMIMS Online — UGC-DEB Approved Online MBA & BBA | CampusUnlock
- **Meta description:** Explore NMIMS Online's UGC-DEB approved MBA, PGDM, and BBA programs — no entrance exam required, deemed-university degree, 100% online delivery.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC grade conflict:** the official site (`online.nmims.edu/about`) title says "NAAC A++," but Careers360, CollegeDekho, and SearchUrCollege all independently cite **"NAAC A+ with a 3.59 CGPA."** Your existing database already has `"NAAC A+"` recorded for NMIMS — given three independent aggregators agree with your existing value against one ambiguous official-site headline, I'd lean toward trusting what's already in your DB, but flagging so you can confirm directly with NMIMS if it matters for compliance.
2. **Established year conflict:** your DB has `established_year: 2007`. Sources instead describe 1994 (NGASCE founding), 1981 (parent trust SVKM), and 2003 (NMIMS granted deemed-university status). I did **not** change your existing value — but none of the sources I found actually said "2007," so it's worth tracing where that number originally came from.
3. **Student/alumni counts vary widely by source** (55,000–69,000 students; 9,500–12,500+ alumni) — likely just different snapshot dates from different aggregators, not something to hard-code without a current official figure.
4. **Placement %, package figures, and recruiter names** — deliberately left blank; only one low-quality source made these claims and I don't consider that reliable enough to publish.
