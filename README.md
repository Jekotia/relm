# Overview

The creation of this application was inspired by the loss of sibbell.com

This was developed under Python 3.7, but should work on 3.4 and newer.

# How it Works

The application works by hitting the API for a supported source and comparing the latest release information to what has been stored. If the API contains a newer release, a notification is created and storage is updated.

In practical usage, storage and notifications are handled separately, with the exception of `github --user`. The `--add` and `--remove` arguments are used in conjunction with most sources in order to manage which pieces of software are in storage. Executing the program with only a source argument will check for updates for software in storage.

`github --user` behaves differently since the data-set is remotely managed. When run, it compares storage to what the GitHub API says the user has starred. Any repos found in storage but not in the API response are removed from storage. Any repos found in the API response but missing from storage are added to storage. It then iterates over the contents of storage and makes a request for each 

## Supporting files

./config.ini is created with default & placeholder values if it does not exist.

./email.template is created if it does not exist.

## Supported Sources

- GitHub
  - All public repositories
  - A users starred repos
- Mozilla
  - Firefox
  - Thunderbird

## Supported Storages

- file

## Supported Notifications

- Email

## Dependencies

- [requests](https://github.com/requests/requests) (I intend to do away with this in a future release)

# Feature Requests

I am open to feature requests for new sources, storages, and notifications, and any other ideas users may have. Please submit an issue with the label 'enhancement' to make a request. For new sources, I'm much more likely to add it in a timely manner if you can provide me with details about the API in question.

# Usage examples

## Storage Management

### Github

#### Repositories

To add a repo to storage

`python3 relm.py github --add=docker/docker-ce`

To remove a repo from storage

`python3 relm.py github --remove=docker/docker-ce`

#### User-Starred

`python3 relm.py github --user=jekotia`

### Mozilla

To add a product to storage

`python3 relm.py mozilla --add=firefox`

To remove a product from storage

`python3 relm.py mozilla --remove=thunderbird`

## Release Checking

Release checking is intended to be run at regular intervals utilising a scheduler, such as cron.

### Everything

`python3 relm.py all`

### GitHub

#### Repositories

`python3 relm.py github`

#### User-Starred

`python3 relm.py github --user=jekotia`

### Mozilla

`python3 relm.py mozilla`