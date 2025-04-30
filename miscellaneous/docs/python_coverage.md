# Python code coverage with Coverage.py

We will calculate the code coverage of the following tool.

- Localstack

## Install and Configure

Clone the following repo:

```bash
git clone https://github.com/localstack/localstack.git
```

Run this command to install all the dependencies::

```bash
make install
```

Activate virtual python env:

```bash
source localstack/.venv/bin/activate 
```

Create a config file for coverage tool (already install in env) `.coveragerc` and copy the following configs:

```python
# .coveragerc to control coverage.py

[run]
relative_files = True
sigterm = True
debug = trace
source = 
    /home/anna/[MS]UIUC-new/Research/localstack/localstack/services/s3/
```

## Run coverage

Now, run the following command to start localstack in coverage mode on host machine (NOT DOCKER):

```bash
coverage run -p localstack/bin/localstack start --host
```

Combine the coverage data:

```bash
coverage combine
```

To generate the report, run:

```bash
coverage html
```
