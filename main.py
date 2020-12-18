import sys
from data.json import (
    load_json,
    output_json,
    simplify_collection,
    raw_parse_item,
    JsonBaseException,
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


def separate_notes(data):
    return [parseEntry(idx, scheduleEntry) for idx, scheduleEntry in enumerate(data)]


def program():
    try:
        out = separate_notes(
            load_and_clean("fixtures/schedule_of_notices_of_lease_examples.json")
        )
        print(output_json(out))
    except BaseException as e:
        print(e, file=sys.stderr)
        exit(None, 2)


if __name__ == "__main__":
    program()
