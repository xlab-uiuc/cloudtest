# Projects under evaluation

## [Sleet](https://github.com/emgarten/Sleet)
Version: 7fb3c59b57e6454fba5a91b871f2b78b4c303bde

#### Azure
Emulator:
- Set environment variable via `export SLEET_TEST_ACCOUNT=UseDevelopmentStorage=true`

Cloud:
- Set environment variable via `export SLEET_TEST_ACCOUNT=YOUR_CONNECTION_STRING`

#### AWS
Emulator:
- Apply patch `patches/sleet_aws.patch`
- Set environment vairbale via `export AWS_ACCESS_KEY_ID=dummy` and `export AWS_SECRET_ACCESS_KEY=dummy`

Cloud:
- Set environment vairbale via `export AWS_ACCESS_KEY_ID=YOUR_ACCESS_ID` and `export AWS_SECRET_ACCESS_KEY=YOUR_ACCESS_KEY` 

## [Durabletask](https://github.com/Azure/durabletask)
Version: d7c3eb46570cd350094132da03c01a8f20ecfb0b

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set environment variable via `export DurableTaskTestStorageConnectionString=YOUR_CONNECTION_STRING`