# EXPERIMENTAL/UNDER DEVELOPMENT/IN NEED OF LOVE

## Digital Marketplace Runner
A utility to run your API/frontend repositories together (and backing services if required), while allowing you to
interact with the running processes and their logs. This script is primarily compatible with OSX; running against other
OSs may require some care and consideration. At its simplest, as an existing developer, you should be able to clone this
repo, run `make setup` and follow the instructions, then just run `make` to bring up all your checked out apps.

## Requirements
You must have the following tools available in order to successfully use the DM Runner:
* Python 3 (including headers if appropriate) installed globally with `pip` and `virtualenv` packages.
* Node v6.12.2 (consider using Node Version Manager), NPM 3+, and Yarn 1.3.2+ installed and available in your path.
* You have Docker/**Docker for Mac 18.03+** installed (if you want backing services managed for you).
* If you want to automatically decrypt and inject credentials (requires SC clearance and AWS access):
  * You have a checkout of `digitalmarketplace-credentials` and export the `DM_CREDENTIALS_REPO` environment variable with
    the path to your local checkout. `DM_CREDENTIALS_REPO/sops-wrapper` must be functional (follow instructions in README).
  * After running setup, edit the `config.yml` file and change the value of `credentials->sops` to `on`.

## Instructions
1. Ensure your environment meets the requirements.
1. Clone this repository into an empty directory (e.g. `~/gds`, `~/dm`, or whatever), so that you have something like 
`~/gds/dmrunner`.
2. Run `make setup` - follow instructions.
4. Run `make` to bring up the Digital Marketplace locally.

## `make` commands
### Options
* `make setup` - Verifies your local environment is suitable and performs basic setup.
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

## Configuration
You can configure certain aspects of the runner by editing config/config.yml (after initial setup). Configurable options
includes:
* The parent directory to scan for Digital Marketplace repositories
* Whether, and where, to persistently store application logs to disk
* Highlighting in logs displayed to the terminal
* Indentation on wrapped log lines in the display
* Whether or not the runner should automatically inject required credentials/tokens for supporting services (e.g. Notify).

## Troubleshooting
* Troubleshooting tips to go here...

## Todo
* Refactoring...
* Add Nix detection to setup and, by default, run apps using Nix to avoid local requirements on node/npm/bower/etc.
* Allow use of frontend-build:watch to continually rebuild assets
* Need to install postgresql locally (api requires pg_config) even if using docker.
