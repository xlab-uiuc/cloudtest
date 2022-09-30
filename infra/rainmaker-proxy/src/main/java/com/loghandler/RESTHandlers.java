package com.loghandler;

import org.apache.commons.lang3.StringUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static com.Rainmaker.*;

public class RESTHandlers {
//    public int _currService;
    public String _currTestName;

    // Put these here to make compiler happy
        //    one test round operation stats
    public static int PUTReqNum=0, DELETEReqNum=0, POSTReqNum=0, GETReqNum=0, HEADReqNum=0, MERGEReqNum=0,
            PATCHReqNum=0;

    //    Queue operation number in one test round:
    public static int createQueueNum=0, setQueueMetadataNum=0, setQueueACLNum=0,
            setQueueServicePropertiesNum=0, deleteQueueNum=0, getQueueMetadataNum=0, getQueueACLNum=0,
            listQueuesNum=0, getQueueServicePropertiesNum=0, getQueueServiceStatsNum=0;

    //    Queue message operation number in one test round:
    public static int updateMsgNum=0, clearMsgsNum=0, deleteMsgNum=0, getMsgsNum=0, peekMsgsNum=0, putMsgNum=0;

    //  Table operation number in one test round:
    public static int setTableACLNum=0, deleteTableNum=0, createTableNum=0, queryTablesNum=0, getTableACLNum=0,
            setTableServicePropertiesNum=0, getTableServiceStatsNum=0, getTableServicePropertiesNum=0;

    // Table entity operation number in one test round:
    public static int insertEntitiesNum=0, queryEntitiesNum=0, deleteEntityNum=0, insertOrMergeEntityNum=0,
            insertOrReplaceNum=0, entityBatchNum=0;

    // Blob Container operation number in one test round:
    public static int createContainerNum=0, setContainerMetadataNum=0, setContainerACLNum=0, leaseContainerNum=0,
            restoreContainerNum=0, deleteContainerNum=0, getContainerPropertiesNum=0, getContainerMetadataNum=0,
            getContainerACLNum=0, listBlobsNum=0, blobBatchNum=0;

    // Blob operation number in one test round:
    public static int putOrCopyBlobNum=0, setBlobMetadataNum=0, setBlobPropertiesNum=0, setBlobTagsNum=0,leaseBlobNum=0,
            snapShotNum=0, abortCopyBlobNum=0, undeleteBlobNum=0, setBlobTierNum=0, setBlobImmutabilityPolicyNum=0,
            setBlobLegalHoldNum=0, deleteBlobNum=0, deleteBlobImmutabilityPolicyNum=0, getBlobNum=0, getBlobMetadataNum=0,
            getBlobTagsNum=0, findBlobsByTagsNum=0, getBlobPropertiesNum=0, queryBlobContentsNum=0, putBlockNum=0,
            putBlockListNum=0, getBlockListNum=0, putPageNum=0, getPageRangesNum=0, incrementalCopyBlobNum=0,
            appendBlobNum=0, appendBlobSealNum=0, setBlobExpiryNum=0;

