#!/usr/bin/env python

import argparse
from dmrunner.runner import DMRunner

"""
TODO:
* old repos without run-all break everything
* nginx bootstrapping
* Proper logging
* Implement --rebuild to run secondary processes for frontend-build:watch on frontend apps
* Big ol' refactor
* nix-shell can't clone repos at the moment
* better config management via configparser
 * eg for colours, filters
* make this command-line accessible from anywhere via eg 'dmrunner' command
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true', help='Download main digitalmarketplace repositories.')
    parser.add_argument('--all', '-a', action='store_true', help='Use `run-all` for each repo rather than `run-app`.')
    parser.add_argument('--rebuild', '-r', action='store_true', help='Also run frontend-build:watch for frontend '
                                                                     'repositories.')
    parser.add_argument('--nix', action='store_true', help='Run all apps inside their respective nix-shell '
                                                           'environments.')

    args = parser.parse_args()

    runner = DMRunner(download=args.download, run_all=args.all, rebuild=args.rebuild, nix=args.nix)
    runner.run()


if __name__ == '__main__':
    main()
