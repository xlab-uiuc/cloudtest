# cloudtest
Things need to do when I am available:
1. If we want to record real service requests, we need to open system proxy now, which is not suitable. Possible solution: 1. Using PAC 2. Add suitable exclude policies.

Estimated time: ~1 week

2. We cannot reach the source code of server side of cloud service. However, there are some unofficial emulator for AWS and official emulator for Azure.  
Like S3 MOCK[https://github.com/adobe/S3Mock#implemented-s3-apis], S3 ninja[https://github.com/scireum/s3ninja]. And one open source official emulator, Azurite[https://github.com/Azure/Azurite#https-setup]. We need to investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.

3. The idea from Suman: We can analyse call-chain to build oracle.

4. Need to discuss proxy with Yinfang.

5. 3 round is not enough for flaky test finding. Need to find a way to solve it.

The Azurite Version I use now is 3.18.0
The Orleans Version is old one for Rainmaker.
