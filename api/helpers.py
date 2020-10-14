from typing import List, Dict, Tuple

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

SlotValidationResult = Tuple[bool, bool, str, Dict]


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def finite_values_helper(values: List[Dict], supported_values: List[str] = None,
                                  invalid_trigger: str = None, key: str = None,
                                  support_multiple: bool = True, pick_first: bool = False,
                                  **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    data_with_value = None
    if len(values) != 0:
        partially_filled = False
        filled = True
        key = key
        trigger = ""

        if not pick_first:
            if values[0]['value'] in supported_values:
                data_with_value = values[0]['value'].upper()
        else:
            data_with_value = [dataIn['value'].upper() for dataIn in values]

        if 'OTHER' in data_with_value:
            partially_filled = True
            filled = False
            trigger = invalid_trigger

            return filled, partially_filled, trigger, {}

        else:
            return filled, partially_filled, trigger, {key: [data_with_value]}
    else:
        return False, False, invalid_trigger, {}


def numeric_value_helper(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    partially_filled = False
    filled = False
    if len(values) != 0:
        filled = True

        value_stated = [] if pick_first else ''

        for value in values:
            globals()[var_name] = value['value']
            if eval(constraint):
                if pick_first:
                    value_stated = value['value']
                else:
                    value_stated.append(value['value'])
            else:
                partially_filled = True

        if not filled and (value_stated != '' or value_stated == []):
            return filled, partially_filled, invalid_trigger, {key: value_stated}
        elif not filled:
            return filled, partially_filled, invalid_trigger, {}
        else:
            return filled, partially_filled, "", {key: value_stated}
    else:
        return filled, partially_filled, invalid_trigger, {}
