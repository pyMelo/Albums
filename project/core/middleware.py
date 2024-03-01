"""
File in which we have the middleware for Django for Authenticating API requests
"""
import json
import jwt
import logging
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from django.shortcuts import render

BLURRED_HTML_PATH = 'blurred_page'  # Assuming you have a URL pattern named 'blurred_page'

logger = logging.getLogger(__name__)

# Get JWT secret key

SECRET_KEY = '259fabc6e7b379d1babad0eb3b8ed8a14c3ccfed5acf7d93c81f1add36f7626f'

EXCEPTION_URLS = ['/','/login/','/signup/','/logout/','/password_reset/']

def create_response(request_id, code, message):

    """
    Function to create a response to be sent back via the API
    :param request_id:Id fo the request
    :param code:Error Code to be used
    :param message:Message to be sent via the APi
    :return:Dict withgoogle-chrome-stable --user-data-dir=/tmp/chrome-guest the above given params
    """

    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')


class CustomMiddleware(MiddlewareMixin):

    """
    Custom Middleware Class to process a request before it reached the endpoint
    """

    def process_request(self, request):

        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else None
        """

        jwt_token = request.COOKIES.get('jwt_token', None)
        logger.info(f"request received for endpoint {str(request.path)}")

        if request.path in EXCEPTION_URLS:
            logger.info("Skipping JWT authentication for exception URL.")
            return None
        if request.path.startswith('/admin'):
            return None
        if request.path.startswith('/password_reset'):
            return None
        if request.path.startswith(settings.MEDIA_URL):
            return None
        print('Token do not exists')
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                username = payload['username']
                logger.info(f"Request received from user - {username}")
                return None
            except jwt.ExpiredSignatureError:
                response = render(
                    request,
                    'core/error_response.html',
                    {'code': 401, 'message': 'Token has expired. '}
                )
                return HttpResponse(response,status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = render(
                    request,
                    'core/error_response.html',
                    {'code': 401, 'message': 'Authorization has failed. Please send a valid token.'}
                )
                return HttpResponse(response, status=401)
        else:
            response = render(
                request,
                'core/error_response.html',
                {'code': 401, 'message': 'Authorization not found. Please send a valid token in headers.'}
            )
            return HttpResponse(response, status=401)