# cookiecutterplus
A wrapper for cookiecutter that provides some extras

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Getting Started
Cookiecutter+ can currently be ran as a CLI tool or a Docker container which runs in API mode.


### Docker Instructions
Cookiecutter+ can also be ran as a Docker container.  When running as a container, Cookiecutter+ will start in API mode and you can then integrate this container as part of a workflow.

#### Environment Variables
| Environment Variable      | Description                                                                                                           | Default Value |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|---------------|
| GITHUB_TOKEN              | This variable should be a valid GitHub PAT token with permissions to the GH org where the cookiecutter templates live |          None |

This is an example of how to run the Cookiecutter+ Docker image in this repo.
`docker run -e GITHUB_TOKEN=my_pat_token -p 9999:5000 cookiecutterplus:$image_tag`
