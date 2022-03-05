from typing import Iterable
from datetime import datetime
import requests as r
import json

from .models import *


class WmsApi:

    _base_url = 'https://api.wms.kznexpress.ru/'
    _base_headers = {
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "ru-RU,ru;q=0.9",
        'Access-Content-Allow-Origin': "*",
        'Connection': "keep-alive",
        'Content-Type': "application/json",
        'Host': "api.wms.kznexpress.ru",
        'Origin': "https://wms.kznexpress.ru",
        'Referer': "https://wms.kznexpress.ru/",
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': "?0",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-site",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

    @classmethod
    def authenticate(cls, phone, password):
        # 200, 401, 500-...
        # 'Authorization': "Basic bXktY2xpZW50Om15LXNlY3JldA==",
        url = cls._base_url + 'account/oauth/token'
        headers = dict(cls._base_headers)
        # base64 decoded - 'myservice:mysecret'
        headers['Authorization'] = "Basic bXktY2xpZW50Om15LXNlY3JldA=="

        params = {
            'grant_type': "password",
            'username': phone,
            'password': password
        }
        res = r.post(url, headers=headers, params=params)
        return AuthResult(res, res.status_code)

    @classmethod
    def get_delivery_points(cls, token):
        # 200, 401, 500-...
        # https://api.wms.kznexpress.ru/de/delivery-point/all?page=0&size=1000
        url = cls._base_url + 'de/delivery-point/all?page=0&size=1000' # yes, hardcoded
        headers = dict(cls._base_headers)
        headers['Authorization'] = 'Bearer %s' % token
        res = r.get(url, headers=headers)
        return RawDeliveryPoints(res, res.status_code)

    @classmethod
    def get_issue(
            cls,
            token: str,
            delivery_point_id: int,
            from_date: datetime=None,
            to_date: datetime=None
    ):
        # 200, 401, 500-...
        # https://api.wms.kznexpress.ru/de/orders?page=0&size=20&deliveryPointKey=63036&status=DELIVERED
        issue = None
        prev_issue = None
        page = 0
        is_last = False
        size = 1000

        url = cls._base_url + 'de/orders'
        headers = dict(cls._base_headers)
        headers['Authorization'] = "Bearer %s" % token
        params = {
            'page': page,
            'size': size,
            'deliveryPointKey': delivery_point_id,
            'status': 'DELIVERED'
        }

        accepted_start_date = int(from_date.timestamp()) if from_date else None
        accepted_end_date = int(to_date.timestamp()) if to_date else None

        if accepted_start_date:
            params['acceptedStartDate'] = accepted_start_date
        if accepted_end_date:
            params['acceptedEndDate'] = accepted_end_date

        while not is_last:
            res = r.get(url, headers=headers, params=params)
            issue = Issue(res, res.status_code)
            if not prev_issue:
                prev_issue = issue
            else:
                prev_issue.merge(issue)
            params['page'] += 1
            #
            is_last = len(prev_issue) < size
        return prev_issue


    @classmethod
    def get_ready_refunds(cls, token, delivery_point_id):
        # 200, 401, 500-...
        # last, empty
        # https://api.wms.kznexpress.ru/or/order-return/all?page=0&size=20&status=CREATED%2CREADY_FOR_DELIVERY&deliveryPointKey=63036
        refunds = None
        prev_refunds = None
        size=1000   # max by default
        page = 0
        is_last = False

        url = cls._base_url + 'or/order-return/all'
        headers = dict(cls._base_headers)
        headers['Authorization'] = "Bearer %s" % token
        params = {
            'page': page,
            'size': size,
            'status': 'CREATED,READY_FOR_DELIVERY',
            'deliveryPointKey': delivery_point_id
        }

        while not is_last:
            res = r.get(url, headers=headers, params=params)
            refunds = ReadyRefunds(res, res.status_code)
            if prev_refunds:
                prev_refunds.merge(refunds)
            else:
                prev_refunds = refunds
            params['page'] += 1
            # костыль, но работает
            is_last = len(prev_refunds) < size
        return prev_refunds

    @classmethod
    def get_products_info(cls, token, sku_ids: Iterable[int]):
        # 200, 401, 500-...
        # https://api.wms.kznexpress.ru/av/sku/all/id?ids=310131%2C2534027
        url = cls._base_url + 'av/sku/all/id'
        headers = dict(cls._base_headers)
        headers['Authorization'] = "Bearer %s" % token
        params = {}

        if sku_ids:
            params = {
                'ids':  ",".join([
                    str(sku_id)
                        for sku_id in sku_ids
                ])
            }
        res = r.get(url, headers=headers, params=params)
        return ProductsInfo(res, res.status_code)
