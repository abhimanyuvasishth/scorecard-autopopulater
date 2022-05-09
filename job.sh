#!/bin/bash
export PYTHONPATH=.
source "$HOME"/miniconda3/bin/activate scorecard-autopopulater && python scorecard_autopopulater/event.py
