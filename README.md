# cloudtest
Things need to do when I am available:
1. If we want to record real service requests, we need to open system proxy now, which is not suitable. Possible solution: 1. Using PAC 2. Add suitable exclude policies.

Estimated time: ~1 week

2. How to install Mockserver certifications safely?

Now when I want to use 18081 and system proxy to catch real service requests,  SSL errors will pop out. IIRC, this is due to Mock server certifications.
https://www.mock-server.com/mock_server/HTTPS_TLS.html#button_configuration_tls_certificate_authority_certificate

Previously, I think we just installed it and it is not safe.
