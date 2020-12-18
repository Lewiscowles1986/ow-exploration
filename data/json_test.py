import pickle
import pytest

from .json import (
    load_json,
    simplify_collection,
    raw_parse_item,
    JsonLoadException,
    CANCELLED_ITEM,
)


SAMPLE_CANCELLED_BODY = "ITEM CANCELLED on 14 February 2019."
SAMPLE_NOTE = "NOTE: As to the parking space only the surface is included in the lease."
SAMPLE_BODY = """08.01.2016      14 Adkins Close (ground       18.12.2015      SF613060   
16 (part of) &  floor flat)                   125 years from             
17                                            01.01.2015                 
"""
SAMPLE_RAW_BODY = SAMPLE_BODY + SAMPLE_NOTE


def test_load_file_fail():
    with pytest.raises(JsonLoadException):
        load_json("../fixutures/I/Dont/Exist")


def test_load_file_call():
    load_json("fixtures/schedule_of_notices_of_lease_examples.json")


@pytest.mark.parametrize(
    (
        "input",
        "expectation",
    ),
    [
        ([], []),
        ([{}], []),
        ([{"leaseschedule": {}}], []),
        ([{"leaseschedule": {"scheduleEntry": {}}}], []),
    ],
)
def test_simplify_collection(input, expectation):
    assert pickle.dumps(simplify_collection(input)) == pickle.dumps(expectation)


@pytest.mark.parametrize(
    (
        "inputText",
        "inputType",
        "expectation",
    ),
    [
        (
            SAMPLE_CANCELLED_BODY,
            CANCELLED_ITEM,
            {
                "notes": [SAMPLE_CANCELLED_BODY],
                "columnsText": "",
                "itemsRawText": SAMPLE_CANCELLED_BODY,
            },
        ),
        (
            SAMPLE_RAW_BODY,
            "Schedule of Notices of Leases",
            {
                "notes": [SAMPLE_NOTE],
                "columnsText": SAMPLE_BODY,
                "itemsRawText": SAMPLE_RAW_BODY,
            },
        ),
    ],
)
def test_raw_parse_item(inputText, inputType, expectation):
    result = raw_parse_item(1, 1, inputText, inputType)
    assert "entryIndex" in result
    assert "itemIndex" in result
    assert "notes" in result
    assert "columnsText" in result
    assert "itemRawText" in result
    assert result["notes"] == expectation["notes"]
    assert result["columnsText"] == expectation["columnsText"]
    assert result["itemRawText"] == inputText
