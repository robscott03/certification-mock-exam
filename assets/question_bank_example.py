"""Question bank for one mock exam. build_exam.py turns this into the HTML page."""

from pathlib import Path

from build_exam import (
    ExamConfig,
    Question,
    Section,
    allocate_question_counts,
    build_exam,
    count_answer_letters,
)

DOCS = "https://docs.databricks.com/aws/en"
TOTAL_QUESTIONS = 45

SECTIONS = [
    Section("s1", "Databricks Intelligence Platform", "6%", 6),
    Section("s2", "Data Ingestion and Loading", "21%", 21),
    Section("s3", "Data Transformation and Modeling", "22%", 22),
    Section("s4", "Working with Lakeflow Jobs", "16%", 16),
    Section("s5", "Implementing CI/CD", "10%", 10),
    Section("s6", "Troubleshooting, Monitoring, and Optimization", "10%", 10),
    Section("s7", "Governance and Security", "15%", 15),
]

QUESTIONS = [
    Question(
        section_id="s4",
        stem="A job is scheduled every 15 minutes, and each run takes about 20 minutes. "
        "The run history shows every other scheduled run as Skipped. Why?",
        options=[
            "The schedule's time zone is wrong",
            "The compute failed to start",
            "An If/else condition evaluated to false",
            "Retries were exhausted",
            "By default only one run of a job can be active, and runs beyond the maximum concurrent runs are skipped",
        ],
        answer="E",
        explanation="The triggers page states that one active run is the default, "
        "and runs exceeding the configured maximum concurrency are skipped.",
        doc_url=f"{DOCS}/jobs/triggers",
        is_checked=True,
    ),
]

CONFIG = ExamConfig(
    title="Data Engineer Associate mock exam 3",
    subtitle="Based on the Databricks exam guide dated May 4, 2026",
    intro="Questions follow the section weightings in the exam guide. Each has five options, "
    "one more than the retired sample questions in the guide, so expect it to be harder than the real exam. "
    "Answers and explanations stay hidden until you submit. When time runs out, the exam submits automatically.",
    pass_mark_note="The exam guide doesn't publish a pass mark.",
    storage_key="databricks-dea-2026-05-set3",
    exam_minutes=90,
    option_count=5,
    question_counts=allocate_question_counts(SECTIONS, TOTAL_QUESTIONS),
    docs_site_name="docs.databricks.com",
    allowed_doc_hosts=("docs.databricks.com",),
    output_path=Path("databricks-dea-mock-exam-3.html"),
)

if __name__ == "__main__":
    build_exam(SECTIONS, QUESTIONS, CONFIG)
    print(dict(count_answer_letters(QUESTIONS)))
