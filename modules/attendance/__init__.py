from abc import ABC, abstractmethod
from typing import Type, Dict, List
from core.logs import LOG_ERROR
import requests  # type: ignore
from modules.attendance.default import DefaultSite


class Site(ABC):
    _registry: Dict[str, Type["Site"]] = {}

    def __init_subclass__(cls, domain_suffixes: List[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if domain_suffixes:
            for suffix in domain_suffixes:
                Site._registry[suffix] = cls

    siteName = NotImplemented
    siteAttendanceURL = NotImplemented

    @staticmethod
    @abstractmethod
    def sign_in(credentials: Dict[str, str]):
        """每个子类需要实现这个方法来执行签到逻辑"""
        pass

    @staticmethod
    def get_site_class(domain: str) -> Type["Site"]:
        """根据 domain 返回相应的 Site 子类"""
        for suffix, cls in Site._registry.items():
            if domain.endswith(suffix):
                return cls
        return DefaultSite

    @staticmethod
    def get_all_suffixes() -> Dict[str, List[str]]:
        """返回所有子类及其前缀"""
        class_suffixes = {}
        for suffix, cls in Site._registry.items():
            if cls not in class_suffixes:
                class_suffixes[cls] = []
            class_suffixes[cls].append(suffix)
        return {cls.__name__: suffixes for cls, suffixes in class_suffixes.items()}

    @staticmethod
    def sendRequest(cookies, url, host=None, headers=None, data=None, method="GET"):
        """
        发送 HTTP 请求，并根据响应状态码返回布尔值。

        :param cookies: 要发送的 cookies
        :param url: 请求的 URL
        :param host: 请求的主机（可选）
        :param headers: 请求的头部（可选）
        :param data: 请求的正文（仅适用于 POST 请求）
        :param method: 请求的方法（'GET' 或 'POST'）
        :return: 请求是否成功（状态码为 200）
        """
        try:
            if headers is None:
                headers = {
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
                }

            if method.upper() == "GET":
                response = requests.get(
                    url, headers=headers, cookies=cookies, timeout=10
                )
            elif method.upper() == "POST":
                response = requests.post(
                    url, headers=headers, cookies=cookies, data=data, timeout=10
                )
            else:
                raise ValueError(
                    "Unsupported HTTP method provided. Use 'GET' or 'POST'."
                )

            return response

        except Exception as e:
            LOG_ERROR(e)
