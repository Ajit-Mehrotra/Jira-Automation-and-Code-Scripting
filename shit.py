# TODO JIRA-123: Do something 0
from dotenv import load_dotenv, set_key
import os
import requests
from requests.auth import HTTPBasicAuth
import logging
import colorlog
import re


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


# TODO JIRA-123: Do something 1
def get_jira_projects(jira_base_url: str, jira_username: str, jira_token: str):

    url = f"{jira_base_url}/rest/api/2/project"

    try:

        auth = HTTPBasicAuth(jira_username, jira_token)
        response = requests.get(url=url, auth=auth)

    except requests.exceptions.HTTPError as error:
        print(error)

    return response.json()


# TODO JIRA-123: Do something 2


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


# TODO JIRA-123: Do something 3
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
        logger.debug("HTTP request for project details was successful")

    except requests.exceptions.HTTPError as error:
        logger.error(error)

    return response.json()


# only works for one-line comments with the format "TODO JIRA-123: Do something"
def find_todo_comments(file_path):

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        todo_comments = {}

        for index, line in enumerate(lines):

            # makes it language agnostic by not factoring in the language-specific comment syntax...I think
            match = re.search(r"TODO (JIRA-\d+): (.+)", line)
            if match:
                logger.debug(
                    f"Found a TODO comment in {file_path}, line {index+1}: {match.group(1) + ': ' + match.group(2)}"
                )

                duplicate = match.group(1) in todo_comments

                if duplicate:
                    existing_comment, existing_line = todo_comments[match.group(1)]
                    print("\n")
                    logger.warning(
                        f"""
    Duplicate {match.group(1)}ticket found in {file_path}.
    First Comment (line {existing_line}): {existing_comment}
    Second Comment (line {index + 1}): {match.group(2)}"""
                    )

                    print(
                        """\nWould you like to:
    1. Change the first comment's JIRA reference number
    2. Change the second comment's JIRA reference number
    3. Keep the second comment and delete the first
    4. Keep the first comment and delete the second
                        """
                    )
                    user_input = input("Enter the number of your choice: ").strip()

                    # for each option, update the dictionary and the actual code/file as well
                    if user_input == "1":
                        new_jira_ref = input(
                            "Enter the new JIRA reference number for the first comment (ex. JIRA-123): "
                        ).strip()
                        logger.debug(
                            f"Changing the first comment's JIRA reference number to {new_jira_ref}"
                        )
                        lines[existing_line - 1] = re.sub(
                            r"TODO JIRA-\d+",
                            f"TODO {new_jira_ref}",
                            lines[existing_line - 1],
                        )
                        # update the first comment's jira number in todo_comments and delete old jira number
                        todo_comments[new_jira_ref] = todo_comments.pop(match.group(1))

                        # add second comment to todo_comments
                        todo_comments[match.group(1)] = (match.group(2), index + 1)

                    elif user_input == "2":
                        new_jira_ref = input(
                            "Enter the new JIRA reference number for the second comment: "
                        ).strip()
                        logger.debug(
                            f"Changing the second comment's JIRA reference number to {new_jira_ref}"
                        )
                        lines[index] = re.sub(
                            r"TODO JIRA-\d+", f"TODO {new_jira_ref}", lines[index]
                        )
                        todo_comments[new_jira_ref] = (match.group(2), index + 1)

                    elif user_input == "3":
                        logger.debug(
                            "Keeping the second comment and deleting the first"
                        )
                        lines[existing_line - 1] = ""
                        todo_comments[match.group(1)] = (match.group(2), index + 1)

                    elif user_input == "4":
                        logger.debug(
                            "Keeping the first comment and deleting the second"
                        )
                        lines[index] = ""

                    else:
                        print("Invalid input. Please enter 1, 2, 3, or 4.")

                else:
                    todo_comments[match.group(1)] = (match.group(2), index + 1)

        with open(file_path, "w") as file:
            file.writelines(lines)
        return todo_comments

    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


# TODO JIRA-123: Do something 4

if __name__ == "__main__":

    # Access env variables
    api_token = load_env_var("JIRA_API_TOKEN")
    jira_base_url = load_env_var("JIRA_BASE_URL")
    jira_username = load_env_var("JIRA_USERNAME")
    jira_project_name = load_env_var("JIRA_PROJECT_NAME")

    logger.info("Environment variables loaded successfully")

    projects = get_jira_projects(jira_base_url, jira_username, api_token)

    selected_project = select_projects(projects)
    project_details = get_project_details(
        jira_base_url, jira_username, api_token, selected_project
    )

    file_comments = find_todo_comments("main.py")
    print(file_comments)
# TODO JIRA-123: Do something 5
