# Projects under evaluation

## [Alpakka](https://github.com/akkadotnet/Alpakka)
Version: 869c6e28c85353577be74aec59801bbe9d498f0e

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/akkadotnet/Alpakka/blob/869c6e28c85353577be74aec59801bbe9d498f0e/src/Azure/Akka.Streams.Azure.StorageQueue.Tests/QueueSpecBase.cs#L17)

## [Durabletask](https://github.com/Azure/durabletask)
Version: d7c3eb46570cd350094132da03c01a8f20ecfb0b

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set environment variable via `export DurableTaskTestStorageConnectionString=YOUR_CONNECTION_STRING`

## [identityazuretable](https://github.com/dlmelendez/identityazuretable)
Version: bc4ba07d6289addd275c425d20db3ee19167805f

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/dlmelendez/identityazuretable/blob/bc4ba07d6289addd275c425d20db3ee19167805f/tests/ElCamino.AspNetCore.Identity.AzureTable.Tests/config.json#L16)

## [IronPigeon](https://github.com/AArnott/IronPigeon)
Version: e4d125f9f9cba04c7eb219cac1f309ead487fa9d

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/AArnott/IronPigeon/blob/e4d125f9f9cba04c7eb219cac1f309ead487fa9d/test/IronPigeon.Tests/Providers/AzureBlobStorageTests.cs#L28C55-L28C76) 

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

## [Streamtone](https://github.com/yevhen/Streamstone)
Version: 71b34da9a76772234406618a95b6d00889dcf376

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/yevhen/Streamstone/blob/71b34da9a76772234406618a95b6d00889dcf376/Source/Streamstone.Tests/Storage.cs#L66) 
