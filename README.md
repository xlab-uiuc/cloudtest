# cloudtest
Things need to do when I am available:
1. If we want to record real service requests, we need to open system proxy now, which is not suitable. Possible solution: 1. Using PAC 2. Add suitable exclude policies.

Estimated time: ~1 week

2. How to install Mockserver certifications safely?

Now when I want to use 18081 and system proxy to catch real service requests,  SSL errors will pop out. IIRC, this is due to Mock server certifications.
https://www.mock-server.com/mock_server/HTTPS_TLS.html#button_configuration_tls_certificate_authority_certificate

Previously, I think we just installed it and it is not safe.

The problem can be solved easily by intalling the certificate when need to test and uninstalling the certificate when not need.

3. Previously, I mentioned that we cannot reach real cloud service server code to investigate. However, I remember there are some unofficial emulator for AWS.  
Like S3 MOCK[https://github.com/adobe/S3Mock#implemented-s3-apis], S3 ninja[https://github.com/scireum/s3ninja]. And one open source official emulator, Azurite[https://github.com/Azure/Azurite#https-setup]. Maybe I can investigate them later. And I need to have a meeting with yinfang to discuss it and get helps.

4. The idea from Suman: We can analyse call-chain to build oracle.
