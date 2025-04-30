# Fuzzing the emulators

## Install packages

Install Azurite:

```bash
npm install -g azurite@3.21.0
```

Install python packages with:

```bash
pip install -r requirements.txt
```

The following packages will be installed:

- fuzzingbook v1.1
- azure.storage.blob v12.15.0
- azure.storage.queue v12.5.0
- azure.data.tables v23.0.1
- localstack v2.0.1
- boto3 v1.28.6

## Configuration

To perform differential fuzzing, the tool requires a valid cloud connection configuration.

For Azure Blob, Queue and Table, set up the following fields in `config.json`:

```json
"cloud_connection_string" : "{insert here}",
"cloud_account_name": "{insert here}"
```

For AWS S3 and DynamoDB, create a profile named `aws` and set up the configuration.

```bash
aws configure --profile aws
```

## Running the fuzzer

### Fuzzing Azurite

Run the following to start Azurite:

```bash
Azurite --skipApiVersionCheck
```

Run the following command to start fuzzing:

```bash
python fuzz.py {service_type}
```

Enter one of the following for each service type:

- 1 : Azure Blob
- 2 : Azure Queue
- 3 : Azure Table

### Fuzzing LocalStack

Run the following to start Azurite:

```bash
Localstack start
```

Run the following command to start fuzzing:

```bash
python fuzz.py {service_type}
```

Enter one of the following for each service type:

- 4 : AWS S3
- 5 : AWS DynamoDB
