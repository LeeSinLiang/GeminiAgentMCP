
"""This module contains the GitHub-related tools for the MCP server."""

import os
import logging
import requests

logger = logging.getLogger(__name__)

def create_github_issue(repo_owner: str, repo_name: str, title: str, body: str = '') -> dict:
    """Creates a new issue in a GitHub repository."""
    logger.info("Executing create_github_issue for repo: %s/%s", repo_owner, repo_name)
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable not set.")
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"title": title, "body": body}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("GitHub issue created successfully: %s", response.json().get('html_url'))
        return {"issue_url": response.json().get('html_url')}
    except requests.exceptions.RequestException as exc:
        logger.error("Error creating GitHub issue: %s", exc)
        raise RuntimeError(f"Error creating GitHub issue: {exc}") from exc

# pylint: disable=too-many-arguments
def create_github_pr(
    repo_owner: str, repo_name: str, title: str, head: str, base: str, body: str = ''
) -> dict:
    """Creates a new pull request in a GitHub repository."""
    logger.info("Executing create_github_pr for repo: %s/%s", repo_owner, repo_name)
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable not set.")
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"title": title, "body": body, "head": head, "base": base}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(
            "GitHub pull request created successfully: %s", response.json().get('html_url'))
        return {"pr_url": response.json().get('html_url')}
    except requests.exceptions.RequestException as exc:
        logger.error("Error creating GitHub pull request: %s", exc)
        raise RuntimeError(f"Error creating GitHub pull request: {exc}") from exc
