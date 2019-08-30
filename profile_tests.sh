
#!/usr/bin/env bash
set -ex

TMP_FILE=$(mktemp)
PYTEST="$(poetry run which pytest)"
poetry run python3 -m cProfile -o "$TMP_FILE" "$PYTEST" --quiet "$@"
poetry run python3 ./profile_stats.py "$TMP_FILE"
