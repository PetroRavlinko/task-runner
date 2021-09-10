# Task Runner project

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=PetroRavlinko_task-runner&metric=alert_status)](https://sonarcloud.io/dashboard?id=PetroRavlinko_task-runner)
[![codecov](https://codecov.io/gh/PetroRavlinko/task-runner/branch/main/graph/badge.svg?token=ZND14Y1O1T)](https://codecov.io/gh/PetroRavlinko/task-runner)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
---

Task runner project should help with automation of some DevOps manual tasks that couldn't be solved with AWS CloudFormation or other IaC tools.

---

## Requirements

- python
- pip


> TODO: migrate on ```virtualenv```


### Dependency management

#### Install required packages

```shell
pip install -r requirements.txt
```

#### Uninstall related dependencies

```shell
pip uninstall -r requirements.txt -y
```


## Code structure

### New task conventions

Ticket name with ```_``` replacement for all special symbols.

## Unit tests

The tests are implemented and run with ```unittest``` framework. You need run a command below to run all tests

```shell
python -m unittest
```
Measure code coverage with next command:
```shell
pip install coverage
coverage run -m unittest
```

## Contributing
You can find how to contribute to the project in contributing guideline [here](CONTRIBUTING.md)

## Code of conduct
The project’s principles, standards, and the moral and ethical expectations that contributors should follow are in code of conduct policy [here](CODE_OF_CONDUCT.md)

