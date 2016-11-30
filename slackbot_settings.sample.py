#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
#
# Authors:
#   Samuel Parra <samerparra@gmail.com> - 2016

# Slack config
API_TOKEN = "YOUR API TOKEN"

# Jenkins config
JENKINS_BASE_URL = "http://JENKINS_URL:PORT"
JENKINS_TOKEN = "JENKINS TOKEN TO TRIGGER BUILDS"

# Bot config
default_reply = "Sorry but I didn't understand you. Type `help` to show the available commands."
POLLING_TIME = 5

# Gitlab config
GIT_BASE_URL = "YOUR GITLAB URL"
GIT_PRIVATE_TOKEN = "YOUR GITLAB TOKEN"

#Team config
team_members = []
random.shuffle(team_members)
TEAM_COMPONENTS = itertools.cycle(team_members)
