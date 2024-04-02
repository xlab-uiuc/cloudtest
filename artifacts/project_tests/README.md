# Projects under evaluation

For each project, the repository must be cloned and checked out to the given version. 

## [Alpakka](https://github.com/akkadotnet/Alpakka)
Version: 869c6e28c85353577be74aec59801bbe9d498f0e

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/akkadotnet/Alpakka/blob/869c6e28c85353577be74aec59801bbe9d498f0e/src/Azure/Akka.Streams.Azure.StorageQueue.Tests/QueueSpecBase.cs#L17)

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test src/Azure/Akka.Streams.Azure.StorageQueue.Tests
```

## [ServiceBus.AttachmentPlugin](https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin)
Version: a074f8f804cb5a15d13f823ba6efd63c3da1a7b4

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin/blob/a074f8f804cb5a15d13f823ba6efd63c3da1a7b4/src/ServiceBus.AttachmentPlugin.Tests/AzureStorageEmulatorFixture.cs#L11)

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test src/ServiceBus.AttachmentPlugin.Tests
```

## [Durabletask](https://github.com/Azure/durabletask)
Version: d7c3eb46570cd350094132da03c01a8f20ecfb0b

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set environment variable via `export DurableTaskTestStorageConnectionString=YOUR_CONNECTION_STRING`

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/DurableTask.AzureStorage.Tests
```

## [identityazuretable](https://github.com/dlmelendez/identityazuretable)
Version: bc4ba07d6289addd275c425d20db3ee19167805f

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/dlmelendez/identityazuretable/blob/bc4ba07d6289addd275c425d20db3ee19167805f/tests/ElCamino.AspNetCore.Identity.AzureTable.Tests/config.json#L16)

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test tests/ElCamino.AspNetCore.Identity.AzureTable.Tests
```

## [Insights](https://github.com/NuGet/Insights)
Version: 21e3ae357d63125721246cf2291db09bd52bc02e

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/NuGet/Insights/blob/21e3ae357d63125721246cf2291db09bd52bc02e/test/Logic.Test/TestSupport/TestSettings.cs#L77-L82)

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/Logic.Test
```

## [IronPigeon](https://github.com/AArnott/IronPigeon)
Version: e4d125f9f9cba04c7eb219cac1f309ead487fa9d

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/AArnott/IronPigeon/blob/e4d125f9f9cba04c7eb219cac1f309ead487fa9d/test/IronPigeon.Tests/Providers/AzureBlobStorageTests.cs#L28C55-L28C76) 

After configurating for either environment, run the following to build and execute the tests: 

```bash
dotnet test test/IronPigeon.Tests
```

## [Orleans](https://github.com/dotnet/orleans)
Version: 6a4cc9099ac151c36e6ecded78d7991a3ed459d7

#### Azure
Emulator:
- Apply patch `patches/orleans_azure_emulator.patch`

Cloud:
- Apply patch `patches/orleans_azure_emulator.patch`
- Modify the value of `DataConnectionString` in this [file](https://github.com/dotnet/orleans/blob/6a4cc9099ac151c36e6ecded78d7991a3ed459d7/test/TestInfrastructure/TestExtensions/TestDefaultConfiguration.cs#L77) to the cloud connection string. 

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/Extensions/TesterAzureUtils
```

#### AWS
Emulator:
- Apply patch `patches/orleans_aws_emulator.patch`

Cloud:
- Apply patch `patches/orleans_azure_emulator.patch`
- Modify the value of `DynamoDbService` `DynamoDbAccessKey` `DynamoDbAccessKey`in this [file](https://github.com/dotnet/orleans/blob/6a4cc9099ac151c36e6ecded78d7991a3ed459d7/test/TestInfrastructure/TestExtensions/TestDefaultConfiguration.cs#L77) to the cloud configurations. 

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/Extensions/AWSUtils.Tests
```

## [ServiceStack](https://github.com/ServiceStack/ServiceStack)
Version: eaaa85f553642e5f721466fafb247132cca00006

#### AWS 
Emulator:
- Apply patch `patches/servicestack_aws_emulator.patch`

Cloud:
- Apply patch `patches/servicestack_aws_cloud.patch`
- Set environment variable via `export AWS_ACCESS_KEY=YOUR_ACCESS_KEY` and `export AWS_SECRET_KEY=YOUR_SECRET_KEY` 


After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test ServiceStack.Aws/tests/ServiceStack.Aws.Tests
```

```bash
dotnet test ServiceStack.Aws/tests/ServiceStack.Aws.DynamoDbTests
```

## [Sleet](https://github.com/emgarten/Sleet)
Version: 7fb3c59b57e6454fba5a91b871f2b78b4c303bde

#### Azure
Emulator:
- Set environment variable via `export SLEET_TEST_ACCOUNT=UseDevelopmentStorage=true`

Cloud:
- Set environment variable via `export SLEET_TEST_ACCOUNT=YOUR_CONNECTION_STRING`

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/Sleet.Azure.Tests
```

#### AWS
Emulator:
- Apply patch `patches/sleet_aws.patch`
- Set environment vairbale via `export AWS_ACCESS_KEY_ID=dummy` and `export AWS_SECRET_ACCESS_KEY=dummy`

Cloud:
- Set environment vairbale via `export AWS_ACCESS_KEY_ID=YOUR_ACCESS_ID` and `export AWS_SECRET_ACCESS_KEY=YOUR_ACCESS_KEY` 

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test test/Sleet.AmazonS3.Tests
```

## [Streamtone](https://github.com/yevhen/Streamstone)
Version: 71b34da9a76772234406618a95b6d00889dcf376

#### Azure
Emulator:
- No extra configuration needed

Cloud:
- Set connection string in this [file](https://github.com/yevhen/Streamstone/blob/71b34da9a76772234406618a95b6d00889dcf376/Source/Streamstone.Tests/Storage.cs#L66) 

After configurating for either environment, run the following to build and execute the tests:

```bash
dotnet test Source/Streamstone.Tests
```
