import json

from django.forms import forms
from django.http.response import HttpResponse
from django.urls import reverse


class JsonRedirectResponse(HttpResponse):
    def __init__(self, url: str):
        data = json.dumps({'url': reverse(url)})
        super().__init__(
            content_type='application/json',
            content=data,
            status=302
        )


class JsonFormErrorsResponse(HttpResponse):
    def __init__(self, form: forms):
        data = json.dumps(form.errors.as_json())
        super().__init__(
            content_type='application/json',
            content=data,
            status=400
        )
