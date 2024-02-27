# cookiecutterplus
A wrapper for cookiecutter that provides some extras

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Getting Started
Cookiecutter+ can currently be ran as a CLI tool or a Docker container which runs in API mode.

## CLI Instructions
Cookiecutter+ can be ran as a CLI tool on any platform that supports Python

### CLI Prerequisites
Cookiecutter+ relies on the Git CLI to access the Repo where the Cookiecutter templates reside.  You should ideally have Git setup with authentication for the repo where your Cookiecutter templates reside.

### CLI Flags
| CLI Flag | CLI Flag (alternate) | Type   |                                                                                                                                                                 **Description**                                                                                                                                                                 | **Example**                                                                                                                                                                                                                                                          | **Required** | **Default Value** |
|:--------:|:--------------------:|--------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------:|:-----------------:|
| -a       | --api-mode           | Bool   | When enabled, CookieCutterPlus runs in API mode allowing users to send JSON payloads to the `/generate` endpoint                                                                                                                                                                                                                                | MyOrg/cookiecutter-templates                                                                                                                                                                                                                                         |     **True** |              None |
| -t       | --template-repo      | String | This CLI flag should be set to the Github Repo where the CookieCutter templates reside.                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                      |              |                   |
| -p       | --payload            | Dict   | This CLI flag should contain the CookieCutter Template payloads that you want CookieCutterPlus to apply.  The key is simply a label and can be set to whatever you like.\\  `template_path`: The path in the `template_repo` where the template resides\ `context_vars`: A map of override variables for the cookiecutter.json on the Template\ | "cookiecutter-gha": {             "template_path": "cookiecutter/shared/cookiecutter-gha",             "context_vars": {                 "component_name": "test-component",                 "author": "Anonymous",                 "version": "0.1.0"             } |     **True** |              None |
| -o       | --output-path        | String | This CLI flag sets the output path where the CookieCutterPlus application will write out the generated templates.                                                                                                                                                                                                                               | ./output                                                                                                                                                                                                                                                             |     **True** |              None |
| -n       | --no-input           | Bool   | When enabled, you will be interactively prompted for Cookiecutter template variable input.                                                                                                                                                                                                                                                      | True                                                                                                                                                                                                                                                                 |     **True** |              True |

## Docker Instructions
Cookiecutter+ can be ran as a Docker container.  When running as a container, Cookiecutter+ will start in API mode and you can then integrate this container as part of an external workflow.

### Environment Variables
| Environment Variable Name | Description                                                                                                           | Required | Default Value |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|----------|---------------|
| **GITHUB_TOKEN**          | This variable should be a valid GitHub PAT token with permissions to the GH org where the cookiecutter templates live | **True** |          None |

### How to run the CookieCutterPlus Docker container
This is an example of how to run the Cookiecutter+ Docker image in this repo.
```
 docker run -e GITHUB_TOKEN=my_pat_token \
            -p 9999:5000 \
            cookiecutterplus:$image_tag
```

## CookieCutterPlus API

### How to hit the CookieCutterPlus API
You can apply Cookiecutter Templates via a convenient API endpoint that accepts a JSON payload.

See the below example for an example of how to use cURL to hit the CookieCutter+ `/generate` endpoint to apply 1 or more CookieCutter templates with a JSON payload.

| **JSON Parameters** | **Type** |                                                                                                                                                               **Description**                                                                                                                                                              | **Example**                                                                                                                                                                                                                                                          | **Required** | **Default Value** |
|:-------------------:|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------:|:-----------------:|
| template_repo       | String   | This parameter should map to the GitHub Repo containing the CookieCutter Templates.                                                                                                                                                                                                                                                        | MyOrg/cookiecutter-templates                                                                                                                                                                                                                                         |     **True** |              None |
| payload             | Object   | This parameter contains the CookieCutter Template payloads that you want CookieCutterPlus to apply.  The key is simply a label and can be set to whatever you like.\\  `template_path`: The path in the `template_repo` where the template resides\ `context_vars`: A map of override variables for the cookiecutter.json on the Template\ | "cookiecutter-gha": {             "template_path": "cookiecutter/shared/cookiecutter-gha",             "context_vars": {                 "component_name": "test-component",                 "author": "Anonymous",                 "version": "0.1.0"             } |     **True** |              None |
| output_path         | String   | This parameter sets the output path where the CookieCutterPlus application will write out the generated templates.                                                                                                                                                                                                                         | ./output                                                                                                                                                                                                                                                             |     **True** |              None |
| no_input            | Bool     | This parameter is for CLI mode and should always be set to **True** when running CookieCutterPlus in API mode.                                                                                                                                                                                                                             | True                                                                                                                                                                                                                                                                 |     **True** |              True |

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
