# Rainmaker Infrastructure for cloudtest

Rainmaker aims to build a large-scale cloud application bug finding infrastructure.

**Warning: You have to put rainmaker & cloud application repos under the path "C:\Users\XX\ " to run rainmaker successfully using template-config.json. Otherwise, you have to modify "project_path_root" in config.json.**

## Environment Setup before Using Rainmaker Proxy

### .NET

The .NET version should be decided by the cloud application under test. In most cases we recommend is .NET 6.0 since it is backward compatible. And now, newest Orleans is using .NET 7.0.

To check .NET SDK: Go to C:\Program Files\dotnet\sdk to view all .NET SDK editions.

If you do not have .NET SDK, please go to [Download .NET](https://dotnet.microsoft.com/en-us/download/dotnet) to download and install.

### Maven

Install Java and Maven.

Java/Maven versions being tested (output from ``mvn -v``):

```
Apache Maven 3.8.4 (9b656c72d54e5bacbed989b64718c159fe39b537)                   
Java version: 11.0.14.1, vendor: Amazon.com Inc., runtime: XXX\.jdks\corretto-11.0.14.1
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"
```

Java version: 11

### Python

Install Python and following packages in your system:

```
pandas
```

### Azure Storage settings

Rainmaker proxy will listen on ``127.0.0.1:10000,10001,10002`` which are default Azure Blob, Queue, Table storage services' ports respectively, and serve as a proxy to forward requests to ``127.0.0.1:20000,20001,20002`` correspondingly.

### If using Azurite (Recommended, because it is open-spurce and still under maintenance)

Azurite is the latest storage emulator platform. Azurite supersedes the [Azure Storage Emulator](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-emulator). Azurite will continue to be updated to support the latest versions of Azure Storage APIs. The reason why we use both Azurite and Azure Storage settings is that some frameworks we tested do not support Azurite.

#### Install latest verison Azurite:  
1. Go to [Download | Node.js (nodejs.org)](https://nodejs.org/en/download/) , Click the **Windows Installer** button to download the latest LTS version. At the time this readme was written, version v16.14.2-x64 was the latest LTS version. The Node.js installer includes the NPM package manager.  
1. Git clone [Azurite](https://github.com/Azure/Azurite).  
2. ``git reset --hard v3.19.0``  
3.  execute following commands to install and start Azurite V3.  
    1. ``npm ci --legacy-peer-deps``
    2. ``npm run build``  
    3. ``npm install -g``
    4. ``azurite --blobPort 20000 --queuePort 20001 --tablePort 20002``  

Reference:  
1. https://github.com/Azure/Azurite  
2. https://github.com/Azure/Azurite/issues/1550

~~Azurite is automatically available with [Visual Studio 2022](https://visualstudio.microsoft.com/vs/). If you are running an earlier version of Visual Studio, you'll need to install Azurite by using either Node Package Manager, DockerHub, or by cloning the Azurite github repository.~~

~~Reference: https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio~~

#### Run Azurite:

Open the Powershell and run ``azurite --blobPort 20000 --queuePort 20001 --tablePort 20002``

##### Caveat for Azurite:

If you want to run tests without Rainmaker, do not listen to ports 20000, 20001 and 20002, i.e.,  `azurite`

### If using legacy Azure Storage Emulator (Not Recommended because it is not open-source, which means it is hard to investigate)

Since Azure Storage Emulator will automatically listen to 10000, 10001, 10002 of localhost, it is necessary to modify the ports configuration in ``AzureStorageEmulator.exe.config`` file under ``C:\Program Files (x86)\Microsoft SDKs\Azure\Storage Emulator`` directory:

```
<services>
  <service name="Blob" url="http://127.0.0.1:20000/"/>
  <service name="Queue" url="http://127.0.0.1:20001/"/>
  <service name="Table" url="http://127.0.0.1:20002/"/>
</services>
```

## How to use Rainmaker Proxy

**Shortcut:** `.\rainmaker.ps1`

The shortcut now will only run the step 2 and 3 below.

Detailed steps: Modify the *config.json* file to configure the target projects, if a project should be skipped, then its corresponding "skip" field should be set to ``true``; then:

1. ``cd rainmaker-proxy``
2. ``mvn package``
3. ``java -jar .\target\rainmaker-proxy-1.0-SNAPSHOT.jar -Xmx8g``

``-Xmx8g`` is used to improve the JAVA heap memory
### Open System proxy when you want to fetch real service requests and responses.  
Notice that extra delay will add and make tests fail. See detail in xlab-uiuc/cloudtest#3  
1. Open Proxy setting of windows and Turn ``Use a proxy server`` on.  
2. Set Address to 127.0.0.1 and Proxy to 18081(The port that rainmaker-proxy listen to)
3. Save the configuration.  
4. If you meet the SSL problem, pls [download](https://raw.githubusercontent.com/jamesdbloom/mockserver/master/mockserver-core/src/main/resources/org/mockserver/socket/CertificateAuthorityCertificate.pem) and install the certificate of Rainmaker-Proxy.  

## How to collect the test results and generate the outcome

1. ``python test_outcome_generator.py`` to generate outcome files that collect passed, failed and skipped files into different places

- Files will be generated for each test round under ``rainmaker/results/PROJECTNAME/``: FAILED_test.csv (list of failed test names), PASSED_test.csv (list of succeeded test names), SKIPPED_test.csv (list of skipped test names), test-stats.txt

2. ``python test_raw_data_generator.py`` to generate beautified json file. Files will be generated for each test under ``infra/rainmaker-proxy/stat/each test name/``: b_request.json (beautified json file)

#### We need to specify the def_XXX for the python script above. You can use -help to find out how to use it.  

<!-- ## Attach Visual Studio debugger to the test

If you want to attach VS debugger to the test, all you need to do is to set the value of a environment variable ``VSTEST_HOST_DEBUG`` to 1.

### Attach when using Rainmaker infra

If you want to use Rainmaker infra at the same time debugging the test, you should add a new variable named ``VSTEST_HOST_DEBUG`` with value set to 1 in System variables via Windows' adavanced system setting GUI. Then open a new Powershell since Powershell will only update its environment varaible at the beginning of its life cycle. Note that if you run in a IntelliJ terminal, you may need to restart IntelliJ.

After setting the variable properly, you should see this when you run Rainmaker:

```
Host debugging is enabled. Please attach debugger to testhost process to continue.
Process Id: 40244, Name: testhost
```

### Attach debugger without Rainmaker

If you are solely running a test and want to debug it (maybe using Fiddler at the same time), an easier way to do is to type ``$env:VSTEST_HOST_DEBUG=1`` in the current Powershell. -->

## Tips for monitoring the on-going tests

Use this command to know the current Nth running test: ``(Get-ChildItem -Directory | Measure-Object).Count``

## Caveat

<!-- - When you are going to analyze a new cloud-backed application, please always remember to turn on the Torch tool. E.g., when analyzing a project A from GitHub, remember to turn off and on Torch tool after git clone A. -->
- You may need to make a global.json file to specify the .NET version at the root of the cloud application repo.

<!-- ### Caveat for AWS S3/SQS cloud applications
(How to automate this step?)
1. Add the MockServer certificate to the machine:
  - reference for adding certificate: https://support.securly.com/hc/en-us/articles/360026808753-How-do-I-manually-install-the-Securly-SSL-certificate-on-Windows
  - Mockserver certificate (PEM file): https://raw.githubusercontent.com/mock-server/mockserver/master/mockserver-core/src/main/resources/org/mockserver/socket/CertificateAuthorityCertificate.pem
2. Open the Windows system proxy on port 18081, IP 127.0.0.1 (Is it possible to automate this?) -->

### Caveat for Orleans project

**Shortcut:**(Must be done before running `rainmaker.ps1`)

1. copy [the file](https://github.com/xlab-uiuc/rainmaker/blob/main/patches/Orleans.patch) into the base folder of Orleans
2. `cd orleans`
3. `git apply .\Orleans_patch_file.patch`

Detailed steps of the shortcut above(If you cannot apply the patch successfully, you have to do the modification below manually):

- Add the connection string ``"UseDevelopmentStorage=true"`` to the repo: you can add a line after [this line](https://github.com/dotnet/orleans/blob/14bc87740e830342a9eafb2e8e057794d7b7156c/test/TestInfrastructure/TestExtensions/TestDefaultConfiguration.cs#L67), i.e.,

```
{ nameof(ZooKeeperConnectionString), "127.0.0.1:2181" },
{ nameof(DataConnectionString), "UseDevelopmentStorage=true" }
```

- Orleans directly check the existence of the Azure Storage Emulator, so if you choose to use Azurite, you could comment out these [lines](https://github.com/dotnet/orleans/blob/3895e070ea4b9870440a5c44eed93262923b73a5/test/TestInfrastructure/TestExtensions/TestUtils.cs#L41-L46) before running the rainmaker proxy.

### Other caveats

1. When running the injection round in PowerShell, it is recommended to disable the "Quick Edit" feature of PowerShell to avoid the risk of accidental pause led by the bug of PowerShell.
2. (Optional) Changing Orleans timeout: #127
3. If you are using non-English language win10 platform for rainmaker, you should change Language for non-Unicode programs into English.


## Config

### Introduction:

 | Entry name                                         | Explanation                                        | Example                                                                                                                                                                                                                                                                                                                                                                                               |
 | :------------------------------------------------- | :------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | `project`                                        | Name of application                                | "Orleans"                                                                                                                                                                                                                                                                                                                                                                                             |
 | `project_test_path`                              | Application Test Unit path                         | "orleans\test\Extensions\TesterAzureUtils"                                                                                                                                                                                                                                                                                                                                                            |
 | `project_path_root`                              | Application root path to find application          | "\\Users\\"                                                                                                                                                                                                                                                                                                                                                                                           |
 | `rainmaker_path`                                 | Rainmaker project path for test  | "cloudtest\\infra\\rainmaker-proxy"                                                                                                                                                                                                                                                                                                                                                                   |
 | `skip`                                           | Whether we choose to test this application  | true means do not test this application; false means test this application.                                                                                                                                                                                                                                                                                                                           |
 | `policy`                                         | Test policy| "vanilla"                                                                                                                                                                                                                                                                                                                                                                                   |
 | `policies(for doc purpose)`                      | Test policies for selection             | ["vanilla","vanilla_real"]                                                                                                                                                                                                                                                                                                                          |
 | `test_dll`                                       | Test_dll path to find application dll              | "%HOMEDRIVE%%HOMEPATH%\\orleans\\test\\Extensions\TesterAzureUtils\\bin\\Debug\\net5.0\\Tester.AzureUtils.dll"                                                                                         |
 | `full_test`                           | Whether we choose the whole test mode              | false means No, true means Yes.                                                                                                                                                                                                                                                                                                                                                                       |
 | `partial_test`                                   | The partial test we run                            | ["Tester.AzureUtils.Streaming.AQProgrammaticSubscribeTest. StreamingTests_Consumer_Producer_SubscribeToStreamsHandledByDifferentStreamProvider"]                                                                                                                                                                                                                                                      |
 | `other_usually_used_tests(for doc purpose)`      | The partial test we usually choose                 | ["Tester.AzureUtils.TimerTests.ReminderTests_AzureTable.Rem_Azure_Wrong_Grain", "Tester.AzureUtils.Streaming.AQStreamingTests.AQ_01_OneProducerGrainOneConsumerGrain", "UnitTests.Streaming.Reliability.StreamReliabilityTests.AQ_StreamRel_SiloRestarts_Consumer", "Tester.AzureUtils.AzureQueueDataManagerTests.AQ_Standalone_1", "Tester.AzureUtils.AzureTableGrainDirectoryTests.LookupNotFound"] |

 
