#!/usr/bin/env python3
"""
Fetches the latest open pull requests for the repository and generates a
Markdown report saved to reports/open_prs.md.

Environment variables (set by the workflow):
  GITHUB_TOKEN    – GitHub token used by the Actions runner.
  GITHUB_REPOSITORY – owner/repo string (e.g. CramerConsultingGroup/operation_abundance_eden_project).
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone


def fetch_open_pull_requests(owner: str, repo: str, token: str) -> list:
    """Return a list of open pull requests via the GitHub REST API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&sort=created&direction=desc&per_page=30"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "list-pull-requests-workflow")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def format_date(iso_date: str) -> str:
    """Format an ISO 8601 date string into a human-readable UTC date."""
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def generate_markdown(pulls: list, owner: str, repo: str) -> str:
    """Generate a Markdown report for the given list of pull requests."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    repo_url = f"https://github.com/{owner}/{repo}"

    lines = [
        "# Open Pull Requests",
        "",
        f"**Repository**: [{owner}/{repo}]({repo_url})",
        f"**Generated**: {timestamp}",
        f"**Total open PRs**: {len(pulls)}",
        "",
    ]

    if not pulls:
        lines.append("_No open pull requests found._")
    else:
        lines += [
            "| # | Title | Author | Created | Draft |",
            "|---|-------|--------|---------|-------|",
        ]
        for pr in pulls:
            number = pr["number"]
            title = pr["title"].replace("|", "\\|")
            html_url = pr["html_url"]
            author = pr["user"]["login"]
            created = format_date(pr["created_at"])
            draft = "Yes" if pr.get("draft") else "No"
            lines.append(
                f"| [#{number}]({html_url}) | {title} | {author} | {created} | {draft} |"
            )

    lines += [
        "",
        "---",
        f"*Last updated: {timestamp}*",
    ]

    return "\n".join(lines) + "\n"


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")

    if not token:
        print("❌ GITHUB_TOKEN environment variable is not set.", file=sys.stderr)
        return 1

    if "/" not in repository:
        print(
            "❌ GITHUB_REPOSITORY must be in 'owner/repo' format.", file=sys.stderr
        )
        return 1

    owner, repo = repository.split("/", 1)

    print(f"Fetching open pull requests for {owner}/{repo}...")
    try:
        pulls = fetch_open_pull_requests(owner, repo, token)
    except urllib.error.HTTPError as exc:
        print(f"❌ GitHub API request failed: {exc}", file=sys.stderr)
        return 1

    print(f"Found {len(pulls)} open pull request(s).")

    markdown = generate_markdown(pulls, owner, repo)

    os.makedirs("reports", exist_ok=True)
    report_path = "reports/open_prs.md"
    with open(report_path, "w") as f:
        f.write(markdown)

    print(f"✅ Report written to {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
