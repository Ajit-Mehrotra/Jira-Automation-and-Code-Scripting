# Python Code Auditor with Jira Integration and Sentiment Analysis

This project provides a comprehensive solution for auditing code, integrating comments with Jira, and performing sentiment analysis on README files. It leverages `pylint` for code quality checks, the Jira REST API for issue management, and `TextBlob` for sentiment analysis.

## Features

- **Code Auditing**: Uses `pylint` to check code quality and adherence to coding standards.
- **Jira Integration**: Connects comments to Jira issues for seamless workflow integration.
- **Sentiment Analysis**: Analyzes the sentiment of the README file using `TextBlob`.

## Installation

To use this project, you need to install the required Python packages. You can install them using `pip`:

```bash
pip install pylint jira textblob
```

## Setup

In order to connect to your project, you do need your Jira project API key. Here's a brief guide:

1. Open Jira, go to settings gear icon, click `Manage account`.
2. Go to the `Security` tab and click `Create API Token`.

Once you have the key, create a `.env` file in the project directory. I have included a `.env.example` file. You can either delete that or just modify by deleting the ".example" part, effectively doing the same thing. 

Next just set the token variable to your new key `JIRA_API_TOKEN = ** Paste Your Jira API Token Here **`

And with that, you're ready  to go. 

## Things I learned:
* Had issues regarding python interpreters. VSCode set to conda initially & zsh terminal set to python installed on mac. Learned about .zshrc. Tried changing both interpreters to homebrew for python by default. VSCode is straightforward. However, with M2 Mac, it wasn't changing despite best research efforts. Ended up just using `brew install python3` and that made it so the zsh terminal uses it by default. Had to give alias though for python3 & pip3 to just python and pip. Then I further learned about virtual enviornments for python because of the way it stores enviornment variables on the system creates dependency issues. The isolation provided by venv prevents dependency conflicts between projects. Hopefully there's a workaround because this is a lil annoying. Luckily, there's a python equivalent for package.json so anyone who clones the repository can get access to the dependencies. It's called requirements.txt and you can generate it through `pip freeze > requirements.txt `. Also learned about pipfiles. But I'll be sticking to requirements.txt for this project. 
* 
