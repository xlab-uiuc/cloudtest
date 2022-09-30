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
import static com.Rainmaker.SDKAPIList;

public class RealService {
    public static class RequestForwardAndResponseCallback implements ExpectationForwardAndResponseCallback {
        @Override
        public HttpRequest handle(HttpRequest httpRequest) {
           return httpRequest;
        }
        @Override
        public HttpResponse handle(HttpRequest httpRequest, HttpResponse httpResponse) {
            return httpResponse;
        }
    }
}
