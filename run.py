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
from slackbot_settings import JENKINS_BASE_URL, JENKINS_TOKEN, POLLING_TIME, GIT_BASE_URL, GIT_PRIVATE_TOKEN


git = gitlab.Gitlab(GIT_BASE_URL, token=GIT_PRIVATE_TOKEN)

projects_dict = {}


@respond_to("run (.*) with branch (.*)", re.IGNORECASE)
def run_job(message, job, branch, jenkins_url=JENKINS_BASE_URL):
    r = requests.get("{}/api/json".format(jenkins_url))

    job_not_found_flag = True

    for retrieved_jobs in r.json()["jobs"]:
        if retrieved_jobs["name"] == job:
            last_build = requests.get("{}lastBuild/buildNumber".format(retrieved_jobs["url"])).text
            next_build = int(last_build) + 1

            requests.post("{}/buildByToken/buildWithParameters?job={}&token={}&auctioneer_branch=origin/{}".format(
                JENKINS_BASE_URL,
                job,
                JENKINS_TOKEN,
                branch))

            console_url = "{}{}/console".format(retrieved_jobs["url"], str(next_build))
            message.send("> Running job {} with branch {}.".format(job, branch))

            while requests.get(console_url).status_code == 404:
                sleep(POLLING_TIME)

            message.send("> Check the status of the build in {}".format(console_url))
            job_not_found_flag = False

    if job_not_found_flag:
        message.send("I didn't find the job called {}". format(job))


@respond_to("show jobs in (.*)", re.IGNORECASE)
def retrieve_available_jobs(message, project, jenkins_url=JENKINS_BASE_URL):
    r = requests.get("{}/api/json".format(jenkins_url))

    message.send("> *These are the jobs I've found:*")
    message.send("\n".join("> " + job["name"] for job in r.json()["jobs"] if project.lower() in job["name"].lower()))


@respond_to("show all jobs", re.IGNORECASE)
def retrieve_available_jobs(message, jenkins_url=JENKINS_BASE_URL):
    r = requests.get("{}/api/json".format(jenkins_url))

    message.send("> *These are the jobs I've found:* ")
    message.send("\n".join("> " + job["name"] for job in r.json()["jobs"]))


def jenkins_url_builder(base_url, port):
    return "http://{}:{}".format(base_url, port)


@respond_to("show branches for project (.*)", re.IGNORECASE)
def retrieve_repository_branches(message, project_to_list):
    message.send("> These are the branches I've found for project *{}*:".format(project_to_list))

    branches_list = list_branches_for_project(project_to_list)

    message.send("\n".join(">" + branch_name for branch_name in branches_list))


@respond_to("show all projects", re.IGNORECASE)
def retrieve_all_projects(message):
    if len(projects_dict) == 0:
        list_projects()
    message.send("> *These are the projects I've found:*")
    for key in projects_dict.keys():
        print(projects_dict[key]["name"])
    message.send("\n".join("> " + str(key) + " - " + projects_dict[key]["name"] for key in projects_dict.keys()))
    #message.send("> " + str(projects_dict[key]) for key in projects_dict.keys())
    #message.send("> " + key + " - " + projects_dict[key]["name"] for key in projects_dict.keys())


@respond_to("help", re.IGNORECASE)
def show_help(message):
    message.send("*These are the available commands you can use:*\n")
    message.send("`show jobs in [project]`\n"
                 "> Example: show jobs in auctioneer\n"
                 "`show all jobs`\n"
                 "> Example: show all jobs\n"
                 "`show all projects`\n"
                 "> Example: show all projects\n"
                 "`show branches for project [project_name]`\n"
                 "> Example: show branches for project auctioneer\n"
                 "`run [job_name] with branch [branch_name]`\n"
                 "> Example: run Auctioneer - E2E tests with branch HD_2767_avg_cost\n")


def list_branches_for_project(project_to_list):
    branches_list = []

    for project in git.getall(git.getprojects):
        if project_to_list in project["name"]:
            for branch in git.getbranches(project["id"]):
                branches_list.append(branch["name"])
    return branches_list


def list_projects():
    key = 0
    for project in git.getall(git.getprojects):
        projects_dict[key] = project
        key += 1
    return projects_dict


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()

