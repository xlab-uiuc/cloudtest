# cloudtest
Things need to do:

1. We cannot reach the source code of server side of cloud service. However, there are some unofficial emulator for AWS and official emulator for Azure.  
Like S3 MOCK[https://github.com/adobe/S3Mock#implemented-s3-apis], S3 ninja[https://github.com/scireum/s3ninja]. And one open source official emulator, Azurite[https://github.com/Azure/Azurite#https-setup]. We need to investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.

2. 3 round is not enough for flaky test finding. Need to find a way to solve it.

3. Rerun the tests using the newest Orleans.

4. Set up cloudtest in linux and update readme.

5. https://learn.microsoft.com/en-us/dotnet/orleans/overview Orleans Doc  
6. .Net storage SDK source code: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables   
Breif Intro: https://www.nuget.org/packages/Azure.Data.Tables/  
Microsoft Doc: https://learn.microsoft.com/en-us/azure/cosmos-db/table/support?toc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fstorage%2Ftables%2Ftoc.json&bc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fbread%2Ftoc.json  

The Azurite Version we should use is 3.19.0. The one installed with Visual Studio Azure Development Pacakage is 3.18.0, but the newest one is 3.19.0  
The Orleans Version should be v7.0.0-rc2.
