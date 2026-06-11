from html import unescape
import re

from Module import Module
from Results import Results


RESULT_HEADERS = [
    "subject_code",
    "description",
    "offering_type",
    "half_period",
    "full_period",
    "final_mark",
    "result",
    "withheld_reasons",
]

RESULT_CELL_INDEXES = {
    "subject_code": 0,
    "description": 1,
    "offering_type": 3,
    "half_period": 13,
    "full_period": 14,
    "final_mark": 15,
    "result": 16,
    "withheld_reasons": 17,
}


def _clean_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()



def _parse_result_row(row: list[str]) -> Module:
    padded_row = row + [""] * max(0, 18 - len(row))
    row_data = {field: padded_row[index] for field, index in RESULT_CELL_INDEXES.items()}
    return Module(**row_data)


def extract_results_section(page_html: str | None) -> str | None:
    if not page_html:
        return None

    table_pattern = re.compile(
        r'<table class="w3-table-all w3-small">(.*?)</table>',
        flags=re.IGNORECASE | re.DOTALL,
    )

    for table_match in table_pattern.finditer(page_html):
        table_html = table_match.group(1)
        if re.search(r'Subject\s*<br\s*/?>\s*Code', table_html, flags=re.IGNORECASE | re.DOTALL):
            section_start = page_html.rfind('<tr class="rlheader"><th>Period&nbsp;of&nbsp;Study</th>', 0, table_match.start())
            if section_start == -1:
                section_start = page_html.rfind('<table class="w3-table-all w3-small">', 0, table_match.start())

            section_end = table_match.end()
            return page_html[section_start:section_end]

    return None




def get_results(student, page_html: str | None = None) -> Results:
    if not page_html:
        return Results(getattr(student, "name", None), getattr(student, "student_number", None), [])

    modules = []

    for row_html in re.findall(r'<tr[^>]*class="[^"]*rldata[^"]*"[^>]*>(.*?)</tr>', page_html, flags=re.IGNORECASE | re.DOTALL):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row_html, flags=re.IGNORECASE | re.DOTALL)
        row = [_clean_cell(cell) for cell in cells]

        if len(row) < 18:
            row = row + [""] * (18 - len(row))

        if not any(row):
            continue

        if row[0] and re.match(r"^[A-Z]{2,5}\d{3}[A-Z]?", row[0]):
            modules.append(_parse_result_row(row))

    return Results(getattr(student, "name", None), getattr(student, "student_number", None), modules)