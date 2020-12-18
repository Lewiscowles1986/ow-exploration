import json


CANCELLED_ITEM = "Cancelled Item - Schedule of Notices of Leases"
NOTE_PREFIX = "NOTE"


class JsonBaseException(BaseException):
    pass


class JsonLoadException(JsonBaseException):
    pass


def output_json(data):
    """
    Utility method used to encapsulate dependency
    """
    try:
        return json.dumps(data)
    except BaseException as e:
        """
        Deliberately capturing all
        """
        raise JsonBaseException(e)


def load_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except (OSError, AttributeError, TypeError) as e:
        raise JsonLoadException("Unable to load file")


def simplify_collection(data):
    """
    Removes outer redundant envelope from results
    """
    raw = [item.get("leaseschedule", {}).get("scheduleEntry", None) for item in data]
    return [item for item in raw if item]


def raw_parse_item(entryIndex, itemIndex, itemRawText, itemEntryType):
    out = {}
    if itemEntryType != CANCELLED_ITEM:
        itemTextSections = itemRawText.split(NOTE_PREFIX)
        itemTextSections.reverse()
        nonNotes = itemTextSections.pop()
        itemTextSections.reverse()
        notes = [NOTE_PREFIX + note for note in itemTextSections if note]
        out = {
            "entryIndex": entryIndex,
            "itemIndex": itemIndex,
            "notes": notes,
            "columnsText": nonNotes,
            "itemRawText": itemRawText,
        }
    else:
        out = {
            "entryIndex": entryIndex,
            "itemIndex": itemIndex,
            "notes": [itemRawText],
            "columnsText": "",
            "itemRawText": itemRawText,
        }
    return out
