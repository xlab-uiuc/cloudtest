# cloudtest
Things need to do when I am available:
1. If we want to record real service requests, we need to open system proxy now, which is not suitable. Possible solution: 1. Using PAC 2. Add suitable exclude policies.

Estimated time: ~1 week

2. We cannot reach the source code of server side of cloud service. However, there are some unofficial emulator for AWS and official emulator for Azure.  
Like S3 MOCK[https://github.com/adobe/S3Mock#implemented-s3-apis], S3 ninja[https://github.com/scireum/s3ninja]. And one open source official emulator, Azurite[https://github.com/Azure/Azurite#https-setup]. We need to investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.

3. The idea from Suman: We can analyse call-chain to build oracle.

4. How to install Mockserver certifications safely? Done. List here for later reference.

Now when I want to use 18081 and system proxy to catch real service requests,  SSL errors will pop out. IIRC, this is due to Mock server certifications.
https://www.mock-server.com/mock_server/HTTPS_TLS.html#button_configuration_tls_certificate_authority_certificate

Previously, I think we just installed it and it is not safe.

The problem can be solved easily by intalling the certificate when need to test and uninstalling the certificate when not need. And we should only install the certificate for current user.
