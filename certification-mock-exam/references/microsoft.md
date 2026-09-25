# Microsoft certifications (Azure, Fabric, Power Platform, Microsoft 365, Dynamics 365)

## Sources

- **Exam guide:** the study guide on learn.microsoft.com for the exam code, found by searching learn.microsoft.com for "<exam code> study guide". It lists "Skills measured" as functional groups with a percentage range each, plus a "Skills at a glance" summary and a change log with the date the current version took effect.
- **Docs for answers:** learn.microsoft.com (product docs, Microsoft Learn training modules, and the certification support pages). Set `allowed_doc_hosts=("learn.microsoft.com",)` and `docs_site_name="Microsoft Learn"`.
- **Microsoft's own practice assessment:** each certification page links a free practice assessment on Microsoft Learn. Use it to calibrate style and difficulty. Never copy its questions.
- **Not allowed:** exam dumps, third-party practice tests, blogs, YouTube, Tech Community forum answers, and Microsoft Q&A answers. Q&A lives on learn.microsoft.com but is community content, so the host check won't catch it: don't cite any `learn.microsoft.com/answers/` URL.

## Exam spec

Microsoft doesn't publish a fixed question count or a single weight per section, so:

1. **Weights.** Each group has a range such as "25–30%". Put the range in `weight_label` and its midpoint in `weight_percent`. The midpoints rarely sum to exactly 100; `allocate_question_counts` normalises them.
2. **Question count and time.** Search learn.microsoft.com for the exam's current duration (the certification page and the "exam duration and exam experience" support page cover this). If no fixed count is published, pick a count (50 is a reasonable default for associate and expert exams) and say in `intro` that the real exam's count varies.
3. **Pass mark.** Microsoft's "Exam scoring and score reports" page (last seen at `learn.microsoft.com/certifications/exam-scoring-reports`; search for it if that moves) says technical exams report a scaled score from 1 to 1,000 with 700 to pass, and that this is not 70% of the points. Re-check it at build time, then use a note such as: "Microsoft reports a scaled score where 700 passes, and a raw percentage here doesn't convert to that scale."
4. **Options.** The template supports single-answer multiple choice only. Real Microsoft exams also use multiple-response, drag-and-drop, hot area, and case studies. Rewrite those skills as single-answer scenarios and say so in `intro`. For case-study style, put the scenario in the stem and keep it self-contained.

## Product names

Microsoft renames often (Azure AD became Microsoft Entra ID, for example). When the study guide and the docs disagree, use the name the current learn.microsoft.com product page uses, and mention the older name in brackets in the stem only if the study guide still uses it. Search to confirm any rename; don't rely on memory.

## Writing notes

- Study guides list skills as verbs ("Configure", "Implement", "Recommend"). Match the verb: "Recommend" skills suit trade-off scenarios; "Configure" skills suit setting or syntax questions.
- Many skills name a specific tool surface (Azure portal, Azure CLI, PowerShell, Power Query, DAX, KQL). Test the surface the skill names.
- Fabric and Power BI exams are on the same study-guide format and the same rules apply.
