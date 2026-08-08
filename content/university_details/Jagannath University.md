# Jagannath University (Jaipur) Online/Distance — Detail Page Content

> Sourced from Jagannath University's own domains (sdlju.org, onlineju.com) plus multiple independent aggregators (CollegeVidya, CampusOption, Uniadda, CollegePortal, RKIMT, BigNewsNetwork). Where sources disagreed, flagged rather than picked — see **⚠️ Flags** at the end.

---

## Hero

- **Name:** Jagan Nath University (Jaipur) — Centre for Distance and Online Education (CDOE)
- **City / State:** Jaipur, Rajasthan
- **Type:** Private University — established by an Act of the Rajasthan State Legislature (Act No. 19 of 2008); part of the JIMS Group of Institutions (*not* a deemed university)
- **Tagline:** *UGC-DEB approved online and distance degrees, backed by 30+ years of the JIMS Group's academic legacy*

## About

Jagan Nath University, Jaipur, was founded on 16 April 2008 by an Act of the Rajasthan State Legislature. It is a multidisciplinary private university offering programs across Engineering & Technology, Management, Law, Architecture, Agriculture Science, Pharmacy, Physiotherapy, Education, and Vocational Studies, alongside PhD programs in select disciplines. Its distance/online education is run through the **Centre for Distance and Online Education (CDOE)**, which multiple sources date to 2010 (one describes it as originally the "School of Distance Learning," established as part of the JIMS group). The university is also described as benefiting from the wider, 30+ year academic legacy of the JIMS Group of Institutions.

**Flag:** Do not confuse this Jaipur-based Jagan Nath University with any other similarly-named institution — sources consistently and specifically describe this one as a Rajasthan State Legislature-established private university in Jaipur, distinct from any other "Jagannath"-named institution elsewhere. Also note the name is spelled both "Jagannath University" and "Jagan Nath University" interchangeably across sources — recommend standardizing on one spelling for the CampusUnlock schema and noting the variant in search/alias fields.

## Highlights

- NAAC accredited — reported consistently as **grade "A"** (2nd cycle, per one source; one source additionally specifies the accreditation occurred in 2002, which reads oddly given the university was only founded in 2008 — likely a source error or a reference to a predecessor institution, **needs clarification**)
- Approved by UGC-DEB for online and distance learning programs — reported consistently and clearly across all sources, including two official-adjacent domains (sdlju.org, onlineju.com)
- Also approved/recognized by a wide range of statutory bodies depending on discipline: Bar Council of India (BCI), Pharmacy Council of India (PCI), National Council for Teacher Education (NCTE), Institute of Town Planners India (ITPI), Council of Architecture (CoA), and AICTE — these apply to specific on-campus disciplines (law, pharmacy, teacher education, architecture, engineering) and should not be presented as blanket approvals covering the online/distance catalogue, which is narrower (business, mass communication, arts)
- AIU (Association of Indian Universities) member
- ICAR accreditation (5 years) for its B.Sc. (Hons.) Agriculture program — on-campus only, not relevant to the distance/online catalogue
- Access to the government SWAYAM portal mentioned for online MBA students (per one aggregator) — a genuinely distinctive, checkable claim if accurate, since SWAYAM integration is a specific, named government platform rather than vague marketing language

## Approvals & Accreditations

| Approval | Status | Source confidence |
|---|---|---|
| UGC-DEB | ✅ Approved for online and distance programs | High — confirmed across official-adjacent domains (sdlju.org, onlineju.com) and multiple independent aggregators |
| NAAC | Grade "A" | Medium-high — consistent grade across sources, but the "2002" accreditation date cited by one source doesn't align with the university's 2008 founding and needs clarification |
| UGC (general recognition) | ✅ Yes | High |
| AIU membership | ✅ Yes | Medium-high — mentioned by multiple sources |
| BCI / PCI / NCTE / ITPI / CoA / AICTE | ✅ Yes, but each scoped to a specific on-campus discipline (law / pharmacy / teacher education / town planning / architecture / engineering) | High for the on-campus disciplines they cover; **not applicable to the online/distance catalogue** and should not be shown as blanket approvals on the CDOE-specific profile |
| ICAR | ✅ Yes, 5-year accreditation for B.Sc. (Hons.) Agriculture | High, but on-campus only, not relevant to online/distance profile |

## Rankings

No NIRF or other national ranking figure was found for Jagan Nath University, Jaipur, in this research pass — unlike Amity, SPPU, or BMU, none of the sources reviewed cited a specific NIRF rank (overall or category) for this university. Recommend leaving the ranking field unset rather than inferring a figure, and treating "no ranking found" as itself a data point worth surfacing rather than guessing.

## Programs, Fees & Eligibility

| Program category | Duration | Eligibility | Fees |
|---|---|---|---|
| Online mode | Varies by program | Not separately detailed by discipline in sources reviewed | Online MBA fee reported as **₹26,250 per annum** by one source |
| Distance mode | Varies by program | Not separately detailed by discipline in sources reviewed | Distance MBA fee reported as **₹12,500 per semester** by a different source |

**Program list — online mode:** MBA, BBA, B.Com, MA (JMC — Journalism & Mass Communication), BA (JMC) — per one aggregator's explicit breakdown.

**Program list — distance mode:** BBA, B.Com, MA (JMC), BA, BA (JMC) — per the same source, listed as a slightly different set from the online-mode list (notably, plain "BA" appears in the distance list but not explicitly in the online list, and "MBA" appears in the online list but not explicitly in the distance list as stated). **This distinction — a different course mix for online vs. distance mode, rather than the same courses offered in two delivery formats — is an important structural detail for the CampusUnlock ODL/Online schema and should be verified directly against onlineju.com / sdlju.org before publishing, since it affects how program-mode filtering should work for this university.**

