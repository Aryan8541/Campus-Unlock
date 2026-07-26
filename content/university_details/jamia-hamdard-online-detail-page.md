# Jamia Hamdard Online — Detail Page Content
*(Jamia Hamdard — Centre for Distance and Online Education / School of Open and Distance Learning)*

> Sourced from what appears to be the genuine official online portal (jamiahamdardonline.in) plus multiple aggregators (CareerHike, EdifyEdu, CosmosIQ/CampusIQ, DistanceEducationSchool, eDigitalUniversity, DegreeFyd, YugEdu, MyOnlineCollege). Cleaner and more clearly-confirmed than MIT-WPU — a genuine, broad UGC-DEB catalog exists here. One useful finding: a source-reliability pattern repeating from earlier in this project.

---

## Hero

- **Name:** Jamia Hamdard Online
- **City / State:** New Delhi, Delhi
- **Type:** Deemed-to-be University (Section 3, UGC Act 1956) — **your DB's existing "Deemed University" classification checks out correctly here**, unlike the MIT-WPU case
- **Tagline:** *UGC-DEB approved online degrees from a deemed university ranked #1 in Pharmacy nationally*

## About

Jamia Hamdard is a deemed-to-be university established in 1989 under Section 3 of the UGC Act, 1956, known nationally for its strength in pharmacy, Unani medicine, and health sciences — its School of Pharmaceutical Education and Research has been ranked #1 in India by NIRF across multiple years. Its Centre for Distance and Online Education (CDOE) / School of Open and Distance Learning offers a genuinely broad UGC-DEB approved catalog spanning management, commerce, computer applications, and humanities.

## Highlights

- **#1 in India for Pharmacy (NIRF), across multiple years** — very strongly corroborated, one of the most solid specific claims found in this entire project
- UGC-DEB approved, AICTE approved
- Deemed-to-be University under Section 3, UGC Act 1956 — well-corroborated, confirms your existing DB classification
- Broad, clearly-confirmed online catalog (unlike VISTAS or MIT-WPU, where the online offering itself needed real scrutiny)
- ⚠️ One source claims "Institute of Eminence" status — treat with real skepticism, see flags

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC (Section 3, deemed university) | ✅ Yes | High — consistent everywhere, with the specific legal citation |
| UGC-DEB | ✅ Approved | High — consistent across every source, including an explicit reference to being listed on deb.ugc.ac.in |
| AICTE | ✅ Approved | High — consistent |
| **NAAC** | **Genuinely mixed — roughly 4 sources say plain A, 4 say A+** | See the dedicated note below — this needed real analysis, not a simple majority count |

### NAAC grade — a closer look, not just a source tally

What appears to be the genuine official online portal (jamiahamdardonline.in — domain name matches the institution directly) says plain **"A."** One aggregator (CosmosIQ/CampusIQ) also says "A" but pairs it with a specific CGPA score of **3.80** — and NAAC's actual grading bands put 3.80 in the **A++** range (3.51-4.00), not plain A. This is the exact same type of error I caught for **Jain University earlier in this project — also from a CosmosIQ/CampusIQ-family source**, where a CGPA score was paired with a mismatched letter grade. Seeing this happen twice from the same aggregator family is a useful, generalizable finding: **treat this specific source's letter-grade labels with real skepticism whenever it also provides a CGPA score**, since the two don't appear to be reliably generated together. Given this, and that the official-looking portal's "A" claim doesn't come with a contradicting score, I'd lean toward plain **A** being correct, but flag this as genuinely less certain than most NAAC calls made in this batch.

## Rankings

Well-corroborated but split by year — presenting as a timeline:

| Year | NIRF Rank (University category) |
|---|---|
| 2024 | 40th (2 independent sources agree) |
| 2025 | 47th (2 independent sources agree) |
| Multiple years | **#1 in Pharmacy specifically** — very strongly corroborated |

A slight overall decline (40th → 47th) is plausible normal year-to-year NIRF variance, not necessarily an error. Since your DB's `ranking` field is empty, nothing existing to conflict with.

## Programs, Fees & Eligibility

**Broad, clearly-confirmed catalog** — much more clearly established as genuinely online than VISTAS or MIT-WPU:

