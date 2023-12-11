# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
GitHub API integration for pygpm.
"""

import requests

from dataclasses import dataclass
from optparse import Values
from typing import Any, List

from pygpm.config import CONFIG
from pygpm.command import Command


class URL(str):
    pass


@dataclass
class User:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


@dataclass
class License:
    key: str
    name: str
    url: str
    spdx_id: str
    node_id: str
    html_url: str


# TODO: Redo init
@dataclass
class Repository:
    id: int
    node_id: str
    name: str
    full_name: str
    owner: User
    private: bool
    html_url: str
    description: str
    fork: bool
    url: str
    archive_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: str
    mirror_url: str
    hooks_url: str
    svn_url: str
    homepage: str
    language: Any
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: str
    pushed_at: str
    crated_at: str
    updated_at: str
    permissions: dict[str, bool]
    allow_rebase_merge: bool
    template_repository: Any
    temp_clone_token: str
    allow_squash_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_merge_commit: bool
    subscribers_count: int
    network_count: int
    license: License
    forks: int
    open_issues: int
    watchers: int


# TODO: Redo init
@dataclass
class Head:
    label: str
    ref: str
    sha: str
    user: User
    repo: Repository


# TODO: Redo init
@dataclass
class Base:
    label: str
    ref: str
    sha: str
    user: User
    repo: Repository


@dataclass
class Team:
    id: int
    node_id: str
    url: str
    html_url: str
    name: str
    slug: str
    description: str
    privacy: str
    permission: str
    notification_setting: str
    members_url: str
    repositories_url: str
    parent: Any


@dataclass
class Label:
    id: int
    node_id: str
    url: str
    name: str
    description: str
    color: str
    default: bool


# TODO: Redo init
@dataclass
class Milestone:
    url: str
    html_url: str
    labels_url: str
    id: int
    node_id: str
    number: int
    state: str
    title: str
    description: str
    creator: User
    open_issues: int
    closed_issues: int
    created_at: str
    updated_at: str
    closed_at: str
    due_on: str


# TODO: Redo init
@dataclass
class PR:
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: User
    body: str
    labels: List[Label]
    milestone: Milestone
    active_lock_reason: str
    created_at: str
    updated_at: str
    closed_at: str
    merged_at: str
    merge_commit_sha: str
    assignee: User
    assignees: List[User]
    requested_reviewers: List[User]
    requested_teams: List[Team]
    head: Head
    base: Base
    _links: dict[str, dict[str, str]]
    author_association: str
    auto_merge: Any
    draft: bool


@dataclass
class Issue:
    # TODO
    pass


def get_access_token() -> str:
    return CONFIG.get("master", "auth_token")


def get_issues(repo: URL) -> List[Issue]:
    pass


def get_pull_requests(owner: str, repo: str) -> List[PR]:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {get_access_token()}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    response_text = response.text
    response_text = response_text.replace("false", "False")
    response_text = response_text.replace("true", "True")
    response_text = response_text.replace("null", "None")

    # TODO: Need a replacement for eval?
    response_text = eval(response_text)
    assert isinstance(response_text, list)

    for x in response_text:
        assert isinstance(x, dict)

    return [PR(**x) for x in response_text]
