import logging

import azure.functions as func
from azf_wsgi import AzureFunctionsWsgi

from .flaskApp.application import application


# Wrap the Flask app as WSGI app
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AzureFunctionsWsgi(application.wsgi_app).main(req, context)
