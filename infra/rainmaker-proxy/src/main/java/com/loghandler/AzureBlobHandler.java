package com.loghandler;

import org.json.JSONArray;
import org.json.JSONObject;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureBlobHandler extends Handler {
    public AzureBlobHandler(JSONObject request) {
        _request = request;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        // Includes:
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                putOrCopyBlobOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
                    case "metadata": setBlobMetadataOp(); break;
                    case "setBlobProperties": setBlobPropertiesOp(); break;
                    case "tags": setBlobTagsOp(); break;
                    case "lease": leaseBlobOp(); break;
                    case "snapshot": snapShotOp(); break;
                    case "copy": abortCopyBlobOp(); break;
                    case "undelete": undeleteBlobOp(); break;
                    case "tier": setBlobTierOp(); break;
                    case "immutabilityPolicies": setBlobImmutabilityPolicyOp(); break;
                    case "legalhold": setBlobLegalHoldOp(); break;
                    case "block": putBlockOp(); break;
                    case "blocklist": putBlockListOp(); break;
                    case "page": putPageOp(); break;
                    case "incrementalcopy": incrementalCopyBlobOp(); break;
                    case "appendblock": appendBlobOp(); break;
                    case "seal": appendBlobSealOp(); break;
                    case "expiry": setBlobExpiryOp(); break;
                    default: System.out.println("!!!Blob Container Service: PUT comp value not covered: " + compValString + " !!!"); break;
                }
            }
        }
        else {
            putOrCopyBlobOp();
        }
        totalPUTReqNum += 1;
        PUTReqNum += 1;
    }

    @Override
    protected void deleteRequest() {
        // Includes:
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                deleteBlobOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                if ("immutabilityPolicies".equals(compValString)) {
                    deleteBlobImmutabilityPolicyOp();
                } else {
                    System.out.println("!!!Blob Container Service: DELETE comp value not covered: " + compValString + " !!!");
                }
            }
        }
        else {
            deleteBlobOp();
        }
        totalDELETEReqNum += 1;
        DELETEReqNum += 1;
    }

    @Override
    protected void patchRequest() {

    }

    @Override
    protected void getRequest() {
        // Includes:
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                getBlobOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                switch (compValString) {
                    case "metadata": getBlobMetadataOp(); break;
                    case "tags": getBlobTagsOp(); break;
                    case "blobs": findBlobsByTagsOp(); break;
                    case "blocklist": getBlockListOp(); break;
                    case "pagelist": getPageRangesOp(); break;
                    default: System.out.println("!!!Blob Container Service: GET comp value not covered: " + compValString + " !!!"); break;
                }
            }
        }
        else {
            getBlobOp();
        }
        totalGETReqNum += 1;
        GETReqNum += 1;
    }

    @Override
    protected void headRequest() {
        // Includes:
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (!queryStr.has("comp")) {
                getBlobPropertiesOp();
            }
            else {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                if ("metadata".equals(compValString)) {
                    getBlobMetadataOp();
                } else {
                    System.out.println("!!!Blob Container Service: HEAD comp value not covered: " + compValString + " !!!");
                }
            }
        }
        else {
            getBlobPropertiesOp();
        }
        totalGETReqNum += 1;
        GETReqNum += 1;
    }

    @Override
    protected void postRequest() {
        // Includes:
        if (_request.has("queryStringParameters")) {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            if (queryStr.has("comp")) {
                final JSONArray compArray = queryStr.getJSONArray("comp");
                final String compValString = compArray.getString(0);
                if (compValString == "query") {
                    queryBlobContentsOp();
                    totalPOSTReqNum += 1;
                    POSTReqNum += 1;
                }
            }
        }
        else {
            System.out.println("!!!Unexpected behavior happens in AzureBlobHandler postRequest!!! " + _request);
        }
    }

    @Override
    protected void mergeRequest() {

    }

    private void putOrCopyBlobOp() {
        putOrCopyBlobNum += 1;
        totalPutOrCopyBlobNum += 1;
    }

    private void setBlobMetadataOp() {
        setBlobMetadataNum += 1;
        totalSetBlobMetadataNum += 1;
    }

    private void setBlobPropertiesOp() {
        setBlobPropertiesNum += 1;
        totalSetBlobPropertiesNum += 1;
    }

    private void setBlobTagsOp() {
        setBlobTagsNum += 1;
        totalSetBlobTagsNum += 1;
    }

    private void leaseBlobOp() {
        leaseBlobNum += 1;
        totalLeaseBlobNum += 1;
    }

    private void snapShotOp() {
        snapShotNum += 1;
        totalSnapShotNum += 1;
    }

    private void abortCopyBlobOp() {
        abortCopyBlobNum += 1;
        totalAbortCopyBlobNum += 1;
    }

    private void undeleteBlobOp() {
        undeleteBlobNum += 1;
        totalUndeleteBlobNum += 1;
    }

    private void setBlobTierOp() {
        setBlobTierNum += 1;
        totalSetBlobTierNum += 1;
    }

    private void setBlobImmutabilityPolicyOp() {
        setBlobImmutabilityPolicyNum += 1;
        totalSetBlobImmutabilityPolicyNum += 1;
    }

    private void setBlobLegalHoldOp() {
        setBlobLegalHoldNum += 1;
        totalSetBlobLegalHoldNum += 1;
    }

    private void deleteBlobOp() {
        deleteBlobNum += 1;
        totalDeleteBlobNum += 1;
    }

    private void deleteBlobImmutabilityPolicyOp() {
        deleteBlobImmutabilityPolicyNum += 1;
        totalDeleteBlobImmutabilityPolicyNum += 1;
    }

    private void getBlobOp() {
        getBlobNum += 1;
        totalGetBlobNum += 1;
    }

    private void getBlobMetadataOp() {
        getBlobMetadataNum += 1;
        totalGetBlobMetadataNum += 1;
    }

    private void getBlobTagsOp() {
        getBlobTagsNum += 1;
        totalGetBlobTagsNum += 1;
    }

    private void findBlobsByTagsOp() {
        findBlobsByTagsNum += 1;
        totalFindBlobsByTagsNum += 1;
    }

    private void getBlobPropertiesOp() {
        getBlobPropertiesNum += 1;
        totalGetBlobPropertiesNum += 1;
    }

    private void queryBlobContentsOp() {
        queryBlobContentsNum += 1;
        totalQueryBlobContentsNum += 1;
    }

    private void putBlockOp() {
        putBlockNum += 1;
        totalPutBlockNum += 1;
    }

    private void putBlockListOp() {
        putBlockListNum += 1;
        totalPutBlockListNum += 1;
    }

    private void getBlockListOp() {
        getBlockListNum += 1;
        totalGetBlockListNum += 1;
    }

    private void putPageOp() {
        putPageNum += 1;
        totalPutPageNum += 1;
    }

    private void getPageRangesOp() {
        getPageRangesNum += 1;
        totalGetPageRangesNum += 1;
    }

    private void incrementalCopyBlobOp() {
        incrementalCopyBlobNum += 1;
        totalIncrementalCopyBlobNum += 1;
    }

    private void appendBlobOp() {
        appendBlobNum += 1;
        totalAppendBlobNum += 1;
    }

    private void appendBlobSealOp() {
        appendBlobSealNum += 1;
        totalAppendBlobSealNum += 1;
    }

    private void setBlobExpiryOp() {
        setBlobExpiryNum += 1;
        totalSetBlobExpiryNum += 1;
    }
}