| Program | Duration | Eligibility | Notes |
|---|---|---|---|
| Online MBA | 2 years | Graduation in any discipline, 50% marks | 7 specializations: Finance, Marketing, HRM, Operations, Data Science, Digital Marketing, International Business |
| Online MCA | 2 years | Bachelor's with relevant background | 1 specialization confirmed |
| Online MA | 2 years | Graduation in relevant/any discipline | 2 specializations |
| Online BBA | 3 years | Class 12 pass, 45-50% marks | — |
| Online BCA | 3 years | Class 12 pass with Math background | Data Science track mentioned |
| Online B.Com (Hons) | 3 years | Class 12 pass | Accountancy track mentioned |

⚠️ **Fees:** single source cites **₹75,000-₹1,80,000** depending on program — plausible, specific, but not confirmed against the official fee page.

## Admission Process

Standard online application, merit-based (no entrance exam mentioned), document verification, fee payment, LMS access — consistent with the pattern seen across nearly every genuinely UGC-DEB program in this project.

## Documents Required

⚠️ **Not explicitly itemized** by any source — standard expected set, same caveat as previous universities:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

No specific Jamia Hamdard Online scholarship (name, amount, eligibility) was found in any source reviewed. Leaving empty rather than inventing one:

```python
# No verified Jamia-Hamdard-Online-specific scholarship found. Leave
# university_id-linked scholarships empty unless/until real data is sourced.
```

## Placements

Only generic marketing language found ("top recruiters across government and private sectors worldwide") — no package figures or named companies in any source, so nothing to withhold or flag as suspicious here.

- `placement_support`: **True** — career advice sessions, resume writing, interview prep, and technical mentoring are described with real specificity across multiple sources.
- `highest_package` / `average_package`: leave `None` — no figure found.
- `top_recruiters`: leave empty — no company names found in any source.

## Learning Methodology

- LMS with 24/7 access to study materials
- Live and recorded lectures, semester-based structure
- Internal and proctored examinations
- Regular webinars and skill-development workshops

## FAQs

```python
faqs = [
    {
        "question": "Is a Jamia Hamdard Online degree valid?",
        "answer": "Yes. Jamia Hamdard Online programs are UGC-DEB approved, meaning the degree is equivalent to a regular on-campus degree for employment, higher education, and government/PSU recruitment.",
    },
    {
        "question": "What is Jamia Hamdard known for academically?",
        "answer": "Jamia Hamdard's School of Pharmaceutical Education and Research has been ranked #1 in India for Pharmacy by NIRF across multiple years, reflecting the university's particular strength in health sciences.",
    },
    {
        "question": "What programs does Jamia Hamdard Online offer?",
        "answer": "Jamia Hamdard Online offers UGC-DEB approved MBA (7 specializations), MCA, MA, BBA, BCA, and B.Com programs through its Centre for Distance and Online Education.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** Jamia Hamdard Online — UGC-DEB Approved Degrees | CampusUnlock
- **Meta description:** Explore Jamia Hamdard's UGC-DEB approved Online MBA, MCA, BBA, and BCA programs from a deemed university ranked #1 in Pharmacy by NIRF.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC grade genuinely uncertain, but for an interesting reason** — not just "sources disagree," but a specific, identified error pattern in one recurring source (CosmosIQ/CampusIQ pairing a CGPA score with the wrong letter grade — the same mistake I caught for Jain University earlier). Worth deprioritizing that specific source's letter-grade claims generally, not just for this one university.
2. **"Institute of Eminence" claim is single-sourced and worth real skepticism** — this is a specific, exclusive Government of India designation with a well-publicized, limited list, and I don't believe Jamia Hamdard is generally understood to be on it. Don't publish this without direct verification.
3. **Established year (1989) and deemed-university status are unanimous and well-corroborated**, including the specific Section 3 legal citation — clean, no DB conflict since the field was empty.
4. **NIRF #1 in Pharmacy is one of the strongest, most consistently-repeated specific claims found across this entire project** — high confidence.
5. Unlike MIT-WPU, **this university's online division is clearly and broadly confirmed as genuine** — no entity-confusion risk found here.
