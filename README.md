# Digital Marketplace Runner ('DMRunner')

** EXPERIMENTAL / UNDER DEVELOPMENT / IN NEED OF LOVE **

A local development environment for running Digital Marketplace applications and backing services.

DMRunner also provides an interactive shell to manage processes and their logs.

## Requirements

DMRunner is compatible with macOS and Ubuntu 16.04.

Running against other OSs may require some care and consideration.

* Python 3, including headers if appropriate (consider using [pyenv]),
  installed with `pip` and `virtualenv` packages.
  * macOS/Homebrew users can install with `brew install pyenv && pyenv shell 3.6.8`
* Node ^v10.15.0 (consider using [Node Version Manager]) and NPM 6+ installed
  and available in your path.
  * If you have NVM the command `nvm install && nvm use` will install and
    select the correct version of node for you
* [Docker CE/Docker Desktop for Mac][Docker] 18.03+ installed (if you want
  backing services managed for you).
  * By default, the Docker daemon starts with a max RAM allowance of only 2
    GiB.  This generally proves insufficient - you should consider raising it
    to around 4 GiB.
* If you want to automatically decrypt and inject credentials (requires SC
  clearance and AWS access):
  * You have a checkout of `digitalmarketplace-credentials` and export the
    `DM_CREDENTIALS_REPO` environment variable with the path to your local
    checkout. `$DM_CREDENTIALS_REPO/sops-wrapper` must be functional (follow
    instructions in README).
  * After running setup, edit the `config.yml` file and change the value of
    `credentials->sops` to `on`.

macOS/[Homebrew] users can run `make brew` to install all these prerequisites.

It will also suggest you source the file `Brewfile.env` into your environment.
This will make sure that the correct Python and Node versions are in your path, and that the
correct version of Postgres is available for use with the
[digitalmarketplace-api](https://github.com/alphagov/digitalmarketplace-api) repo.

[Homebrew]: https://brew.sh
[Node Version Manager]: https://github.com/nvm-sh/nvm
[pyenv]: https://github.com/pyenv/pyenv
[Docker]: https://docs.docker.com/install/

## Instructions
1. Ensure your environment meets the requirements above.
2. Clone this repository into an empty directory (e.g. `~/gds`, `~/dm`, or whatever), so that you have something like
`~/gds/dmrunner`.
3. Run `make setup` - follow instructions.
4. Run `make` to bring up the Digital Marketplace locally.

## Using a virtual machine
If you do not use macOS or wish to use a completely isolated environment to use DM Runner you can alternatively use the
provided `Vagrantfile` to create a virtual machine which contains DM Runner on a Linux box. To use this the only
requirements are to have Vagrant and VirtualBox installed. You can then access the system using

```
vagrant up
vagrant ssh
cd ~/digitalmarketplace/digitalmarketplace-runner
```

Then follow the above instructions from step 3.

## `make` commands
### Options
* `make setup` - Verifies your local environment is suitable and performs basic setup.
* `make data` - Performs an abridged setup that removes your existing managed Postgres and Elasticsearch and repopulates them with fresh data.
* `make`/`make run` - Launches all repos using `make run-app`.
* `make rebuild` - Launches all repos with an initial `make run-all` to build eg frontend assets.

## Commands
After the apps have done their initial boot-up cycle, you have a few commands at your disposal which are detailed below.
There is tab-completion for app names and you can scroll up/down to see your command history.

#### H / Help
Print out a list of commands available to you.

#### S / Status
Print out current status of the running apps.

#### B / Branch / Branches
Print which branches you're running for each app.

#### R / Restart
Restart any failed or down apps using `make run-app`.

#### RB / Rebuild
Rebuild and restart any failed or down apps using `make rebuild`, which also does NPM install and frontend-build.

#### F / Filter
By default, incoming logs from all apps are interleaved together. You can use this to toggle on a filter to show only
logs from specific apps. With no arguments, this command resets any filters, showing all logs. With arguments, the
closest-matching app name for each word will be filtered in for logging purposes (eg 'f api buyer' will cause only
logs for the data api and the buyer-frontend to be shown).

#### FE / Frontend
Runs `make frontend-build` against frontend apps. With arguments, the closest-matching app name for each word will be
rebuilt (eg 'fe buyer supplier' will run a `frontend-build` on the buyer-frontend and the supplier-frontend. With no
arguments, all frontend apps will be rebuilt. This is a one-off rebuild; for ongoing rebuilds use `FW`.

#### K / Kill
Kill apps that are running. With no arguments, all apps will be killed. With arguments, the closest-matching app name
for each word will be killed (eg 'k search briefs' will take down the search-api and the briefs-frontend).

#### Q / Quit
Kill all running apps and quit back to your shell.

## Configuration and settings
You can configure certain aspects of the runner by editing config/config.yml (after initial setup).

There are two files that determine the majority of the mutable state of the dmrunner - ``config/config.yml`` and
``config/settings.yml``.

``config.yml`` is intended to be a user-edited file and is derived from  ``config/example-config.yml``.  Configurable options include:
* The parent directory to scan for Digital Marketplace repositories
* Whether, and where, to persistently store application logs to disk
* Highlighting in logs displayed to the terminal
* Indentation on wrapped log lines in the display
* Whether or not the runner should automatically inject required credentials/tokens for supporting services (e.g. Notify).

``settings.yml`` should be shared state across all users of the dmrunner in most cases, and
lists (for example), the URLs for each of the apps, which apps there are to run and in which order they need to be run,
what frameworks need to be indexed for search, etc.

## Troubleshooting
Check if your issue is listed under https://github.com/alphagov/digitalmarketplace-runner/issues.

## Code formatting
This repository uses the opinionated Python code formatter `black` to keep the code consistently styled. Git hooks are
provided for this repository to seamlessly check and re-style your code as needed. Run `./install_hooks.sh` to install
the necessary hooks. Alternatively, configure your IDE of choice to run the formatter on save (note: PyCharm currently
doesn't seem to support this).

**Note**: If you have your own global git hooks, this may not work. Global and local hooks cannot run at the same time.

## Todo
* Refactoring...
* Add Nix detection to setup and, by default, run apps using Nix to avoid local requirements on node/npm/bower/etc.
* Allow use of frontend-build:watch to continually rebuild assets
* Need to install postgresql locally (api requires pg_config) even if using docker (this is a digitalmarketplace-api dependency, not a dmrunner dependency, but you're likely to come across it using this).

## Credits 🏆

This project was created by ex-GDSer @samuelhwilliams as a side-project, and is
now maintained by the Digital Marketplace team until he comes back 😝

## Licence

Unless stated otherwise, the codebase is released under [the MIT License][mit].
This covers both the codebase and any sample code in the documentation.

The documentation is [&copy; Crown copyright][copyright] and available under the terms
of the [Open Government 3.0][ogl] licence.

[mit]: LICENCE
[copyright]: http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[ogl]: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