⚠️ **Fee conflict:** the ₹26,250/annum (online MBA) and ₹12,500/semester (~₹25,000/annum, distance MBA) figures are reasonably close to each other, which is plausible if they describe genuinely different online-vs-distance MBA fee structures — but they come from two different sources describing two different modes, so this should be read as "two separate, unreconciled data points" rather than confirmation of one number.

One further, separate source states 16 available MBA specialization streams and a per-semester MBA fee, without giving the same figure as either of the above — a third, slightly different fee reference that adds to the reconciliation work needed here.

## Admission Process

1. Apply via the official CDOE portal (onlineju.com or sdlju.org) or the university's general admissions site
2. Selection is merit-based for most programs
3. Submit required documents
4. Pay the application form fee — reported as **₹500** by one source
5. Complete enrollment and gain access to the learning platform (including SWAYAM portal access for some programs, per one source)

## Documents Required

⚠️ **Not explicitly enumerated by any source in this pass** — same caveat as Amity, SPPU, and BMU. Standard expected set, not verified specifically for Jagannath University:
- 10th and 12th mark sheets
- Bachelor's degree certificate/marksheet (for PG programs)
- Government photo ID
- Passport-size photograph

## Scholarships

No specific Jagannath University CDOE scholarship (name, amount, eligibility) was found in any source reviewed. Leaving this empty rather than inventing one:

```python
# No verified Jagannath University (Jaipur) CDOE-specific scholarship found.
# Leave university_id-linked scholarships empty unless/until real data is sourced.
```

## Placements

One source describes "exceptional placement assistance" and industry interactions, projects, skill-upgradation programs, and workshops for online MBA learners, but gives no specific numbers (placement rate, packages, named recruiters).

- `placement_support`: **True** — described consistently enough (industry interactions, workshops, placement assistance language) to treat as a genuine stated feature, though vaguely.
- `highest_package` / `average_package`: leave `None` — no figures found.
- `top_recruiters`: leave empty — no specific companies named for the online/distance cohort.

## Learning Methodology

- Internet-based teaching mode with specially designed study materials, per one source
- Personal Contact Programme (PCP) offered for direct query resolution with mentors
- Access to the government SWAYAM portal for high-quality video lectures and study materials, for online MBA students specifically (per one source) — a distinctive, checkable claim worth verifying and highlighting if confirmed, since SWAYAM is a named, real government platform rather than a vague feature claim
- Multiple entry-exit options aligned with NEP 2020, for undergraduate programs
- AI-based support for personalized learning and academic guidance, per one official-adjacent source (sdlju.org) — a fairly specific, checkable claim
- Continuous support through interactive forums for peer-to-peer learning, per the same official-adjacent source

## FAQs

```python
faqs = [
    {
        "question": "Is Jagan Nath University's online/distance degree valid and recognized?",
        "answer": "Yes. Jagan Nath University's Centre for Distance and Online Education (CDOE) is approved by the UGC-DEB (Distance Education Bureau), and the university itself is NAAC accredited with an 'A' grade.",
    },
    {
        "question": "Is Jagan Nath University a deemed university?",
        "answer": "No. Jagan Nath University, Jaipur, is a private university established by an Act of the Rajasthan State Legislature in 2008, not a deemed-to-be university.",
    },
    {
        "question": "Are the same programs offered in both online and distance mode?",
        "answer": "Not exactly — sources describe a slightly different course mix for each mode (for example, MBA appears explicitly in the online-mode list and BA appears explicitly in the distance-mode list). This should be confirmed directly with the university before assuming full overlap between the two modes.",
    },
]
```

## Meta Title & Description
*(Original marketing copy — not a factual claim requiring a source)*

- **Meta title:** Jagan Nath University Online & Distance Education (Jaipur) — UGC-DEB Approved Degrees | CampusUnlock
- **Meta description:** Explore Jagan Nath University's UGC-DEB approved online and distance MBA, BBA, B.Com, BA, and MA (JMC) programs from a Rajasthan-legislature-established university backed by the JIMS Group's academic legacy.

---

## ⚠️ Flags — things to double-check before publishing

1. **NAAC "2002" accreditation date doesn't align with the university's 2008 founding** — likely a source error or reference to a predecessor institution; needs clarification before including any specific accreditation date.
2. **No NIRF ranking found** — unlike the other universities profiled, treat "no ranking" as a genuine data point rather than a research gap to paper over with a guess.
3. **Online vs. distance program-mix discrepancy:** one source lists a slightly different set of courses for online mode (MBA, BBA, B.Com, MA-JMC, BA-JMC) vs. distance mode (BBA, B.Com, MA-JMC, BA, BA-JMC) — confirm whether this is a real structural difference or a source listing error before building program-mode filters around it.
4. **Fee conflict:** three different, unreconciled fee references for the MBA program (₹26,250/annum online; ₹12,500/semester distance; a third unspecified figure tied to "16 specialization streams") — needs direct confirmation from onlineju.com/sdlju.org.
5. **Broad statutory-approval list (BCI/PCI/NCTE/ITPI/CoA/AICTE) applies to specific on-campus disciplines only** — do not present these as blanket approvals for the online/distance business and mass-communication catalogue actually being profiled here.
6. **Name-spelling inconsistency:** "Jagannath University" vs. "Jagan Nath University" used interchangeably — pick one canonical form for the CampusUnlock database and store the other as an alias.
7. **SWAYAM portal access and AI-based learning support** are specific, checkable claims (not vague marketing language) — worth verifying directly since, if true, they're a genuine differentiator versus the other universities profiled in this batch.
