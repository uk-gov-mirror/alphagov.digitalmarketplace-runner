#!/bin/bash

# Symbolic links to git hooks need to be installed relative to the hooks directory to be resolved.
(cd .git/hooks; ln -sf ../../hooks/pre-commit pre-commit)
(cd .git/hooks; ln -sf ../../hooks/post-commit post-commit)
echo "DMRunner hooks installed."
