import pytest

from .json import load_json, JsonLoadException


def test_load_file_fail():
    with pytest.raises(JsonLoadException):
        load_json("../fixutures/I/Dont/Exist")


def test_load_file_call():
    load_json("fixtures/schedule_of_notices_of_lease_examples.json")
