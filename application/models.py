"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- models.py --

@author: Informed Solutions
"""
from django.db import models


class PostcodeRequest(models.Model):
    """
    Model used for making a postcode search
    """
    postcode = models.CharField(max_length=7, blank=False)


class ApiKey(models.Model):
    """
    Model used for serialization of API key JSON object, ensures legitimately sized input
    See change_api_key method in application/views.py for an example of implementation
    """
    # API key validation rules
    # Name is a placeholder as there needs to be more than one entry to execute without error
    api_key = models.CharField(max_length=100, blank=False)
