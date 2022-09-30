package com.loghandler;

import org.json.JSONArray;
import org.json.JSONObject;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureQueueHandler extends Handler {
    public AzureQueueHandler(JSONObject request) {
        _request = request;
//        _service = serviceInUse;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        // Includes: createQueueOp, setQueueMetadataOp, setQueueACL, setQueueServiceProperties,
        if (!_request.has("queryStringParameters")) {
            createQueueOp();
            totalPUTReqNum += 1;
            PUTReqNum += 1;
            return;
        }
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                createQueueOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
                    case "metadata": setQueueMetadataOp(); break;
                    case "acl": setQueueACLOp(); break;
                    case "properties": setQueueServicePropertiesOp(); break;
                    default: System.out.println("!!!PUT comp value not covered: " + compValString + " !!!"); break;
                }
            }
            totalPUTReqNum += 1;
            PUTReqNum += 1;
            return;
        }
    }

    @Override
    protected void deleteRequest() {
        // Includes: deleteQueueOp
        deleteQueueOp();
        totalDELETEReqNum += 1;
        DELETEReqNum += 1;
    }

    @Override
    protected void patchRequest() {

    }

    @Override
    protected void getRequest() {
        // Includes: listQueuesOp, getQueueMetadataOp, getQueueACLOp, getQueueServicePropertiesOp, getQueueServiceStatsOp
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            final JSONArray compArray = queryStr.getJSONArray("comp");
            final String compValString = compArray.getString(0);
            switch (compValString) {
                case "list": listQueuesOp(); break;
                case "acl": getQueueACLOp(); break;
                case "properties": getQueueServicePropertiesOp(); break;
                case "metadata": getQueueMetadataOp(); break;
                case "stats": getQueueServiceStatsOp(); break;
                default: System.out.println("!!!GET comp value not covered: " + compValString + " !!!"); break;
            }
            totalGETReqNum += 1;
            GETReqNum += 1;
            return;
        }
    }

    @Override
    protected void headRequest() {
        // Includes: getQueueMetadataOp, getQueueACL
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            final JSONArray compArray = queryStr.getJSONArray("comp");
            final String compValString = compArray.getString(0);
            switch (compValString) {
                case "acl": getQueueACLOp(); break;
                case "metadata": getQueueMetadataOp(); break;
                default: System.out.println("!!!HEAD comp value not covered: " + compValString + " !!!"); break;
            }
            totalHEADReqNum += 1;
            HEADReqNum += 1;
            return;
        }
    }

    @Override
    protected void postRequest() {
        // NONE for Queue operation
    }

    @Override
    protected void mergeRequest() {

    }

    private void createQueueOp() {
        createQueueNum += 1;
        totalCreateQueueNum += 1;
    }

    private void deleteQueueOp() {
        deleteQueueNum += 1;
        totalDeleteQueueNum += 1;
    }

    private void getQueueMetadataOp() {
        getQueueMetadataNum += 1;
        totalGetQueueMetadataNum += 1;
    }

    private void setQueueMetadataOp() {
        setQueueMetadataNum += 1;
        totalSetQueueMetadataNum += 1;
    }

    private void getQueueACLOp() {
        getQueueACLNum += 1;
        totalGetQueueACLNum += 1;
    }

    private void setQueueACLOp() {
        setQueueACLNum += 1;
        totalSetQueueACLNum += 1;
    }

    private void listQueuesOp() {
        listQueuesNum += 1;
        totalListQueuesNum += 1;
    }

    private void setQueueServicePropertiesOp() {
        setQueueServicePropertiesNum += 1;
        totalSetQueueServicePropertiesNum += 1;
    }

    private void getQueueServicePropertiesOp() {
        getQueueServicePropertiesNum += 1;
        totalGetQueueServicePropertiesNum += 1;
    }

    private void getQueueServiceStatsOp() {
        getQueueServiceStatsNum += 1;
        totalGetQueueServiceStatsNum += 1;
    }
}
