import pickle
import pytest

from .json import load_json, simplify_collection, JsonLoadException


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
