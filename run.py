#!/usr/bin/env python3

import sys

import github

def main(access_token, owner_name, new_default):
    g = github.Github(access_token)

    # Get all repos the authenticated user has access to, then filter
    # down to only those owned by owner_name.
    owner = g.get_user(owner_name)
    repos = (r for r in g.get_user().get_repos() if r.owner == owner)

    for repo in repos:
        # Ignore forks and archived repos.
        if repo.fork or repo.archived:
            continue

        # Rename.
        changed = rename_default_branch(repo, new_default)
        if changed:
            print(f'Changed default branch for {repo.name}')


def rename_default_branch(repo, new_default='main', master_only=True):
    old_default = repo.default_branch
    if old_default == new_default:
        return False

    # Optionally ignore repos that already have a non-standard default.
    if master_only and old_default != 'master':
        return False

    # Ignore *.github.io repos, because github pages doesn't support this yet.
    if repo.name.endswith('.github.io'):
        return False

    # Get current default's ref hash.
    try:
        old_default_ref = repo.get_git_ref(f'heads/{old_default}')
    except github.GithubException as e:
        if e.status == 409:
            # Repo is empty?
            return False

    old_default_sha = old_default_ref.object.sha

    try:
        repo.create_git_ref(f'refs/heads/{new_default}', old_default_sha)
    except github.GithubException as e:
        if e.status == 422:
            # Already exists? Try to continue.
            pass

    repo.edit(default_branch=new_default)

    old_default_ref.delete()
    return True


if __name__ == "__main__":
    try:
        owner = sys.argv[1]
        access_token = sys.argv[2]
    except IndexError:
        print("usage:")
        print(f"  {sys.argv[0]} GITHUB_OWNER GITHUB_TOKEN [NEW_DEFAULT_BRANCH=main]")
        exit(1)

    new_default = 'main'
    try:
        new_default = sys.argv[3]
    except IndexError:
        pass


    main(access_token, owner, new_default)
