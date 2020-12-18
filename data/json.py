import json


class JsonBaseException(BaseException):
    pass


class JsonLoadException(JsonBaseException):
    pass


def load_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except OSError as e:
        raise JsonLoadException("Unable to load file")
