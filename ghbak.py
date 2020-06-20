#!/usr/bin/python3

import re, subprocess, sys, time

from pathlib import Path

import click, requests

API       = "https://api.github.com"
REPOS     = "/users/{}/repos"
GISTS     = "/users/{}/gists"

REPOSSH   = "git@github.com:{}/{}.git"
GISTSSH   = "git@gist.github.com:{}.git"

REPOHTTP  = "https://github.com/{}/{}.git"
GISTHTTP  = "https://gist.github.com/{}.git"

SAFE      = re.compile(r"[A-Za-z0-9-]+")
CLONE     = "git clone --mirror -n".split()
TODAY     = time.strftime("%Y%m%d")

class Error(RuntimeError): pass

def safe_name(name): return SAFE.fullmatch(name)

def gh_dir(user, gist = False):
  return Path(TODAY) / user / ("gist" if gist else "github")

def get(url, token = None, verbose = False):
  if verbose: click.secho("GET " + url, fg = "blue")
  hdrs = dict(Authorization = "token " + auth) if token else {}
  resp = requests.get(url, headers = hdrs)
  resp.raise_for_status()
  return resp

def get_paginated(url, *a, **kw):
  while url:
    resp  = get(url, *a, **kw)
    url   = resp.links.get("next", {}).get("url")
    for x in resp.json(): yield x

def get_repos(user, *a, **kw):
  return get_paginated(API + REPOS.format(user), *a, **kw)

def get_gists(user, *a, **kw):
  return get_paginated(API + GISTS.format(user), *a, **kw)

# TODO
def clone(parent, name, url, verbose = False):
  path = Path(parent) / name
  if not safe_name(name): raise Error("unsafe name: " + name)
  if path.exists(): raise Error("path already exists: " + path)
  path.parent.mkdir(parents = True, exist_ok = True)
  cmd = ["echo"] + CLONE + [url, name]
  if verbose:
    click.secho("$ cd " + str(path.parent), fg = "blue")
    click.secho("$ " + " ".join(cmd), fg = "blue")
  subprocess.run(cmd, cwd = path.parent, check = True)

def clone_repos(user, token = None, ssh = False, verbose = False):
  if verbose: click.secho("cloning repos...", fg = "yellow")
  repos = list(get_repos(user, token = token, verbose = verbose))
  for repo in repos:
    if verbose:
      click.secho("==> repo {}/{} | {}".format(
        user, repo["name"], repo["description"]
      ), fg = "magenta")
    url = (REPOSSH if ssh else REPOHTTP).format(user, repo["name"])
    clone(gh_dir(user), repo["name"], url, verbose)
  return len(repos)

def clone_gists(user, token = None, ssh = False, verbose = False):
  if verbose: click.secho("cloning gists...", fg = "yellow")
  gists = list(get_gists(user, token = token, verbose = verbose))
  for gist in gists:
    if verbose:
      click.secho("==> gist {} | {} | {}".format(
        user, gist["id"], gist["description"]
      ), fg = "magenta")
    url = (GISTSSH if ssh else GISTHTTP).format(gist["id"])
    clone(gh_dir(user), gist["id"], url, verbose)
  return len(gists)

@click.command(help = "github backup")
@click.option("--repos", is_flag = True, help = "clone repos")
@click.option("--gists", is_flag = True, help = "clone gists")
@click.option("--auth" , is_flag = True, help = "authenticate")
@click.option("--ssh"  , is_flag = True, help = "clone using ssh")
@click.option("-v", "--verbose", is_flag = True)
@click.argument("user")
def cli(user, repos, gists, auth, **kw):
  verbose = kw["verbose"]
  if verbose: click.secho("user: " + user, fg = "red")
  token = click.prompt("token", hide_input = True).strip() if auth else None
  stats = {}
  if repos: stats["repos"] = clone_repos(user, token, ssh, verbose)
  if gists: stats["gists"] = clone_gists(user, token, ssh, verbose)
  if verbose:
    click.secho("\n=== summary ===\n", fg = "green")
    for x in "repos gists".split():
      if stats[x]:
        click.secho("  #{}: {}".format(x, stats[x]), fg = "red")

if __name__ == "__main__":
  cli()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
