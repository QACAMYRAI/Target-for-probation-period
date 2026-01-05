import os

from utils.requests_helper import BaseSession


def main_url() -> BaseSession:
    base_domain = os.getenv('BASE_DOMAIN')
    return BaseSession(base_url=base_domain)

