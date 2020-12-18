import pytest

from .column_parsing import (
    line_parse_regex_split,
    fix_double_space_in_second_column,
)


lines = [
    "28.01.2009      Transformer Chamber (Ground   23.01.2009      EGL551039 ",
    "17.12.2009      Flat  207, Landmark West      01.12.2009      EGL565086  ",
]


@pytest.mark.parametrize(
    (
        "lineIndex",
        "description",
    ),
    [
        (0, "known green case all four columns"),
    ],
)
def test_line_parse_regex_split_always_four_columns(lineIndex, description):
    result = line_parse_regex_split(lines[lineIndex])
    assert len(result) == 4


@pytest.mark.parametrize(
    (
        "lineIndex",
        "description",
    ),
    [
        (1, "known edge case 'Flat  [0-9]+'"),
    ],
)
def test_helper_fixes_incorrect_column_count(lineIndex, description):
    result = line_parse_regex_split(lines[lineIndex])
    assert len(result) == 5
    fixed = fix_double_space_in_second_column(result)
    assert len(fixed) == 4
