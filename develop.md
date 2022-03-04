# Development Guide

## Preamble
C-o-C, can get the generality here, but for 99% it should be fine, we don't like sitting on broom handles anyway.

## Setup
### Virtual environment
Once the repository is cloned, you can create a *virtual environment* using one of the following commands:
```bash
...
```

#### Windows
In order to enter the newly created *virtual environment* on Windows you should use the following command:
```batch
.\venv\Scripts\activate.bat
```

#### Linux
In order to enter the newly created *virtual environment* on Linux you should use the following command:
```batch
???
```

#### MacOS
MacOS is currently not explicitly supported since I do not have access to a machine running that OS.

### Dependencies

## Building

`pip install -e .[dev]`<br>
`pip install --upgrade -t requirements-dev.txt`

`check-manifest --create`<br>
`python -m check-manifest --create`
