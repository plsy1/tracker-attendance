import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.log import LOG_ERROR, LOG_INFO
import re, random


class dmhy(Site, domain_suffixes=["u2.dmhy.org"]):

    siteName = "U2"
    siteAttendanceURL = "https://u2.dmhy.org/showup.php?action=show"

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")
            response = super(dmhy, dmhy).sendRequest(
                cookies, "https://u2.dmhy.org/showup.php", method="GET"
            )
            match = re.search(
                r'<input type="hidden" name="req" value="([^"]+)" />\s*<input type="hidden" name="hash" value="([^"]+)" />\s*<input type="hidden" name="form" value="([^"]+)" />',
                response.text,
            )
            req_value, hash_value, form_value = match.groups()
            matches = re.findall(
                r'<input type="submit" name="([^"]+)" value="([^"]+)"', response.text
            )
            submit_values = [{"name": match[0], "value": match[1]} for match in matches]
            random_submit_value = random.choice(submit_values)

            data = {
                "message": "签到咧签到咧签到咧签到咧签到咧签到咧签到咧签到咧签到咧签到咧",
                "req": req_value,
                "hash": hash_value,
                "form": form_value,
                random_submit_value["name"]: random_submit_value["value"],
            }

            response = super(dmhy, dmhy).sendRequest(
                cookies, dmhy.siteAttendanceURL, data=data, method="POST"
            )
            if response.status_code == 200:
                LOG_INFO(f"{dmhy.siteName}：签到成功")
                return {dmhy.siteName:'签到成功'}
            else:
                LOG_INFO(f"{dmhy.siteName} 签到失败")
                return {dmhy.siteName:'签到失败'}

        except Exception as e:
            LOG_ERROR(e)
