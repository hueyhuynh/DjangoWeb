from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Returns a basic response.
    :param request: Django http request
    :return:
    """
    return HttpResponse("If this works then you are running the server correctly! Welcome to SEPGroup8")
