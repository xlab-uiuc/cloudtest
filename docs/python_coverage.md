# Python code coverage with Coverage.py

We will calculate the code coverage of the following tool.

- Localstack


## Install and Configure


Install `Coverage.py`

```bash
pip install coverage
```

Copy the following python script to a file (start_localstack.py):

```python

def main():
    from localstack.cli import main

    main.main()


if __name__ == "__main__":
    main()

```

Configure the following argument in `config.py` for the *coverage* package which can be found in python packages either in `/usr/local/lib/pythonX.Y/site-packages` or `~/.local/lib/pythonX.Y/site-packages`.

```python

self.source: Optional[List[str]] = ["/home/anna/.local/lib/python3.8/site-packages/localstack"]
      
```

The coverage tool will now include the code coverage of this external module (our main target) which is invoked by a our little script above.

## Run coverage

Now, run the following command to execute the script in coverage mode:

```bash
coverage run start_localstack.py start
```

To generate the report, run:

```bash
coverage html
```