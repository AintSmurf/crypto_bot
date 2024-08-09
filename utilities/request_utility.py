import logging
import json
import requests

logger = logging.getLogger()


class RequestsUtility:

    def __init__(self, base_url):
        self.base_url = base_url
        self.expected_status_code = 0

    # vaildate the response code
    def assert_status_code(self):
        assert self.rs_status_code == self.expected_status_code, (
            f"Expected status code{self.expected_status_code} but actual status code is {self.rs_status_code}\n"
            f"URL:{self.url}, Response Json: {self.rs_json}"
        )

    def post(self, endpoint, payload=None, headers=None) -> json:
        if not headers:
            headers = {"Content-Type": "application/json"}
        self.url = self.base_url + endpoint
        rs_api = requests.post(url=self.url, params=payload, headers=headers)
        self.rs_status_code = rs_api.status_code
        self.expected_status_code = 200
        self.rs_json = rs_api.json()
        self.assert_status_code()
        logger.debug(f"post request posted the data succssefully")
        return rs_api.json()

    def get(self, endpoint, payload=None, headers=None) -> json:
        if not headers:
            headers = {"Content-Type": "application/json"}
        self.url = self.base_url + endpoint
        rs_api = requests.get(url=self.url, params=payload, headers=headers)
        self.rs_status_code = rs_api.status_code
        self.expected_status_code = 200
        self.rs_json = rs_api.json()
        self.assert_status_code()
        logger.debug(f"get request extracted the data succssefully")
        return rs_api.json()

    def delete(self, endpoint, payload=None, headers=None):
        if not headers:
            headers = {"Content-Type": "application/json"}
        self.url = self.base_url + endpoint
        rs_api = requests.delete(url=self.url, params=payload, headers=headers)
        self.rs_status_code = rs_api.status_code
        self.expected_status_code = 200
        self.rs_json = rs_api.json()
        self.assert_status_code()
        logger.debug(f"delete request deleted the data succssefully")
        return rs_api.json()

    def put(self, endpoint, payload=None) -> json:
        pass
