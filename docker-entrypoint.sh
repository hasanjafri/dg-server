#!/bin/bash

ENTRYPOINT="$*"

if [ -z "$ENTRYPOINT" ]; then
    python /app/__init__.py
else
    /bin/sh -c "$ENTRYPOINT"
fi