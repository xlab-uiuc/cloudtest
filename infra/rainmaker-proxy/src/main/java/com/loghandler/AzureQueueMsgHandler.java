package com.loghandler;

import org.json.JSONObject;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureQueueMsgHandler extends Handler {
    public AzureQueueMsgHandler(JSONObject request) {
        _request = request;
//        _service = serviceInUse;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        updateMsgOp();
        totalPUTReqNum += 1;
        PUTReqNum += 1;
    };

    @Override
    protected void patchRequest() {

    }

    @Override
    protected void deleteRequest() {
        if (!_request.has("queryStringParameters")) {
            clearMsgsOp();
            totalDELETEReqNum += 1;
            DELETEReqNum += 1;
            return;
        }
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("popreceipt")) {
                clearMsgsOp();
            }
            else {
                deleteMsgOp();
            }
            totalDELETEReqNum += 1;
            DELETEReqNum += 1;
            return;
        }
    };

    @Override
    protected void getRequest() {
        if (!_request.has("queryStringParameters")) {
            getMsgsOp();
            totalGETReqNum += 1;
            GETReqNum += 1;
            return;
        }
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("peekonly")) {
                getMsgsOp();
            }
            else {
                peekMsgsOp();
            }
            totalGETReqNum += 1;
            GETReqNum += 1;
            return;
        }
    };

    @Override
    protected void headRequest() {};

    @Override
    protected void mergeRequest() {};

    @Override
    protected void postRequest() {
        putMsgOp();
        totalPOSTReqNum += 1;
        POSTReqNum += 1;
    };

    private void updateMsgOp() {
        updateMsgNum += 1;
        totalUpdateMsgNum += 1;
    }

    private void clearMsgsOp() {
        clearMsgsNum += 1;
        totalClearMsgsNum += 1;
    }

    private void deleteMsgOp() {
        deleteMsgNum += 1;
        totalDeleteMsgNum += 1;
    }

    private void getMsgsOp() {
        getMsgsNum += 1;
        totalGetMsgsNum += 1;
    }

    private void peekMsgsOp() {
        peekMsgsNum += 1;
        totalPeekMsgsNum += 1;
    }

    private void putMsgOp() {
        putMsgNum += 1;
        totalPutMsgNum += 1;
    }
}
