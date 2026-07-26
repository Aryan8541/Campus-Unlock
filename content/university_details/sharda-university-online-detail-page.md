# Sharda University Online — Detail Page Content

> Sourced from Sharda's own official domain (shardauniversity.uz — the Uzbekistan branch campus page, which describes the parent Indian university's accreditation) plus many aggregators (CollegeVidya, TopperGrad, CollegesGyan, Uniadda, MBATours, APS Admission Panel, Unifostedu, DistanceEducationSchool). Unlike the previous 9 universities, your DB entry here is one of the minimal auto-generated ones — `accreditation`, `established_year`, `ranking`, and `website` are all currently `None`. So there's nothing existing to conflict with; everything below is new-fact population, not a correction.

---

## Hero

- **Name:** Sharda University Online
- **City / State:** Greater Noida, Uttar Pradesh
- **Type:** Private University (full-fledged, under UGC Act 1956 Section 2(f) — **not** a deemed university)
- **Tagline:** *NAAC A+ accredited, UGC-DEB approved online degrees from a multidisciplinary university*

## About

Sharda University is a private university in Greater Noida, recognized by the UGC under Section 2(f) of the UGC Act, 1956, spread across a large multi-campus footprint (Greater Noida, Agra, Mathura). Its online division delivers UGC-DEB approved undergraduate and postgraduate programs, primarily in management and computer applications, alongside the university's much larger on-campus catalog spanning engineering, medicine, law, and more.

## Highlights

- NAAC A+ accredited — very strongly corroborated (9+ independent sources)
- UGC-DEB approved
- AIU (Association of Indian Universities) member — confirmed on Sharda's own official domain
- ACU (Association of Commonwealth Universities) affiliated — official source, not a schema field but worth noting
- Global academic partnerships claimed across 30+ countries (single source)
- Large-scale institution: 130+ total programs across all modes (per one source)

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC (Section 2(f)) | ✅ Recognized | High — confirmed on Sharda's own official domain, with the exact UGC Act reference number |
| UGC-DEB | ✅ Approved | High — consistent everywhere |
| NAAC | ✅ A+ | Very high — 9+ independent sources agree, including Sharda's own official domain |
| AICTE | Likely yes | Medium — single clear source (TopperGrad) |
| NBA | Mentioned | Single source (CollegeVidya) |
| AIU member | ✅ Yes | High — confirmed on Sharda's own official domain, with a direct link to the AIU member registry |

## Rankings

Unlike every other university in this batch, **no source gave a specific NIRF rank number** — several sources vaguely say Sharda is "among the top universities... as per NIRF" (including the official Uzbekistan-campus page), confirming NIRF recognition exists, but without a number to report. Since your DB's `ranking` field is currently empty, I'm leaving it empty rather than inventing a figure — this is a case where "no data" is the honest answer, not a conflict to resolve.

## Programs, Fees & Eligibility

| Program | Duration | Eligibility | Notes |
|---|---|---|---|
| Online MBA | 2 years | Graduation in any discipline | — |
| Online MCA | 2 years | Bachelor's with relevant background | — |
| Online BBA | 3 years | Class 12 pass | — |
| Online BCA | 3 years | Class 12 pass with Math background | — |
| Online M.Com, BA | Varies | Varies | — |

⚠️ **No fee figures found in any source** — every other university in this batch had at least one single-sourced number; Sharda genuinely had none. Leave blank until sourced from the official fee page.

## Admission Process

*(Single detailed source, plausible and consistent with the general pattern seen across other universities in this batch)*

1. Register on the Sharda Online admission portal (email/mobile, OTP or credential-based login)
2. Select program and specialization
3. Pay application/program fee (net banking, card, UPI, or EMI)
4. Upload required documents
5. Submit application, receive confirmation/Application ID
6. Document and eligibility verification by the admissions team
7. LMS access granted upon confirmation

⚠️ Admission cycles cited as **January / July** (one source) — standard for most universities in this batch, but time-sensitive; confirm the current cycle before publishing. One source's specific deadline ("15 November 2025" for July 2025 admission) is now stale/past and was excluded rather than reused.

