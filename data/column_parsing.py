import re


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
