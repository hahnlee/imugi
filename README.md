# Imugi
The experimental python compiler written in python

imugi compiles python to use the [Objective-C Runtime](https://developer.apple.com/documentation/objectivec/objective_c_runtime).

[Objective-C Runtime](https://developer.apple.com/documentation/objectivec/objective_c_runtime) is used only for PoC and can be changed later.

# Development
* imugi only supports Python 3.6 or later
* imugi only supports macOS

```
pip install -e .[dev]
```

# Pre-commit
```
isort imugi/**/*.py -c
flake8
```
