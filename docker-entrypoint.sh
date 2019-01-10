#!/bin/bash

ENTRYPOINT="$*"

if [ -z "$ENTRYPOINT" ]; then
    python /src/manage.py run
else
    /bin/sh -c "$ENTRYPOINT"
fi