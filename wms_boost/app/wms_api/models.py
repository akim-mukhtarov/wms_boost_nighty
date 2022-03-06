from __future__ import annotations
import requests as r
from pydantic import BaseModel, Field
from .exceptions import AuthenticationError, UnexpectedApiResponse, WmsServerError


def raise_for_status(response: r.Response, status_code):
    if status_code > 499:
        raise WmsServerError(response.request.url, status_code)
    if not status_code == 200:
        raise AuthenticationError()


class AuthResult:
    """ Validates authentication result
        and provide access to its fields """
    class UserInfo(BaseModel):
        id: int
        first_name: str = Field(alias="firstName")
        last_name: str = Field(alias="lastName")

    def __init__(self, response: r.Response, status_code: int):
        self._raise_for_status(response, status_code)
        try:
            json = response.json()
            self.user_info = self.UserInfo.parse_obj(json['userInfo'])
            self.access_token = json['access_token']
            self.refresh_token = json['refresh_token']
        except Exception as e:
            raise UnexpectedApiResponse(response.request.url, response.text)

    @staticmethod
    def _raise_for_status(response: r.Response, status_code):
        if status_code > 499:
            raise WmsServerError(response.request.url, status_code)
        if not (status_code == 200 or status_code == 201):
            raise AuthenticationError()


class RawDeliveryPoints:
    def __init__(self, response: r.Response, status_code: int):
        raise_for_status(response, status_code)
        self._str_data=response.text

    def __repr__(self):
        return self._str_data


class ReadyRefunds:

    class Refund:
        def __init__(self, json_object):
            self._json_obj = json_object

        def __getitem__(self, key: str):
            return self._json_obj[key]

        def __repr__(self):
            return str(self._json_obj)

    def __init__(self, response: r.Response, status_code: int):
        raise_for_status(response, status_code)
        try:
            json = response.json()
            self._content = json['content']
        except Exception as e:
            raise UnexpectedApiResponse(response.request.url, response.text)

    def merge(self, refunds: ReadyRefunds):
        self._content += refunds._content

    def __getitem__(self, idx):
        return self.Refund(self._content[idx])

    def __len__(self):
        return len(self._content)

    def __str__(self):
        return str(self._content)

    def iter_items(self):
        for item in self._content:
            yield self.Refund(item)

class Issue:
    # Extends Collection ?
    class Order:
        def __init__(self, json_object):
            self._json_obj = json_object

        def __getitem__(self, key: str):
            return self._json_obj[key]

    def __init__(self, response: r.Response, status_code: int):
        raise_for_status(response, status_code)
        try:
            json = response.json()
            self._content = json['content']
        except Exception as e:
            raise UnexpectedApiResponse(reponse.request.url, response.text)

    def merge(self, issue: Issue):
        self._content += issue._content

    def __getitem__(self, idx):
        return self.Order(self._content[idx])

    def __len__(self):
        return len(self._content)

    def iter_items(self):
        for item in self._content:
            yield self.Order(item)


class ProductsInfo:

    class Product:
        def __init__(self, json_object):
            self._json_obj = json_object

        def __getitem__(self, key: str):
            return self._json_obj[key]

        def __repr__(self):
            return str(self._json_obj)

    def __init__(self, response: r.Response, status_code: int):
        raise_for_status(response, status_code)
        try:
            self._content = response.json()
        except Exception as e:
            raise UnexpectedApiResponse(reponse.request.url, response.text)

    def iter_items(self):
        for item in self._content:
            yield self.Product(item)
