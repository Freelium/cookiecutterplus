# Development

## Python's gonna python.

You may have your own method of practice when it comes to navigating the python morass of virtual environments and dependency management, but for this codebase this is what works for me.

### I use pyenv to manage my python versions.

```
pyenv versions
* system (set by ~/.pyenv/version)
```

Currently this works out to be python 3.10.0 for my system.

```
python --version
Python 3.10.0
```

### We use poetry to manage dependencies.
Read the [poetry documentation](https://python-poetry.org/docs/) for more information.
```
pip install pipx
pipx install poetry
pipx ensurepath
source ~/.zshrc
poetry install
```