package com.loghandler;

import org.json.JSONArray;
import org.json.JSONObject;
import org.mockserver.model.HttpRequest;

import static com.loghandler.RESTHandlers.*;
import static com.Rainmaker.*;

public class AzureTableHandler extends Handler {
    public Operation _currOperation = Operation.NONE;

    public enum Operation {
        NONE,
        CREATE_TABLE,
    }

    public AzureTableHandler(JSONObject request) {
        _request = request;
//        _service = serviceInUse;
        decideWhichOperation();
    }

    public AzureTableHandler(HttpRequest request) {
        _HTTPRequest = request;
        _realTimeFlag = true;
//        _service = serviceInUse;
        decideWhichOperation();
    }

    @Override
    protected void putRequest() {
        // Includes: setTableACLOp, setTableServicePropertiesOp
//        System.out.println("Entering Table PUT handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            if (!_request.has("queryStringParameters")) {
                setTableACLOp();
                totalPUTReqNum += 1;
                PUTReqNum += 1;
                return;
            }
            if (_request.has("queryStringParameters")) {
                final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
                if (!queryStr.has("comp")) {
                    setTableACLOp();
                } else {
                    final JSONArray compArray = queryStr.getJSONArray("comp");
                    final String compValString = compArray.getString(0);
                    if (compValString == "properties") {
                        setTableServicePropertiesOp();
                    } else {
                        System.out.println("!!!Table Service: PUT comp value not covered: " + compValString + " !!!");
                    }
                }
                totalPUTReqNum += 1;
                PUTReqNum += 1;
                return;
            }
        }
    }

    @Override
    protected void deleteRequest() {
        // Includes: deleteTableOp
//        System.out.println("Entering Table DELETE handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            deleteTableOp();
            totalDELETEReqNum += 1;
            DELETEReqNum += 1;
        }
    }

    @Override
    protected void getRequest() {
        // Includes: getTableACLOp, queryTablesOp, getTableServiceStatsOp, getTableServicePropertiesOp
//        System.out.println("Entering Table GET handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            if (!_request.has("queryStringParameters")) {
                queryTablesOp();
                totalGETReqNum += 1;
                GETReqNum += 1;
                return;
            }
            if (_request.has("queryStringParameters")) {
                final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
                if (!queryStr.has("comp")) {
                    queryTablesOp();
                } else {
                    final JSONArray compArray = queryStr.getJSONArray("comp");
                    final String compValString = compArray.getString(0);
                    switch (compValString) {
                        case "acl":
                            getTableACLOp();
                            break;
                        case "stats":
                            getTableServiceStatsOp();
                            break;
                        case "properties":
                            getTableServicePropertiesOp();
                            break;
                        default:
                            System.out.println("!!!Table Service: GET comp value not covered: " + compValString + " !!!");
                            break;
                    }
                }
                totalGETReqNum += 1;
                GETReqNum += 1;
                return;
            }
        }
    }

    @Override
    protected void headRequest() {
        // Includes: getTableACLOp
//        System.out.println("Entering Table HEAD handler");
        if (_realTimeFlag) {
            return;
        }
        else {
            final JSONObject queryStr = _request.getJSONObject("queryStringParameters");
            final JSONArray compArray = queryStr.getJSONArray("comp");
            final String compValString = compArray.getString(0);
            if (compValString == "acl") {
                getTableACLOp();
            }
            else {
                System.out.println("!!!PUT comp value not covered: " + compValString + " !!!");
            }
        }
    }

    @Override
    protected void postRequest() {
        // Includes: createTableOp
//        System.out.println("Entering Table POST handler");
        if (_realTimeFlag) {
            _currOperation = Operation.CREATE_TABLE;
            return;
        }
        else {
            createTableOp();
            totalPOSTReqNum += 1;
            POSTReqNum += 1;
        }
    }

    @Override
    protected void mergeRequest() {
//        System.out.println("Entering Table MERGE handler");
    }

    @Override
    protected void patchRequest() {

    }

    private void setTableACLOp() {
        setTableACLNum += 1;
        totalSetTableACLNum += 1;
    }

    private void deleteTableOp() {
        deleteTableNum += 1;
        totalDeleteTableNum += 1;
    }

    private void createTableOp() {
        createTableNum += 1;
        totalCreateTableNum += 1;
    }

    private void queryTablesOp() {
        queryTablesNum += 1;
        totalQueryTablesNum += 1;
    }

    private void getTableACLOp() {
        getTableACLNum += 1;
        totalGetTableACLNum += 1;
    }

    private void setTableServicePropertiesOp() {
        setTableServicePropertiesNum += 1;
        totalSetTableServicePropertiesNum += 1;
    }

    private void getTableServiceStatsOp() {
        getTableServiceStatsNum += 1;
        totalGetTableServiceStatsNum += 1;
    }

    private void getTableServicePropertiesOp() {
        getTableServicePropertiesNum += 1;
        totalGetTableServicePropertiesNum += 1;
    }

}
