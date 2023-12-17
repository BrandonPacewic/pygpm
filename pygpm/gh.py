# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
GitHub API integration for pygpm.
"""

import requests

from typing import Any, List

from pygpm.config import CONFIG
from pygpm.gh_classes import PR, Issue


def get_access_token() -> str:
    return CONFIG.get("master", "auth_token")


HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {get_access_token()}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_api_response(url: str) -> List[dict[str, Any]]:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    response_text = response.text
    response_text = response_text.replace("false", "False")
    response_text = response_text.replace("true", "True")
    response_text = response_text.replace("null", "None")
    response_dicts = eval(response_text)
    assert isinstance(response_dicts, list)

    return response_dicts


def get_issues(owner: str, repo: str) -> List[Issue]:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response_dicts = get_api_response(url)

    return [Issue(**x) for x in response_dicts]


def get_pull_requests(owner: str, repo: str) -> List[PR]:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    response_dicts = get_api_response(url)

    return [PR(**x) for x in response_dicts]
