import re
import numpy as np
import pandas as pd
from io import StringIO


pattern = re.compile("([ ]{2,}){1,4}")


def line_parse_regex_split(line):
    columns = [
        column.strip() for column in pattern.split(line.strip()) if column.strip()
    ]
    # print([len(columns), columns])
    return [column.strip() for column in pattern.split(line) if column.strip()]


def fix_double_space_in_second_column(line):
    if len(line) == 5:
        line = [line[0], line[1] + " " + line[2], line[3], line[4]]
    return line


def pandas_fixed_width_parsing(columnRawData):
    fakeFile = StringIO(columnRawData)
    df = pd.read_fwf(fakeFile, "infer", (16, 30, 16, 11)).replace({np.nan: None})
    out = df.values.tolist()
    out.insert(0, df.columns.tolist())
    return out


def fixed_width_third_column_date_in_first_column(columnData):
    all_other_columns_nan = all(
        [
            columnData[-1][0],
            not all([columnData[-1][1], columnData[-1][2], columnData[-1][3]]),
        ]
    )
    if all_other_columns_nan:
        columnData[-1][2] = columnData[-1][0]
        columnData[-1][0] = columnData[-1][1]
    return columnData
