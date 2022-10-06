# cloudtest
Things need to do when I am available:
1. Now I remove request retrieve part, and only keep outcome part. If we need to do investigation on request, I need to add it back and make it fit for real service tests. If we want to record real service requests, we need to open system proxy now, which is not suitable.

Estimated time: ~1 week

2. Need to write a scirpt to prune out flaky tests and find out potential candidate tests.

Estimated time: Done, but need to confirm details with folks to make things solid.

3. How to install Mockserver certifications safely?

Now when I want to use 18081 and system proxy to catch real service requests,  SSL errors will pop out. IIRC, this is due to Mock server certifications.
https://www.mock-server.com/mock_server/HTTPS_TLS.html#button_configuration_tls_certificate_authority_certificate

Previously, I think we just installed it and it is not safe.