## Documents Required

⚠️ **Not explicitly itemized** by any source — standard expected set, same caveat as previous universities:
- 10th and 12th mark sheets
- Graduation certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

No specific Sharda Online scholarship (name, amount, eligibility) was found in any source reviewed. Leaving empty rather than inventing one:

```python
# No verified Sharda-specific scholarship found. Leave university_id-linked
# scholarships empty unless/until real data is sourced.
```

## Placements

⚠️ **Worth flagging something unusual here, not just the normal single-source caveat.** One source (CollegesGyan) gives a fairly specific list — recruiters named as *HCL, Infosys, Wipro, TCS, Deloitte, ICICI Bank, and Amazon*, with an average package of **₹3-6 LPA for freshers**. That average-package range is identical to what I found for Sikkim Manipal University two universities ago — which raises a real possibility that this figure is a generic template number reused across multiple aggregator pages rather than something researched specifically for each institution. That's a reason for *more* caution, not less, so — consistent with how every other university in this batch was handled — I'm not writing these into `top_recruiters` or `average_package` as confirmed data.

Hiring-partner counts also conflict between sources: **"750+ recruiters"** (TopperGrad) vs. **"300+ Hiring Partners"** (DistanceEducationSchool) — a real disagreement, not corroboration.

- `placement_support`: **True** — described consistently and with real specificity (career counseling, resume building, interview prep, internship partnerships) across multiple sources, not just a vague marketing line.
- `highest_package` / `average_package`: leave `None` — see the duplicate-figure concern above.
- `top_recruiters`: leave empty — single-sourced, and the identical-to-SMU average package makes me trust this source's specificity less, not more.

## Learning Methodology

- Modern LMS with live and recorded lectures, e-library, discussion forums
- AI-driven assessments (per one source)
- Personalized mentorship alongside standard faculty instruction
- 24/7 LMS access

## FAQs

```python
faqs = [
    {
        "question": "Is Sharda University Online degree valid?",
        "answer": "Yes. Sharda University Online programs are UGC-DEB approved, and the university is NAAC A+ accredited, making the degree valid for both private and government job openings.",
    },
    {
        "question": "Is Sharda a deemed university?",
        "answer": "No. Sharda University is a full-fledged private university recognized under Section 2(f) of the UGC Act, 1956 — not a deemed-to-be university.",
    },
    {
        "question": "What online programs does Sharda University offer?",
        "answer": "Sharda University Online offers UGC-DEB approved programs including MBA, MCA, BBA, and BCA, alongside a much larger on-campus catalog spanning engineering, medicine, and law.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** Sharda University Online — NAAC A+ UGC-DEB Approved Degrees | CampusUnlock
- **Meta description:** Explore Sharda University Online's NAAC A+ accredited, UGC-DEB approved MBA, MCA, BBA, and BCA programs from a multidisciplinary private university in Greater Noida.

---

## ⚠️ Flags — things to double-check before publishing

1. **Established year:** 5 independent sources (plus the official Uzbekistan campus page's exact UGC approval reference number) agree on **2009**; one outlier source (CollegeVidya) says 1996. Given the strength of agreement elsewhere, 2009 looks like the reliable figure — 1996 may reflect confusion with a different Sharda Group entity.
2. **Suspicious duplicate placement figure:** the ₹3-6 LPA average package matches exactly what one source claimed for Sikkim Manipal University earlier in this batch — worth treating as a possible generic template number from low-effort aggregator content, not independently researched data for either university.
3. **Recruiter-count conflict:** 750+ vs. 300+ hiring partners between two sources — don't publish either without confirming.
4. **No ranking or fee data exists anywhere** — unlike every other university so far, this isn't a conflict to resolve, just genuinely missing information. Both fields should stay empty until sourced directly.
5. Everything else (NAAC A+, UGC-DEB, UGC Section 2(f), AIU membership) is strongly corroborated, including via Sharda's own official domain.
