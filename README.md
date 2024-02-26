# cookiecutterplus
A wrapper for cookiecutter that provides some extras

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Getting Started
Cookiecutter+ can currently be ran as a CLI tool or a Docker container which runs in API mode.


### Docker Instructions
Cookiecutter+ can also be ran as a Docker container.  When running as a container, Cookiecutter+ will start in API mode and you can then integrate this container as part of a workflow.

#### Environment Variables
| Environment Variable Name | Description                                                                                                           | Required | Default Value |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|----------|---------------|
| **GITHUB_TOKEN**          | This variable should be a valid GitHub PAT token with permissions to the GH org where the cookiecutter templates live | **True** |          None |

#### How to run the CookieCutterPlus Docker container
This is an example of how to run the Cookiecutter+ Docker image in this repo.

`docker run -e GITHUB_TOKEN=my_pat_token -p 9999:5000 -v ./output:app/output/ cookiecutterplus:$image_tag`

#### How to hit the CookieCutterPlus API
You can apply Cookiecutter Templates via a convenient API endpoint that accepts a JSON payload.

See the below example for an example of how to use cURL to have CookieCutterPlus to apply 1 or more CookieCutter templates with the Docker container.

```
curl --location 'http://127.0.0.1:9999/generate' \
--header 'Content-Type: application/json' \
--data '{
    "template_repo": "MyOrg/my-cookiecutter-template-repo",
    "payload": {
        "cookiecutter-gha": {
            "template_path": "cookiecutter/shared/cookiecutter-gha",
            "context_vars": {
                "component_name": "test-component",
                "author": "Anonymous",
                "version": "0.1.0"
            }
        },
        "cookiecutter-java": {
            "template_path": "cookiecutter/shared/cookiecutter-java",
            "context_vars": {
                "component_name": "test-component",
                "author": "Anonymous",
                "echo": "Hello, World!",
                "java_version": "0.1.0"
            }
        }
    },
    "output_path": "./output",
    "no_input": "True"
}'
{
  "message": "CookieCutter generation completed successfully"
}
```
