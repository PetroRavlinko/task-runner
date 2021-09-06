# Task Runner project

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=PetroRavlinko_task-runner&metric=alert_status)](https://sonarcloud.io/dashboard?id=PetroRavlinko_task-runner)
---

Task runner project should help with automation of some DevOps manual tasks that couldn't be solved with AWS CloudFormation or other IaC tools.

---


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
