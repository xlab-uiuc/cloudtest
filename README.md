# cloudtest
Things need to do when I am available:

1. We cannot reach the source code of server side of cloud service. However, there are some unofficial emulator for AWS and official emulator for Azure.  
Like S3 MOCK[https://github.com/adobe/S3Mock#implemented-s3-apis], S3 ninja[https://github.com/scireum/s3ninja]. And one open source official emulator, Azurite[https://github.com/Azure/Azurite#https-setup]. We need to investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.

2. The idea from Suman: We can analyse call-chain to build oracle.

3. 3 round is not enough for flaky test finding. Need to find a way to solve it.

4. Modify the README of cloudtest infra and rerun the tests using the newest Orleans.

The Azurite Version I use now is 3.18.0. Maybe we should upgrade it manually. The one installed with Visual Studio Azure Development Pacakage is 3.18.0, but the newest one is 3.19.0  
The Orleans Version is old one for Rainmaker.