    public RESTHandlers(String testName, JSONArray requestArray) {
        reqInSingleTestCNT = new HashMap<String, Integer>();

//        _currService = serviceUsed;
        _currTestName = testName;
        final int loggedReq = requestArray.length();
        for (int i = 0; i < loggedReq; ++i) {
            JSONObject jsonObj = requestArray.getJSONObject(i);

            if (jsonObj.has("httpRequest")) {
                JSONObject request = jsonObj.getJSONObject("httpRequest");
                // sometimes table service will give us very large json size (e.g., body part in entity batch operation)
                // so lets truncate the body first
                if (request.has("body"))
                    request.remove("body");
//                dispatchHandler(request);
            }
        }

        // Disk version: Writing the request as JSONArray into a json file
        // TODO: This write to file should mv to another place?
        try {
            FileWriter fileWriter = new FileWriter(curTestStatDirWithSeq+"/request.json", true);
            fileWriter.write(requestArray.toString());
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

//      TODO: for developing and debugging hash table implementation
//         System.exit(0);

//        totalRequestNum += loggedReq;
//        testRESTAPIsNumMap.put(testName, loggedReq);
//        testUniqueRESTAPIsNumMap.put(testName, reqInSingleTestCNT.size());
    }

    private void dispatchHandler(JSONObject request) {
//        System.out.println("Entering dispatch handler with service number: " + _currService);
//        System.out.println("request: " + jsonObj.toString());
        JSONObject headers = request.getJSONObject("headers");
        if (!headers.has("Host"))
            System.out.println("A request must have a host!");

        final JSONArray host = headers.getJSONArray("Host");
        final String hostString = host.getString(0);
        final String httpMethodString = request.getString("method");
        final String httpPath = request.getString("path");

        int dirLevel = StringUtils.countMatches(httpPath, "/");

        String tableOpString = "";
        String batchString = "";
        if (dirLevel >= 2) {
//            System.out.println(httpPath.split("/", 3)[1]);
            String[] httpPathArr = httpPath.split("/", -1);
            if (httpPathArr[httpPathArr.length-1].equals("Tables"))
                tableOpString = "Tables";
            if (httpPathArr[httpPathArr.length-1].equals("$batch"))
                batchString = "$batch";
        }

        String compVal = "";
        String restypeVal = "";
        String peekonlyVal = "";
        String popreceiptVal = "";
        String svVal = "";
        String whereVal = "";
        String snapshotVal = "";
        String versionidVal = "";
        String copyidVal = "";
        String blockidVal = "";
        String prevsnapshotVal = "";
        String visibilitytimeoutVal = "";
        String messagettlVal = "";
        String $filterVal = "";
        String $selectVal = "";

        if (request.has("queryStringParameters")) {
            final JSONObject queryStringParameters = request.getJSONObject("queryStringParameters");
//          list of query string parameter we should focus on
            if (queryStringParameters.has("comp")) {
                final JSONArray comp = queryStringParameters.getJSONArray("comp");
                compVal = "comp = " + comp.getString(0);
            }

            if (queryStringParameters.has("restype")) {
                final JSONArray restype = queryStringParameters.getJSONArray("restype");
                restypeVal = "restype = " + restype.getString(0);
            }

            if (queryStringParameters.has("peekonly")) {
                final JSONArray peekonly = queryStringParameters.getJSONArray("peekonly");
                peekonlyVal = "peekonly = " + peekonly.getString(0);
            }

            if (queryStringParameters.has("popreceipt")) {
                popreceiptVal = "popreceipt = string-value";
            }
            // New info to be collected
            if (queryStringParameters.has("sv")) {
                svVal = "sv = myvalidsastoken";
            }
            
            if (queryStringParameters.has("where")) {
                whereVal = "where = <expression>";
            }
            
            if (queryStringParameters.has("snapshot")) {
                snapshotVal = "snapshot = <DateTime>";
            }

            if (queryStringParameters.has("versionid")) {
                versionidVal = "versionid = <DateTime>";
            }

            if (queryStringParameters.has("copyid")) {
                copyidVal = "copyid = <id>";
            }
            
            if (queryStringParameters.has("blockid")) {
                blockidVal = "blockid = id";
            }

            if (queryStringParameters.has("prevsnapshot")) {
                prevsnapshotVal = "prevsnapshot = <DateTime>";
            }
            
            if (queryStringParameters.has("visibilitytimeout")) {
                visibilitytimeoutVal = "visibilitytimeout = <int-seconds>";
            }
            
            if (queryStringParameters.has("messagettl")) {
                messagettlVal = "messagettl = <int-seconds>";
            }
            //Not sure now Ref: https://docs.microsoft.com/en-us/rest/api/storageservices/query-entities
            if (queryStringParameters.has("$filter")) {
                $filterVal = "$filter = <query-expression>";
            }
            
            if (queryStringParameters.has("$select")) {
                $selectVal = "$select = <comma-separated-property-names>";
            }
        }

//        final String reqHashStr = hostString + " " + httpMethodString + " "
//                + "dirLevel: " + dirLevel + " " + restypeVal + " " + peekonlyVal + " "
//                + compVal + " " + popreceiptVal + " " + tableOpString + " " + batchString;

        final String reqHashStr = Stream.of(hostString, httpMethodString, "dirLevel: " + dirLevel, restypeVal,
                        peekonlyVal, compVal,
                        blockidVal, whereVal, svVal, versionidVal, copyidVal, snapshotVal, prevsnapshotVal, visibilitytimeoutVal, messagettlVal, 
                        $filterVal, $selectVal,
                        popreceiptVal, tableOpString, batchString)
                .filter(s -> s != null && !s.isEmpty())
                .collect(Collectors.joining(" "));

//        System.out.println(reqHashStr);

        int reqNum = reqInSingleTestCNT.getOrDefault(reqHashStr, 0);
        reqInSingleTestCNT.put(reqHashStr, reqNum+1);
    }


    private int decideQueueOrMsg(JSONObject request) {
        // A request must have a path, so it is not a must to check the existence of path
        if (request.getString("path").contains("messages")) {
            // Message operation
            return 1;
        }
        else {
            // Queue operation
            return 0;
        }
    }

    private int decideTableOrEntity(JSONObject request) {
        if (request.has("queryStringParameters")) {
            if (request.getJSONObject("queryStringParameters").has("comp")) {
                return 0;
            }
        }
        if (request.getString("path").contains("Tables")) {
            // Table operation
//            System.out.println("Table operation in decideTableOrEntity..");
            return 0;
        }
        else {
            // Entity operation, set/get ACL is the second condition
//            System.out.println("Table Entity operation in decideTableOrEntity--");
            return 1;
        }
    }

    private int decideContainerOrBlob(JSONObject request) {
        if (request.has("queryStringParameters")) {
            if (request.getJSONObject("queryStringParameters").has("restype")) {
                // Container operation
                return 0;
            }
            else {
                return 1;
            }
        }
        else {
            // Blob operation
            return 1;
        }
    }
}


