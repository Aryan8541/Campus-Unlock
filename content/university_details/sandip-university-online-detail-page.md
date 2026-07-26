# Sandip University Online — Detail Page Content

> **⚠️ STOP — READ THIS BEFORE PUBLISHING.**
> Research conducted across 5 rounds of search and a direct web_fetch of the official university website (sandipuniversity.edu.in) has produced a consistent, high-confidence finding: **Sandip University Nashik does not appear to have a UGC-DEB approved online or distance education division.** The full evidence is documented under the primary flag below. This file records what was found, what was not found, and what the DB should reflect — it is not a publishing-ready detail page.

---

> Sources consulted: official university website (sandipuniversity.edu.in — web_fetched directly), Wikipedia (Sandip University, Nashik), multiple independent aggregators (CollegeDekho, CollegeDunia, Shiksha, CollegeBatch, BetterStudy, CareerGuide, GetMyUni, TimesOfCollege, Grokipedia), and searches targeting UGC-DEB portal (deb.ugc.ac.in) specifically for this institution. No UGC-DEB disclosure PDF was found for Sandip University Nashik.

---

## Brand-Name Collision — Resolved First

⚠️ **Two legally distinct "Sandip University" entities exist in India:**

| Entity | Location | Status |
|---|---|---|
| **Sandip University, Nashik** | Trimbak Road, Nashik, Maharashtra | The institution in the DB (city: Nashik, state: Maharashtra) |
| **Sandip University, Sijoul** | Sijoul, Madhubani District, Bihar | A legally separate private university in Bihar |

Wikipedia confirms the Bihar campus was formerly part of the Nashik-based institution and later separated into its own distinct university. The Vedantu source consulted in early searches was about the **Bihar entity** — that content was disregarded once the collision was identified. Every fact below refers exclusively to the **Nashik, Maharashtra entity**, verified via address and official website.

---

## Primary Flag — No UGC-DEB Online Division Found

**Finding:** Sandip University Nashik does not appear to be UGC-DEB approved for online or distance education programs. This is the single most important finding in this file.

**Evidence — converging from multiple independent directions:**

1. **Official website (sandipuniversity.edu.in — direct web_fetch):** The full site navigation includes Schools, Admissions, Placements, Research, IQAC, and Campus Life sections. There is **no mention of online learning, distance education, a Centre for Distance and Online Education (CDOE), or UGC-DEB** anywhere on the homepage or navigation menu.

2. **CollegeDekho (aggregator):** Explicitly states: *"The university doesn't offer any distance learning courses. However, various part-time courses have been launched by Sandip University in 2020-21."*

3. **CareerGuide (aggregator):** Explicitly states in a FAQ: *"No — all programs are regular; however part-time courses were introduced from AY 2020-21."*

4. **UGC-DEB portal search:** Searches targeting `deb.ugc.ac.in` combined with "Sandip University" returned no disclosure PDF for this institution. No HEI registration ID was found for Sandip University Nashik on the UGC-DEB system, unlike Parul University (whose HEI-Exempted-U-0763 PDF was immediately retrievable). The absence of a findable PDF is consistent with no approval existing.

5. **Zero aggregators describe an online division:** Every aggregator describes Sandip University exclusively in terms of on-campus UG, PG, and doctoral programs. None mention online degrees, an online portal URL, or UGC-DEB approval — a sharp contrast to universities like Parul, Amity, or NMIMS where multiple aggregators consistently describe the online division.

**Confidence level:** High that no UGC-DEB approved online division exists **as of the date of this research (July 2026).** This could change if the university applies for UGC-DEB approval in the future.

**Recommendation:** Do not publish a detail page for "Sandip University Online" under the current DB entry. The entry in the seed data appears to have been included in error, or may reflect a future institution that has not yet obtained UGC-DEB approval.

---

## What Was Verified About the Parent University (For DB Accuracy)

Even though an online division cannot be confirmed, the research did yield accurate data for several DB fields that are currently `None`. These should be updated in the seed data so the record is accurate if/when an online division is added later.

### Established Year

⚠️ **Genuine conflict across aggregators — needs resolution:**

