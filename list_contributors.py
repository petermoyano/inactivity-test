import os
import requests

GITHUB_ACCOUNT = 'solvdinc'
ACCOUNT_TYPE = 'user'

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    print("Error: Please set the GITHUB_TOKEN environment variable.")
    exit(1)

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_repos(account, account_type):
    repos = []
    page = 1
    per_page = 100
    if account_type == 'user':
        url_template = f'https://api.github.com/users/{account}/repos'
    elif account_type == 'org':
        url_template = f'https://api.github.com/orgs/{account}/repos'
    else:
        print("Error: ACCOUNT_TYPE must be 'user' or 'org'.")
        exit(1)
    while True:
        url = f'{url_template}?page={page}&per_page={per_page}'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            print(response.json())
            exit(1)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_contributors(owner, repo_name):
    contributors = []
    page = 1
    per_page = 100
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo_name}/contributors?page={page}&per_page={per_page}'
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            # No content, skip to next
            break
        elif response.status_code != 200:
            print(f"Error fetching contributors for {repo_name}: {response.status_code}")
            print(response.json())
            break
        data = response.json()
        if not data:
            break
        contributors.extend(data)
        page += 1
    return contributors

def main():
    print(f"Fetching repositories for account: {GITHUB_ACCOUNT}")
    repos = get_repos(GITHUB_ACCOUNT, ACCOUNT_TYPE)
    print(f"Total repositories found: {len(repos)}\n")

    all_contributors = set()

    for repo in repos:
        repo_name = repo['name']
        print(f"Fetching contributors for repository: {repo_name}")
        contributors = get_contributors(GITHUB_ACCOUNT, repo_name)
        contributor_logins = [contributor['login'] for contributor in contributors]
        all_contributors.update(contributor_logins)
        print(f"Contributors: {contributor_logins}\n")

    print("***************************************************")
    print(f"Total repositories: {len(repos)}")
    print(f"Total contributors across all repositories: {len(all_contributors)}")
    print("All contributors across all repositories:")
    for contributor in sorted(all_contributors):
        print(contributor)

if __name__ == '__main__':
    main()
