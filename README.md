<!-- {{{1 -->

    File        : README.md
    Maintainer  : Felix C. Stegerman <flx@obfusk.net>
    Date        : 2020-06-20

    Copyright   : Copyright (C) 2020  Felix C. Stegerman
    Version     : v0.1.0
    License     : GPLv3+

<!-- }}}1 -->

[![CI](https://github.com/obfusk/ghbak/workflows/CI/badge.svg)](https://github.com/obfusk/ghbak/actions?query=workflow%3ACI)
[![GPLv3+](https://img.shields.io/badge/license-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

## Description

ghbak - github backup

Clone (or update) github repos and/or gists to
`./{YYYYMMDD}/{github_username}/github/{repo_name}.git` and
`./{YYYYMMDD}/{github_username}/gist/{gist_id}.git` respectively.

## Examples

```bash
$ export GITHUB_TOKEN=your-github-token
$ ghbak --repos --gists --ssh --verbose your-github-username
user: your-github-username
token $GITHUB_TOKEN
GET https://api.github.com/users/your-github-username/repos
...
GET https://api.github.com/users/your-github-username/gists
...
cloning 42 repos...
==> repo your-github-username/your-repo | description
$ cd 20200101/your-github-username/github
$ git clone --mirror -n git@github.com:your-github-username/your-repo.git your-repo.git
...
cloning 37 gists...
==> gist your-github-username | gist-id | description
$ cd 20200101/your-github-username/gist
$ git clone --mirror -n git@gist.github.com:gist-id.git gist-id.git
...

=== summary ===

backed up repos: 42
backed up gists: 37
```

## Help

```bash
$ ghbak --help
```

## Requirements

Python >= 3.5 + click + requests.

## Installing

Install the dependencies, as e.g. debian packages or using `pip`:

```bash
$ apt install python3-click python3-requests  # debian/ubuntu
$ pip install click requests                  # pip
```

Then just put `ghbak` somewhere on your `$PATH` (e.g. `~/bin`).

## License

[![GPLv3+](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