| Date | What it marks | Source confidence |
|---|---|---|
| **2005** | Sandip Foundation Trust founded (governing body) | High — Grokipedia, CareerGuide |
| **2015** | University Act passed by Maharashtra Government (Act No. XXXVIII of 2015) | **Highest** — Wikipedia (citing UGC's own private university list PDF), CollegeDekho, Shiksha, CollegeBatch |
| **2017** | Operational start / formal university establishment | **Highest** — Wikipedia infobox ("Established: 2017"), Wikipedia article text, TimesOfCollege, multiple other aggregators |

**The conflict between 2015 and 2017** is the most important one to resolve. The most likely explanation: the Maharashtra Government Act was passed in 2015, but the university formally began operations and was listed in the UGC's private university register in 2017. Wikipedia's infobox (which cites the UGC PDF directly) says 2017; the Act number references 2015.

**Recommendation for DB field `established_year`:** Set to `2017` (operational start, corroborated by Wikipedia citing UGC's own records) and note the 2015 Act date in the description. Do not set to 2008 or 2014, which appear in a small number of older/lower-quality aggregators and are inconsistent with the Wikipedia/UGC-sourced evidence.

### Accreditation

**No conflict.** All sources — Wikipedia, official website meta description, CollegeDunia, CollegeDekho, Shiksha, TimesOfCollege, BetterStudy, CollegeBatch — consistently report:

- **NAAC 'A' grade** (not A+, not A++)
- The official website's own meta title reads: *"Sandip university: NAAC 'A' Accredited Top Private University in India"*

**Recommendation:** Set `accreditation` to `"NAAC A"`. Source confidence: **highest** (confirmed on official domain itself).

### Other Approvals

| Approval | Status | Source confidence |
|---|---|---|
| UGC (Section 2f) | ✅ Recognized | **Highest** — official website, Wikipedia, all aggregators |
| AICTE | ✅ Approved | High — 4+ independent aggregators |
| AIU member | ✅ Yes | High — 3+ aggregators; CollegeDekho specifically names AIU membership |
| BCI (Bar Council) | ✅ Approved | High — 3+ aggregators |
| PCI (Pharmacy Council) | ✅ Approved | High — 3+ aggregators |
| UGC-DEB | ❌ Not found | No evidence of online/distance approval; see Primary Flag |
| NIRF ranking | ❌ Not ranked | Multiple aggregators note SU is **not** in NIRF rankings; Shiksha specifically says it has "yet to feature in top NIRF or QS World University rankings" |
| WES recognized | ❌ Not confirmed | No source mentions this |

### Rankings

**No NIRF ranking exists** for Sandip University Nashik. The DB field `ranking` should remain `None`.

Rankings that were found are from private/commercial ranking bodies only:
- Times Engineering Survey 2024: 1st in "Research Capability" (Emerging Engineering Institutes category), 2nd in Placement, 3rd overall (Emerging Engineering Institutes)
- Times B-School 2024: 22nd in "Top 40 Private Universities"
- Times B-School 2023: 4th "Top Emerging B School"
- TOI MBA ranking 2024: 67th

These are private commercial rankings, not NIRF, and should not populate the `ranking (int, NIRF)` DB field.

### Website

**Confirmed:** `https://www.sandipuniversity.edu.in/`

---

## DB Field Recommendations (Parent University Corrections Only)

```python
{
    # Fields that CAN be updated now with confidence:
    "website": "https://www.sandipuniversity.edu.in",  # confirmed
    "established_year": 2017,                           # Wikipedia/UGC-sourced; see flag on 2015 vs 2017
    "accreditation": "NAAC A",                          # confirmed on official domain itself
    "ugc_approved": True,                               # confirmed everywhere
    "aicte_approved": True,                             # high confidence — 4+ sources
    "aiu_member": True,                                 # high confidence — 3+ sources
    "ranking": None,                                    # no NIRF ranking exists — leave None

    # Fields that must remain None — no online division confirmed:
    "ugc_deb_approved": None,                           # no UGC-DEB approval found
    "wes_approved": None,                               # not found
    "placement_support": None,                          # cannot be attributed to a non-existent online division
    "highest_package": None,                            # on-campus only; figures of ₹28 LPA domestic /
                                                        # ₹1.12 Cr international are for on-campus BTech/MBA
    "average_package": None,                            # on-campus aggregator consensus: ~₹5-6 LPA; do not
                                                        # attribute to online
    "top_recruiters": None,                             # on-campus: TCS, Wipro, Infosys, Bosch, HDFC, Amazon,
                                                        # Cognizant, Mahindra, Godrej — do not attribute to online

    # These fields were already correct in DB:
    "name": "Sandip University",                        # correct (no separate online entity name found)
    "city": "Nashik",                                   # confirmed
    "state": "Maharashtra",                             # confirmed
    "university_type": "Private University",            # confirmed
    "ownership": "Private",                             # confirmed
}
```

---

## FAQs

```python
# Cannot produce FAQs for an online division that has not been confirmed.
# If UGC-DEB approval is obtained in the future, FAQs should be built at that point.
# The following FAQs can be produced for the parent university only:

faqs_parent_only = [
    {
        "question": "Is Sandip University recognized by UGC?",
        "answer": "Yes. Sandip University, Nashik is recognized by the University Grants Commission (UGC) and was established under Maharashtra Government Act No. XXXVIII of 2015.",
    },
    {
        "question": "What is Sandip University's NAAC accreditation grade?",
        "answer": "Sandip University holds NAAC 'A' grade accreditation.",
    },
    {
        "question": "Does Sandip University offer online or distance education programs?",
        "answer": "As of mid-2026, Sandip University Nashik does not appear to offer UGC-DEB approved online or distance education programs. The university's programs are offered in regular on-campus mode, with some part-time options introduced from AY 2020-21.",
    },
]
```

---

## ⚠️ Flags Summary

1. **No UGC-DEB online division confirmed — do not publish an online detail page.** This is the central finding. The evidence is consistent across the official website, two aggregators with explicit statements, and an absence of any UGC-DEB disclosure PDF. The DB entry "Sandip University Online" appears to be an error in the seed data, or anticipates a future approval that has not yet occurred.

2. **Brand-name collision with Sandip University Sijoul (Bihar)** — actively confirmed and resolved. Any research not carefully filtered by city/state could pull in Bihar-entity data. The Vedantu page found in early searches was about the Bihar entity.

3. **Established year conflict (2015 vs 2017):** The Maharashtra Act was passed in 2015 but Wikipedia (citing the UGC's own list) records 2017 as the establishment year. Recommend 2017 for the DB field; 2015 should appear only in narrative description as the Act date.

4. **NAAC grade is 'A', not A+ or A++.** Confirmed unambiguously on the official website itself. This is a meaningful distinction from universities like Parul (A++) or Amity (A+) that should not be conflated.

5. **No NIRF ranking exists.** The DB field should remain `None`. Do not import any commercial ranking figure (Times, IIRF, etc.) into the `ranking (int, NIRF)` field.
