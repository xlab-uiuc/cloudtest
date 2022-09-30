package com.loghandler;

import org.json.JSONObject;
import org.mockserver.model.HttpRequest;

public abstract class Handler {
    public JSONObject _request;
    public HttpRequest _HTTPRequest;

    boolean _realTimeFlag = false;

    public Handler() {
//        _service = Rainmaker.noServiceUse;
    }

    public void decideWhichOperation() {
//        System.out.println("Entering decideWhichOperation in Handler class..");
//        System.out.println("HTTP Method: " + getMethodString());
        String methodString = _realTimeFlag ? getMethodStringRealTime() : getMethodString();
        switch (methodString) {
            case "PUT": putRequest(); break;
            case "DELETE": deleteRequest(); break;
            case "GET": getRequest(); break;
            case "HEAD": headRequest(); break;
            case "POST": postRequest(); break;
            case "MERGE": mergeRequest(); break;
            case "PATCH": patchRequest(); break;
            default: System.out.println("!!!Method not covered: " + getMethodString() + " Request: " + _request + " !!!"); break;
        }
    }

    public Handler(JSONObject request) {
        _request = request;
//        _service = serviceInUse;
    }

    public String getMethodString() {
        return _request.getString("method");
    }

    public String getMethodStringRealTime() {
        return _HTTPRequest.getMethod().toString();
    }

    public String getPathString() {
        return _request.getString("path");
    }

    protected abstract void putRequest();

    protected abstract void deleteRequest();

    protected abstract void getRequest();

    protected abstract void headRequest();

    protected abstract void postRequest();

    protected abstract void mergeRequest();

    protected abstract void patchRequest();
}
