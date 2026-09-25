---
name: certification-mock-exam
description: Build a timed, self-contained HTML mock exam for any IT certification (Databricks, Microsoft Azure/Fabric/Power BI, AWS, Google Cloud, Snowflake and others) from the vendor's official exam guide, with every answer grounded in and linked to the vendor's official docs. Produces the same page every time - intro with section weights, countdown timer, question navigator, flags, saved progress, and a results screen with per-section scores, explanations, doc links and "Checked against docs" badges. Use this whenever the user asks for a mock exam, practice exam, practice test, exam simulator, or a batch of exam-style questions for a certification, or shares an exam guide / study guide / skills-measured outline and wants to test themselves, even if they don't say "mock exam".
---

# Certification mock exam builder

Builds one self-contained HTML file that simulates a certification exam. The page format is fixed (it lives in `assets/template.html`); what changes per exam is the question bank and a small config. The value of the output rests on two things: the questions match the official exam outline, and every answer is backed by the vendor's official docs. Most of this skill is about protecting those two things.

## Files in this skill

| Path | Use |
|---|---|
| `scripts/build_exam.py` | Validates the bank and fills the template. Also has `allocate_question_counts`. |
| `scripts/check_page.js` | Confirms the built page's script parses. |
| `assets/template.html` | The page. Don't edit it per exam; everything exam-specific is a placeholder. |
| `assets/question_bank_example.py` | A one-question bank showing every config field. |
| `references/databricks.md` | Databricks sources, current product names, known pitfalls. |
| `references/microsoft.md` | Microsoft Learn sources, weight ranges, scaled scoring, question formats. |
| `references/other-vendors.md` | How to handle any other vendor. |

## Workflow

### 1. Identify the exam and read the vendor reference

Work out the vendor and exam code, then read the matching file in `references/` (fall back to `other-vendors.md`). If the user's project holds its own guide or renames file, read those too; they're usually newer than this skill.

### 2. Get the official exam guide

Use the guide the user uploaded, or find it on the vendor's site. If you can't read an uploaded PDF, say so and ask the user to paste the sections and objectives as text. Extract:

- guide version or date
- scored question count (or range) and time limit
- sections, each with its weight as printed ("6%" or "25–30%")
- the objectives (bullets) under each section
- question formats and the option count used in the guide's sample questions
- pass mark policy

If you can't browse and the user hasn't given you the guide, stop and ask for it. Don't reconstruct an outline from memory.

### 3. Fix the exam spec and allocate questions

Use `allocate_question_counts(sections, total_questions)` (largest-remainder method: floor each share, then hand leftovers to the biggest fractional parts; ties go to the later section). Show the user a table of section, weight, exact share, and question count, plus the time limit and option count, and flag any choice you made (a count picked because the vendor gives a range, a tie, merged sections). Proceed unless they object.

Option count: match the guide's samples by default. More options makes the exam harder; if you use more, say so in `intro`.

### 4. Research each section in the official docs

Before writing a section's questions, search the vendor's docs site for each objective and read the relevant pages. Only official vendor sources count; never third-party blogs, tutorials, practice-test sites, forums, or community Q&A, even when they rank first. Record per question:

- `doc_url`: the official page backing the answer. The build rejects hosts outside `allowed_doc_hosts`.
- `is_checked`: `True` only if you read the key claim on that page in this session. Otherwise `False`, which shows "Verify in docs".

When you can't confirm a claim on the official docs, say so in the explanation: name what to confirm and where you did find it. If you can't browse at all, set every `is_checked` to `False` and tell the user up front that nothing was verified.

### 5. Write the questions

Scope comes from the guide only. Map each question to one objective bullet. Don't test adjacent topics the guide doesn't list, however closely related.

Use current product names (see the vendor reference). Where the guide still uses an older name in brackets, the current name leads.

Match the guide's sample questions in style. Most stems describe a scenario with two or three constraints (cost, latency, governance, maintenance, security) and ask which solution meets them, or describe a symptom and ask for the cause. Keep a few shorter recall questions for syntax and defaults.

