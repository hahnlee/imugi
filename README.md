# Imugi
The experimental python compiler written in python

# Development
* imugi only supports Python 3.6 or later
* imugi only supports macOS and Linux

```
pip install -e .[dev]
```

# Test
```
python -m unittest discover imugi/tests
```

# Pre-commit
```
isort imugi/**/*.py -c
flake8
python -m unittest discover imugi/tests
```

# Docker
```
docker build -t imugi .
docker run -it -v $PWD:/imugi -w /imugi imugi
```
