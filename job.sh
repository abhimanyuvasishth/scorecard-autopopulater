#!/bin/bash
export PYTHONPATH=.
source "$HOME"/miniconda3/bin/activate scorecard-autopopulater && python cli/cricket_cli.py process_current_matches