Exactly one option is right. Every distractor should be something a candidate might believe: a real feature used in the wrong place, a real setting that doesn't fix this symptom, or an older behaviour. For code questions, each wrong option should fail for a reason you can name in the explanation.

Explanations say why the answer is right and why the tempting distractor is wrong, and point at what the doc page says. Keep them to two to four sentences.

Balance answer letters. Write each question with its correct option wherever it reads best, then move options so each letter holds roughly an equal share. The build prints the spread.

Wrap code in backticks in stems, options, and explanations; the build escapes HTML and turns backtick spans into `<code>`.

Writing 40–60 questions is long. Write the bank section by section, appending to `question_bank.py` as you go, and re-run the build after each section to catch structural errors early (the section-count check will fail until the last section lands; that's expected).

### 6. Build and check

```bash
mkdir -p /home/claude/exam && cd /home/claude/exam
cp <skill>/scripts/build_exam.py <skill>/assets/template.html .
cp <skill>/assets/question_bank_example.py question_bank.py   # then replace its contents
python question_bank.py
node <skill>/scripts/check_page.js <output>.html
```

`validate_exam` raises `InvalidExamError` for a wrong option count, a duplicate option, an answer letter out of range, an empty explanation, an unknown section, a `doc_url` outside `allowed_doc_hosts`, or section counts that don't match `question_counts`. `render_exam_page` raises `TemplateMismatchError` if a placeholder is left unfilled.

Rebalance if one letter dominates the printed spread. Then spot-check the page: extract the base64 key with Python and confirm, for three or four questions, that the stored answer index matches the option you meant.

Write Python in the bank the way `build_exam.py` is written: descriptive names, typed dataclasses, no commented-out code or narration comments.

### 7. Deliver

Copy the HTML to `/mnt/user-data/outputs/` and present the file. Share the file rather than a hosted page by default; an earlier hosted copy failed to load while the downloaded file worked. Offer to publish it as well if the user wants a link.

In the reply, keep it short: the section allocation, the letter spread, how many questions are "Checked against docs" versus "Verify in docs", and one line telling the user not to view the page source, since the answer key is only base64-encoded.

## Config reference

```python
ExamConfig(
    title="<Exam name> mock exam <n>",
    subtitle="Based on the <vendor> exam guide dated <date>",
    intro="<How questions were built, option count, anything that differs from the real exam>",
    pass_mark_note="<One sentence on the real pass mark, e.g. 'The exam guide doesn't publish a pass mark.'>",
    storage_key="<vendor>-<exam-code>-<guide-date>-set<n>",   # unique per exam, or progress collides
    exam_minutes=90,
    option_count=4,                                          # 2-6
    question_counts=allocate_question_counts(SECTIONS, 45),
    docs_site_name="<shown in the results note, e.g. 'Microsoft Learn'>",
    allowed_doc_hosts=("<official docs host>",),
    output_path=Path("<vendor>-<exam-code>-mock-exam-<n>.html"),
)
```

`Section(id, name, weight_label, weight_percent)`: `weight_label` is shown as printed; `weight_percent` drives allocation (use a range's midpoint). At most ten sections.

The page never shows pass or fail, because a raw percentage on a mock rarely maps onto the real exam's scoring. The `pass_mark_note` tells the user what the real exam uses.

If the user has built mock exams before, look for their earlier set numbers and use the next one so `storage_key` and the file name don't clash.

## What the page does (don't reimplement; the template handles it)

Intro screen with sections, weights and counts; one question at a time; countdown that survives refresh and turns red at five minutes; auto-submit at zero; navigator grouped by section with answered, flagged, and current states; keyboard shortcuts (option letters, arrows, F); submit dialog warning about unanswered and flagged questions; results with score, time used, per-section bars, filters (all, wrong or unanswered, flagged), explanations, doc links, and verification badges; progress in `localStorage` under `storage_key`; light and dark themes; safe-area insets on phones.
