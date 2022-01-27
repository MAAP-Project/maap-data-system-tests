# MAAP Data System Services System Tests

- [MAAP Data System Services System Tests](#maap-data-system-services-system-tests)
  - [GitHub App Creation and Installation](#github-app-creation-and-installation)
  - [GitHub Docker Container Action Creation](#github-docker-container-action-creation)
  - [Invoking the Repository Workflow from another Repo](#invoking-the-repository-workflow-from-another-repo)
  - [Manually Invoking the Repository Workflow with GitHub App Authentication](#manually-invoking-the-repository-workflow-with-github-app-authentication)
  - [Running the Notebook Manually](#running-the-notebook-manually)
  - [Notebook Input Parameters](#notebook-input-parameters)
  - [Installing maap-py](#installing-maap-py)
  - [Running Cypress](#running-cypress)
  - [References](#references)

## GitHub App Creation and Installation

A GitHub App is used as an authentication principal within GitHub that can be granted
fine-grained permissions to perform actions within a repo. This allows clients to perform authorized actions in GitHub without needing to use credentials for a specific user.  

The GitHub App [maap-system-tests](https://github.com/settings/apps/maap-system-tests) has been created
to be used by GitHub Actions in the service repos to invoke the system tests in this repo. 
In this case, a single permission granted is granted to allow invocation of the `workflow_dispatch`
Action.

The [Creating a GitHub App
](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app) describes how to create a new app. The relevant permission for this app is "Actions", and "Read and Write" is required to invoke a workflow dispatch.  Homepage URL is required, but can just be set to `https://www.maap-project.org`. Add a private key to get a PEM that can be used in the auth steps if one has not yet been created.

Go to the installations page (e.g., https://github.com/settings/apps/maap-system-tests/installations), click the Install button for the organization you wish to install it in. Choose the radio button "Only select repositories" and then choose the repo that will have it's workflow invoked, e.g., maap-data-system-tests, and click the Install button. You can now use the App's PEM to invoke the workflow in that repo.

## GitHub Docker Container Action Creation

The file [action.yml](action.yml) defines a GitHub Docker Container Action that builds an runs the [Dockerfile in this repo](Dockerfile). This can either be built and published to the GitHub Marketplace (recommended) or built and used with each invocation. Currently, the latter method is used in [.github/workflows/test.yml](.github/workflows/test.yml) with:

```
- name: Run the tests
  uses: ./
  id: test_run
```

This has the drawback that the Docker image layers must be pulled from GitLab on every invocation, whereas deploying the Action to the GitHub Marketplace would (presumably) cache them in the GitHub repository, which is (presumably) faster to retrieve from.

## Invoking the Repository Workflow from another Repo

The typical usage pattern will be for service repos to invoke the tests after they deploy.
This describes how to set that up for such as service repo.

The GitHub Action [invoke_system_tests.yml](
https://github.com/MAAP-Project/fake-service-for-invoking-system-tests/blob/main/.github/workflows/invoke_system_tests.yml) is an example of doing a checkout of the system tests repo, installing the necessary Python dependencies, and running the workflow invocation script [invocation/invoke_gh_action_with_pem.py](invocation/invoke_gh_action_with_pem.py) with the appropriate configuration.

There is secret that must be created named `PEM`. This should be set to the contents of the App's PEM file, including new lines (e.g., just cut and paste it into the Secret textarea.

The invocation of the script will usually take two parameters:

- `--branch` to determine which branch of the repo should be used (which also determines the deployment stage/environment to use)
- `--private_key` for the PEM.

Additionally, these parameters can be passed, through the default values in the script should be correct for all invocations.

- `--issuer` the GitHub App's identifier, used for the JWT issuer field
- `--installation_id` the GitHub App's installation id when installed in this repo
- `--repo` the GitHub repo on which to invoke the workflow dispatch, which should be this repo (MAAP-Project/maap-data-system-tests)
- `--workflow` the workflow to dispatch, by default, [test.yml](.github/workflows/test.yml)

## Manually Invoking the Repository Workflow with GitHub App Authentication

The workflow can be manually invoked when testing it using the following steps.

0. [maap-system-tests](https://github.com/settings/apps/maap-system-tests) is a "github app" of the MAAP-Project org.

1. Copy the PEM file (e.g., maap-system-tests.2021-11-23.private-key.pem) somewhere.

2. Use the PEM file to generate a JWT token.

```
JWT_TOKEN=$(python ./invocation/generate_jwt.py --pem maap-system-tests.2021-11-23.private-key.pem)
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

5. Use the API token to invoke the GitHub Actions Workflow Dispatch endpoint. This returns
   a 204 No Content status code on success.

```
curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer ${API_TOKEN}" -H 'Accept: application/vnd.github.v3+json' -d '{"ref":"main"}' https://api.github.com/repos/MAAP-Project/maap-data-system-tests/actions/workflows/test.yml/dispatches
```

6. Go to the [System Tests Workflow](https://github.com/MAAP-Project/maap-data-system-tests/actions/workflows/test.yml) page to see that the workflow is running.

## Running the Notebook Manually

1. Install the Python dependencies with `pip install -r requirements.txt`
2. Run with `papermill system-tests.ipynb system-tests-output.ipynb`

## Notebook Input Parameters

Notebooks will always need input parameters, if for no more than to know which stage to run the tests
against. When running with Papermill, create a cell tagged with "parameters". Papermill will then
inject a cell after this one with all of the passed parameters as Python variables with assignments.

## Installing maap-py

1. Switch to your virtual environment that you wish to install in.
2. `pip install matplotlib==3.3.1` 
3. Clone maap-py with `git clone git@github.com:MAAP-Project/maap-py.git`
4. `cd maap-py` then `python setup.py install`

## Running Cypress

```
npm install
npx cypress open
```
## References

- Running GitHub Actions locally using act: https://github.com/nektos/act
- Papermill CLI: https://papermill.readthedocs.io/en/latest/usage-cli.html
- Docker Container Action: https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
