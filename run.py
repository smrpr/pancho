#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
#
# Authors:
#   Samuel Parra <samerparra@gmail.com> - 2016
import itertools
import json
import random
import re

import gitlab
from slackbot.bot import Bot, listen_to
from slackbot.bot import respond_to

from slackbot_settings import (GIT_BASE_URL, GIT_PRIVATE_TOKEN,
                               TEAM_MEMBERS, RESPONSES_LIST, KOKSAL_LIST)

git = gitlab.Gitlab(GIT_BASE_URL, token=GIT_PRIVATE_TOKEN)

projects_dict = {}
jobs_dict = {}
branches_dict = {}

job_to_run = None
branch = None


@respond_to("help", re.IGNORECASE)
def show_help(message):
    """
    Prints available commands.
    :param message: Slackbot required component to send messages to Slack.
    :return:
    """
    message.send("_*DISCLAIMER:* I am a ßeta!!! I may fail/crash/don't display what you expect. "
                 "If you find any bug :pray: please ping `@samuelparra` :pray:_\n")


@respond_to("are we going to finish travel api this sprint?", re.IGNORECASE)
def retrieve_available_jobs_for_project(message):
    """
    Responds with prediction.
    :param message: Slackbot required component to send messages to Slack.
    """
    message.send("http://i.imgur.com/uMNAEeX.gif")


@listen_to("^ *koksal *$", re.IGNORECASE)
def koksal_is_love(message):
    try:
        if message.body['channel'] == 'G59V03UMC':
            url = random.choice(KOKSAL_LIST)
            attachments = [{'image_url': url,
                            'text': '',
                            'title': ''}]

            message.send_webapi('', json.dumps(attachments))
    except:
        import traceback
        traceback.print_exc()


@respond_to(".*standup.*", re.IGNORECASE)
def choose_standup_responsible(message):
    """
    Choose a random person from the squad.
    :param message: Slackbot required component to send messages to Slack.
    :return:
    """
    random.shuffle(TEAM_MEMBERS)
    chosen_one = next(itertools.cycle(TEAM_MEMBERS))

    random.shuffle(RESPONSES_LIST)
    chosen_response = next(itertools.cycle(RESPONSES_LIST))

    message.send("> {}\n"
                 "> Everyone prepare answers to the following questions: \n"
                 "> How much time did you spend on house-work? \n"
                 "> What technical decisions you took and should share with the two teams?".format(
        chosen_response.format(chosen_one)))


def post_message(self, channel, text, **params):
    """ Post message to a channel (id or name)

    :returns: the slack API response
    """
    params['as_user'] = params.get('as_user', self.username)
    params['link_names'] = params.get('link_names', True)
    return self.client.webapi.chat.post_message(channel, text, **params)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
