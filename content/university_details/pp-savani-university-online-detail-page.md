# P P Savani University Online — Detail Page Content
*(PPSU — Centre for Distance and Online Education)*

> ⚠️ **Read the NAAC section before anything else in this file.** This university has the single most extreme, unresolved accreditation-grade conflict found across this entire project — worse than the genuinely-uncertain Shoolini case, and different in kind from the clean chronology-resolvable cases (VISTAS, Bharati Vidyapeeth, JSS AHER). I'm not resolving this one; it needs direct verification before anything gets published.

---

## Hero

- **Name:** P P Savani University Online (PPSU)
- **City / State:** Surat (Dhamdod, Kosamba), Gujarat
- **Type:** Private University (established under the Gujarat Private Universities (Amendment) Act, 2017) — matches your DB's existing "Private University" classification
- **Tagline:** *A newer Gujarat private university with a small, developing online catalog*

## About

P P Savani University (PPSU) is a private university in Surat, established in 2017 under a specific Gujarat state legislative act, run by the PP Savani Group. It offers a wide range of on-campus programs (engineering, architecture, nursing, pharmacy, and more) and has recently begun offering online programs through its Centre for Distance and Online Education (CDOE) — though the exact size of that online catalog is itself disputed across sources (see flags).

## Highlights

- Established 2017, well-corroborated including the specific legislative act citation
- ⚠️ **NAAC grade is genuinely unresolved — see the dedicated section below before treating any grade as fact**
- ⚠️ **Online program count is disputed**: one source says only 2 programs currently exist (MBA + M.Sc Data Science); another vaguely claims 10, without naming them
- 17+ international collaborations claimed (single source, on-campus context)

## Approvals & Accreditations — ⚠️ major unresolved conflict

| Approval | Status | Source confidence |
|---|---|---|
| UGC | ✅ Recognized | High — consistent everywhere |
| AICTE | ✅ Approved | High — consistent |
| PCI / INC / COA / GNC / NCH / GSCPT (professional councils) | ✅ Yes, for relevant on-campus schools | High for the parent university generally — not clearly relevant to the small online MBA/M.Sc catalog |
| **NAAC** | **Genuinely unresolved — five different claims found** | **See below — do not trust any single source here, including the official site** |

### The NAAC situation, laid out fully

I found **five mutually incompatible claims** across sources:
- **A+** — the university's own official site (ppsu.ac.in), plus 5 aggregators (CollegeVidya, Careers360, CollegeDunia, FindMyCollege, CollegeBatch)
- **A++** — one source (Zollege)
- **B** — one source (UniversityKart's dedicated "Recognitions & Accreditations" page — a page format I've generally found reliable for other universities in this project)
- **No formal grade accreditation at all** — one source (Vedantu), directly contradicting every other claim
- **C--** — **Wikipedia**, citing what appears to be a specific footnoted reference

This is a far wider spread than any other university in this batch — it's not "which specific high grade," it's "does this university have a credible current grade at all, and if so, is it near the top or near the bottom of the scale." Given the university's own official site and the majority of aggregators say A+, I'd guess that's the more likely current status — but **Wikipedia citing a specific, footnoted "C--" is not something I'm comfortable dismissing without checking**, especially for a newer, smaller regional private university where an official site's marketing claims may run ahead of actual verified status. **This needs a direct check against naac.gov.in before anything about PPSU's accreditation goes on a live page** — I would not seed any accreditation value for this university without that verification.

## Rankings

Single source: NIRF 251-300 band — from the same UniversityKart source I'm treating cautiously above given the NAAC conflict. Since your DB's `ranking` field is empty, nothing existing to conflict with, but I'd weight this figure with the same caution.

## Programs, Fees & Eligibility

⚠️ **Program count is disputed, not just a minor count mismatch like Galgotias/MAHE — this is a 2-vs-10 gap:**
- CollegeVidya explicitly and specifically states: "PPSU online course list involves only **two** programs for now: the online MBA and the online MSc in Data Science" — framed as a deliberate, small, new catalog
- FindMyCollege vaguely claims "**10** UGC-DEB Online Programmes" without naming any of them

