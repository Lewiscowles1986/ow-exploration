import pytest

from .column_parsing import (
    line_parse_regex_split,
    fix_double_space_in_second_column,
    pandas_fixed_width_parsing,
    fixed_width_third_column_date_in_first_column,
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


def test_pandas_raw_parsing_fwf():
    rawData = """19.07.2006      10 Century House, (second     20.06.2006      SY751695   
2 (part of and  floor flat)                   199 years from             
4 (part of)                                   20.6.2006"""
    data = pandas_fixed_width_parsing(rawData)
    for line in data:
        assert len(line) == 4
    assert data[0][0] == "19.07.2006"
    assert data[0][1] == "10 Century House, (second"
    assert data[0][2] == "20.06.2006"
    assert data[0][3] == "SY751695"
    assert data[1][0] == "2 (part of and"
    assert data[1][1] == "floor flat)"
    assert data[1][2] == "199 years from"
    assert data[2][0] == "4 (part of)"
    assert data[2][2] == "20.6.2006"


def test_pandas_raw_parsing_fwf_3rd_column_as_1st():
    rawData = """19.07.2006      9 Century House (second       20.06.2006      SY751694   
2 (part of)     floor flat)                   199 years from             
20.6.2006"""
    data = pandas_fixed_width_parsing(rawData)
    for line in data:
        assert len(line) == 4
    assert data[0][0] == "19.07.2006"
    assert data[0][1] == "9 Century House (second"
    assert data[0][2] == "20.06.2006"
    assert data[0][3] == "SY751694"
    assert data[1][0] == "2 (part of)"
    assert data[1][1] == "floor flat)"
    assert data[1][2] == "199 years from"
    assert data[2][0] == "20.6.2006"


def test_pandas_fix_missing_column_date_repeat_in_first():
    rawData = """19.07.2006      9 Century House (second       20.06.2006      SY751694   
2 (part of)     floor flat)                   199 years from             
20.6.2006"""
    data = pandas_fixed_width_parsing(rawData)
    for line in data:
        assert len(line) == 4
    assert data[0][0] == "19.07.2006"
    assert data[0][1] == "9 Century House (second"
    assert data[0][2] == "20.06.2006"
    assert data[0][3] == "SY751694"
    assert data[1][0] == "2 (part of)"
    assert data[1][1] == "floor flat)"
    assert data[1][2] == "199 years from"
    assert data[2][0] == "20.6.2006"
    data = fixed_width_third_column_date_in_first_column(data)
    assert data[2][2] == "20.6.2006"
