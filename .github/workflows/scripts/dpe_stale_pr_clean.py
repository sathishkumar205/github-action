import os
from datetime import datetime, timedelta
from github import Github
# GitHub API token
token = os.environ.get('GITHUB_TOKEN')
# Create a PyGithub instance
g = Github(base_url="https://github.com/sathishkumar205/github-action", login_or_token="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")
# Stale PR configuration
pr_stale_days = 0
# Stale branch configuration
branch_stale_days = 0
# Calculate the date threshold for stale PRs and branches
pr_threshold = datetime.now() - timedelta(days=pr_stale_days)
branch_threshold = datetime.now() - timedelta(days=branch_stale_days)
# Keep track of stale pull requests
stale_pull_requests = []
# Iterate over repositories
for repo in g.get_user().get_repos():
    if repo.name.startswith('github-action'):
        print(f"Processing repository: {repo.full_name}")
        # Delete stale pull requests
        pull_requests = repo.get_pulls(state='open')
        for pull_request in pull_requests:
            if pull_request.updated_at < pr_threshold:
                print(f"Deleting PR #{pull_request.number}")
                pull_request.edit(state='closed')
                stale_pull_requests.append(pull_request)
        # Delete branches belonging to stale pull requests
        branches = repo.get_branches()
        for branch in branches:
            if branch.commit.commit.author.date < branch_threshold:
                if branch.name != repo.default_branch:  # Skip the default branch
                    for pr in stale_pull_requests:
                        if branch.name == pr.head.ref:
                            print(f"Deleting branch: {branch.name}")
                            branch.ref.delete()
                            break

