# Certification Mock Exam Skill

A Claude skill that turns a certification's official exam guide into a timed mock exam you open in a browser. Every answer links to the vendor's official documentation.

It works for any vendor that publishes an exam outline. It includes notes for Databricks and Microsoft (Azure, Fabric, Power BI). For AWS, Google Cloud, Snowflake and other vendors, it follows a general procedure.

## Contents

- [What you get](#what-you-get)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How the skill builds an exam](#how-the-skill-builds-an-exam)
- [Sourcing rules](#sourcing-rules)
- [Repository structure](#repository-structure)
- [Limitations](#limitations)
- [Contributing](#contributing)

## What you get

Claude produces one HTML file. It runs offline in any browser, except for Google Fonts, and falls back to system fonts without them. Every exam uses the same page:

- **Intro screen.** It lists each exam section with the weight the guide prints ("6%" or "25–30%") and its question count.
- **Exam screen.** You see one question at a time, with a countdown timer, a question navigator grouped by section, and flags for review.
- **Keyboard shortcuts.** Option letters pick an answer, the arrow keys move between questions, and F flags the current one.
- **Saved progress.** The page stores your answers and timer in the browser, so a refresh loses nothing. When time runs out, the exam submits itself.
- **Results screen.** You get a raw score, time used and a bar per section. You can filter the review list to wrong or flagged questions. Each question shows an explanation, a link to the official doc page, and a badge: **Checked against docs** or **Verify in docs**.
- **Themes.** The page follows your system's light or dark setting and works on phones.

The results screen never says pass or fail. A raw percentage on a mock exam rarely maps onto the real exam's scoring, so the page shows a one-line note on how the real exam scores you instead.

## Requirements

- Claude with code execution enabled. Skills need it on Claude.ai, in Claude Code and on the Claude API.
- Web search and fetch, so Claude can read the official docs. Without them, Claude marks every answer **Verify in docs** and tells you nothing was checked.
- Python 3.9 or later to run the build script. Claude's sandbox already has it.
- Node.js (optional) for `check_page.js`, which confirms the page's script parses.

## Installation

### Claude.ai

1. Zip the `certification-mock-exam` folder. The zip must contain the folder itself, with `SKILL.md` inside it.
2. Upload the zip from the Skills section of your settings. Anthropic's guide [Use skills in Claude](https://support.claude.com/en/articles/12512180) has the current steps for your plan.
3. Turn the skill on.

Uploaded skills stay private to your account. On Team and Enterprise plans, you can share them with colleagues or your whole organisation.

### Claude Code

Copy the folder into your personal skills directory, or into a project's skills directory:

```bash
cp -r certification-mock-exam ~/.claude/skills/
cp -r certification-mock-exam <your-project>/.claude/skills/
```

## Usage

Ask for a mock exam and name the certification. Attaching the exam guide gives the best result. Without an attachment, Claude looks for the guide on the vendor's site.

```text
Build me a mock exam for the Databricks Data Engineer Associate from the attached guide.
```

```text
I'm sitting DP-600 next month. Make me a practice exam sourced from Microsoft Learn.
```

```text
Quick 20-question timed practice test for AWS Solutions Architect Associate.
```

You can steer the build in plain language: the number of options per question, a shorter exam, or a set number such as "mock exam 4". Before writing any questions, Claude shows you the section allocation so you can change it.

Download the HTML file and open it in a browser. Don't view the page source while you take the exam. The answer key is base64-encoded, which stops a glance but not a determined reader.

## How the skill builds an exam

1. **Read the guide.** Claude extracts the sections, weights, objectives, question count, time limit and pass-mark policy from the official exam guide.
2. **Allocate questions.** `allocate_question_counts` splits the total by section weight using the largest-remainder method. For weight ranges, it uses the midpoint.
3. **Research.** For each section, Claude searches the vendor's official docs and reads the pages it will cite.
4. **Write.** Each question maps to one objective in the guide. Stems describe a scenario with two or three constraints, in the style of the guide's sample questions. Each wrong option is something a candidate might believe, and Claude spreads correct answers evenly across the letters.
5. **Build and check.** `build_exam.py` validates the question bank and fills the template. `check_page.js` confirms the page's script runs.

## Sourcing rules

- Questions come only from objectives the exam guide lists.
- Answers cite only the vendor's official docs. The build rejects any link outside the approved hosts you set in `allowed_doc_hosts`, such as `docs.databricks.com` or `learn.microsoft.com`.
- Claude uses current product names. The vendor notes list known renames, such as Databricks Repos to Databricks Git folders.
- A question gets **Checked against docs** only when Claude read the key claim on the cited page during the build. When Claude couldn't confirm a claim, the explanation says what to check and where.

## Repository structure

```text
certification-mock-exam/
├── SKILL.md                         Workflow Claude follows
├── scripts/
│   ├── build_exam.py                Validation, question allocation, page build
│   └── check_page.js                Confirms the built page's script parses
├── assets/
│   ├── template.html                The exam page, with placeholders
│   └── question_bank_example.py     One-question bank showing every setting
├── references/
│   ├── databricks.md                Sources, product renames, known pitfalls
│   ├── microsoft.md                 Microsoft Learn sources, weight ranges, scaled scores
│   └── other-vendors.md             Procedure for any other vendor
└── evals/
    └── evals.json                   Test prompts for checking the skill
```

## Limitations

- The page supports single-answer multiple choice only. Claude rewrites drag-and-drop, multiple-response and case-study formats as single-answer scenarios, and says so on the intro screen.
- Microsoft and some other vendors publish a range of question counts, not a fixed number. Claude picks a count and states it on the intro screen.
- The page has colours for ten sections. For guides with more, Claude merges the smallest sections and tells you.
- Claude writes the questions, so a question can be wrong. Treat **Verify in docs** questions with care, and check any answer you disagree with against the linked page.

## Contributing

To add a vendor, create `references/<vendor>.md` with the same headings as `microsoft.md`: sources, exam spec, product names and writing notes. Then add a row for it to the table in `SKILL.md`.

To test a change, run one of the prompts in `evals/evals.json` with the skill installed. Check the results page for correct section counts, doc links on the vendor's own site, and a balanced spread of answer letters.
