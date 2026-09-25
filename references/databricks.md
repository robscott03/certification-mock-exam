# Databricks certifications

## Sources

- **Exam guide:** the PDF linked from the certification's page on databricks.com. Each guide states the exam version date, the number of scored items, the time limit, and a single weight per section.
- **Docs for answers:** docs.databricks.com. Set `allowed_doc_hosts=("docs.databricks.com",)` and `docs_site_name="docs.databricks.com"`.
- **Training:** Databricks Academy courses named in the guide's "Recommended Training". Use them to understand scope, not as `doc_url` targets, because the results page links must open without a login.
- **Not allowed:** third-party blogs, tutorials, practice-test sites, forums, Medium, Stack Overflow.

Docs exist per cloud: `docs.databricks.com/aws/en/` and `docs.databricks.com/gcp/en/`, with the Azure Databricks copy at `learn.microsoft.com/azure/databricks/`. Prefer the AWS path as the canonical link. If a claim only appears on the Azure Databricks copy (learn.microsoft.com), you may cite that page but say so in the explanation and add `learn.microsoft.com` to `allowed_doc_hosts`.

## Exam spec (Data Engineer Associate, guide dated May 4, 2026)

45 scored multiple-choice questions, 90 minutes, four-option samples, no published pass mark. Section allocation with the largest-remainder method gives 3 / 9 / 10 / 7 / 4 / 5 / 7; Sections 5 and 6 tie at 4.5 and the extra question goes to Section 6. `allocate_question_counts` reproduces this.

Suggested pass-mark note: "The exam guide doesn't publish a pass mark."

For other Databricks exams, read the new guide and take the numbers from it. Don't carry these over.

## Product names

Use current names. The guide may still mention older names in brackets.

| Current name | Older names |
|---|---|
| Lakeflow Spark Declarative Pipelines (docs also say "Lakeflow pipelines") | Delta Live Tables (DLT), Lakeflow Declarative Pipelines |
| Lakeflow Jobs | Databricks Workflows, Databricks Jobs |
| Databricks Git folders | Databricks Repos |
| Declarative Automation Bundles | Databricks Asset Bundles (DABs) |
| Standard access mode | Shared access mode |
| Dedicated access mode | Single user access mode |

If the user has a renames file in their project (for example `databricks-product-renames.md`), read it first; it may be newer than this table. Names move quickly, so search docs.databricks.com to confirm any name you're unsure of.

## Pitfalls seen in earlier exams

- PySpark DataFrame behaviour (`union`, `explode`, `summary`, `approx_count_distinct`) is documented on spark.apache.org, not docs.databricks.com. Point `doc_url` at the nearest Databricks page and say in the explanation where the behaviour is actually documented.
- Pull requests are opened in the Git provider, not in Databricks Git folders. Questions that imply otherwise are wrong.
- Keep scope to the listed bullets. The Data Engineer Associate guide lists inner, left, broadcast, multi-key and cross joins, so anti joins are out.
- The Databricks docs increasingly say "compute" rather than "cluster" (all-purpose compute, jobs compute). Prefer the docs' wording.
