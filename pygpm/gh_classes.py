# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Data classes for storing GitHub API responses.
"""

from dataclasses import dataclass
from typing import Any, List


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


@dataclass
class _Repository:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
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
    language: Any  # TODO: Check type
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
    created_at: str
    pushed_at: str
    updated_at: str
    forks: int
    open_issues: int
    watchers: int
    has_discussions: bool
    allow_forking: bool
    web_commit_signoff_required: bool


class Repository(_Repository):
    def __init__(self, owner: dict[str, Any],
                 license: dict[str, Any],
                 **kwargs: Any,
                 ) -> None:
        self.owner = User(**owner) if owner else None
        self.license = License(**license) if license else None
        super().__init__(**kwargs)


@dataclass
class _Head:
    label: str
    ref: str
    sha: str


class Head(_Head):
    def __init__(self, user: dict[str, Any],
                 repo: dict[str, Any],
                 **kwargs: Any,
                 ) -> None:
        self.user = User(**user) if user else None
        self.repo = Repository(**repo) if repo else None
        super().__init__(**kwargs)


@dataclass
class _Base:
    label: str
    ref: str
    sha: str


class Base(_Base):
    def __init__(self, user: dict[str, Any],
                 repo: dict[str, Any],
                 **kwargs: Any,
                 ) -> None:
        self.user = User(**user) if user else None
        self.repo = Repository(**repo) if repo else None
        super().__init__(**kwargs)


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
    parent: Any  # TODO: Check type


@dataclass
class Label:
    id: int
    node_id: str
    url: str
    name: str
    description: str
    color: str
    default: bool


@dataclass
class _Milestone:
    url: str
    html_url: str
    labels_url: str
    id: int
    node_id: str
    number: int
    state: str
    title: str
    description: str
    open_issues: int
    closed_issues: int
    created_at: str
    updated_at: str
    closed_at: str
    due_on: str


class Milestone(_Milestone):
    def __init__(self, creator: dict[str, Any], **kwargs: Any) -> None:
        self.creator = User(**creator) if creator is not None else None
        super().__init__(**kwargs)


@dataclass
class _PR:
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
    body: str
    active_lock_reason: str
    created_at: str
    updated_at: str
    closed_at: str
    merged_at: str
    merge_commit_sha: str
    _links: dict[str, dict[str, str]]
    author_association: str
    auto_merge: Any  # TODO: Check type
    draft: bool


class PR(_PR):
    def __init__(self,
                 user: dict[str, Any],
                 labels: List[dict[str, Any]],
                 milestone: dict[str, Any],
                 assignee: dict[str, Any],
                 assignees: List[dict[str, Any]],
                 requested_reviewers: List[dict[str, Any]],
                 requested_teams: List[dict[str, Any]],
                 head: dict[str, Any],
                 base: dict[str, Any],
                 **kwargs: Any,
                 ) -> None:
        self.user = User(**user)
        self.labels = [Label(**x) for x in labels]
        self.milestone = Milestone(**milestone) if milestone else None
        self.assignee = User(**assignee) if assignee else None
        self.assignees = [User(**x) for x in assignees]
        self.requested_reviewers = [User(**x) for x in requested_reviewers]
        self.requested_teams = [Team(**x) for x in requested_teams]
        self.head = Head(**head) if head else None
        self.base = Base(**base) if base else None
        super().__init__(**kwargs)


@dataclass
class _Issue:
    id: int
    node_id: str
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    html_url: str
    number: int
    state: str
    title: str
    body: str
    locked: bool
    active_lock_reason: str
    comments: int
    closed_at: str
    created_at: str
    updated_at: str
    author_association: str


class Issue(_Issue):
    def __init__(self,
                 labels: List[dict[str, Any]],
                 user: dict[str, Any],
                 assignee: dict[str, Any],
                 assignees: List[dict[str, Any]],
                 milestone: dict[str, Any],
                 pull_request: dict[str, Any],
                 repository: dict[str, Any],
                 **kwargs,
                 ) -> None:
        self.labels = [Label(**x) for x in labels]
        self.user = User(**user) if user else None
        self.assignee = User(**assignee) if assignee else None
        self.assignees = [User(**x) for x in assignees]
        self.milestone = Milestone(**milestone) if milestone else None
        self.pull_request = PR(**pull_request) if pull_request else None
        self.repository = Repository(**repository) if repository else None
        super().__init__(**kwargs)
