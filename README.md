Bulk-change the default branch for all your GitHub repos at once, from `master` to `main` (or another new default you choose).

Usage:

    pip3 install -r requirements.txt
    python3 run.py GITHUB_OWNER GITHUB_TOKEN [NEW_DEFAULT_BRANCH=main]

`GITHUB_OWNER` is your username, unless you want to change repos under an organization (in which case you should use the org name).

Get a token from [your account settings](https://github.com/settings/tokens). Make sure it has full repo permissions.

By default, the script ignores:

* Forks
* Archived repositories
* Repos where the default branch is already non-standard (e.g. `development`).
* Repos ending in `.github.io`, because GitHub Pages has hardcoded branch names.

Side effects:

* Existing clones will need to be updated, with `git fetch && git checkout NEW_DEFAULT_BRANCH`.
* Open pull requests to the old branch will be closed.
* Branch protection rules, CIs, and other systems that exclicitly reference the old branch by name may need to be updated seperately.
* You may get @dependabot PRs on repos that haven't been updated recently and have outdated pinned dependencies.
