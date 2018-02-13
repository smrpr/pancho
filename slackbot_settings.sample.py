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

# Team config
team_members = []

# Standup responses
RESPONSES_LIST = [":yo_dawg: YO DAWG I HERD U LIEK STANDUPS SO I CHOSE *{}* SO YOU CAN PREPARE STANDUP WHILE U DO "
                  "STANDUP :yo_dawg:",
                  ":super_lopez: In a land of Agile, one hero stands above all to prepare standup… that hero "
                  "is *{}* :super_lopez:",
                  ":yoda: Prepare the standup room you has to, *{}* :yoda:",
                  ":sherlock: Who should prepare the standup, you say? Elementary, my dear Watson. It should obviously "
                  "be *{}* :sherlock:",
                  ":terminator: Hasta la standup, baby *{}* :terminator:",
                  ":godfather: Keep your friends close, your enemies closer… and the standup room prepared,"
                  " *{}* :godfather:",
                  ":back: Standups? Where we’re going we don’t need standups. But just in case, prepare it *{}* :back:",
                  ":explode: Hey *{}*, I love the smell of standup in the morning :explode:",
                  ":gun: Yippie-yi-standup-yay, *{}* :gun:",
                  ":crossed_swords: Hello *{}*, my name is Pancho Gonzales. You killed my sprint. "
                  "Prepare the standup :crossed_swords:",
                  "Frankly, my dear, I don’t give a damn."]

KOKSAL_LIST = []
