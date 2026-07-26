"""
Campus Unlock — University Detail Page Content
==================================================
Rich per-university content for the University Details page: long-form
descriptions, approval/recognition flags, placement info, FAQs, and
scholarships.

Sourcing standard
------------------
Every entry here was compiled from each university's own official
domain(s) plus multiple independent third-party aggregators. Where
sources disagreed with each other, or a claim was only single-sourced
without independent corroboration, the field is left as None / omitted
rather than guessed — this file never invents a number or fact.

Approval flags (`ugc_approved`, `aicte_approved`, `aiu_member`,
`wes_approved`) specifically only get set to True when the sourcing
material rated that fact "High" or "Very high" confidence (i.e.
multiple independent sources agreed, or an official domain confirmed
it directly). "Medium"/"Low"/"possibly"/"unconfirmed" ratings are left
as None here — see the original per-university research notes for the
reasoning behind each borderline case if you want to review or
override one directly.

Deliberately NOT included here
--------------------------------
`ranking`, `accreditation` (NAAC grade string), and `established_year`
are NOT touched by this file, even where the source research flagged a
conflict with what's already in data/universities.py — several of
those conflicts are well-corroborated (e.g. multiple independent
sources disagreeing with the current NAAC grade on file), but
resolving them is a judgment call for you to make directly, not
something to silently overwrite. seed_university_details() in seed.py
only backfills a field when it is currently None/blank anyway, so
these existing values are preserved automatically regardless.

Shape per entry
-----------------
    {
        "name": <must exactly match a "name" in UNIVERSITY_DEFS>,
        "short_description": str | None,
        "full_description": str | None,
        "why_choose": str | None,
        "ugc_approved": bool | None,
        "aicte_approved": bool | None,
        "aiu_member": bool | None,
        "wes_approved": bool | None,
        "placement_support": bool | None,
        "highest_package": float | None,
        "average_package": float | None,
        "top_recruiters": str | None,     # comma-separated
        "meta_title": str | None,
        "meta_description": str | None,
        "faqs": [{"question": str, "answer": str}, ...],
        "scholarships": [
            {"title": str, "description": str, "amount": float | None, "deadline": str | None},
            ...
        ],
    }
"""