Given CollegeVidya's claim is specific, named, and explicitly scoped ("only two... for now," consistent with a genuinely new online offering), I'd trust it over FindMyCollege's unitemized "10":

| Program | Duration | Eligibility | Notes |
|---|---|---|---|
| Online MBA | 2 years | Graduation in any discipline | — |
| Online M.Sc Data Science | 2 years | Graduation in a relevant discipline | — |

⚠️ **No online-specific fee figures found** — the ₹55,000-₹1,35,000 range found is for the general on-campus catalog (B.Tech, nursing, etc.), not confirmed for the online MBA/M.Sc specifically.

## Admission Process

No online-specific process found; general campus admission involves entrance exams and document verification, not clearly applicable to the online catalog.

## Documents Required

⚠️ **Not explicitly itemized** by any source — standard expected set, same caveat as previous universities:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

General scholarship programs are mentioned for the university broadly, not confirmed as applicable to online CDOE students specifically:

```python
# UNVERIFIED for the online division — general PPSU scholarship programs
# exist per one source, but no online-specific terms found. Leave
# university_id-linked scholarships empty unless/until confirmed.
```

## Placements

⚠️ Careers360 gives specific figures — **₹78 lakhs highest package**, recruiters including **Britannia, Casepoint, Cipla** — but this is clearly for the general/on-campus university (a very large, diverse catalog including engineering and pharmacy), not the tiny 2-program online catalog. Do not apply this to the online MBA/M.Sc record.

- `placement_support`: Leaving **unconfirmed for the online division specifically** — no source made an online-specific placement claim.
- `highest_package` / `average_package` / `top_recruiters`: leave empty for the online-specific record — the figures found describe an entirely different, much larger on-campus program population.

## Learning Methodology

- Dedicated LMS platform (per one source)
- SWAYAM collaboration mentioned for CDOE programs specifically (per one source)
- Video lectures, e-books, live classes, discussion forums, expert webinars (per CollegeVidya)

## FAQs

```python
faqs = [
    {
        "question": "What online programs does P P Savani University currently offer?",
        "answer": "As of the most recent information available, PPSU's online catalog is small and developing — one detailed source specifically names only two programs: an Online MBA and an Online M.Sc in Data Science. Confirm the current catalog directly before assuming a broader range of programs is available online.",
    },
    {
        "question": "What is P P Savani University's NAAC grade?",
        "answer": "Sources disagree significantly on this — ranging from A++ to no formal accreditation at all. Confirm the current grade directly via naac.gov.in before relying on any single claim.",
    },
    {
        "question": "Is P P Savani University a deemed university?",
        "answer": "No. PPSU is a private university established by a specific Gujarat state legislative act in 2017, not a deemed-to-be university.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** PP Savani University Online — Online MBA & M.Sc Data Science | CampusUnlock
- **Meta description:** Explore P P Savani University's growing online catalog, including an Online MBA and M.Sc in Data Science, from a Gujarat private university established in 2017.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC grade is the single most unresolved accreditation question in this entire project.** Five incompatible claims exist, spanning the full range from no accreditation to near-top grades, including a specific, footnoted Wikipedia claim of "C--" that directly contradicts the official site's "A+." Do not seed an accreditation value for this university without direct verification against naac.gov.in.
2. **Online program count is disputed by a wide margin (2 vs. 10)** — I trusted the more specific, named source (2 programs) over the vague, unitemized one (10), but this should be confirmed directly given how new and apparently small this online offering is.
3. **Don't conflate on-campus placement/fee data with the tiny online catalog** — PPSU's on-campus catalog (engineering, pharmacy, nursing, etc.) is much larger and better-documented than its online offering, and several sources' figures clearly describe that larger population.
4. **Established year (2017) is the one clean, well-corroborated fact here** — no issue there.
