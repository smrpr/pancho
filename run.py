#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
#
# Authors:
#   Samuel Parra <samerparra@gmail.com> - 2016

import re
import requests
import gitlab

from time import sleep
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot_settings import (JENKINS_BASE_URL, JENKINS_TOKEN, POLLING_TIME, GIT_BASE_URL, GIT_PRIVATE_TOKEN,
                               default_reply)

git = gitlab.Gitlab(GIT_BASE_URL, token=GIT_PRIVATE_TOKEN)

projects_dict = {}
jobs_dict = {}
branches_dict = {}


@respond_to("help", re.IGNORECASE)
def show_help(message):
    """
    Prints available commands.
    :param message: Slackbot required component to send messages to Slack.
    :return:
    """
    message.send("_*DISCLAIMER:* I am in ßeta!!! I may fail/crash/don't display what you expect. "
                 "If you find any bug :pray: please ping `@samuelparra` :pray:_\n")
    message.send("*These are the available commands you can use:*\n")
    message.send("`show all jobs`\n"
                 "> Example: show all jobs\n"
                 "`show jobs in [project]`\n"
                 "> Example: show jobs in auctioneer\n"
                 "`show all projects`\n"
                 "> Example: show all projects\n"
                 "`show branches for project [project_name]`\n"
                 "> Example: show branches for project auctioneer\n"
                 "`refresh [jobs|projects] (useful for when you've added new jobs and want to display them)`\n"
                 "> Example: refresh jobs\n"
                 "`run project [job_name] with branch [branch_name]`\n"
                 "> Example: run project Auctioneer - E2E tests with branch HD_2767_avg_cost\n")


@respond_to("show jobs in (.*)", re.IGNORECASE)
def retrieve_available_jobs_for_project(message, project):
    """
    Responds with a list of jobs which match the given regexp.
    :param message: Slackbot required component to send messages to Slack.
    :param project: Project name to look for branches in. Can be a part of the project name
    :return:
    """
    if len(jobs_dict) == 0:
        list_jobs()

    message.send("> *These are the jobs I've found in project {}:*".format(project))
    message.send("\n".join("> " + str(key) + " - " + jobs_dict[key]["name"] for key in jobs_dict
                           if project.lower() in jobs_dict[key]["name"].lower()))


@respond_to("show all jobs", re.IGNORECASE)
def retrieve_available_jobs(message):
    """
    Responds with a list of available Jenkins jobs.
    :param message: Slackbot required component to send messages to Slack.
    :return:
    """
    if len(jobs_dict) == 0:
        list_jobs()

    message.send("> *These are the jobs I've found:* ")
    message.send("\n".join("> " + str(key) + " - " + jobs_dict[key]["name"] for key in jobs_dict))


@respond_to("show branches for project (.*)", re.IGNORECASE)
def retrieve_repository_branches(message, project_to_list):
    """
    Responds with a list of branches which match the given project regexp.
    :param message: Slackbot required component to send messages to Slack.
    :param project_to_list: string to look for in project names
    :return:
    """
    message.send("> These are the branches I've found for project *{}*:".format(project_to_list))
    if len(branches_dict) == 0:
        list_branches_for_project(project_to_list)

    message.send("\n".join("> " + str(key) + " - " + branches_dict[key] for key in branches_dict.keys()))


@respond_to("show all projects", re.IGNORECASE)
def retrieve_all_projects(message):
    """
    Responds with a list of projects the user has access to in Gitlab.
    :param message: Slackbot required component to send messages to Slack.
    :return:
    """
    if len(projects_dict) == 0:
        list_projects()
    message.send("> *These are the projects I've found:*")
    message.send("\n".join("> " + str(key) + " - " + projects_dict[key]["name"] for key in projects_dict.keys()))


@respond_to("refresh (.*)", re.IGNORECASE)
def empty_and_fill_dictionary(message, target):
    """
    Empties the given dictionary and fills it again with the latest info.
    :param message: Slackbot required component to send messages to Slack.
    :param target: Dictionary to clean and fill again.
    :return:
    """
    if target == "jobs":
        jobs_dict.clear()
        list_jobs()
    elif target == "projects":
        projects_dict.clear()
        list_projects()
    else:
        message.send(default_reply)


@respond_to("run project (.*) with branch (.*)", re.IGNORECASE)
def run_job(message, job, branch):
    """

    :param message: Slackbot required component to send messages to Slack.
    :param job: Job name or id to run
    :param branch: Branch name or id to run
    :return:
    """
    if len(jobs_dict) == 0:
        list_jobs()

    for value in jobs_dict.values():
        if job == value["name"]:
            job_to_run = value["name"]
            last_build = requests.get("{}lastBuild/buildNumber".format(value["url"])).text
            next_build = int(last_build) + 1

            r = requests.post("{}/buildByToken/buildWithParameters?job={}&token={}&auctioneer_branch=origin/{}".format(
                JENKINS_BASE_URL,
                job_to_run,
                JENKINS_TOKEN,
                branch))
            print(r.status_code, type(r.status_code))
            if r.status_code == 201:
                console_url = "{}{}/console".format(value["url"], str(next_build))
                message.send("> Running job {} with branch {}.".format(job_to_run, branch))

                while requests.get(console_url).status_code == 404:
                    sleep(POLLING_TIME)

                message.send("> Check the status of the build in {}".format(console_url))
            else:
                message.send("I couldn't run the job. Please try again.")
        # else:
        #     message.send("I didn't find the job called {}". format(job))


def list_branches_for_project(project_to_list):
    """
    Returns a dictionary of branches for a specified project in Git.
    :param project_to_list: Project name or key in the projects dictionary to retrieve branches from.
    :return: Dictionary of branches for the specified project.
    """
    key = 0
    for project in git.getall(git.getprojects):
        if project_to_list in project["name"]:
            for branch in git.getbranches(project["id"]):
                branches_dict[key] = branch["name"]
                key += 1
    return branches_dict


def list_projects():
    """
    Returns a dictionary of projects the user has access to in Git.
    :return: Dictionary of projects including name and id.
    """
    key = 0
    for project in git.getall(git.getprojects):
        projects_dict[key] = project
        key += 1
    return projects_dict


def list_jobs(jenkins_url=JENKINS_BASE_URL):
    """
    Returns a dictionary of jobs from the Jenkins API endpoint.
    :param jenkins_url: Jenkins URL to retrieve jobs from.
    :return: Dictionary of Jenkins jobs including name and url.
    """
    r = requests.get("{}/api/json".format(jenkins_url))
    key = 0
    for job in r.json()["jobs"]:
        jobs_dict[key] = job
        key += 1
    return jobs_dict


def main():
    """
    Starts the bot.
    :return:
    """
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()