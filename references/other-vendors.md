# Any other certification

Use this when the vendor has no reference file of its own (AWS, Google Cloud, Snowflake, dbt, HashiCorp, CompTIA, and so on).

## 1. Find the two official sources

- **The exam guide**: the vendor's own published outline for this exam code and version. It usually sits on the certification page as a PDF or web page. Record its version or date.
- **The docs site**: the vendor's own product documentation domain. Confirm it by opening a docs page from the vendor's website rather than trusting a search result's domain. Examples to check, not assume: AWS uses docs.aws.amazon.com, Google Cloud uses cloud.google.com/docs, Snowflake uses docs.snowflake.com.

Put the docs host (or hosts) in `allowed_doc_hosts`. The build rejects any `doc_url` outside them, which keeps third-party blogs out of the answer key.

If the vendor also runs a learning platform (AWS Skill Builder, Google Cloud Skills Boost), use it to understand scope. Only cite pages that open without a login.

## 2. Read the exam spec from the guide

Collect: number of scored questions, time limit, section names, weights (single figure or range), question formats, pass mark policy, and any note about unscored items.

- Ranges: midpoint in `weight_percent`, the printed range in `weight_label`.
- No fixed count: pick one close to the stated range and say so in `intro`.
- Scaled scores (AWS reports 100–1,000, for example): say in `pass_mark_note` that a raw percentage doesn't map onto the scale. Confirm the figure on the vendor's site first.
- Multiple-response or other formats: rewrite as single-answer and say so in `intro`.
- More than ten sections: merge the smallest by the guide's own grouping, and tell the user, since the template has ten section colours.

## 3. Product names

Search the vendor's docs for renames of anything the guide names. Use the current name, and add the older name in brackets only where the guide itself still uses it.

## 4. If a vendor's docs are thin

Some behaviour is documented only in an upstream open-source project (Apache Spark, Terraform, Kubernetes). Cite the nearest vendor page as `doc_url`, set `is_checked` to reflect whether that page states the claim, and name the upstream source in the explanation.
