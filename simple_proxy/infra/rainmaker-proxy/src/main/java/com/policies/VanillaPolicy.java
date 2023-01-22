package com;

import org.mockserver.mock.action.ExpectationForwardAndResponseCallback;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;
import org.mockserver.model.MediaType;
import org.mockserver.model.SocketAddress;

import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.Rainmaker.*;

public class VanillaPolicy {
    public static class RequestForwardAndResponseCallback implements ExpectationForwardAndResponseCallback {
        @Override
        public HttpRequest handle(HttpRequest httpRequest) {
        //    return httpRequest;
           String requestHost = httpRequest.getHeader("Host").toString();
        //    System.out.println(requestHost);
           if (Objects.equals(requestHost, "[127.0.0.1:10000]"))
               return httpRequest
                       .withSocketAddress("127.0.0.1", 20000, SocketAddress.Scheme.HTTPS);
           else if (Objects.equals(requestHost, "[127.0.0.1:10001]"))
               return httpRequest
                       .withSocketAddress("127.0.0.1", 20001, SocketAddress.Scheme.HTTPS);
           else if (Objects.equals(requestHost, "[127.0.0.1:10002]"))
               return httpRequest
                       .withSocketAddress("127.0.0.1", 20002, SocketAddress.Scheme.HTTPS);
           else
               return httpRequest;
        }

        @Override
        public HttpResponse handle(HttpRequest httpRequest, HttpResponse httpResponse) {
            return httpResponse;
        }
    }
}
