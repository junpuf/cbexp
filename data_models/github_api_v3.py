from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class PullRequest:
    """Response Data Model for GitHub REST API v3
    Endpoint: GET /repos/:owner/:repo/commits/:commit_sha/pulls
    Doc: https://developer.github.com/v3/repos/commits/#list-pull-requests-associated-with-a-commit
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
    user: Dict
    body: str
    created_at: str
    updated_at: str
    closed_at: Any
    merged_at: Any
    merge_commit_sha: str
    assignee: Any
    assignees: List
    requested_reviewers: List
    requested_teams: List
    labels: List
    milestone: Any
    draft: str
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    head: Dict
    base: Dict
    _links: Dict
    author_association: str
    active_lock_reason: Any