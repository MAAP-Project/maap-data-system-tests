# MAAP Data System Services System Tests

- [MAAP Data System Services System Tests](#maap-data-system-services-system-tests)
  - [Running GitHub Actions locally](#running-github-actions-locally)
  - [Papermill CLI](#papermill-cli)
  - [Docker Container Action](#docker-container-action)
  - [GitHub App Creation and Installation](#github-app-creation-and-installation)
  - [Invoking the Repository Workflow with GitHub App Authentication](#invoking-the-repository-workflow-with-github-app-authentication)

## Running GitHub Actions locally

https://github.com/nektos/act

## Papermill CLI

https://papermill.readthedocs.io/en/latest/usage-cli.html

## Docker Container Action

https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

## GitHub App Creation and Installation

The GitHub App is used as the principal in GitHub that has been granted fine-grained permissions
to perform actions in this repo. In this case, it's only to invoke the workflow_dispatch Action.

The [Creating a GitHub App
](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app) describes how to create a new app. The relevant permission for this app is "Actions", and "Read and Write" is required to invoke a workflow dispatch.  Homepage URL is required, but can just be set to https://www.maap-project.org. Add a private key to get a PEM that can be used in the auth steps if there hasn't been one created yet.

Go to the installations page (e.g., https://github.com/settings/apps/maap-system-tests/installations), click the Install button for the organization you wish to install it in. Choose the radio button "Only select repositories" and then choose the repo that will have it's workflow invoked, e.g., maap-data-system-tests, and click the Install button. You can now use the PEM for the App to invoke the workflow in that repo.

## Invoking the Repository Workflow with GitHub App Authentication

0. The App is [https://github.com/settings/apps/maap-system-tests](https://github.com/settings/apps/maap-system-tests). It's currently part of Phil's account, but will be moved to the MAAP-Project org as soon as we can coordinate it.

1. Copy the PEM file (maap-system-tests.2021-11-23.private-key.pem) into this directory.

2. Use the PEM to generate a JWT token.

```
JWT_TOKEN=$(./generate_jwt.rb)
```

3. Find the Installation ID of the App

```
curl -s -H "Authorization: Bearer ${JWT_TOKEN}" -H 'Accept: application/vnd.github.v3+json' https://api.github.com/app/installations
```

then use the URL value of the field `access_tokens_url` as the URL in the next step. Set
`INSTALLATION_ID` to the installation ID.

```
INSTALLATION_ID=20905774
```

This ID will change each time the App is installed, so if you start getting errors in these calls, that may be why.

4. Use JWT token to get an API token.

```
API_TOKEN=$(curl -s -X POST -H "Authorization: Bearer ${JWT_TOKEN}" -H 'Accept: application/vnd.github.v3+json' https://api.github.com/app/installations/${INSTALLATION_ID}/access_tokens | jq -r .token)
```

4. Use the API token to invoke the GitHub Actions Workflow Dispatch endpoint. This returns
   a 204 No Content status code on success.

```
curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer ${API_TOKEN}" -H 'Accept: application/vnd.github.v3+json' -d '{"ref":"main"}' https://api.github.com/repos/MAAP-Project/maap-data-system-tests/actions/workflows/test.yml/dispatches
```

5. Go to the [System Tests Workflow](https://github.com/MAAP-Project/maap-data-system-tests/actions/workflows/test.yml) page to see that the workflow is running.