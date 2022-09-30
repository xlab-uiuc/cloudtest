package com.loghandler;

import org.json.JSONObject;
import org.mockserver.model.HttpRequest;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureTableEntityHandler extends Handler {
    public Operation _currOperation = Operation.NONE;

    public enum Operation {
        NONE,
        DELETE_ENTITY,
    }

    public AzureTableEntityHandler(JSONObject request) {
        _request = request;
        decideWhichOperation();
    }

    public AzureTableEntityHandler(HttpRequest request) {
        _HTTPRequest = request;
        _realTimeFlag = true;
//        _service = serviceInUse;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        // Includes: insertOrReplaceOp
//        System.out.println("Entering Entity PUT handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            insertOrReplaceOp();
            totalPUTReqNum += 1;
            PUTReqNum += 1;
        }
    }

    @Override
    protected void deleteRequest() {
        // Includes: deleteEntityOp
//        System.out.println("Entering Entity DELETE handler");
        if (_realTimeFlag) {
            _currOperation = Operation.DELETE_ENTITY;
            return;
        }
        else {
            deleteEntityOp();
            totalDELETEReqNum += 1;
            DELETEReqNum += 1;
        }
    }

    @Override
    protected void getRequest() {
        // Includes: queryEntitiesOp
//        System.out.println("Entering Entity GET handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            queryEntitiesOp();
            totalGETReqNum += 1;
            GETReqNum += 1;
        }
    }

    @Override
    protected void headRequest() {
        // Includes: NONE
//        System.out.println("Entering Entity HEAD handler");
    }

    @Override
    protected void postRequest() {
        // Includes: insertEntitiesOp
//        System.out.println("Entering Entity POST handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            if (_request.getString("path").contains("$batch")) {
                entityBatchOps();
            }
            else {
                insertEntitiesOp();
            }
            totalPOSTReqNum += 1;
            POSTReqNum += 1;
        }
    }

    @Override
    protected void mergeRequest() {
        // Includes: insertOrMergeEntityOp
//        System.out.println("Entering Entity MERGE handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            insertOrMergeEntityOp();
            totalMERGEReqNum += 1;
            MERGEReqNum += 1;
        }
    }

    @Override
    protected void patchRequest() {
        // Includes: insertOrReplaceOp()
        if (_realTimeFlag) {
            return;
        }
        else {
            insertOrReplaceOp();
            totalPATCHReqNum += 1;
            PATCHReqNum += 1;
        }
    }

    private void insertEntitiesOp() {
        insertEntitiesNum += 1;
        totalInsertEntitiesNum += 1;
    }

    private void queryEntitiesOp() {
        queryEntitiesNum += 1;
        totalQueryEntitiesNum += 1;
    }

    private void deleteEntityOp() {
        deleteEntityNum += 1;
        totalDeleteEntityNum += 1;
    }

    private void insertOrMergeEntityOp() {
        insertOrMergeEntityNum += 1;
        totalInsertOrMergeEntityNum += 1;
    }

    private void insertOrReplaceOp() {
        insertOrReplaceNum += 1;
        totalInsertOrReplaceNum += 1;
    }

    private void entityBatchOps() {
        entityBatchNum += 1;
        totalEntityBatchNum += 1;
    }
}
