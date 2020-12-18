import functools
import sys

from data.json import (
    load_json,
    output_json,
    simplify_collection,
    raw_parse_item,
    JsonBaseException,
)
from data.column_parsing import (
    line_parse_regex_split,
    fix_double_space_in_second_column,
)


def entryText(entryText):
    return "\n".join([line for line in entryText if line])


def parseEntry(entryIdx, scheduleEntry):
    raw_items = [
        raw_parse_item(
            entryIdx,
            idx,
            entryText(scheduleItem.get("entryText")),
            scheduleItem.get("entryType"),
        )
        for idx, scheduleItem in enumerate(scheduleEntry)
    ]
    return raw_items


def load_and_clean(data_path):
    try:
        simplified_data = simplify_collection(load_json(data_path))
    except JsonBaseException as e:
        print(e, file=sys.stderr)
        exit(None, 1)
    return simplified_data


def columns_raw_to_naive(lines):
    columnLines = [line_parse_regex_split(line) for line in lines.split("\n")]
    out = [[], [], [], []]
    for lineIdx, line in enumerate(columnLines):
        line = fix_double_space_in_second_column(line)
        for idx, col in enumerate(line):
            out[idx].append(col)
    return out


def augment_entry_with_column_data(entry):
    entry.setdefault("columnsData", columns_raw_to_naive(entry.get("columnsText", "")))
    return entry


def refine_column_data(data):
    return [augment_entry_with_column_data(entry) for entry in data]


def separate_notes(data):
    parsed = [parseEntry(idx, scheduleEntry) for idx, scheduleEntry in enumerate(data)]
    flatList = [item for elem in parsed for item in elem]
    return flatList


def program():
    try:
        stage1 = separate_notes(
            load_and_clean("fixtures/schedule_of_notices_of_lease_examples.json")
        )
        print(output_json(refine_column_data(stage1)))
    except BaseException as e:
        print(e, file=sys.stderr)
        exit(None, 2)


if __name__ == "__main__":
    program()
