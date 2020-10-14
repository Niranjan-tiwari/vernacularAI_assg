import collections
import json
import traceback

from rest_framework.decorators import api_view

from .helpers import finite_values_helper, numeric_value_helper, JSONResponse


# Create your views here.

@api_view(['POST'])
def validate_slot_view(request):
    try:
        data = json.loads(request.body)
        values = data.get('values')
        invalid_trigger = data.get('invalid_trigger')
        key = data.get('key')
        pick_first = data.get('pick_first')
        supported_values = data.get('supported_values')
        filled, partially_filled, trigger, parameters = finite_values_helper(values=values,
                                                                             supported_values=supported_values,
                                                                             key=key,
                                                                             invalid_trigger=invalid_trigger,
                                                                             pick_first=pick_first)
        data_dict = collections.OrderedDict()
        data_dict['filled'] = filled
        data_dict['partially_triggered'] = partially_filled
        data_dict['trigger'] = trigger
        data_dict['parameters'] = parameters

        return JSONResponse({
            "code": 200,
            "response": data_dict})
    except Exception as e:
        print(e, traceback.format_exc())


@api_view(['POST'])
def validate_numeric_constraint(request):
    try:
        data = json.loads(request.body)
        print(data)
        values = data.get('values')
        invalid_trigger = data.get('invalid_trigger')
        key = data.get('key')
        pick_first = data.get('pick_first')
        constraint = data.get('constraint')
        var_name = data.get('var_name')
        filled, partially_filled, trigger, parameters = numeric_value_helper(values=values,
                                                                             invalid_trigger=invalid_trigger,
                                                                             key=key,
                                                                             pick_first=pick_first,
                                                                             constraint=constraint,
                                                                             var_name=var_name)
        data_dict = collections.OrderedDict()
        data_dict['filled'] = filled
        data_dict['partially_triggered'] = partially_filled
        data_dict['trigger'] = trigger
        data_dict['parameters'] = parameters
        return JSONResponse({
            "code": 200,
            "response": data_dict})
    except Exception as e:
        print(e, traceback.format_exc())
