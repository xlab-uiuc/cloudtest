package com.loghandler;

import org.json.JSONArray;
import org.json.JSONObject;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureContainerHandler extends Handler {
    public AzureContainerHandler(JSONObject request) {
        _request = request;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        // Includes: createContainerOp, setContainerMetadataOp, setContainerACL, leaseContainerOp,
        // restoreContainerOp
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                createContainerOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
                    case "metadata": setContainerMetadataOp(); break;
                    case "acl": setContainerACLOp(); break;
                    case "lease": leaseContainerOp(); break;
                    case "undelete": restoreContainerOp(); break;
                    default: System.out.println("!!!Blob Container Service: PUT comp value not covered: " + compValString + " !!!"); break;
                }
            }
            totalPUTReqNum += 1;
            PUTReqNum += 1;
            return;
        }
        else {
            System.out.println("!!!Unexpected behavior happens in AzureContainerHandler putRequest!!!");
        }
    }

    @Override
    protected void deleteRequest() {
        // Includes: deleteContainerOp
        deleteContainerOp();
        totalDELETEReqNum += 1;
        DELETEReqNum += 1;
    }

    @Override
    protected void patchRequest() {

    }


    // hash table implemenation: query field => get the value => compose the result => put it as the hash key
    @Override
    protected void getRequest() {
        // Includes: getContainerPropertiesOp, getContainerMetadataOp, getContainerACLOp, listBlobsOp
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                getContainerPropertiesOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
//                    Inefficient way to parse
                    case "metadata": getContainerMetadataOp(); break;
                    case "acl": getContainerACLOp(); break;
                    case "list": listBlobsOp(); break;
                    default: System.out.println("!!!Blob Container Service: GET comp value not covered: " + compValString + " !!!"); break;
                }
            }
            totalGETReqNum += 1;
            GETReqNum += 1;
            return;
        }
        else {
            System.out.println("!!!Unexpected behavior happens in AzureContainerHandler getRequest!!! " + _request);
        }
    }

    @Override
    protected void headRequest() {
        // Includes: getContainerPropertiesOp, getContainerMetadataOp, getContainerACLOp
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                getContainerPropertiesOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
                    case "metadata": getContainerMetadataOp(); break;
                    case "acl": getContainerACLOp(); break;
                    default: System.out.println("!!!Blob Container Service: HEAD comp value not covered: " + compValString + " !!!"); break;
                }
            }
            totalHEADReqNum += 1;
            HEADReqNum += 1;
            return;
        }
        else {
            System.out.println("!!!Unexpected behavior happens in AzureContainerHandler headRequest!!!");
        }
    }

    @Override
    protected void postRequest() {
        // Includes: blobBatchOp
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (queryStr.has("comp")) {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                if (compValString == "batch") {
                    blobBatchOp();
                    totalPOSTReqNum += 1;
                    POSTReqNum += 1;
                }
            }
        }
    }

    @Override
    protected void mergeRequest() {

    }

    private void createContainerOp() {
        createContainerNum += 1;
        totalCreateContainerNum += 1;
    }

    private void setContainerMetadataOp() {
        setContainerMetadataNum += 1;
        totalSetContainerMetadataNum += 1;
    }

    private void setContainerACLOp() {
        setContainerACLNum += 1;
        totalSetContainerACLNum += 1;
    }

    private void leaseContainerOp() {
        leaseContainerNum += 1;
        totalLeaseContainerNum += 1;
    }

    private void restoreContainerOp() {
        restoreContainerNum += 1;
        totalRestoreContainerNum += 1;
    }

    private void deleteContainerOp() {
        deleteContainerNum += 1;
        totalDeleteContainerNum += 1;
    }

    private void getContainerPropertiesOp() {
        getContainerPropertiesNum += 1;
        totalGetContainerPropertiesNum += 1;
    }

    private void getContainerMetadataOp() {
        getContainerMetadataNum += 1;
        totalGetContainerMetadataNum += 1;
    }

    private void getContainerACLOp() {
        getContainerACLNum += 1;
        totalGetContainerACLNum += 1;
    }

    private void listBlobsOp() {
        listBlobsNum += 1;
        totalListBlobsNum += 1;
    }

    private void blobBatchOp() {
        blobBatchNum += 1;
        totalBlobBatchNum += 1;
    }


}
