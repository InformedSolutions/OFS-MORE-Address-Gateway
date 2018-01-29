"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- views.py --

@author: Informed Solutions
"""

import json
import logging
import traceback

import requests
from application.serializers import ApiKeySerializer, PostcodeRequestSerializer
from application.utilities import Utilities
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

# initiate logging
log = logging.getLogger('django.server')

# Get API key from settings.py
api_key = settings.OS_API_KEY


@api_view(['GET'])
def postcode_request(request, postcode):
    """
    :param request: The html request (not used)
    :param postcode: The postcode to lookup
    :return: JsonResponse with the success/error message
    """
    # handle empty postcode request
    if len(api_key) == 0:
        return JsonResponse({'message': 'Missing API key, please enter one before you make a postcode search'},
                            status=403)
    try:
        # ensure the postcode is long enough
        if len(postcode) > 5:
            serializer = PostcodeRequestSerializer(data={'postcode': postcode})
            # ensures that the data fits the data model (ensures it's long enough)
            if serializer.is_valid():
                return __create_postcode_search_request(serializer.data)
            err = __format_error(serializer.errors)
            log.error("Django serialization error: " + err[0] + err[1])
            return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'The post code is too short',
                                 'error': 'Bad Request'},
                                status=400)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['PUT'])
def change_api_key(request):
    """
    :param request: The api key is stored in the request
    :return: JsonResponse with the success/error message
    """
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = ApiKeySerializer(data=mapped_json_request)
        if serializer.is_valid():
            # API key set
            global api_key
            api_key = mapped_json_request['api_key']
            return JsonResponse({"message": "Api key successfully updated"}, status=200)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request", }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


def __create_postcode_search_request(postcode):
    """
    :param postcode: json with postcode in it
    :return: JsonResponse with the success/error message
    """
    postcode = postcode['postcode']
    if len(postcode) == 6:
        postcode = postcode[:3] + ' ' + postcode[3:]
    if len(postcode) == 7:
        postcode = postcode[:4] + ' ' + postcode[4:]
    header = {'content-type': 'application/json'}
    response = requests.get("https://api.ordnancesurvey.co.uk/places/v1/addresses/postcode?postcode=" + str(
        postcode) + "&key=" + api_key, headers=header)

    if response.status_code == 200:
        returned_json = json.loads(response.content.decode('utf-8'))
        return __format_response(returned_json)
    else:
        return JsonResponse(json.loads(response.text), status=response.status_code)


def get_organisation_name(address):
    try:
        org = address.get('ORGANISATION_NAME')
        return str(org)
    except Exception as ex:
        print(ex)
        return '_empty'


def __get_building_name(address):
    try:
        name = address.get('BUILDING_NAME')
        return str(name)
    except Exception as ex:
        print(ex)


def __get_sub_building_name(address):
    try:
        number = address.get('SUB_BUILDING_NAME')
        return str(number)
    except Exception as ex:
        print(ex)


def __get_building_number(address):
    try:
        number = address.get('BUILDING_NUMBER')
        return str(number)
    except Exception as ex:
        print(ex)


def __get_thoroughfare_name(address):
    try:
        name = address.get('THOROUGHFARE_NAME')
        return str(name)
    except Exception as ex:
        print(ex)


def format_address(address):
    address_line1 = ''
    address_line2 = ''
    try:
        org = get_organisation_name(address)
        building_name = __get_building_name(address)
        sub_building_name = __get_sub_building_name(address)
        building_number = __get_building_number(address)
        thoroughfare_name = __get_thoroughfare_name(address)
        address_line2 = building_number + ' ' + thoroughfare_name
        if org != 'None':
            if sub_building_name or building_name:
                address_line1 = org + ', ' + sub_building_name + ' ' + building_name
            elif building_name:
                address_line1 = org + ', ' + building_name
            else:
                address_line1 = org
        elif org == 'None':
            if sub_building_name != 'None' or building_name != 'None':
                address_line1 = sub_building_name + ' ' + building_name
            elif sub_building_name == 'None' and building_name == 'None':
                address_line1 = address_line2
                address_line2 = ''
        address_line1 = address_line1.replace('None', '')
        address_line2 = address_line2.replace('None', '')
        addr = [address_line1, address_line2]
    except Exception as ex:
        print(ex)
        return False
    return addr


def __format_response(json_response):
    try:
        results = []
        for address in json_response['results']:
            address_lines = format_address(address['DPA'])
            temp = {
                "combinedAddress": address['DPA']['ADDRESS'],
                "line1": address_lines[0],
                "line2": address_lines[1],
                "townOrCity": address['DPA']['POST_TOWN'],
                "country": "United Kingdom",
                "postcode": address['DPA']['POSTCODE'],
            }
            results.append(temp)
            temp = {}
        count = json_response['header']['totalresults']

    except Exception as ex:
        print(ex)
        return JsonResponse({"message": "Problem formatting results", "error": str(ex)}, status=500)
    return JsonResponse({"count": count, "results": results}, status=200)


def __format_error(ex):
    """
    Helper function for formatting errors encountered when serializing Django requests
    :param ex: the exception encountered by a Django serializer
    :return: a json friendly response detailing an exception incurred whilst serializing a request
    """
    # Formatting default Django error messages
    err = str(ex).split(":", 1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[', '')
    err[1] = err[1].replace(']', '')
    return err
