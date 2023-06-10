# Grammar and Mutation based fuzzing with Python

## Install packages

The following tools are assumed to be installed on your system:

- Azurite
- nyc

Install python packages with:

```bash
pip install -r requirements.txt
```

Run the following to start Azurite in coverage mode:

```bash
npm run coverage
```

Clone the cloudtest repo and navigate to this [directory](../python_fuzzer/).
Run the following command to start fuzzing of Azurite:

```bash
python fuzz.py
```


## Fuzzing strategies details

## Results