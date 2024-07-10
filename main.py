from typing import List
from dotenv import load_dotenv, set_key
import os
import requests
from requests.auth import HTTPBasicAuth
import logging
import colorlog


# ---setup---


# Load the .env file
load_dotenv()

# Log-Related Prep
logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

handler.setFormatter(formatter)
logger.addHandler(handler)


# ---functions---


def load_env_var(env_var: str):
    val = os.getenv(env_var)
    if not val:
        logger.error(f"{env_var} does not exist in the .env file")
        val = input("Please enter required information:")
        set_key(".env", env_var, val)
    else:
        logger.debug(f"{env_var} exists in the file")

    return val


def get_jira_projects(jira_base_url: str, jira_username: str, jira_token: str):

    url = f"{jira_base_url}/rest/api/2/project"

    try:

        auth = HTTPBasicAuth(jira_username, jira_token)
        response = requests.get(url=url, auth=auth)

    except requests.exceptions.HTTPError as error:
        print(error)

    return response.json()


def select_projects(projects: str):

    project_map = {}

    for i, project in enumerate(projects):
        project_map[i + 1] = project["name"]
        print(f"{i+1}: {project['name']}")

    while True:
        try:
            project_num = input("Enter the number of the project you're working on: ")
            selected_project = project_map[int(project_num)]
            # returns name of project
            return selected_project
        except (ValueError, KeyError) as error:
            logger.error(f"{error}. Please enter a valid number.")


def get_project_details(
    jira_base_ur: str, jira_username: str, jira_token: str, project_name: str
):

    projects = get_jira_projects(jira_base_url, jira_username, jira_token)

    project_id = None

    for project in projects:

        if project["name"] == project_name:
            project_id = project["id"]
            break

    url = f"{jira_base_url}/rest/api/2/project/{project_id}"

    try:
        auth = HTTPBasicAuth(jira_username, jira_token)
        response = requests.get(url=url, auth=auth)

    except requests.exceptions.HTTPError as error:
        logger.error(error)

    return response.json()


if __name__ == "__main__":

    # Access env variables
    api_token = load_env_var("JIRA_API_TOKEN")
    jira_base_url = load_env_var("JIRA_BASE_URL")
    jira_username = load_env_var("JIRA_USERNAME")
    jira_project_name = load_env_var("JIRA_PROJECT_NAME")

    logger.info("Environment variables loaded successfully")

    projects = get_jira_projects(jira_base_url, jira_username, api_token)

    selected_project = select_projects(projects)
    print(
        get_project_details(jira_base_url, jira_username, api_token, selected_project)
    )
