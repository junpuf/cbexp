from dataclasses import dataclass
from typing import List
from datetime import datetime


def _to_datetime_obj(datetime_str):
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(datetime_str, TIMESTAMP_FORMAT) if datetime_str else None


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


@dataclass
class Repo:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str
    description: str
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: str
    size: int
    stargazers_count: int
    watchers_count: int
    language: str
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    forks_count: int
    mirror_url: str
    archived: bool
    disabled: bool
    open_issues_count: int
    license: License
    forks: int
    open_issues: int
    watchers: int
    default_branch: str

    def __post_init__(self):
        self.owner = User(**self.owner) if self.owner else None
        self.license = License(**self.license) if self.license else None
        self.created_at = _to_datetime_obj(self.created_at)
        self.updated_at = _to_datetime_obj(self.updated_at)
        self.pushed_at = _to_datetime_obj(self.pushed_at)


@dataclass
class Head:
    label: str
    ref: str
    sha: str
    user: User
    repo: Repo

    def __post_init__(self):
        self.user = User(**self.user) if self.user else None
        self.repo = Repo(**self.repo) if self.repo else None


@dataclass
class Base:
    label: str
    ref: str
    sha: str
    user: User
    repo: Repo

    def __post_init__(self):
        self.user = User(**self.user) if self.user else None
        self.repo = Repo(**self.repo) if self.repo else None


@dataclass
class Href:
    href: str


@dataclass
class _Links:
    self: Href
    html: Href
    issue: Href
    comments: Href
    review_comments: Href
    review_comment: Href
    commits: Href
    statuses: Href

    def __post_init__(self):
        self.self = Href(**self.self) if self.self else None
        self.html = Href(**self.html) if self.html else None
        self.issue = Href(**self.issue) if self.issue else None
        self.comments = Href(**self.comments) if self.comments else None
        self.review_comments = Href(**self.review_comments) if self.review_comments else None
        self.review_comment = Href(**self.review_comment) if self.review_comment else None
        self.commits = Href(**self.commits) if self.commits else None
        self.statuses = Href(**self.statuses) if self.statuses else None


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
    created_at: datetime
    updated_at: datetime
    closed_at: datetime
    due_on: datetime

    def __post_init__(self):
        self.creator = User(**self.creator) if self.creator else None
        self.created_at = _to_datetime_obj(self.created_at)
        self.updated_at = _to_datetime_obj(self.updated_at)
        self.closed_at = _to_datetime_obj(self.closed_at)
        self.due_on = _to_datetime_obj(self.due_on)


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
    members_url: str
    repositories_url: str


@dataclass
class PullRequest:
    """PullRequest Data Model for GitHub REST API v3
    Endpoint: get /repos/{owner}/{repo}/pulls/{pull_number}
    Doc: https://docs.github.com/en/free-pro-team@latest/rest/reference/pulls#get-a-pull-request
    """
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    number: str
    state: str
    locked: bool
    title: str
    user: User
    body: str
    created_at: datetime
    updated_at: datetime
    closed_at: datetime
    merged_at: datetime
    merge_commit_sha: str
    assignee: User
    assignees: List[User]
    requested_reviewers: List[User]
    requested_teams: List[Team]
    labels: List[Label]
    milestone: Milestone
    draft: str
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    head: Head
    base: Base
    _links: _Links
    author_association: str
    active_lock_reason: str
    merged: bool
    mergeable: bool
    rebaseable: bool
    mergeable_state: str
    merged_by: User
    comments: int
    review_comments: int
    maintainer_can_modify: bool
    commits: int
    additions: int
    deletions: int
    changed_files: int

    def __post_init__(self):
        self.user = User(**self.user) if self.user else None
        self.head = Head(**self.head) if self.head else None
        self.base = Base(**self.base) if self.base else None
        self._links = _Links(**self._links) if self._links else None
        self.labels = [Label(**i) for i in self.labels]
        self.assignees = [User(**i) for i in self.assignees] 
        self.requested_reviewers = [User(**i) for i in self.requested_reviewers]
        self.requested_teams = [Team(**i) for i in self.requested_teams]
        self.created_at = _to_datetime_obj(self.created_at)
        self.updated_at = _to_datetime_obj(self.updated_at)
        self.closed_at = _to_datetime_obj(self.closed_at)
        self.merged_at = _to_datetime_obj(self.merged_at)
        self.merged_by = User(**self.merged_by) if self.merged_by else None
