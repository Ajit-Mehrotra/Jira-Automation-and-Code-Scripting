# Python Code Auditor with Jira Integration and Sentiment Analysis

This project provides a comprehensive solution for auditing Python code, integrating comments with Jira, and performing sentiment analysis on README files. It leverages `pylint` for code quality checks, the Jira REST API for issue management, and `TextBlob` for sentiment analysis.

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