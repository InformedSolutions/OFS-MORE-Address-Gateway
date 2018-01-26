"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- serializers.py --

@author: Informed Solutions
"""

from rest_framework import serializers

from application.models import PostcodeRequest, ApiKey


class PostcodeRequestSerializer(serializers.ModelSerializer):
    """
    Defines fields names and order for use in model serializers in models.py
    """
    class Meta:
        model = PostcodeRequest
        fields = ('postcode',)


class ApiKeySerializer(serializers.ModelSerializer):
    """
    Defines fields names and order for use in model serializers in models.py
    """
    class Meta:
        model = ApiKey
        # Note this is still kept in tuple format whilst only containing one element, please keep this in a tuple
        fields = ('api_key',)
