"""Build a self-contained mock exam page from a question bank and the HTML template."""

import base64
import html
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

TEMPLATE_PATH = Path(__file__).with_name("template.html")
OPTION_LETTERS = "ABCDEF"
MIN_OPTION_COUNT = 2
MAX_SECTION_COUNT = 10
SHARE_PRECISION = 9
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
PLACEHOLDER_PATTERN = re.compile(r"__[A-Z_]+__")


@dataclass(frozen=True)
class Section:
    """One exam-guide section.

    `weight_label` is shown on the page exactly as the guide prints it ("6%" or
    "25–30%"). `weight_percent` drives question allocation; use a range's midpoint.
    """

    id: str
    name: str
    weight_label: str
    weight_percent: float


@dataclass(frozen=True)
class Question:
    section_id: str
    stem: str
    options: list[str]
    answer: str
    explanation: str
    doc_url: str
    is_checked: bool


@dataclass(frozen=True)
class ExamConfig:
    title: str
    subtitle: str
    intro: str
    pass_mark_note: str
    storage_key: str
    exam_minutes: int
    option_count: int
    question_counts: dict[str, int]
    docs_site_name: str
    allowed_doc_hosts: tuple[str, ...]
    output_path: Path


class InvalidExamError(ValueError):
    """Raised when a question bank or config breaks the exam's structural rules."""


class TemplateMismatchError(ValueError):
    """Raised when the template holds a placeholder the build doesn't fill."""


def allocate_question_counts(sections: list[Section], total_questions: int) -> dict[str, int]:
    """Split questions by section weight with the largest-remainder method.

    Ties on the fractional part go to the section listed later, matching the
    Databricks mock exams where Section 6 beat Section 5 at 4.5 each.
    """
    total_weight = sum(section.weight_percent for section in sections)
    exact_shares = {
        section.id: round(total_questions * section.weight_percent / total_weight, SHARE_PRECISION)
        for section in sections
    }
    counts = {section_id: math.floor(share) for section_id, share in exact_shares.items()}
    leftover = total_questions - sum(counts.values())
    sections_by_remainder = sorted(
        enumerate(sections),
        key=lambda item: (exact_shares[item[1].id] - counts[item[1].id], item[0]),
        reverse=True,
    )
    for _, section in sections_by_remainder[:leftover]:
        counts[section.id] += 1
    return counts


def is_allowed_doc_url(url: str, allowed_hosts: tuple[str, ...]) -> bool:
    host = urlparse(url).hostname or ""
    return any(host == allowed or host.endswith(f".{allowed}") for allowed in allowed_hosts)


def validate_config(sections: list[Section], config: ExamConfig) -> None:
    if not MIN_OPTION_COUNT <= config.option_count <= len(OPTION_LETTERS):
        raise InvalidExamError(f"option_count must be {MIN_OPTION_COUNT}-{len(OPTION_LETTERS)}")
    if len(sections) > MAX_SECTION_COUNT:
        raise InvalidExamError(f"The template has colours for {MAX_SECTION_COUNT} sections at most")
    if config.exam_minutes <= 0:
        raise InvalidExamError("exam_minutes must be positive")
    if not config.allowed_doc_hosts:
        raise InvalidExamError("allowed_doc_hosts must name the vendor's official docs site")


def validate_question(number: int, question: Question, section_ids: set[str], config: ExamConfig) -> None:
    letters = OPTION_LETTERS[: config.option_count]
    if question.section_id not in section_ids:
        raise InvalidExamError(f"Question {number} has unknown section {question.section_id!r}")
    if len(question.options) != config.option_count:
        raise InvalidExamError(f"Question {number} has {len(question.options)} options")
    if len(set(question.options)) != len(question.options):
        raise InvalidExamError(f"Question {number} repeats an option")
    if question.answer not in letters:
        raise InvalidExamError(f"Question {number} has answer {question.answer!r}")
    if not question.explanation.strip():
        raise InvalidExamError(f"Question {number} has no explanation")
    if not is_allowed_doc_url(question.doc_url, config.allowed_doc_hosts):
        raise InvalidExamError(f"Question {number} cites {question.doc_url}, outside {config.allowed_doc_hosts}")


def validate_section_counts(questions: list[Question], config: ExamConfig) -> None:
    actual_counts = Counter(question.section_id for question in questions)
    if actual_counts != Counter(config.question_counts):
        raise InvalidExamError(f"Section counts {dict(actual_counts)} != {config.question_counts}")


def validate_exam(sections: list[Section], questions: list[Question], config: ExamConfig) -> None:
    validate_config(sections, config)
    section_ids = {section.id for section in sections}
    for number, question in enumerate(questions, start=1):
        validate_question(number, question, section_ids, config)
    validate_section_counts(questions, config)


def render_inline_code(text: str) -> str:
    return INLINE_CODE_PATTERN.sub(r"<code>\1</code>", html.escape(text))


def build_public_questions(questions: list[Question]) -> list[dict]:
    return [
        {
            "section": question.section_id,
            "stem": render_inline_code(question.stem),
            "options": [render_inline_code(option) for option in question.options],
        }
        for question in questions
    ]


def encode_answer_key(questions: list[Question]) -> str:
    """Base64-encode answers so they aren't readable at a glance in the page source."""
    answer_key = [
        {
            "answer": OPTION_LETTERS.index(question.answer),
            "explanation": render_inline_code(question.explanation),
            "doc": question.doc_url,
            "checked": question.is_checked,
        }
        for question in questions
    ]
    return base64.b64encode(json.dumps(answer_key).encode("utf-8")).decode("ascii")


def collect_placeholder_values(sections: list[Section], questions: list[Question], config: ExamConfig) -> dict[str, str]:
    section_payload = [
        {"id": section.id, "name": section.name, "weight": section.weight_label} for section in sections
    ]
    return {
        "__TITLE__": html.escape(config.title),
        "__SUBTITLE__": html.escape(config.subtitle),
        "__INTRO__": html.escape(config.intro),
        "__PASS_MARK_NOTE__": html.escape(config.pass_mark_note),
        "__DOCS_SITE__": html.escape(config.docs_site_name),
        "__EXAM_MINUTES__": str(config.exam_minutes),
        "__STORAGE_KEY__": config.storage_key,
        "__LETTERS__": json.dumps(list(OPTION_LETTERS[: config.option_count])),
        "__SECTIONS__": json.dumps(section_payload),
        "__QUESTIONS__": json.dumps(build_public_questions(questions)),
        "__KEY__": encode_answer_key(questions),
    }


def render_exam_page(template: str, placeholder_values: dict[str, str]) -> str:
    unfilled = set(PLACEHOLDER_PATTERN.findall(template)) - set(placeholder_values)
    if unfilled:
        raise TemplateMismatchError(f"Template placeholders with no value: {sorted(unfilled)}")
    page = template
    for placeholder, value in placeholder_values.items():
        page = page.replace(placeholder, value)
    return page


def count_answer_letters(questions: list[Question]) -> Counter:
    return Counter(question.answer for question in questions)


def build_exam(sections: list[Section], questions: list[Question], config: ExamConfig) -> None:
    validate_exam(sections, questions, config)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    placeholder_values = collect_placeholder_values(sections, questions, config)
    page = render_exam_page(template, placeholder_values)
    config.output_path.write_text(page, encoding="utf-8")
