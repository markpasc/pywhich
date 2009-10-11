#!/bin/bash

# lns -- a friendly program for making symbolic links by Sean M. Burke
# http://interglacial.com/~sburke/pub/lns.html
curl -o ~/bin/lns http://interglacial.com/~sburke/pub/lns
chmod +x ~/bin/lns

# ack -- grep-like text finder by Andy Lester
# http://betterthangrep.com/

# Would just curl it but want to fix this bug in 1.90.
#    curl -o ~/bin/ack http://betterthangrep.com/ack-standalone
curl http://betterthangrep.com/ack-standalone | sed 's/return unless App::Ack::output_to_pipe();/return if App::Ack::output_to_pipe();/' > ~/bin/ack
chmod +x ~/bin/ack

