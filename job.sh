#!/bin/bash
export PYTHONPATH=.
source "$HOME"/anaconda2/bin/activate scorecard-autopopulater && python scorecard_autopopulater/event.py
