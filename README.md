# cloudtest
Things need to do:

1. We cannot reach the source code of server side of cloud service. However, there are some unofficial emulator for AWS and official emulator for Azure.  
Like [S3 MOCK](https://github.com/adobe/S3Mock#implemented-s3-apis), [S3 ninja](https://github.com/scireum/s3ninja). And one open source official emulator, [Azurite](https://github.com/Azure/Azurite#https-setup). We need to investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.  
In addition: Anna provides a popular integrated AWS emulator [link](https://github.com/localstack/localstack) called localstack.  
Now, I believe it is better to start from [localstack](https://github.com/localstack/localstack) and [Azurite](https://github.com/Azure/Azurite#https-setup) because these two have detailed doc.  Priority: High  
2. 3 round is not enough for flaky test finding. We can run fully tests for heavy repo like Orleans for three times to pick up potential tests and rerun picked ones multiple times more(usually ~3 rounds more, but need to confirm a number later) to see if they are flaky. Priority: Medium
3. [Orleans Doc](https://learn.microsoft.com/en-us/dotnet/orleans/overview)   
4. [.Net Azure Table storage SDK Source Code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables)  
[Breif Intro of Azure Table SDK](https://www.nuget.org/packages/Azure.Data.Tables/)  
[Microsoft Doc of Azure Table SDK](https://learn.microsoft.com/en-us/azure/cosmos-db/table/support?toc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fstorage%2Ftables%2Ftoc.json&bc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fbread%2Ftoc.json) 
5. [Azurite Table support info](https://github.com/Azure/Azurite/wiki/Azurite-V3-Table)   
The Azurite Version we should use is 3.19.0. The one installed with Visual Studio Azure Development Pacakage is 3.18.0, but the newest one is 3.19.0(To the time I update cloudtest). And Azurite updated to 3.20.1 last night.  
The Orleans Version should be v7.0.0-rc2.  
6. Azurite releases a new version call 3.20.1 last night. Need to upgrade later. Priority: Low.  
7. Set up cloudtest in linux and update readme. Priority: Low.
