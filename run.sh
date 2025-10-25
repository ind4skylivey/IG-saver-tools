#!/bin/bash
# Convenience script to run IGsaver

cd "$(dirname "$0")"
venv/bin/python igsaver.py "$@"
