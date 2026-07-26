# MIT World Peace University Online — Detail Page Content

> ⚠️ **This file needs a different kind of read than the previous 19.** Before writing the usual sections, I need to lay out a structural problem I found: **there's no solid evidence that MIT World Peace University (MIT-WPU) itself has a UGC-DEB approved online degree program.** What actually appears to exist is a separate, legally distinct sister institution — and at least two lower-quality sources appear to have conflated the two. Read this section before treating anything below as settled.

---

## The core problem, laid out plainly

Two institutions are getting mixed up across the sources I found:

1. **MIT World Peace University (MIT-WPU)** — the actual university. Established as a college in 1983 (Maharashtra Institute of Technology), granted full private-university status in **2017** via a specific Maharashtra state act. Offers on-campus and hybrid programs, including an MBA that requires entrance exams (CAT/XAT/CMAT/GMAT/MAH-CET/MIT-WPU CET) — **not** the merit-based, no-entrance-exam admission pattern seen at every genuinely UGC-DEB-approved online program researched in this entire 20-university project.

2. **MIT School of Distance Education (MITSDE)** — a **separate institution**, founded in **2008**, described in its own sources as "affiliated to MIT-WPU" rather than being MIT-WPU itself. This is the entity that actually offers AICTE-approved distance/online management programs — but specifically **PGDM and Executive-MBA-equivalent diplomas**, not a UGC-DEB approved University *degree*. PGDM is a diploma awarded by an autonomous institute, which is a fundamentally different credential category from the UGC-DEB degree programs every other university in this batch offers.

3. **Two lower-quality aggregator sources** (MBAEarth, AdmissionDIY) directly attribute "UGC-DEB approval," a NAAC A++ grade, and even a specific "94th NIRF Rank" to something they label "MIT (World Peace University)" — but the founding year they give (2008) matches **MITSDE's** founding, not MIT-WPU's (1983/2017). This strongly suggests these two sources mislabeled MITSDE's program as if it were MIT-WPU's directly. Also worth noting: the "94th NIRF Rank" figure doesn't match any of MIT-WPU's actual NIRF figures found elsewhere (51-100 band overall, 70th for Pharmacy, 101-150 band for Engineering) — another sign this specific claim doesn't hold up.

**My recommendation:** before publishing anything under "MIT World Peace University Online," confirm directly with MIT-WPU/MITSDE which entity your program listing is actually supposed to represent, and whether it's a UGC-DEB degree or an AICTE-approved PGDM/diploma — these are materially different products for a comparison site to present accurately. I'm presenting what's confirmed for each entity separately below, rather than merging them into one page the way I would for a normal university.

---

## What's confirmed about MIT-WPU itself (the university)

- **Established:** 1983 (as Maharashtra Institute of Technology), granted full private university status in 2017 (Government of Maharashtra Act No. XXXV, 2017)
- **Type:** Private University established by state act — **explicitly not a deemed university**, per a direct correction on an official-recognitions-focused aggregator page ("University is a full fledged university and not a deemed [university]"). ⚠️ **This conflicts with your existing DB, which has `university_type: 'Deemed University'`** — worth correcting given the explicit sourcing.
- **NAAC:** Genuinely mixed evidence — most sources (including two tagged "Verified Answer") say plain **A**; only one or two say A+, and those are weaker/more ambiguous sources (one is a Reddit-style comparison snippet with genuine risk of referring to a *different* "MIT Pune" entirely). I'd lean toward "A" as more reliable here.
- **UGC / AICTE:** Approved, well-corroborated
- **NIRF:** 51-100 band overall (2024), 70th for Pharmacy (2025), 101-150 band for Engineering — multiple figures by year/category, no single number to report
- **On-campus MBA:** entrance-exam based (CAT/XAT/CMAT/GMAT/MAH-CET/MIT-WPU CET), 60% aggregate minimum, dual-specialization model
- **Recruiters (on-campus, well-corroborated by 2 independent sources overlapping):** Amazon, TCS, Deloitte named by both; one source adds NVIDIA, Skoda, ONGC, Rakuten, E&Y

## What's confirmed about MITSDE (the actual distance/online provider)

- **Established:** 2008
- **Approvals:** UGC, AICTE, DEB — per its own listing (though note: DEB approval for a *diploma-granting* institute functions differently than DEB approval for a university's *degree* programs)
- **Programs:** MBA-equivalent, PGDM, Executive MBA — explicitly described as diploma-equivalent, not full university degrees
- **Admission:** No entrance exam; general academic path with work experience and interview
- **One source claims:** "MIT Pune Online MBA," 4 variants (Executive/PGDM/PGDM Executive/PGDBA), 2 years, 30+ specializations, **₹96,000 total fee**, and recruiter collaborations (Accenture, IBM, TCS, Amazon) — but this same source honestly notes "official placement data for the online MBA program is not publicly available." Single-sourced throughout.

## Documents Required

⚠️ **Not explicitly itemized** by any source for either entity — standard expected set:
- 10th and 12th mark sheets
- Graduation certificate/marksheet
- Government photo ID
- Passport-size photograph

## Scholarships

MIT-WPU's on-campus site mentions merit scholarships worth ₹50 crore total pool, tied to entrance-exam scores — but this is explicitly for on-campus programs, not confirmed for any online/distance offering:

```python
# UNVERIFIED for any online program — MIT-WPU's ₹50 crore scholarship
# pool is confirmed for on-campus, entrance-exam-based admission only.
# Leave university_id-linked scholarships empty for the "Online" entry
# unless/until the entity confusion above is resolved.
```

## FAQs

```python
faqs = [
    {
        "question": "Is 'MIT World Peace University Online' the same as MIT-WPU's on-campus programs?",
        "answer": "Not necessarily. Available evidence suggests the online/distance program is actually run by MIT School of Distance Education (MITSDE), a separate but affiliated institution founded in 2008, offering AICTE-approved PGDM and Executive MBA diplomas rather than a UGC-DEB university degree. Confirm which entity a specific listing represents before treating it as equivalent to a full MIT-WPU degree.",
    },
    {
        "question": "Is MIT World Peace University a deemed university?",
        "answer": "No. MIT-WPU is a private university established by a specific Maharashtra state legislative act (2017), not a deemed-to-be university.",
    },
]
```

---

## ⚠️ Flags — read this before anything else in the file

1. **This is the first university in the entire 20-institution batch where the basic premise of the request ("does an online division exist and is it UGC-DEB approved") isn't clearly confirmed.** Every other university had a real, sourced online/CDOE division. This one appears to route through a separate sister institution instead, with real risk that some source content conflates the two.
2. **`university_type` conflict:** your DB says "Deemed University" — one detailed source explicitly and directly states MIT-WPU is "not a deem[ed university]," and Wikipedia's description (established by state act) is consistent with that correction, not with deemed-university status. Worth fixing.
3. **NAAC grade leans toward plain "A", not the A+/A++ claims found on two weaker sources** — this is a case for treating the *weaker* evidence with suspicion rather than genuinely 50/50 like Shoolini.
4. **Recommend resolving the entity question directly with MIT-WPU/MITSDE before publishing anything under this name** — this is the one case in the whole batch where I'd stop and ask a human to make a judgment call before treating any of this as ready to seed, rather than just flagging conflicts within an otherwise-solid page.
