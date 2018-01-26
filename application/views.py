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


def __format_response(json_response):
    try:
        results = []
        for address in json_response['results']:
            temp = {
                "combinedAddress": address['DPA']['ADDRESS'],
                "line1": address['DPA']['ADDRESS'].split(',')[0].strip(),
                "line2": address['DPA']['ADDRESS'].split(',')[1].strip() + ' ' + address['DPA']['ADDRESS'].split(',')[
                    2].strip(),
                "townOrCity": address['DPA']['POST_TOWN'],
                "county": "TBD",
                "country": "United Kingdom",
                "postcode": address['DPA']['POSTCODE'],
            }
            results.append(temp)
            temp = {}

        count = json_response['header']['totalresults']

        return JsonResponse({"count": count, "results": results}, status=200)
    except Exception as ex:
        return JsonResponse({"message": "Problem formatting results", "error": "Internal Error"}, status=500)


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