UNIVERSITY_DETAILS = [
    # ------------------------------------------------------------------
    {
        "name": "NMIMS Global Access",
        "short_description": (
            "NMIMS Global Access School for Continuing Education (NMIMS Online) — the "
            "UGC-DEB approved online arm of SVKM's NMIMS, a deemed-to-be university, "
            "offering online MBA, PGDM, and BBA programs with no entrance exam required."
        ),
        "full_description": (
            "NMIMS Online is the distance and online learning school of SVKM's NMIMS, a "
            "deemed-to-be university under Section 3 of the UGC Act, 1956. Originally "
            "launched as NGASCE (NMIMS Global Access School for Continuing Education), it "
            "now also operates as NMIMS CDOE (Centre for Distance and Online Education). "
            "It offers UGC-DEB approved undergraduate, postgraduate, diploma, and "
            "certificate programs — primarily in management, finance, and business "
            "analytics — aimed at working professionals who can't attend a full-time "
            "campus program."
        ),
        "why_choose": (
            "UGC-DEB approved and NAAC accredited. Online MBA/PGDM admission is merit-based "
            "on prior academic marks — no CAT/NMAT/GMAT required. 800+ hours of live "
            "faculty-led sessions, a dedicated digital library (journals, case studies, "
            "whitepapers), and career services offered specifically to online/distance "
            "students and alumni."
        ),
        "ugc_approved": True,
        "placement_support": True,
        "meta_title": "NMIMS Online — UGC-DEB Approved Online MBA & BBA | CampusUnlock",
        "meta_description": (
            "Explore NMIMS Online's UGC-DEB approved MBA, PGDM, and BBA programs — no "
            "entrance exam required, deemed-university degree, 100% online delivery."
        ),
        "faqs": [
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
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Amity University Online",
        "short_description": (
            "The online-learning arm of Amity University, Uttar Pradesh — a private "
            "university offering UGC-DEB approved, NAAC A+ accredited MBA, BBA, MCA, and "
            "BCA degrees from one of India's largest private universities."
        ),
        "full_description": (
            "Amity University Online is the online-learning arm of Amity University, Uttar "
            "Pradesh — a private university established in 2005 by an act of the Uttar "
            "Pradesh state legislature, part of the wider Amity Education Group. It was "
            "among the first Indian institutions to offer UGC-DEB approved online degree "
            "programs, and now runs 80+ online undergraduate, postgraduate, and "
            "certificate programs across management, IT, commerce, and the arts."
        ),
        "why_choose": (
            "UGC-DEB approved, one of the first institutions in India to receive this. "
            "NAAC A+ accredited. AIU (Association of Indian Universities) member, "
            "confirmed via Amity's own official page. 80+ online programs and "
            "specializations, delivered through a dedicated LMS with an AI-powered "
            "learning assistant."
        ),
        "ugc_approved": True,
        "aiu_member": True,
        "placement_support": True,
        "meta_title": "Amity University Online — UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore Amity University Online's UGC-DEB approved, NAAC A+ accredited MBA, "
            "BBA, MCA, and BCA programs — 80+ online degrees from one of India's largest "
            "private universities."
        ),
        "faqs": [
            {
                "question": "Is an Amity University Online degree valid and recognized?",
                "answer": "Yes. Amity University Online is UGC-DEB approved and UGC-recognized, and the university itself is NAAC A+ accredited.",
            },
            {
                "question": "Is Amity University Online a deemed university?",
                "answer": "No. Amity University (Uttar Pradesh) is a private university established by an act of the UP state legislature, not a deemed-to-be university.",
            },
            {
                "question": "What programs does Amity University Online offer?",
                "answer": "Amity Online offers a wide range of UG, PG, and certificate programs, including MBA, BBA, MCA, BCA, M.Com, and MA, across management, IT, commerce, and the arts.",
            },
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Lovely Professional University Online",
        "short_description": (
            "LPU Online — NAAC A++ accredited, UGC-DEB approved online degrees from "
            "India's highest-graded dual-mode university, with AICTE-approved MBA and "
            "MCA programs."
        ),
        "full_description": (
            "LPU Online is the distance and online-learning division of Lovely "
            "Professional University, offering UGC-DEB approved undergraduate, "
            "postgraduate, and diploma programs in management, technology, commerce, and "
            "the arts. LPU itself holds NAAC's highest grade (A++) and UGC Category 1 "
            "status with Graded Autonomy, and its online division carries the same degree "
            "validity as its on-campus programs."
        ),
        "why_choose": (
            "NAAC A++ (3.68/4) — the highest grade among all dual-mode universities, "
            "government and private. UGC-DEB approved. MBA and MCA programs specifically "
            "AICTE-approved. WES-recognized for Canada and the USA, confirmed on LPU's own "
            "official site. UGC Category 1 University with Graded Autonomy. Two intakes "
            "per year, in January and July."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "wes_approved": True,
        "placement_support": True,
        "meta_title": "LPU Online — NAAC A++ UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore LPU Online's NAAC A++ accredited, UGC-DEB approved MBA, MCA, and BBA "
            "programs — AICTE-approved MBA/MCA, WES-recognized, two intakes a year."
        ),
        "faqs": [
            {
                "question": "Is LPU Online recognized and valid for government jobs?",
                "answer": "Yes. LPU Online is UGC-DEB approved and NAAC A++ accredited, so the degree carries the same validity as LPU's on-campus programs for government jobs, private jobs, and further study.",
            },
            {
                "question": "Are LPU's online MBA and MCA programs AICTE approved?",
                "answer": "Yes. LPU's online MBA and MCA programs specifically hold AICTE approval, in addition to UGC-DEB entitlement.",
            },
            {
                "question": "When can I apply to LPU Online?",
                "answer": "LPU Online runs two admission intakes per year, in January and July.",
            },
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Jain Online (Deemed-to-be University)",
        "short_description": (
            "Jain Online — UGC-entitled online degrees from JAIN (Deemed-to-be "
            "University), with AICTE-approved MBA and MCA programs."
        ),
        "full_description": (
            "Jain Online is the e-learning arm of JAIN (Deemed-to-be University), offering "
            "UGC-entitled undergraduate and postgraduate degree programs across "
            "management, computer applications, and commerce. It draws on Jain's decades "
            "of on-campus academic history, delivered through a Learning Management "
            "System built for working professionals."
        ),
        "why_choose": (
            "UGC-DEB approved online programs. Deemed-to-be University status with UGC "
            "Category I recognition. MBA and MCA programs specifically hold AICTE "
            "approval, in addition to UGC-DEB entitlement. LMS with live classes, recorded "
            "lectures, and one-on-one mentorship."
        ),
        "ugc_approved": True,
        "placement_support": True,
        "meta_title": "Jain Online — UGC-DEB Approved Degrees from a Deemed University | CampusUnlock",
        "meta_description": (
            "Explore Jain Online's UGC-entitled MBA, MCA, BBA, and B.Com programs from "
            "JAIN (Deemed-to-be University) — AICTE-approved MBA/MCA, flexible online "
            "learning."
        ),
        "faqs": [
            {
                "question": "Is a Jain Online degree valid for government jobs?",
                "answer": "Yes. Jain Online programs are UGC-DEB approved, which ensures equivalency with regular-mode degrees for government jobs, PSU recruitment, bank exams, and other public-sector opportunities.",
            },
            {
                "question": "Are Jain Online's MBA and MCA programs AICTE approved?",
                "answer": "Yes. Jain's online MBA and MCA programs specifically hold AICTE approval, in addition to the university's overall UGC-DEB entitlement.",
            },
            {
                "question": "Is Jain a deemed university?",
                "answer": "Yes. JAIN is a Deemed-to-be University with UGC Category I status.",
            },
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Chandigarh University Online",
        "short_description": (
            "Chandigarh University Online — UGC-entitled, AICTE-approved, NAAC A+ "
            "accredited online degrees delivered through the CU-VERSE learning platform."
        ),
        "full_description": (
            "Chandigarh University Online is the distance and online-learning division of "
            "Chandigarh University, founded in 2012 as a full-fledged private university "
            "under the Punjab State Legislature. Its online programs are delivered "
            "through CU-VERSE, a dedicated digital platform, and span undergraduate and "
            "postgraduate degrees in management, computer applications, and commerce."
        ),
        "why_choose": (
            "NAAC A+ accredited — unanimous across every source checked, including "
            "official domains. UGC-DEB and AICTE approved. WES-recognized, confirmed by "
            "two independent sources. Scholarships are a genuine, actively-marketed "
            "feature, confirmed via the official site's own banner. CU-VERSE: a dedicated "
            "online learning platform with live classes and recorded lectures."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "wes_approved": True,
        "placement_support": True,
        "meta_title": "Chandigarh University Online — NAAC A+ UGC-DEB Approved Degrees | CampusUnlock",
        "meta_description": (
            "Explore Chandigarh University Online's NAAC A+ accredited, UGC-DEB & AICTE "
            "approved MBA, MCA, and BBA programs — no entrance exam, WES-recognized, "
            "scholarships available."
        ),
        "faqs": [
            {
                "question": "Is Chandigarh University's online degree valid?",
                "answer": "Yes. Chandigarh University Online programs are UGC-DEB approved and NAAC A+ accredited, making the degrees valid for jobs, higher education, and government exams.",
            },
            {
                "question": "Do I need an entrance exam for CU Online programs?",
                "answer": "No. Admission to CU Online programs is merit-based on your academic performance — no entrance exam is required.",
            },
            {
                "question": "Is Chandigarh University Online AICTE approved?",
                "answer": "Yes. Chandigarh University holds AICTE approval in addition to its UGC-DEB entitlement and NAAC A+ accreditation.",
            },
        ],
        "scholarships": [
            {
                "title": "CU Online Early Bird / Merit Scholarship",
                "description": (
                    "Fee discount scholarship for CU Online programs. Confirmed as an "
                    "active, currently-running program via the official site's own "
                    "marketing banner. The exact discount percentage is single-sourced "
                    "(one aggregator cites 25% for the Online MBA specifically) and not "
                    "independently confirmed — verify current terms directly before "
                    "advertising a specific figure."
                ),
                "amount": None,
                "deadline": None,
            }
        ],
    },
    # ------------------------------------------------------------------
    {
        "name": "Dr. D. Y. Patil Vidyapeeth Online",
        "short_description": (
            "Dr. D. Y. Patil Vidyapeeth, Pune — NAAC accredited online degrees through "
            "its Centre for Online Learning (DPU-COL), with a distinctive healthcare-"
            "management specialization track."
        ),
        "full_description": (
            "Dr. D. Y. Patil Vidyapeeth, Pune is a deemed-to-be university offering online "
            "undergraduate and postgraduate programs through its Centre for Online "
            "Learning (DPU-COL). It's particularly known for healthcare-management "
            "specializations alongside standard MBA/BBA offerings. Note: 'D.Y. Patil' is a "
            "brand shared by multiple, legally distinct universities in India — this page "
            "covers Dr. D. Y. Patil Vidyapeeth, Pune (Pimpri, Sant Tukaram Nagar) "
            "specifically, not the separate D. Y. Patil (Deemed) University in Navi Mumbai."
        ),
        "why_choose": (
            "UGC-DEB and AICTE approved. Distinctive healthcare-management specialization "
            "track (Healthcare Management, Hospital Administration & Healthcare) alongside "
            "general management programs. A dedicated online-division-only placement cell."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Dr. D. Y. Patil Vidyapeeth Online — NAAC A++ Accredited Degrees | CampusUnlock",
        "meta_description": (
            "Explore Dr. D. Y. Patil Vidyapeeth's UGC-DEB approved, NAAC A++ accredited "
            "Online MBA and BBA — including specialized healthcare management tracks."
        ),
        "faqs": [
            {
                "question": "Is Dr. D. Y. Patil Vidyapeeth Online the same as D.Y. Patil University in Navi Mumbai?",
                "answer": "No. Dr. D. Y. Patil Vidyapeeth (Pune) and D. Y. Patil University (Navi Mumbai) are separate, distinct universities that share the D.Y. Patil name. Make sure you're comparing the correct institution when researching either one.",
            },
            {
                "question": "Is a DPU Online degree valid for jobs and higher education?",
                "answer": "Yes. DPU Online programs are UGC-DEB approved, and the university is NAAC accredited, so the degrees are recognized for both employment and further study.",
            },
            {
                "question": "What is DPU Online known for?",
                "answer": "DPU Online is particularly known for its healthcare-management specializations, in addition to standard MBA and BBA programs.",
            },
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Manipal University Jaipur Online",
        "short_description": (
            "MUJ Online — NAAC accredited online degrees from Manipal University Jaipur, "
            "part of the Manipal Education Group's shared \"Online Manipal\" platform."
        ),
        "full_description": (
            "Manipal University Jaipur Online is the online-learning platform of Manipal "
            "University Jaipur (MUJ), a state private university established in 2011 "
            "under a specific Rajasthan legislative act, and part of the wider Manipal "
            "Education Group. It's delivered through the shared \"Online Manipal\" "
            "platform, which also hosts online programs from two sibling Manipal-group "
            "institutions — Manipal Academy of Higher Education (MAHE) and Sikkim Manipal "
            "University (SMU), each separately and independently accredited."
        ),
        "why_choose": (
            "UGC-DEB and AICTE approved. Established in 2011 under a specific Rajasthan "
            "legislative act — well-confirmed across independent sources. Part of the "
            "wider Manipal Education Group's shared online learning platform, with an "
            "advanced digital platform designed around live sessions, recorded videos, "
            "and self-paced assessments."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        # placement_support intentionally left unset — no placement-specific claim found
        # for MUJ Online specifically across any source reviewed.
        "meta_title": "Manipal University Jaipur Online — NAAC A+ UGC-DEB Approved Degrees | CampusUnlock",
        "meta_description": (
            "Explore Manipal University Jaipur Online's NAAC A+ accredited, UGC-DEB and "
            "AICTE approved MBA, MCA, and BBA programs — part of the Manipal Education "
            "Group."
        ),
        "faqs": [
            {
                "question": "Is Manipal University Jaipur a real, accredited university?",
                "answer": "Yes. MUJ is a government-recognized state private university, established in 2011 under a specific Rajasthan legislative act, with UGC-DEB approval and NAAC accreditation for its online programs.",
            },
            {
                "question": "Is MUJ Online the same as MAHE Online?",
                "answer": "No, though they're related. Both are part of the Manipal Education Group and share the Online Manipal platform, but MUJ and MAHE are separately accredited, independently ranked institutions.",
            },
            {
                "question": "Is an MUJ Online degree accepted by employers?",
                "answer": "Yes. MUJ Online degrees are UGC-DEB approved and NAAC accredited, carrying the same recognition as on-campus degrees for both private and public sector jobs.",
            },
        ],
        "scholarships": [],
    },
    # ------------------------------------------------------------------
    {
        "name": "Sikkim Manipal University Distance Education",
        "short_description": (
            "SMU Distance Education — one of India's earliest UGC-DEB approved distance "
            "education providers, run as a public-private partnership between the "
            "Government of Sikkim and the Manipal Group."
        ),
        "full_description": (
            "Sikkim Manipal University (SMU) is a unique joint venture between the "
            "Government of Sikkim and the Manipal Group, incorporated under a 1995 State "
            "Legislative Act. Its Directorate of Distance Education (SMU-DE) was set up in "
            "2001 specifically to offer professional distance-learning programs in "
            "management and IT — making it one of the earlier entrants into UGC-DEB "
            "recognized distance education in India, well before \"online learning\" "
            "became a common category."
        ),
        "why_choose": (
            "UGC-DEB approved. A public-private partnership structure between the "
            "Government of Sikkim and the Manipal Group — a genuinely distinctive "
            "institutional fact. Over 5 lakh students have graduated from SMU-DE (per the "
            "university's own official page). A dedicated SMU-DE mobile app and personal "
            "academic advisors alongside core faculty."
        ),
        "ugc_approved": True,
        "placement_support": True,
        "meta_title": "SMU Distance Education — UGC-DEB Approved Since 2001 | CampusUnlock",
        "meta_description": (
            "Explore Sikkim Manipal University's Distance Education programs — UGC-DEB "
            "approved MBA, MCA, and BBA from one of India's earliest distance-learning "
            "providers."
        ),
        "faqs": [
            {
                "question": "Is SMU-DE one of the older distance education providers in India?",
                "answer": "Yes. Sikkim Manipal University's Directorate of Distance Education was set up in 2001, making it one of the earlier UGC-DEB recognized distance learning providers in India.",
            },
            {
                "question": "Who runs Sikkim Manipal University?",
                "answer": "SMU is a public-private partnership between the Government of Sikkim and the Manipal Group, incorporated under a 1995 State Legislative Act.",
            },
            {
                "question": "Does SMU-DE offer any special scholarships?",
                "answer": "SMU Online has been reported to offer scholarships for defense personnel, differently-abled learners, and students from North-Eastern regions, alongside standard reserved-category fee concessions — confirm current terms directly with the university.",
            },
        ],
        "scholarships": [
            {
                "title": "SMU Reserved-Category & Defense Scholarship",
                "description": (
                    "Reported scholarship categories for defense personnel, "
                    "differently-abled learners, and students from North-Eastern "
                    "regions. Single-sourced (same domain, two of its own pages) — "
                    "eligible categories were named but no specific discount amount "
                    "was given. Verify exact terms directly before publishing a figure."
                ),
                "amount": None,
                "deadline": None,
            }
        ],
    },

    # ==================================================================
    # NEW ENTRIES — from the 16 detail page research files (July 2026)
    # ==================================================================

    # ------------------------------------------------------------------
    # PARUL UNIVERSITY
    # Source anchor: UGC-DEB disclosure PDF HEI-Exempted-U-0763 (Mar 2023)
    # ------------------------------------------------------------------
    {
        "name": "Parul University",
        "short_description": (
            "Parul University Online — the youngest private university in India to receive "
            "NAAC A++ in its first assessment cycle, offering 13+ UGC-DEB approved online "
            "programs through its Centre for Distance and Online Education (CDOE)."
        ),
        "full_description": (
            "Parul University is a private multidisciplinary university in Vadodara, Gujarat, "
            "established in 2015 under the Gujarat Private Universities Act. Its online division "
            "operates under the Centre for Distance and Online Education (CDOE), with UGC-DEB "
            "registration ID HEI-Exempted-U-0763 (filed 2023). The university made national "
            "headlines as the youngest private university in India to achieve NAAC A++ "
            "accreditation in its first assessment cycle (CGPA 3.55, valid to February 2028). "
            "The online catalog spans 13+ UGC-approved programs at UG, PG, and Diploma levels, "
            "including MBA (20 specializations), MCA (AI/ML), BCA, BBA, BA, and M.Sc programs."
        ),
        "why_choose": (
            "NAAC A++ — India's youngest private university to achieve this in a first cycle "
            "(CGPA 3.55, valid to Feb 2028). UGC-DEB approved (HEI-Exempted-U-0763). AIU member. "
            "AICTE approved. 13+ online programs including MBA with 20 specializations and BCA "
            "with AI/ML, IoT, Cyber Security, and Blockchain tracks. No entrance exam — "
            "merit-based admission. 100% online delivery via AI-powered LMS with live sessions, "
            "proctored exams, and personalized mentorship."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "aiu_member": True,
        # wes_approved: NOT set — official site mentions WES only as a general pathway for
        # Indian graduates going abroad, not as a stated institutional recognition.
        "placement_support": True,
        "meta_title": "Parul University Online — UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore Parul University Online's UGC-DEB approved, NAAC A++ accredited MBA, BCA, "
            "BBA, MCA, and BA programs — 13+ online degrees from Gujarat's top-ranked private university."
        ),
        "faqs": [
            {
                "question": "Is Parul University Online UGC-DEB approved?",
                "answer": (
                    "Yes. Parul University is approved by the UGC Distance Education Bureau under "
                    "Registration ID HEI-Exempted-U-0763. Online degrees are legally equivalent to "
                    "on-campus degrees under UGC 2020 regulations."
                ),
            },
            {
                "question": "What is Parul University's NAAC accreditation?",
                "answer": (
                    "Parul University holds NAAC A++ — the highest possible grade — with a CGPA of 3.55, "
                    "assessed in 2023 and valid until February 2028. It is the youngest private university "
                    "in India to receive this grade in its first assessment cycle."
                ),
            },
            {
                "question": "Is Parul University Online a deemed university?",
                "answer": (
                    "No. Parul University is a private university established by the Government of Gujarat "
                    "under the Gujarat Private Universities Act — not a deemed-to-be university."
                ),
            },
            {
                "question": "Is there an entrance exam for Parul University Online admissions?",
                "answer": (
                    "No. Admissions are merit-based and do not require an entrance exam. Applications go "
                    "through the official admission portal at admissions.paruluniversity.ac.in."
                ),
            },
        ],
        "scholarships": [],
        # ⚠️ All known Parul scholarships (Sports, Cultural, Defence, Merit) are confirmed
        # for on-campus programs only — not confirmed for the online division. Leave empty.
    },

    # ------------------------------------------------------------------
    # BHARATI VIDYAPEETH
    # ⚠️ Name in UNIVERSITY_DEFS: "Bharati Vidyapeeth (Deemed to be University)"
    # This covers the School of Online Education (fully online), NOT the
    # separate School of Distance Education (blended / study centers).
    # ------------------------------------------------------------------
    {
        "name": "Bharati Vidyapeeth (Deemed to be University)",
        "short_description": (
            "Bharati Vidyapeeth Online — School of Online Education offering 100% online "
            "UGC-entitled MBA, MCA, BBA, and BCA programs from a NAAC A++ accredited "
            "UGC Category I Deemed University."
        ),
        "full_description": (
            "Bharati Vidyapeeth is a large, multi-campus deemed university founded in 1964 "
            "in Pune, holding UGC Category I Deemed University status. Its School of Online "
            "Education delivers 100% online UGC-entitled programs — distinct from its "
            "separately-run School of Distance Education, which uses a blended model with "
            "physical study centers. The university was re-accredited to NAAC A++ in 2024, "
            "up from A+ (third cycle, 2017)."
        ),
        "why_choose": (
            "NAAC A++ (2024 re-accreditation) — the highest grade. UGC Category I Deemed "
            "University. UGC-DEB and AICTE approved. 100% online delivery via live and "
            "recorded sessions, digital study materials, and online proctored exams. "
            "300+ total programs across the parent university."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "meta_title": "Bharati Vidyapeeth Online — NAAC A++ UGC-Entitled Degrees | CampusUnlock",
        "meta_description": (
            "Explore Bharati Vidyapeeth's School of Online Education — NAAC A++ accredited, "
            "UGC-entitled MBA, MCA, BBA, and BCA programs from a deemed university."
        ),
        "faqs": [
            {
                "question": "What is Bharati Vidyapeeth's current NAAC grade?",
                "answer": (
                    "Bharati Vidyapeeth holds NAAC's highest grade, A++, following a 2024 re-accreditation. "
                    "The university previously held an A+ grade (third cycle, 2017)."
                ),
            },
            {
                "question": "Is Bharati Vidyapeeth Online the same as its Distance Education program?",
                "answer": (
                    "No. Bharati Vidyapeeth runs two separate divisions: the School of Online Education "
                    "(fully online) and a separate School of Distance Education (a blended model with "
                    "physical study centers). Make sure you're applying to the right one."
                ),
            },
            {
                "question": "Is a Bharati Vidyapeeth Online degree valid?",
                "answer": (
                    "Yes. Programs are UGC-entitled and AICTE-approved (where applicable), and the "
                    "university is NAAC A++ accredited with UGC Category I Deemed University status."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # SANDIP UNIVERSITY
    # ⚠️ NO UGC-DEB online division confirmed as of July 2026.
    # Only parent-university fields populated here. Do NOT publish an
    # online detail page until UGC-DEB approval is confirmed.
    # ------------------------------------------------------------------
    {
        "name": "Sandip University",
        "short_description": (
            "Sandip University, Nashik — a NAAC 'A' accredited private university "
            "recognized by UGC, currently offering programs in regular on-campus mode."
        ),
        "full_description": (
            "Sandip University, Nashik is a private university established under Maharashtra "
            "Government Act No. XXXVIII of 2015, operational from 2017. It holds NAAC 'A' "
            "grade accreditation and UGC recognition. As of mid-2026, no UGC-DEB approved "
            "online or distance education division has been confirmed — programs are offered "
            "in regular on-campus mode, with some part-time options introduced from AY 2020-21. "
            "Note: a separate 'Sandip University Sijoul' exists in Bihar — these are legally "
            "distinct institutions."
        ),
        "why_choose": None,  # no online division to promote
        "ugc_approved": True,
        "aicte_approved": True,
        "aiu_member": True,
        # ugc_deb_approved / placement_support: not set — no online division confirmed
        "meta_title": None,
        "meta_description": None,
        "faqs": [
            {
                "question": "Is Sandip University recognized by UGC?",
                "answer": (
                    "Yes. Sandip University, Nashik is recognized by the UGC and was established under "
                    "Maharashtra Government Act No. XXXVIII of 2015."
                ),
            },
            {
                "question": "Does Sandip University offer online or distance programs?",
                "answer": (
                    "As of mid-2026, Sandip University Nashik does not appear to offer UGC-DEB approved "
                    "online or distance education programs. Programs are offered in regular on-campus mode, "
                    "with some part-time options introduced from AY 2020-21."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # SHARDA UNIVERSITY
    # ------------------------------------------------------------------
    {
        "name": "Sharda University",
        "short_description": (
            "Sharda University Online — NAAC A+ accredited, UGC-DEB approved online MBA, "
            "MCA, BBA, and BCA from a full-fledged private university in Greater Noida."
        ),
        "full_description": (
            "Sharda University is a private university in Greater Noida recognized under "
            "UGC Act 1956 Section 2(f) — not a deemed university. It is NAAC A+ accredited "
            "and an AIU (Association of Indian Universities) member. Its online division "
            "offers UGC-DEB approved programs in management and computer applications, "
            "with AI-driven assessments and personalized mentorship through a modern LMS."
        ),
        "why_choose": (
            "NAAC A+ accredited (9+ independent sources agree). UGC-DEB approved. AIU member "
            "— confirmed on the university's own official domain. Full-fledged private university "
            "under UGC Section 2(f) — not a deemed university. Career counseling, resume building, "
            "and interview prep confirmed across multiple sources."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "aiu_member": True,
        "placement_support": True,
        "meta_title": "Sharda University Online — NAAC A+ UGC-DEB Approved Degrees | CampusUnlock",
        "meta_description": (
            "Explore Sharda University Online's NAAC A+ accredited, UGC-DEB approved MBA, MCA, BBA, "
            "and BCA programs from a multidisciplinary private university in Greater Noida."
        ),
        "faqs": [
            {
                "question": "Is a Sharda University Online degree valid?",
                "answer": (
                    "Yes. Sharda University Online programs are UGC-DEB approved and the university is "
                    "NAAC A+ accredited, making the degree valid for both private and government jobs."
                ),
            },
            {
                "question": "Is Sharda a deemed university?",
                "answer": (
                    "No. Sharda University is a full-fledged private university recognized under "
                    "Section 2(f) of the UGC Act, 1956 — not a deemed-to-be university."
                ),
            },
            {
                "question": "What online programs does Sharda University offer?",
                "answer": (
                    "Sharda University Online offers UGC-DEB approved programs including MBA, MCA, BBA, "
                    "BCA, M.Com, and BA, delivered through a modern LMS with live and recorded sessions."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # SHOOLINI UNIVERSITY ONLINE
    # (already in EXISTING_UNIVERSITY_DEFS as "Shoolini University Online")
    # ------------------------------------------------------------------
    {
        "name": "Shoolini University Online",
        "short_description": (
            "Shoolini University Online (SCDOE) — UGC-DEB approved online degrees from a "
            "research-focused private university ranked 69th in NIRF 2025, with a "
            "distinctive 'Pay After Placement' MBA option."
        ),
        "full_description": (
            "Shoolini University is a research-focused private university in Solan, Himachal "
            "Pradesh, established in 2009 by a specific Himachal Pradesh state act. It has "
            "filed 1,500+ patents and operates 11 research centers. Its Centre for Online and "
            "Distance Education (SCDOE) offers UGC-DEB approved programs including a "
            "'Pay After Placement' MBA option — marketed as India's first — alongside "
            "standard online BBA, BCA, MCA, and commerce programs."
        ),
        "why_choose": (
            "UGC-DEB approved. NIRF 2025 rank: 69th (University category). 1,500+ patents "
            "filed, 11 research centers — a genuinely research-active institution. Distinctive "
            "'Pay After Placement' MBA option. ISO 9001:2015 certified quality management. "
            "Faculty/mentor network from IIMs, IITs, and international institutions."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        # ⚠️ NAAC grade genuinely uncertain: majority of sources say A+, but one specific
        # source says B+, and the official recognitions page avoids stating any grade.
        # Verify directly with Shoolini before publishing the grade.
        "meta_title": "Shoolini University Online — UGC-DEB Approved, NIRF-Ranked Degrees | CampusUnlock",
        "meta_description": (
            "Explore Shoolini University Online's UGC-DEB approved MBA, BBA, and MCA programs from a "
            "research-focused university ranked 69th in NIRF 2025."
        ),
        "faqs": [
            {
                "question": "Is a Shoolini University Online degree valid?",
                "answer": "Yes. Programs are UGC-DEB approved, making the degree valid for jobs and further study at par with on-campus programs.",
            },
            {
                "question": "What is Shoolini University's NIRF ranking?",
                "answer": "Shoolini University was ranked 69th in the University category in NIRF 2025.",
            },
            {
                "question": "Is Shoolini University research-focused?",
                "answer": "Yes. Shoolini University has over 1,500 patents filed and 11 dedicated research centers across its campus.",
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
    # Source anchor: official UGC-DEB government filing (deb.ugc.ac.in)
    # ------------------------------------------------------------------
    {
        "name": "SRM Institute of Science and Technology",
        "short_description": (
            "SRM Online — NAAC A++ accredited, UGC-DEB and AICTE approved online degrees "
            "from a UGC Category I deemed university with Graded Autonomy, backed by 40 "
            "years of academic history."
        ),
        "full_description": (
            "SRM Institute of Science and Technology (SRMIST), founded in 1985 as SRM "
            "Engineering College and granted deemed-university status in 2002, is one of "
            "Tamil Nadu's few UGC Category I institutions with Graded Autonomy. NAAC A++ "
            "accredited (score 3.55, per official UGC-DEB government filing). SRM Online "
            "offers UGC-DEB and AICTE approved programs with a dedicated Online Career "
            "Service Track (OCST) for placement support. Note: the institution was known "
            "as SRM University until 2017, when it reverted to its current name following "
            "a UGC order."
        ),
        "why_choose": (
            "NAAC A++ (score 3.55) — confirmed by the official UGC-DEB government filing, "
            "the highest-authority source possible. UGC Category I with Graded Autonomy — "
            "one of only 3 Tamil Nadu universities with this distinction. Dedicated Online "
            "Career Service Track (OCST) for placement. 172+ total online programs. Students "
            "can simultaneously pursue one full-time and one online degree per UGC guidelines."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "SRM Online — NAAC A++ UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore SRM Online's NAAC A++ accredited, UGC-DEB and AICTE approved MBA, MCA, BBA, "
            "and BCA programs from a deemed university with 40 years of academic history."
        ),
        "faqs": [
            {
                "question": "Is SRM Online's degree valid and recognized?",
                "answer": (
                    "Yes. SRM Online programs are UGC-DEB and AICTE approved, and SRMIST is a deemed "
                    "university with NAAC A++ — the highest grade possible."
                ),
            },
            {
                "question": "Can I pursue an SRM Online degree alongside a full-time program?",
                "answer": (
                    "Per UGC guidelines, students are permitted to pursue one full-time (offline) degree "
                    "and one online degree simultaneously — this is a general UGC policy, not specific to SRM."
                ),
            },
            {
                "question": "Is SRM University the same as SRM Institute of Science and Technology?",
                "answer": (
                    "Yes. The institution was known as SRM University until 2017, when it officially "
                    "reverted to SRM Institute of Science and Technology following a UGC order."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # UPES (UNIVERSITY OF PETROLEUM AND ENERGY STUDIES)
    # Source anchor: UPES's own official UGC-DEB mandatory disclosure PDF
    # ------------------------------------------------------------------
    {
        "name": "UPES (University of Petroleum and Energy Studies)",
        "short_description": (
            "UPES Online — UGC-DEB approved online degrees with a distinctive energy-sector "
            "specialization, including MBA tracks in Oil & Gas, Aviation, and Logistics & "
            "Supply Chain, from a NAAC 'A' accredited private university."
        ),
        "full_description": (
            "UPES is a private university in Dehradun established under the UPES Act 2003, "
            "distinguished by its focus on energy, engineering, and industry-aligned "
            "professional education. Its Centre for Distance and Online Education (CDOE) — "
            "under the UPES Online brand — offers UGC-DEB approved programs, particularly "
            "known for MBA specializations in Oil & Gas, Aviation, Power, and Logistics & "
            "Supply Chain that reflect the parent university's energy-sector identity. NAAC "
            "Grade A, Score 3.02, per the university's own government-filed disclosure document."
        ),
        "why_choose": (
            "Genuinely distinctive specialization: energy, aviation, oil & gas, and "
            "logistics/supply chain MBA tracks not found at most online universities. "
            "UGC-DEB approved, AIU member (3 independent sources). NIRF rank improved from "
            "100 (2021) to 65 (2022) per official filing. BBA (Aviation Management) — a "
            "distinctive UG offering tied to UPES's Aviation Studies department."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "aiu_member": True,
        "placement_support": True,
        "meta_title": "UPES Online — UGC-DEB Approved Energy & Management Degrees | CampusUnlock",
        "meta_description": (
            "Explore UPES Online's UGC-DEB approved MBA and BBA programs with unique specializations "
            "in Energy, Aviation, and Logistics — NAAC accredited, AIU member university."
        ),
        "faqs": [
            {
                "question": "Is UPES Online's degree valid and UGC recognized?",
                "answer": (
                    "Yes. UPES Online programs are UGC-DEB approved, and UPES is recognized under "
                    "Section 2(f) of the UGC Act, 1956, and is NAAC accredited."
                ),
            },
            {
                "question": "What makes UPES Online different from other online universities?",
                "answer": (
                    "UPES Online specializes in energy-sector and industry-aligned management programs — "
                    "including MBA specializations in Oil & Gas, Aviation, Power, and Logistics & Supply "
                    "Chain — reflecting the parent university's institutional focus on energy studies."
                ),
            },
            {
                "question": "What is UPES's NAAC grade?",
                "answer": (
                    "UPES holds a NAAC 'A' grade with a score of 3.02, per the university's own "
                    "official accreditation filing."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # UTTARANCHAL UNIVERSITY
    # ------------------------------------------------------------------
    {
        "name": "Uttaranchal University",
        "short_description": (
            "Uttaranchal University Online — Uttarakhand's first NAAC A+ accredited private "
            "university (CGPA 3.30), offering UGC-DEB approved MBA, MCA, BBA, and BCA online."
        ),
        "full_description": (
            "Uttaranchal University is a private university in Dehradun, established by "
            "Uttarakhand Act No. 11 of 2013. It was the first university in Uttarakhand to "
            "receive NAAC A+ accreditation in its first cycle (CGPA 3.30). Its online division "
            "offers UGC-DEB approved undergraduate and postgraduate programs in management, "
            "computer applications, and commerce. The university is recognized under Sections "
            "2(f) and 12(B) of the UGC Act."
        ),
        "why_choose": (
            "NAAC A+ — first university in Uttarakhand to achieve this in a first cycle (CGPA 3.30). "
            "UGC recognized under Sections 2(f) and 12(B). UGC-DEB and AICTE approved. Technology-"
            "enabled learning: live + recorded lectures, virtual labs, digital library, LMS, and "
            "online proctored exams. Early Bird scholarships available (verify current terms)."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Uttaranchal University Online — Uttarakhand's First NAAC A+ University | CampusUnlock",
        "meta_description": (
            "Explore Uttaranchal University Online's NAAC A+ accredited, UGC-DEB approved MBA, MCA, "
            "BBA, and BCA programs — Uttarakhand's first university with this accreditation."
        ),
        "faqs": [
            {
                "question": "Is Uttaranchal University Online degree valid?",
                "answer": (
                    "Yes. Programs are UGC-DEB approved and the university is NAAC A+ accredited — the "
                    "first university in Uttarakhand to achieve this in its first accreditation cycle."
                ),
            },
            {
                "question": "Is Uttaranchal University a deemed university?",
                "answer": (
                    "No. Uttaranchal University is a private university established by a specific "
                    "Uttarakhand state legislative act (2013), recognized under Sections 2(f) and 12(B) "
                    "of the UGC Act, 1956."
                ),
            },
        ],
        "scholarships": [
            {
                "title": "UU Online Early Bird Scholarship — MBA",
                "description": "30% fee discount for early applicants to the Online MBA. Single-sourced — verify current terms directly with the university.",
                "amount": None,
                "deadline": None,
            },
            {
                "title": "UU Online Early Bird Scholarship — MCA",
                "description": "20% fee discount for early applicants to the Online MCA. Single-sourced — verify current terms directly with the university.",
                "amount": None,
                "deadline": None,
            },
            {
                "title": "UU Online Early Bird Scholarship — BBA/BCA/BA",
                "description": "15% fee discount for early applicants to Online BBA, BCA, and BA programs. Single-sourced — verify current terms directly with the university.",
                "amount": None,
                "deadline": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # VIVEKANANDA GLOBAL UNIVERSITY ONLINE
    # (in EXISTING_UNIVERSITY_DEFS as "Vivekananda Global University Online")
    # ⚠️ DB currently has "NAAC B++" — 10 of 11 sources including VGU's own
    # domain say A+ (score 3.29/4). Almost certainly a DB error. Fix in
    # UNIVERSITY_DEFS directly.
    # ------------------------------------------------------------------
    {
        "name": "Vivekananda Global University Online",
        "short_description": (
            "VGU Online — UGC-DEB approved online degrees from India's youngest NAAC A+ "
            "accredited university (score 3.29/4), offering MBA, MCA, BBA, BCA, BA, and "
            "MA programs through its Centre for Distance and Online Education."
        ),
        "full_description": (
            "Vivekananda Global University (VGU) is a private university in Jaipur established "
            "in 2012 under the Bagaria Education Trust. It is marketed as 'India's youngest "
            "NAAC A+ university' (score 3.29/4) — this exact phrase appears on VGU's own "
            "official site. Its Centre for Distance and Online Education (CDOE) offers "
            "UGC-DEB approved programs including MBA, MCA, MA (English and JMC), M.Sc "
            "Mathematics at PG level and BBA, BCA, and BA at UG level."
        ),
        "why_choose": (
            "NAAC A+ (score 3.29/4) — marketed by VGU itself as 'India's youngest NAAC A+ "
            "university.' UGC-DEB and AICTE approved. 8 programs (3 UG + 5 PG). Dedicated "
            "placement cell and career counseling. Industry certifications integrated into "
            "programs. Self-paced, mobile-friendly platform with live sessions and "
            "one-on-one career counseling."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "VGU Online — NAAC A+ UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore Vivekananda Global University's NAAC A+ accredited, UGC-DEB approved Online MBA, "
            "MCA, BBA, and BCA — from India's youngest NAAC A+ university."
        ),
        "faqs": [
            {
                "question": "What is VGU Online's NAAC accreditation grade?",
                "answer": (
                    "Vivekananda Global University holds NAAC A+ with a score of 3.29/4, and is marketed "
                    "by the university itself as India's youngest NAAC A+ accredited institution."
                ),
            },
            {
                "question": "Is a VGU Online degree valid for jobs and further study?",
                "answer": (
                    "Yes. VGU Online programs are UGC-DEB approved, meaning the degree is treated at par "
                    "with a regular on-campus degree for both employment and higher education."
                ),
            },
            {
                "question": "What programs does VGU Online offer?",
                "answer": (
                    "VGU Online offers 3 UG programs (BBA, BCA, BA) and 5 PG programs (MBA, MCA, "
                    "MA English, MA JMC, M.Sc Mathematics)."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # VELS INSTITUTE OF SCIENCE, TECHNOLOGY AND ADVANCED STUDIES (VISTAS)
    # ⚠️ Confirmed online catalog is narrow — only 1 program (M.Sc Data
    # Science & Business Analytics) clearly confirmed as online offering.
    # ⚠️ UGC-DEB approval for the online division not explicitly confirmed.
    # ------------------------------------------------------------------
    {
        "name": "Vels Institute of Science, Technology and Advanced Studies (VISTAS)",
        "short_description": (
            "VISTAS Online — NAAC A++ accredited deemed university (upgraded Nov 2024) "
            "offering an Online M.Sc in Data Science & Business Analytics, with roots "
            "going back to 1992 and 34 campuses across India."
        ),
        "full_description": (
            "VISTAS (Vels Institute of Science, Technology & Advanced Studies), known as Vels "
            "University, was declared a Deemed-to-be University by the Ministry of Education "
            "in 2008, with institutional roots going back to 1992. NAAC upgraded the "
            "institution to A++ in late 2024 (from 'A'). VISTAS Online currently offers an "
            "Online M.Sc in Data Science & Business Analytics. The parent institution has "
            "34 campuses, 48,000+ students, and 7,700+ faculty and staff."
        ),
        "why_choose": (
            "NAAC A++ (awarded late 2024 — the highest grade). Large, established institution: "
            "34 campuses, 48,000+ students. Curriculum developed by academicians and industry "
            "experts. Technology-enabled learning with dedicated learner support."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        # ugc_deb_approved: NOT set — not explicitly confirmed for the online division.
        # placement_support: NOT set — on-campus Career Development Cell is documented
        # but not confirmed as extending to the (new and narrow) online division.
        "meta_title": "VISTAS Online — NAAC A++ Accredited Deemed University | CampusUnlock",
        "meta_description": (
            "Explore VISTAS Online's Data Science & Business Analytics M.Sc. from a NAAC A++ accredited "
            "deemed university with 34 campuses and over 48,000 students."
        ),
        "faqs": [
            {
                "question": "What is VISTAS's current NAAC grade?",
                "answer": (
                    "VISTAS holds NAAC's highest grade, A++, awarded in late 2024. The institution "
                    "previously held an 'A' grade before this upgrade."
                ),
            },
            {
                "question": "What online programs does VISTAS currently offer?",
                "answer": (
                    "VISTAS Online's confirmed offering is the Online M.Sc. in Data Science & Business "
                    "Analytics. Confirm additional programs directly with the university."
                ),
            },
            {
                "question": "Is VISTAS a deemed university?",
                "answer": (
                    "Yes. VISTAS was declared a Deemed-to-be University by the Ministry of Education "
                    "in 2008, building on an institutional history dating back to 1992."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # JAMIA HAMDARD
    # ------------------------------------------------------------------
    {
        "name": "Jamia Hamdard",
        "short_description": (
            "Jamia Hamdard Online — UGC-DEB approved online MBA, MCA, BBA, BCA, and B.Com "
            "from a deemed university ranked #1 in India for Pharmacy by NIRF across "
            "multiple years."
        ),
        "full_description": (
            "Jamia Hamdard is a deemed-to-be university established in 1989 under Section 3 "
            "of the UGC Act, 1956, nationally recognized for Pharmacy, Unani medicine, and "
            "health sciences. Its School of Pharmaceutical Education and Research has been "
            "ranked #1 in India for Pharmacy by NIRF across multiple years. Its Centre for "
            "Distance and Online Education (CDOE) offers a broad UGC-DEB approved catalog "
            "spanning MBA (7 specializations), MCA, BBA, BCA, B.Com, and MA programs."
        ),
        "why_choose": (
            "UGC-DEB and AICTE approved. Deemed-to-be University under Section 3, UGC Act "
            "1956. #1 in India for Pharmacy by NIRF — reflects strong institutional research "
            "culture. Broad online catalog: MBA (7 specializations including Data Science and "
            "Digital Marketing), MCA, BBA, BCA, B.Com, MA. Career advice sessions, resume "
            "writing, interview prep, and technical mentoring confirmed across multiple sources."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Jamia Hamdard Online — UGC-DEB Approved Degrees | CampusUnlock",
        "meta_description": (
            "Explore Jamia Hamdard's UGC-DEB approved Online MBA, MCA, BBA, and BCA programs from a "
            "deemed university ranked #1 in Pharmacy by NIRF."
        ),
        "faqs": [
            {
                "question": "Is a Jamia Hamdard Online degree valid?",
                "answer": (
                    "Yes. Programs are UGC-DEB approved, making the degree equivalent to a regular "
                    "on-campus degree for employment, higher education, and government/PSU recruitment."
                ),
            },
            {
                "question": "What is Jamia Hamdard known for academically?",
                "answer": (
                    "Jamia Hamdard's School of Pharmaceutical Education and Research has been ranked "
                    "#1 in India for Pharmacy by NIRF across multiple years."
                ),
            },
            {
                "question": "What programs does Jamia Hamdard Online offer?",
                "answer": (
                    "Jamia Hamdard Online offers UGC-DEB approved MBA (7 specializations), MCA, MA, "
                    "BBA, BCA, and B.Com programs through its Centre for Distance and Online Education."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # MIT WORLD PEACE UNIVERSITY
    # ⚠️ ENTITY CONFUSION — the online/distance program may actually be
    # run by MITSDE (a separate sister body, founded 2008), not MIT-WPU
    # itself. Resolve before publishing an online detail page.
    # ⚠️ university_type in UNIVERSITY_DEFS is "Deemed University" — this
    # is WRONG. MIT-WPU is a Private University (Maharashtra state act 2017).
    # Fix in UNIVERSITY_DEFS.
    # ------------------------------------------------------------------
    {
        "name": "MIT World Peace University",
        "short_description": (
            "MIT World Peace University — a private university in Pune established in 2017 "
            "by a Maharashtra state act, known for its on-campus MBA and engineering programs."
        ),
        "full_description": (
            "MIT World Peace University (MIT-WPU) was established in 2017 under a specific "
            "Maharashtra state legislative act, granting it full private-university status. "
            "It traces its roots to 1983 (Maharashtra Institute of Technology). MIT-WPU is "
            "explicitly not a deemed university. Note: the online/distance programs in this "
            "space appear to be run by MIT School of Distance Education (MITSDE) — a legally "
            "separate but affiliated institution founded in 2008, offering AICTE-approved PGDM "
            "and Executive MBA diplomas rather than UGC-DEB university degrees. Confirm which "
            "entity a listing represents before publishing."
        ),
        "why_choose": None,  # entity question must be resolved first
        "ugc_approved": True,
        "aicte_approved": True,
        # ugc_deb_approved: NOT set — appears to belong to MITSDE (sister body), not MIT-WPU
        "meta_title": None,
        "meta_description": None,
        "faqs": [
            {
                "question": "Is MIT World Peace University a deemed university?",
                "answer": (
                    "No. MIT-WPU is a private university established by a specific Maharashtra state "
                    "legislative act (2017), not a deemed-to-be university."
                ),
            },
            {
                "question": "Is MIT-WPU Online the same as MITSDE?",
                "answer": (
                    "Not necessarily. Available evidence suggests the online/distance program is run by "
                    "MIT School of Distance Education (MITSDE), a separate but affiliated institution "
                    "founded in 2008, offering AICTE-approved PGDM diplomas rather than UGC-DEB "
                    "university degrees. Confirm with the institution directly."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # ALLIANCE UNIVERSITY
    # One of the cleanest, most confidently-verified entries in this batch.
    # ------------------------------------------------------------------
    {
        "name": "Alliance University",
        "short_description": (
            "Alliance University Online — NAAC A+ accredited, UGC-DEB approved online MBA, "
            "BBA, and B.Com from the first private university in South India, with "
            "international IACBE and AACSB accreditation. No entrance exam required."
        ),
        "full_description": (
            "Alliance University is a private university in Bengaluru, established in 2010 "
            "by a specific Karnataka state act — the first private university in South India. "
            "Alliance University Online holds NAAC A+ accreditation (CGPA range 3.26–3.50, "
            "correctly matching NAAC's A+ band) and international business-school "
            "accreditations from IACBE and AACSB (USA). Online programs require no entrance "
            "exam and include a mandatory internship component for BBA and professional "
            "certification alignment (CA/ACCA/CMA/NCFM/NISM) for B.Com."
        ),
        "why_choose": (
            "NAAC A+ — unanimous across 9+ sources; CGPA range correctly matches NAAC's A+ "
            "band. First private university in South India (Karnataka Act 34 of 2010). "
            "International accreditations: IACBE and AACSB (USA). UGC-DEB approved. No "
            "entrance exam required. B.Com aligned with CA, ACCA, CMA, NCFM, and NISM "
            "certifications. BBA includes mandatory internships."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Alliance University Online — NAAC A+ UGC-DEB Approved Degrees | CampusUnlock",
        "meta_description": (
            "Explore Alliance University Online's NAAC A+ accredited, UGC-DEB approved MBA, BBA, and "
            "B.Com programs — no entrance exam required, 15+ years of academic legacy."
        ),
        "faqs": [
            {
                "question": "Is Alliance University a deemed university?",
                "answer": (
                    "No. Alliance University is a private university established by a specific "
                    "Karnataka state act (2010) — it is explicitly not a deemed-to-be university."
                ),
            },
            {
                "question": "Do I need an entrance exam for Alliance University Online?",
                "answer": (
                    "No. Alliance University Online's MBA, BBA, and B.Com programs do not require an "
                    "entrance exam — admission is based on prior academic qualifications."
                ),
            },
            {
                "question": "Is Alliance University Online's degree valid?",
                "answer": (
                    "Yes. Programs are UGC-DEB approved and NAAC A+ accredited, making the degree "
                    "valid for both government and private sector employment nationwide."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # DAYANANDA SAGAR UNIVERSITY
    # ⚠️ DSU and Dayananda Sagar College of Engineering (DSCE) are separate
    # institutions within the DSI group — do not conflate their data.
    # ⚠️ IIRF rankings ≠ NIRF rankings — different organizations.
    # ------------------------------------------------------------------
    {
        "name": "Dayananda Sagar University",
        "short_description": (
            "Dayananda Sagar University Online — NAAC A+ accredited, UGC-DEB approved online "
            "MBA (8 specializations including Healthcare and FinTech), MCA, BBA, BCA, and "
            "B.Com, backed by a 60-year Dayananda Sagar Institutions legacy."
        ),
        "full_description": (
            "Dayananda Sagar University (DSU) was established in 2014 under the Karnataka "
            "Private Universities Act as the newest phase of the Dayananda Sagar Institutions "
            "(DSI) group — founded over 60 years ago by Sri R. Dayananda Sagar. DSU Online is "
            "its dedicated online learning division, offering UGC-DEB approved programs. The "
            "MBA features 8 specializations including niche tracks in Healthcare Management, "
            "AI, FinTech, and Entrepreneurship Management. Note: DSU and Dayananda Sagar "
            "College of Engineering (DSCE) are separate institutions within the DSI group."
        ),
        "why_choose": (
            "NAAC A+ — confirmed by 10+ sources including Wikipedia. UGC-DEB approved (4+ "
            "independent sources for the online division specifically). MBA with 8 specializations "
            "including rare niche tracks: Healthcare, FinTech, AI, and Entrepreneurship Management. "
            "60-year Dayananda Sagar Group educational legacy. Degree certificate explicitly "
            "identifies program as 'Online mode' per UGC 2018 Regulations."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "DSU Online — NAAC A+ UGC-DEB Approved Online Degrees | CampusUnlock",
        "meta_description": (
            "Explore Dayananda Sagar University Online's NAAC A+ accredited, UGC-DEB approved MBA, "
            "MCA, BBA, and BCA programs — 60 years of educational legacy."
        ),
        "faqs": [
            {
                "question": "Is a Dayananda Sagar University Online degree valid?",
                "answer": (
                    "Yes. DSU Online programs are UGC-DEB approved and the university is NAAC A+ "
                    "accredited, making the degree valid for both private and PSU recruitment."
                ),
            },
            {
                "question": "Is DSU Online the same as Dayananda Sagar College of Engineering?",
                "answer": (
                    "No. DSU and DSCE are separate institutions under the wider Dayananda Sagar "
                    "Institutions group — DSU is a private university established in 2014, while DSCE "
                    "is a separate autonomous college affiliated with VTU, established in 1979."
                ),
            },
            {
                "question": "What programs does DSU Online offer?",
                "answer": (
                    "DSU Online offers UGC-DEB approved programs including MBA (8 specializations: "
                    "AI, Business Analytics, Entrepreneurship Management, FinTech, Healthcare, IT, "
                    "and others), MCA, BBA, BCA, and B.Com."
                ),
            },
        ],
        "scholarships": [],
        # ⚠️ DSAT scholarship mechanism exists for on-campus DSU programs but is NOT
        # confirmed for the online division. Leave empty until verified.
    },

    # ==================================================================
    # ON-CAMPUS / GENERAL UNIVERSITIES
    # Entries below cover prominent institutions in universities.py that
    # don't have an online division detail page. Fields are populated
    # only from well-documented public facts — no fabrication.
    # ==================================================================

    # ------------------------------------------------------------------
    # MANIPAL ACADEMY OF HIGHER EDUCATION (MAHE)
    # ------------------------------------------------------------------
    {
        "name": "Manipal Academy of Higher Education",
        "short_description": (
            "Manipal Academy of Higher Education (MAHE) — NAAC A++ accredited deemed "
            "university in Manipal, Karnataka, consistently ranked among India's top "
            "private universities with a 70+ year legacy of global education."
        ),
        "full_description": (
            "Manipal Academy of Higher Education (MAHE), popularly known as Manipal University, "
            "is a deemed-to-be university located in Manipal, Karnataka, with a history spanning "
            "over 70 years. Founded by Dr. T.M.A. Pai in 1953, MAHE is one of India's most "
            "recognized private universities, known for its strengths in medicine, engineering, "
            "management, and allied health sciences. The Manipal Education Group also operates "
            "campuses internationally, including in Dubai and Antigua. MAHE offers programs "
            "online through the shared 'Online Manipal' platform alongside sibling institutions "
            "MUJ and SMU."
        ),
        "why_choose": (
            "NAAC A++ accredited — the highest grade. Consistently ranked among India's top "
            "private universities by NIRF. 70+ year legacy with global campus presence "
            "(Manipal, Jaipur, Sikkim, Dubai, Antigua). Strong placement record in medicine, "
            "engineering, and management. Part of the Manipal Education Group."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Manipal Academy of Higher Education (MAHE) — Fees, Courses & Reviews | CampusUnlock",
        "meta_description": (
            "Explore Manipal Academy of Higher Education (MAHE) — NAAC A++ accredited, "
            "top-ranked deemed university in Manipal with programs in medicine, engineering, "
            "management, and more."
        ),
        "faqs": [
            {
                "question": "Is MAHE the same as Manipal University?",
                "answer": (
                    "Yes. Manipal Academy of Higher Education (MAHE) was formerly known as "
                    "Manipal University. The name was changed following a UGC directive requiring "
                    "the term 'university' be dropped from private deemed-university names."
                ),
            },
            {
                "question": "Is MAHE a deemed university?",
                "answer": (
                    "Yes. MAHE is a deemed-to-be university under Section 3 of the UGC Act, 1956, "
                    "with NAAC A++ accreditation and UGC Category I status."
                ),
            },
            {
                "question": "Does MAHE offer online programs?",
                "answer": (
                    "Yes. MAHE offers online programs through the 'Online Manipal' platform, "
                    "alongside sibling institutions Manipal University Jaipur (MUJ) and "
                    "Sikkim Manipal University (SMU). Each institution is independently accredited."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # VELLORE INSTITUTE OF TECHNOLOGY (VIT)
    # ------------------------------------------------------------------
    {
        "name": "Vellore Institute of Technology (VIT)",
        "short_description": (
            "VIT — NAAC A++ accredited deemed university in Vellore, consistently among "
            "India's top 10 engineering institutions in NIRF, known for strong industry "
            "placements and international academic partnerships."
        ),
        "full_description": (
            "Vellore Institute of Technology (VIT) is a deemed-to-be university founded in 1984 "
            "in Vellore, Tamil Nadu. It has grown into one of India's most prominent engineering "
            "and technology universities, with campuses in Vellore, Chennai, Bhopal, and Amaravati. "
            "VIT is NAAC A++ accredited and holds UGC Category I status with Graded Autonomy. "
            "It is consistently ranked among India's top 10 engineering institutions by NIRF and "
            "has extensive international partnerships with universities across the USA, UK, "
            "Australia, and Europe."
        ),
        "why_choose": (
            "NAAC A++ accredited. Consistently top-10 in NIRF Engineering rankings. "
            "UGC Category I with Graded Autonomy. Strong global academic partnerships. "
            "4 campuses across India. Dedicated placement cell with 500+ recruiters. "
            "Industry-aligned curriculum with research centers across all major engineering disciplines."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "VIT University — Fees, Courses, Rankings & Placements | CampusUnlock",
        "meta_description": (
            "Explore VIT Vellore — NAAC A++ accredited, top-ranked engineering deemed university "
            "with strong placements and 4 campuses across India."
        ),
        "faqs": [
            {
                "question": "Is VIT a deemed university?",
                "answer": (
                    "Yes. VIT is a deemed-to-be university under Section 3 of the UGC Act, 1956, "
                    "with NAAC A++ accreditation and UGC Category I status with Graded Autonomy."
                ),
            },
            {
                "question": "Which campuses does VIT have?",
                "answer": "VIT has campuses in Vellore, Chennai, Bhopal, and Amaravati.",
            },
            {
                "question": "What is VIT's NIRF ranking?",
                "answer": (
                    "VIT is consistently ranked among India's top 10 engineering institutions by NIRF. "
                    "Check the latest NIRF results at nirfindia.org for the current year's rank."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # CHRIST UNIVERSITY (DEEMED TO BE UNIVERSITY)
    # ------------------------------------------------------------------
    {
        "name": "Christ University (Deemed to be University)",
        "short_description": (
            "Christ University — NAAC A+ accredited deemed university in Bengaluru, known "
            "for its commerce, management, and liberal arts programs, with campuses in "
            "Pune, Delhi NCR, and Kengeri."
        ),
        "full_description": (
            "Christ University is a deemed-to-be university in Bengaluru, Karnataka, established "
            "in 1969 as Christ College and granted deemed-university status in 2008. It is NAAC "
            "A+ accredited and is particularly well-known for its B.Com, BBA, MBA, and liberal "
            "arts programs. Christ University operates multiple campuses across Bengaluru (Lavelle "
            "Road, Kengeri) and has extended campuses in Pune and Delhi NCR. It emphasizes a "
            "holistic education model combining academic excellence with personal development."
        ),
        "why_choose": (
            "NAAC A+ accredited. Known for strong commerce and management programs — BBA, B.Com, "
            "MBA. Multi-campus presence: Bengaluru (main), Pune, Delhi NCR. Holistic education "
            "model with emphasis on research, leadership, and co-curricular development. "
            "Strong alumni network across finance, consulting, and corporate sectors."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Christ University Bengaluru — Fees, Courses & Placements | CampusUnlock",
        "meta_description": (
            "Explore Christ University — NAAC A+ accredited deemed university in Bengaluru, "
            "known for BBA, B.Com, MBA, and liberal arts programs with multi-campus presence."
        ),
        "faqs": [
            {
                "question": "Is Christ University a deemed university?",
                "answer": (
                    "Yes. Christ University was granted deemed-university status by the UGC in 2008. "
                    "It is NAAC A+ accredited."
                ),
            },
            {
                "question": "What is Christ University known for?",
                "answer": (
                    "Christ University is particularly known for its commerce and management programs "
                    "(BBA, B.Com, MBA), as well as liberal arts and psychology, with a holistic "
                    "education approach."
                ),
            },
            {
                "question": "How many campuses does Christ University have?",
                "answer": (
                    "Christ University has campuses in Bengaluru (Lavelle Road main campus and Kengeri), "
                    "Pune, and Delhi NCR."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # KALINGA INSTITUTE OF INDUSTRIAL TECHNOLOGY (KIIT)
    # ------------------------------------------------------------------
    {
        "name": "Kalinga Institute of Industrial Technology (KIIT)",
        "short_description": (
            "KIIT — NAAC A++ accredited deemed university in Bhubaneswar, Odisha, "
            "consistently ranked among India's top engineering universities with a strong "
            "placement record and international academic partnerships."
        ),
        "full_description": (
            "Kalinga Institute of Industrial Technology (KIIT) is a deemed-to-be university "
            "in Bhubaneswar, Odisha, founded in 1992 by Dr. Achyuta Samanta. It achieved "
            "deemed-university status in 2004 and has since grown into one of eastern India's "
            "most prominent technical universities. KIIT is NAAC A++ accredited and consistently "
            "ranked in the top 30 engineering institutions by NIRF. It offers programs across "
            "engineering, management, law, medicine, and the arts, with a large residential "
            "campus hosting students from 65+ countries."
        ),
        "why_choose": (
            "NAAC A++ accredited. Consistently top-30 in NIRF Engineering rankings. "
            "Large residential campus with students from 65+ countries. Strong placement "
            "record with 350+ recruiters. Programs across engineering, management, law, "
            "and medicine. Founded with a strong social mission — affiliated with KISS "
            "(Kalinga Institute of Social Sciences)."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "KIIT University — Fees, Courses, Rankings & Placements | CampusUnlock",
        "meta_description": (
            "Explore KIIT Deemed University — NAAC A++ accredited, top-ranked engineering "
            "university in Bhubaneswar with strong placements and international student community."
        ),
        "faqs": [
            {
                "question": "Is KIIT a deemed university?",
                "answer": (
                    "Yes. KIIT was granted deemed-university status in 2004. It is NAAC A++ "
                    "accredited with UGC recognition."
                ),
            },
            {
                "question": "Where is KIIT located?",
                "answer": "KIIT is located in Bhubaneswar, Odisha, with a large self-contained residential campus.",
            },
            {
                "question": "What programs does KIIT offer?",
                "answer": (
                    "KIIT offers programs across engineering, management (MBA), law, medicine, "
                    "biotechnology, and the arts, at both UG and PG levels."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # AMRITA VISHWA VIDYAPEETHAM
    # ------------------------------------------------------------------
    {
        "name": "Amrita Vishwa Vidyapeetham",
        "short_description": (
            "Amrita Vishwa Vidyapeetham — NAAC A++ accredited deemed university with "
            "campuses across six states, consistently ranked among India's top 10 "
            "universities by NIRF, known for engineering, medicine, and research."
        ),
        "full_description": (
            "Amrita Vishwa Vidyapeetham is a multi-campus deemed-to-be university founded "
            "under the guidance of Sri Mata Amritanandamayi Devi (Amma), with its main campus "
            "in Coimbatore, Tamil Nadu. It has campuses in Tamil Nadu, Kerala, Karnataka, "
            "Andhra Pradesh, Maharashtra, and Delhi NCR. Amrita is NAAC A++ accredited and "
            "has been consistently ranked among India's top 10 universities overall by NIRF. "
            "It is particularly strong in engineering, medicine, pharmacy, and social sciences, "
            "with a large research output and over 1,600 patents filed."
        ),
        "why_choose": (
            "NAAC A++ accredited. Consistently top-10 in NIRF Overall University rankings. "
            "Multi-campus across 6 states. 1,600+ patents filed — strong research focus. "
            "Programs in engineering, medicine, pharmacy, management, and social sciences. "
            "Strong industry connections and placement record."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Amrita Vishwa Vidyapeetham — Fees, Courses & Rankings | CampusUnlock",
        "meta_description": (
            "Explore Amrita Vishwa Vidyapeetham — NAAC A++ accredited, top-10 NIRF-ranked "
            "deemed university with campuses across 6 states in India."
        ),
        "faqs": [
            {
                "question": "Is Amrita Vishwa Vidyapeetham a deemed university?",
                "answer": "Yes. Amrita Vishwa Vidyapeetham is a deemed-to-be university with NAAC A++ accreditation.",
            },
            {
                "question": "How many campuses does Amrita have?",
                "answer": (
                    "Amrita has campuses across six states — Tamil Nadu (Coimbatore, Chennai), "
                    "Kerala (Kochi, Thiruvananthapuram, Kollam), Karnataka (Bengaluru), "
                    "Andhra Pradesh (Amaravati), Maharashtra, and Delhi NCR."
                ),
            },
            {
                "question": "What is Amrita's NIRF ranking?",
                "answer": "Amrita Vishwa Vidyapeetham is consistently ranked among India's top 10 universities overall by NIRF.",
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # SYMBIOSIS INTERNATIONAL (DEEMED UNIVERSITY)
    # ------------------------------------------------------------------
    {
        "name": "Symbiosis International (Deemed University)",
        "short_description": (
            "Symbiosis International — NAAC A accredited deemed university in Pune, "
            "known for its constituent institutes in management (SIBM), law (SLS), "
            "media, and IT, with a strong international student community."
        ),
        "full_description": (
            "Symbiosis International (Deemed University) is a multi-institutional deemed "
            "university in Pune, Maharashtra, established in 2002. It operates through a "
            "federation of specialized constituent institutes, most notably the Symbiosis "
            "Institute of Business Management (SIBM), Symbiosis Law School (SLS), Symbiosis "
            "Institute of Technology (SIT), and Symbiosis Centre for Management Studies (SCMS). "
            "It is NAAC A accredited and known for attracting a large international student "
            "body, particularly from South Asia and Africa."
        ),
        "why_choose": (
            "NAAC A accredited. Specialized constituent institutes covering management, law, "
            "media, and technology — rather than one generalist university. Strong international "
            "student community and global exposure. SIBM's MBA is among the most sought-after "
            "management programs in western India. Centrally located in Pune with easy industry "
            "access."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Symbiosis International University — Fees, Courses & Placements | CampusUnlock",
        "meta_description": (
            "Explore Symbiosis International Deemed University, Pune — NAAC A accredited, "
            "known for SIBM MBA, Symbiosis Law School, and strong international community."
        ),
        "faqs": [
            {
                "question": "Is Symbiosis a deemed university?",
                "answer": "Yes. Symbiosis International is a deemed-to-be university, established in 2002, with NAAC A accreditation.",
            },
            {
                "question": "What is Symbiosis known for?",
                "answer": (
                    "Symbiosis is best known for its management programs (SIBM MBA), law programs "
                    "(SLS), and media/communication courses, through its network of specialized "
                    "constituent institutes."
                ),
            },
            {
                "question": "Does Symbiosis require an entrance exam?",
                "answer": (
                    "Yes. Most Symbiosis programs require the SET (Symbiosis Entrance Test), "
                    "specific to each constituent institute. Some programs also accept CAT/MAT scores."
                ),
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # CHITKARA UNIVERSITY
    # ------------------------------------------------------------------
    {
        "name": "Chitkara University",
        "short_description": (
            "Chitkara University — NAAC A+ accredited private university in Punjab, "
            "known for its engineering, business, and health sciences programs with "
            "strong industry partnerships and placement record."
        ),
        "full_description": (
            "Chitkara University is a private university in Rajpura, Punjab, established "
            "in 2010 under the Chitkara University Punjab Act. It is NAAC A+ accredited "
            "and offers programs across engineering, business administration, pharmacy, "
            "health sciences, education, and the arts. The university has a reputation "
            "for strong industry linkages, entrepreneurship support through its innovation "
            "hub, and high placement rates in core engineering and IT sectors."
        ),
        "why_choose": (
            "NAAC A+ accredited. Strong engineering, IT, and business programs. "
            "Industry-integrated curriculum with dedicated placement cell. "
            "Innovation and entrepreneurship hub on campus. "
            "Two campuses in Punjab and Himachal Pradesh."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "Chitkara University — Fees, Courses & Placements | CampusUnlock",
        "meta_description": (
            "Explore Chitkara University Punjab — NAAC A+ accredited private university "
            "with strong engineering, business, and health sciences programs."
        ),
        "faqs": [
            {
                "question": "Is Chitkara University recognized by UGC?",
                "answer": "Yes. Chitkara University is a UGC-recognized private university established under the Chitkara University Punjab Act, 2010.",
            },
            {
                "question": "What programs is Chitkara University known for?",
                "answer": "Chitkara University is well-known for its engineering (B.Tech), pharmacy, business administration, and health sciences programs.",
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # BITS PILANI
    # ------------------------------------------------------------------
    {
        "name": "Birla Institute of Technology and Science, Pilani (BITS Pilani)",
        "short_description": (
            "BITS Pilani — one of India's most prestigious private engineering universities, "
            "a deemed-to-be university consistently ranked in the top 25 by NIRF, known "
            "for its rigorous curriculum and strong alumni network in tech and research."
        ),
        "full_description": (
            "Birla Institute of Technology and Science (BITS) Pilani is one of India's most "
            "prestigious and competitive private engineering institutions, established in 1964 "
            "as a deemed-to-be university. It operates campuses in Pilani (Rajasthan), Goa, "
            "Hyderabad, and Dubai. BITS is known for its unique dual-degree programs, practice "
            "school (PS) internship system offering real-world industry exposure, and a highly "
            "competitive admission process through BITSAT. Its alumni include prominent leaders "
            "in technology, entrepreneurship, and academia globally."
        ),
        "why_choose": (
            "One of India's most competitive and prestigious private engineering universities. "
            "Unique dual-degree programs and Practice School (PS) system for deep industry exposure. "
            "4 campuses: Pilani, Goa, Hyderabad, Dubai. Strong global alumni network in Silicon "
            "Valley, Wall Street, and top research institutions. Admission through BITSAT — "
            "highly merit-based and transparent."
        ),
        "ugc_approved": True,
        "aicte_approved": True,
        "placement_support": True,
        "meta_title": "BITS Pilani — Fees, Courses, BITSAT & Placements | CampusUnlock",
        "meta_description": (
            "Explore BITS Pilani — one of India's top engineering deemed universities, "
            "with campuses in Pilani, Goa, Hyderabad, and Dubai. Admission via BITSAT."
        ),
        "faqs": [
            {
                "question": "How do I get into BITS Pilani?",
                "answer": (
                    "Admission to BITS Pilani's integrated first-degree programs is through BITSAT "
                    "(BITS Admission Test), conducted online. Board marks and BITSAT score together "
                    "determine admission."
                ),
            },
            {
                "question": "What is BITS Pilani's Practice School (PS)?",
                "answer": (
                    "The Practice School is BITS Pilani's signature industry internship program, "
                    "where students spend a semester working at companies across India and abroad, "
                    "earning academic credit alongside real-world experience."
                ),
            },
            {
                "question": "Does BITS Pilani have campuses outside Pilani?",
                "answer": "Yes. BITS Pilani has campuses in Goa, Hyderabad, and Dubai, in addition to the original Pilani campus in Rajasthan.",
            },
        ],
        "scholarships": [],
    },

    # ------------------------------------------------------------------
    # INDIRA GANDHI NATIONAL OPEN UNIVERSITY (IGNOU)
    # ------------------------------------------------------------------
    {
        "name": "Indira Gandhi National Open University (IGNOU)",
        "short_description": (
            "IGNOU — the world's largest open university by enrollment, a central "
            "institution offering 200+ UGC-approved distance and online programs across "
            "all disciplines at highly affordable fees."
        ),
        "full_description": (
            "Indira Gandhi National Open University (IGNOU) is a central open university "
            "established by an Act of Parliament in 1985, headquartered in New Delhi. "
            "It is the world's largest university by enrollment, with over 3 million active "
            "learners. IGNOU offers 200+ certificate, diploma, undergraduate, postgraduate, "
            "and doctoral programs across all disciplines through distance and online modes. "
            "Its programs are UGC-DEB approved and widely recognized for government jobs, "
            "higher education, and professional advancement. IGNOU operates through 67 "
            "regional centers and over 3,000 study centers across India."
        ),
        "why_choose": (
            "World's largest university by enrollment (3M+ learners). Established by an "
            "Act of Parliament — highest institutional credibility. 200+ programs across all "
            "disciplines. Extremely affordable fees, accessible to all income groups. "
            "67 regional centers and 3,000+ study centers. UGC-DEB approved degrees recognized "
            "for government jobs and PSU recruitment."
        ),
        "ugc_approved": True,
        "placement_support": True,
        "meta_title": "IGNOU — Distance & Online Degrees from India's National Open University | CampusUnlock",
        "meta_description": (
            "Explore IGNOU's 200+ UGC-approved distance and online programs — world's largest "
            "university, affordable fees, recognized for government jobs and higher education."
        ),
        "faqs": [
            {
                "question": "Is an IGNOU degree recognized by the government?",
                "answer": (
                    "Yes. IGNOU is a central university established by an Act of Parliament. "
                    "Its degrees are fully recognized by UGC, AICTE (where applicable), and "
                    "are accepted for government jobs, PSU recruitment, and higher education admission."
                ),
            },
            {
                "question": "How many programs does IGNOU offer?",
                "answer": "IGNOU offers 200+ programs including certificates, diplomas, undergraduate, postgraduate, and doctoral degrees across all disciplines.",
            },
            {
                "question": "When can I apply to IGNOU?",
                "answer": "IGNOU has two admission cycles per year — January and July. Most programs accept applications online through the IGNOU admission portal.",
            },
        ],
        "scholarships": [],
    },
]
