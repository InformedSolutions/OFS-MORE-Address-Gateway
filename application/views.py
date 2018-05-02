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
from ast import literal_eval
import re
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
    # remove whitespace from postcode and convert to uppercase
    pc=postcode.replace(' ', '').upper()
    # handle empty postcode request
    if api_key is None and not settings.TEST_MODE:
        return JsonResponse({'message': 'Missing API key, please enter one before you make a postcode search'},
                            status=403)
    try:
        # ensure the postcode is long enough
        if len(pc) >= 5:
            postcode_regex = re.compile(r'\b[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][ABD-HJLNP-UW-Z]{2}\b')
            if postcode_regex.match(pc):
                serializer = PostcodeRequestSerializer(data={'postcode': pc})
                # ensures that the data fits the data model (ensures it's long enough)
                if serializer.is_valid():
                    return create_postcode_search_request(serializer.data)
                err = __format_error(serializer.errors)
                log.error("Django serialization error: " + err[0] + err[1])
                return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'message': 'This is not a valid postcode, it does not match the regular expression',
                                     'error': 'Bad Request'},
                                    status=400)
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


def create_postcode_search_request(postcode):
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
    if hasattr(settings, 'TEST_MODE'):
        if settings.TEST_MODE == 'True':
            static_response_message = """[
            {
              "postcode": "WA14 4PA",
              "line2": " OLD MARKET PLACE",
              "townOrCity": "ALTRINCHAM",
              "line1": "FORTIS DEVELOPMENTS LTD, BANK HOUSE",
              "combinedAddress": "FORTIS DEVELOPMENTS LTD, BANK HOUSE, OLD MARKET PLACE, ALTRINCHAM, WA14 4PA",
              "county" : ""
            },
            {
              "postcode": "WA14 4PA",
              "line2": " OLD MARKET PLACE",
              "townOrCity": "ALTRINCHAM",
              "line1": "INFORMED SOLUTIONS LTD, THE OLD BANK",
              "combinedAddress": "INFORMED SOLUTIONS LTD, THE OLD BANK, OLD MARKET PLACE, ALTRINCHAM, WA14 4PA",
              "county" : ""
            }
          ]
        """
            returned_json = json.loads(static_response_message)
            return JsonResponse({"count": 2, "results": returned_json}, status=200)
        else:
            response = requests.get("https://api.ordnancesurvey.co.uk/places/v1/addresses/postcode?postcode=" + str(
            postcode) + "&key=" + api_key, headers=header)
        if response.status_code == 200:
            returned_json = json.loads(response.content.decode('utf-8'))
            return __format_response(returned_json)
        else:
            return JsonResponse(json.loads(response.text), status=response.status_code)
    else:
        return JsonResponse({"Error":"Missing Test Mode field in settings file"})

def __format_response(json_response):
    try:
        results = []
        for address in json_response['results']:
            # format address lines
            address_lines = __format_address(address['DPA'])
            temp = {
                "combinedAddress": address['DPA']['ADDRESS'],
                "line1": address_lines[0],
                "line2": address_lines[1],
                "townOrCity": address['DPA']['POST_TOWN'],
                "postcode": address['DPA']['POSTCODE'],
                "county": ''
                #"county": address['DPA']['LOCAL_CUSTODIAN_CODE_DESCRIPTION'],
            }
            # add result to array
            results.append(temp)
            temp = {}

        # Get the total number of matches for the requested postcode
        count = json_response['header']['totalresults']

    except Exception as ex:
        if (json_response['header']['totalresults']) == 0:
            return JsonResponse({"message": "No results were found", "error": "invalid postcode"}, status=404)
        return JsonResponse({"message": "Problem formatting results", "error": ex}, status=500)
    return JsonResponse({"count": count, "results": results}, status=200)


def __format_address(address):
    """
    :param address: an individual address object
    :return: An array with the address line 1 and address line 2 in it.
    """
    address_line1 = ''
    address_line2 = ''
    try:
        # Use getters to get all address line variables
        org = get_organisation_name(address)
        building_name = __get_building_name(address)
        sub_building_name = __get_sub_building_name(address)
        building_number = __get_building_number(address)
        thoroughfare_name = __get_thoroughfare_name(address)
        address_line2 = building_number + ' ' + thoroughfare_name

        # If a variable is set to None, that means that it does not exist for that address
        # these statements are to determine the formatting of address line 1 vs 2
        if org != 'None':
            if building_name != 'None' and sub_building_name == 'None':
                address_line1 = org + ', ' + building_name
            elif sub_building_name == 'None' and building_name != 'None':
                address_line1 = org + ', ' + sub_building_name
            else:
                address_line1 = org
        elif org == 'None':
            if sub_building_name != 'None' and building_name != 'None':
                address_line1 = sub_building_name + ' ' + building_name
            elif sub_building_name == 'None' and building_name != 'None':
                address_line1 = building_name
            elif building_name == 'None' and sub_building_name != 'None':
                address_line1 = sub_building_name
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


def get_organisation_name(address):
    """

    :param address: an individual address object
    :return: organisation name
    """
    try:
        org = address.get('ORGANISATION_NAME')
        return str(org)
    except Exception as ex:
        print(ex)
        return '_empty'


def __get_building_name(address):
    """

    :param address: an individual address object
    :return: building name
    """
    try:
        name = address.get('BUILDING_NAME')
        return str(name)
    except Exception as ex:
        print(ex)


def __get_sub_building_name(address):
    """

    :param address: an individual address object
    :return: sub building name
    """
    try:
        number = address.get('SUB_BUILDING_NAME')
        return str(number)
    except Exception as ex:
        print(ex)


def __get_building_number(address):
    """

    :param address: an individual address object
    :return: building number
    """
    try:
        number = address.get('BUILDING_NUMBER')
        return str(number)
    except Exception as ex:
        print(ex)


def __get_thoroughfare_name(address):
    """

    :param address: an individual address object
    :return: street/road name
    """
    try:
        name = address.get('THOROUGHFARE_NAME')
        return str(name)
    except Exception as ex:
        print(ex)


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
