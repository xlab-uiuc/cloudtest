package com;

import com.loghandler.RESTHandlers;

import org.apache.commons.lang3.StringUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.mockserver.configuration.ConfigurationProperties;
import org.mockserver.integration.ClientAndServer;
import org.mockserver.logging.MockServerLogger;
import org.mockserver.model.Format;
import org.mockserver.socket.tls.KeyStoreFactory;

import javax.net.ssl.HttpsURLConnection;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.LogManager;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.mockserver.model.HttpClassCallback.callback;
import static org.mockserver.model.HttpRequest.request;

public class Rainmaker {
    public static ClientAndServer mockServer;
    public static ClientAndServer blockRequestServer;

    public static final int noServiceUse = -1;
    public static final int exceptionHappenedWhenRetrieving = -3;

    public static List<String> skippedTestCaseExceptionHappens;

    private static int resultNameSpecializedEnum = 2;


    public static int testSuccess=0, testFail=0, testSkipped=0;

    public static boolean exemptFromRetrieving=false;

    JSONArray recordedRequests;

    public static Map<String, List<String>> injectTestCallSitesMap;

    public static HashMap<String, Integer> reqInSingleTestCNT;

    public static Map<String, Integer> requestNumMapping;
    public static int injectionCNT = 0;
    public static int seqToInject = 0;
    public static String injectCallSiteStr;
    public static String msClientReqID = "XXX";
    public static ReentrantLock lock = new ReentrantLock();
    public static final int sleepTime = 102;

    Duration timeElapsed;
    Duration eachRoundTimeElapsed;
    public static Map<String, String> testRoundTimeMap;

    public static FileWriter fwReqWithMissingHeader;

    public static String projPath;
    public static String projPathRoot;
    public static String projName;
    public static String testDLL;
    public static String rainmakerPath;
    public static String torchPath;
    public static String rainmakerPolicy;
    public static String resultDir;
    public static String statDir;
    public static String projectName;
    public static int cosmosErrorCode;
    public static boolean appFlag;

    private static String vanillaDir;

    public static boolean vanillaRun = false;
    private final boolean testFlag;
    private final boolean includePUTTestFlag;
    private final boolean fullTestFlag;
    private final boolean validationFlag;
    private final boolean cosmosAppFlag;
    private String configCallSiteStr;
    
    private final int validationRound;
    private final boolean fullValidationFlag;
    private final List<String> partialTestOrValidationNameList;

    public static List<String> callSiteList;
    public static List<String> SDKAPIList;
    public static List<String> RestList;

    public static final SimpleDateFormat runTimestampFormat = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss");

    public static String curTestStatDirWithSeq;
    public static String curTestOutcomeDir;

    public Rainmaker(JSONObject config) {
        projPath = System.getProperty("user.home")+"\\"+config.getString("project_test_path");
        projPathRoot = config.getString("project_path_root");

        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        System.out.println(runTimestampFormat.format(timestamp));

        testDLL = config.getString("test_dll");
        rainmakerPolicy = config.getString("policy");
        vanillaRun = Objects.equals(rainmakerPolicy, "vanilla");
        projectName = config.getString("project").toLowerCase();

        rainmakerPath = System.getProperty("user.home")+"\\"+config.getString("rainmaker_path");
        torchPath = System.getProperty("user.home")+"\\"+config.getString("torch_path");
        resultDir = Paths.get(System.getProperty("user.dir"), "..\\..\\results", config.getString("project").toLowerCase()).toString();
        if (!vanillaRun)
           vanillaDir = Paths.get(System.getProperty("user.dir"), "..\\..\\results", config.getString("stat_dir").split("\\\\")[1]).toString();
        statDir = Paths.get(System.getProperty("user.dir"), config.getString("stat_dir")).toString();

        if (config.has("test"))
            testFlag = config.getBoolean("test");
        else
            testFlag = true;

        
        if (config.has("include_PUT_test"))
            includePUTTestFlag = config.getBoolean("include_PUT_test");
        else
            includePUTTestFlag = false;

        if (config.has("full_test_or_vanilla"))
            fullTestFlag = config.getBoolean("full_test_or_vanilla");
        else
            fullTestFlag = true;

        if (config.has("validation"))
            validationFlag = config.getBoolean("validation");
        else
            validationFlag = false;

        if (config.has("full_validation"))
            fullValidationFlag = config.getBoolean("full_validation");
        else
            fullValidationFlag = false;

        if (config.has("app_flag")) {
            appFlag = config.getBoolean("app_flag");
            if (config.has("config_callsite"))
                configCallSiteStr = config.getString("config_callsite");
            else 
                configCallSiteStr = "NO_CONFIG_CALLSITE";
        }
        else
            appFlag = false;

        if (config.has("cosmos_app")) {
            cosmosAppFlag = config.getBoolean("cosmos_app");
            appFlag = cosmosAppFlag;
            if (config.has("config_callsite"))
                configCallSiteStr = config.getString("config_callsite");
            else 
                configCallSiteStr = "NO_CONFIG_CALLSITE";
        }
        else
            cosmosAppFlag = false;

        if (config.has("validation") && config.has("validation_round"))
            validationRound = config.getInt("validation_round");
        else
            validationRound = 1;

        if (config.has("cosmos_error_code") && cosmosAppFlag)
            cosmosErrorCode = config.getInt("cosmos_error_code");
        else
            cosmosErrorCode = 503;

        if (vanillaRun)
            projName = config.getString("project") + "_" + runTimestampFormat.format(timestamp);
        else if (validationFlag && !testFlag)
            projName = config.getString("project") + "-validation-round_" + runTimestampFormat.format(timestamp);
        else if (testFlag && !validationFlag)
            projName = config.getString("project") + "-injection-round_" + runTimestampFormat.format(timestamp);
        else if (testFlag && validationFlag) {
            System.out.println("full_test_or_vanilla and full_validation cannot be true at the same time");
            System.exit(0);
        }
        else {
            System.out.println("Should specify whether it is a test or validation run when it is not vanilla!");
            System.exit(0);
        }
        System.out.println(projName);

        if (testFlag && config.has("partial_test")) {
            JSONArray jsonArray = config.getJSONArray("partial_test");
            partialTestOrValidationNameList = new ArrayList<String>();
            for (int i=0; i<jsonArray.length(); i++){
                //Adding each element of JSON array into ArrayList
                partialTestOrValidationNameList.add(jsonArray.getString(i));
            }
        }
        else if (validationFlag && config.has("partial_validation")) {
            JSONArray jsonArray = config.getJSONArray("partial_validation");
            partialTestOrValidationNameList = new ArrayList<String>();
            for (int i=0; i<jsonArray.length(); i++){
                //Adding each element of JSON array into ArrayList
                partialTestOrValidationNameList.add(jsonArray.getString(i));
            }
        }
        else {
            JSONArray jsonArray = config.getJSONArray("partial_test");
            partialTestOrValidationNameList = new ArrayList<String>();
            for (int i=0; i<jsonArray.length(); i++){
                //Adding each element of JSON array into ArrayList
                partialTestOrValidationNameList.add(jsonArray.getString(i));
            }
        }

        File statFile = new File("stat/"+projName);
        if(statFile.mkdir()){
            System.out.println("stat folder is created successfully");
        }else{
            System.out.println("Error Found!");
        }

        File outcomeFile = new File("outcome/"+projName);
        if(outcomeFile.mkdir()){
            System.out.println("outcome folder is created successfully");
        }else{
            System.out.println("Error Found!");
        }
//        System.exit(0);
    }

    public static List<String> findTestCases() throws Exception {
        List<String> listTestCaseNames = new ArrayList<String>();
        skippedTestCaseExceptionHappens = new ArrayList<String>();
        File dirTest = new File(projPath);
        try {
//          Process process = Runtime.getRuntime().exec(
//          "dotnet test --list-tests", null, dirTest);

            System.out.println(projPath + "\\" + "test.runsettings");
            ProcessBuilder procBuilder;
            if (projectName.equals("masstransit")) 
                procBuilder = new ProcessBuilder("cmd.exe", "/c", "dotnet test " + testDLL +
                        " --list-tests --settings " + projPath + "\\" + "test.runsettings");
            if (projectName.equals("acmesharp")) 
                procBuilder = new ProcessBuilder("cmd.exe", "/c",
                "\"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\CommonExtensions\\Microsoft\\TestWindow\\vstest.console.exe\" "
                        + "/lt "+ testDLL);
            else
                procBuilder = new ProcessBuilder("cmd.exe", "/c", "dotnet test " + testDLL + " --list-tests");

            procBuilder.directory(dirTest);
            procBuilder.redirectErrorStream(true);
            Process process = procBuilder.start();

            InputStreamReader isr = new InputStreamReader(process.getInputStream());
            BufferedReader rdr = new BufferedReader(isr);
            String line;
            boolean testNamesStartFlag = false;
            boolean testNamesEndFlag = false;
            int testRunForCNT = 0;
            while ((line = rdr.readLine()) != null) {
                System.out.println(line);
//                should flag the second "Test run for" (there are three "test run for")
//              TODO: if it is using NUnit test framework, then it does not have this key sentence 
                if (line.contains("Test run for")) {
                    testRunForCNT += 1;
                    if (testRunForCNT == 2) {
                        testNamesEndFlag = true;
                    }
                }
                if (testNamesStartFlag && !testNamesEndFlag) {
                    listTestCaseNames.add(line.trim().replace(":", "."));
                }
                if (line.contains("The following Tests are available:")) {
                    testNamesStartFlag = true;
                }
            }

            process.waitFor();

        } 
        catch (Exception e){
            e.printStackTrace();
        }
        return listTestCaseNames;
    }

//    Construct the test case that needs to be injected (Passed in the data collection round)
//    The key is the test case name => list of unique call sites
    public static Map<String, List<String>> constructRequestNumMapping(boolean testRun) {
        Map<String, List<String>> testCallSitesMap = new HashMap<String, List<String>>();
//        For test run
        if (testRun) {
            // TODO: maybe should not rely on this PASSED_test.csv
            Path passedFilePath = Paths.get(vanillaDir, "PASSED_test.csv");
            try (BufferedReader csvBufferReader = new BufferedReader(new FileReader(passedFilePath.toString()))) {
                String testName;
                while ((testName = csvBufferReader.readLine()) != null) {
                        Path callSiteFilePath = Paths.get(statDir, testName, "0", "CALLSITE.csv");
                        try (BufferedReader callSiteReader = new BufferedReader(new FileReader(callSiteFilePath.toString()))) {
                            String line;
                            List<String> callSitesInSingleTestList = new ArrayList<>();
                            while ((line = callSiteReader.readLine()) != null) {
                                String[] values = line.split("\t");
                                if (values[0].isEmpty())
                                    continue;
                                if (values[0].equals("[', , ,']"))
                                    continue;
                                String callSiteString = Objects.requireNonNull(Optional.of(values[0].trim())
                                        .filter(str -> str.length() != 0)
                                        .map(str -> str.substring(2, str.length() - 2))
                                        .orElse(values[0].trim())).replace("\\\\", "\\").trim();
                                callSitesInSingleTestList.add(callSiteString);
                            }
                            testCallSitesMap.put(testName, callSitesInSingleTestList);
//                        System.out.println(testName);
                        } catch (FileNotFoundException fe) {
                            continue;
                        }

                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else {
//            Validation run
            Path bugInspectionPath = Paths.get(resultDir, "bug_inspection.csv");
            System.out.println(resultDir);
            try (BufferedReader csvBufferReader = new BufferedReader(new FileReader(bugInspectionPath.toString()))) {
                String testName;
                String callsiteToInject;
                String row;
//                Skip the header
                csvBufferReader.readLine();
                while ((row = csvBufferReader.readLine()) != null) {
                    System.out.println(row);
                    String[] values = row.split("\t");
                    
                    testName = values[0];
                    System.out.println(testName);
                    callsiteToInject = values[3];
//                    TODO: this may have a problem when we want to reproduce the injection for some tests - shld mod
                    if (Objects.equals(callsiteToInject, "Cannot find SDK API")) {
                        continue;
                    }
                    if (testCallSitesMap.containsKey(testName)) {
                        List<String> updateList = testCallSitesMap.get(testName);
                        updateList.add(callsiteToInject);
                        testCallSitesMap.put(testName, updateList);
                    }
                    else {
                        List<String> callSitesInSingleTestList = new ArrayList<>();
                        callSitesInSingleTestList.add(callsiteToInject.trim());
                        testCallSitesMap.put(testName, callSitesInSingleTestList);
                    }
                }

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return testCallSitesMap;
    }

    public void startMockServer() throws IOException {
        // Configure the socket timeout, otherwise when retrieving records, it may reach timeout
        ConfigurationProperties.maxSocketTimeout(120000);

        mockServer = ClientAndServer.startClientAndServer(10000, 10001, 10002, 18081);


        System.out.println("Mockserver is running: " + mockServer.isRunning());

        if (Objects.equals(rainmakerPolicy, "request_block")) {
            blockRequestServer = ClientAndServer.startClientAndServer(30000);
            System.out.println("BlockRequestServer is running: " + blockRequestServer.isRunning());
        }

        if (Objects.equals(rainmakerPolicy, "timeout_first_request_block")) {
            blockRequestServer = ClientAndServer.startClientAndServer(30000);
            System.out.println("BlockRequestServer is running: " + blockRequestServer.isRunning());
        }

        ConfigurationProperties.logLevel("INFO");
        String loggingConfiguration = "" +
                "java.util.logging.FileHandler.pattern = mockserver.log\n" +
                "java.util.logging.FileHandler.formatter = java.util.logging.SimpleFormatter\n" +
                "java.util.logging.FileHandler.limit=50000\n" +
                "java.util.logging.FileHandler.count=5\n" +
                "java.util.logging.FileHandler.level = INFO\n";
        LogManager.getLogManager().readConfiguration(new ByteArrayInputStream(loggingConfiguration.getBytes(UTF_8)));
    }

    public void stopMockServer() {
        mockServer.stop();
        if (Objects.equals(rainmakerPolicy, "request_block")) {
            blockRequestServer.stop();
        }
        else if (Objects.equals(rainmakerPolicy, "timeout_first_request_block")) {
            blockRequestServer.stop();
        }
    }

    private void setForwardExpectation() {
        if (Objects.equals(rainmakerPolicy, "vanilla"))
            mockServer.when(
                            request()
                    )
                    .forward(
                            callback().withCallbackClass(InjectionPolicy.RequestForwardAndResponseCallback.class)
                    );
        else if (Objects.equals(rainmakerPolicy, "vanilla_real"))
            mockServer.when(
                            request()
                    )
                    .forward(
                            callback().withCallbackClass(RealService.RequestForwardAndResponseCallback.class)
                    );

    }

    private void resetMockserver() {
        mockServer.reset();
        
    }

    private int checkWhichServiceUsed() {
//        TODO: This function should be removed: do all the parsing offline
        System.out.println("Going to check which service was used..");
        try {
            recordedRequests = new JSONArray(mockServer.retrieveRecordedRequestsAndResponses(request(), Format.JSON));
        } catch (Exception e) {
            e.printStackTrace();
            return exceptionHappenedWhenRetrieving;
        }

        if (recordedRequests.length() == 0) {
            System.out.println("No services have been used.");
            return noServiceUse;
        }
        else {
//            TODO: This is not useful any more => modify in the future
            return 1;
        }
    }

//    public void testIteration() throws Exception {
//        setForwardExpectation()
//        long start = System.currentTimeMillis();
//        while (true) {
//            long finish = System.currentTimeMillis();
//            long timeElapsed = finish - start;
//            if (timeElapsed > 30000) {
//                checkWhichServiceUsed();
//                curTestStatDirWithSeq = "stat/"+projName+"/"+"XXXX"+"/"+seqToInject;
//                new File(curTestStatDirWithSeq).mkdirs();
//                retrieveRequestsInAllServers("XXX", 0);
//                break;
//            }
//        }
//    }

    public void testIteration() throws Exception {
        List<String> listTestNames = new ArrayList<String>();
//        out of memory exception???
//        listTestNames.add("UnitTests.StreamingTests.StreamLimitTests.SMS_Limits_Max_Producers_Burst");
        if (!appFlag) {
            if (vanillaRun) {
                if (fullTestFlag) {
                    listTestNames = findTestCases();
                    System.out.println("Collected test cases' names:" + listTestNames);
                    System.out.println("Collected test cases list size:" + listTestNames.size());
                    // Debug
                    // System.exit(0);
                }
                else {
                    if (partialTestOrValidationNameList.size() == 0) {
                        System.out.println("When doing test data collection partially, should specify some test case name(s) in the config.json file!");
                        System.exit(0);
                    }
                    else {
                        listTestNames = partialTestOrValidationNameList;
                        System.out.println("Going to run partial test cases:" + listTestNames);
                    }
                }
            }
            else {
    //            Fault injection round
                if (testFlag) {
                    injectTestCallSitesMap = constructRequestNumMapping(true);
    //                System.out.println(injectTestCallSitesMap.toString());
                    if (fullTestFlag) {
                        List<String> testNamesWithNumList = new ArrayList<String>(injectTestCallSitesMap.keySet());
                        System.out.println("Going to inject test cases' names:" + testNamesWithNumList);
                        System.out.println("Going to inject test cases list size:" + testNamesWithNumList.size());
                        //            sort the test names based on the number of unique call site
                        //            put the test with the fewer number of call sites at the front
                        testNamesWithNumList.sort(new Comparator<String>() {
                            public int compare(String left, String right) {
                                return Integer.compare(injectTestCallSitesMap.get(left).size(), injectTestCallSitesMap.get(right).size());
                            }
                        });
                        listTestNames = testNamesWithNumList;
                    }
                    else {
                        if (partialTestOrValidationNameList.size() == 0) {
                            System.out.println("When doing fault injection partially, should specify some test case name(s) in the config.json file!");
                            System.exit(0);
                        }
                        else {
                            listTestNames = partialTestOrValidationNameList;
                            System.out.println("Going to inject faults to partial test cases:" + listTestNames);
                        }
                    }
                }
    //            Failure reproduction round
                if (validationFlag) {
                    injectTestCallSitesMap = constructRequestNumMapping(false);
                    // System.out.println(injectTestCallSitesMap.toString());
                    if (fullValidationFlag) {
                        List<String> testNamesWithNumList = new ArrayList<String>(injectTestCallSitesMap.keySet());
                        System.out.println("Going to validate test cases' names:" + testNamesWithNumList);
                        System.out.println("Going to validate test cases list size:" + testNamesWithNumList.size());
                        System.out.println("injectTestCallSitesMap:" + injectTestCallSitesMap.toString());
                        //            sort the test names based on the number of unique call site
                        //            put the test with the fewer number of call sites at the front
    //                    STFPlanner planner = new STFPlanner("1h", resultDir, statDir);
                        testNamesWithNumList.sort(new Comparator<String>() {
                            public int compare(String left, String right) {
                                return Integer.compare(injectTestCallSitesMap.get(left).size(), injectTestCallSitesMap.get(right).size());
                            }
                        });
                        listTestNames = testNamesWithNumList;
                    }
                    else {
                        if (partialTestOrValidationNameList.size() == 0) {
                            System.out.println("When doing validation partially, should specify some test case name(s) in the config.json file!");
                            System.exit(0);
                        }
                        else {
                            listTestNames = partialTestOrValidationNameList;
                            System.out.println("Going to validate partial test failures:" + listTestNames);
    //                        System.exit(0);
                        }
                    }
                }
            }
        }
        else {
            // If the software under test is an application
            listTestNames = new ArrayList<String>();
            listTestNames.add("AppTesting");
        }
        // test system
        if (cosmosAppFlag) {
            setForwardExpectation();
            long start = System.currentTimeMillis();
            while (true) {
                long finish = System.currentTimeMillis();
                long timeElapsed = finish - start;
                if (timeElapsed > 180000) {
                    checkWhichServiceUsed();
                    curTestStatDirWithSeq = "stat/" + projName + "/" + "cosmosAppWork" + "/" + seqToInject;
                    new File(curTestStatDirWithSeq).mkdirs();
                    retrieveRequestsInAllServers("cosmosAppWork", 0);
                    break;
                }
            }
            return;
        }

        try {
            File dirTest = new File(rainmakerPath);
            System.out.println("*****************************************");


            skippedTestCaseExceptionHappens = new ArrayList<String>();

            testRoundTimeMap = new HashMap<String, String>();

            Instant startTime = Instant.now();
//            ****************************************
//            Put the vanilla for-loop here
//            ****************************************
//            file writer to write requests with missing x-Location header to a file
            fwReqWithMissingHeader = new FileWriter("request-missing-header.txt");

//            System.out.println("injectTestCallSitesMap = " + injectTestCallSitesMap.toString());
//            System.out.println("injectTestCallSitesMap size = " + injectTestCallSitesMap.size());
            for (String curTestCaseName: listTestNames) {
                // curTestCaseName = "Microsoft.Health.Fhir.Tests.E2E.Rest.AnonymizedExportUsingAcrTests(CosmosDb, Json).GivenAValidConfigurationWithAcrReference_WhenExportingAnonymizedData_ResourceShouldBeAnonymized(path: \"\")";

//                Skip stream limit tests due to out of memory exception
//                    TODO: add this constraint to the config file
                // if (curTestCaseName.contains("StreamLimitTests") || curTestCaseName.contains("CosmosDb")
                //         || curTestCaseName.contains("CosmosDB")
                //         || (!curTestCaseName.contains("AzureEmulatedBlobStorageTest") && projectName.equals("storage")))
                //     continue;

                if (curTestCaseName.contains("StreamLimitTests")
                        || (!curTestCaseName.contains("AzureEmulatedBlobStorageTest") && projectName.equals("storage")))
                    continue;
                System.out.println(curTestCaseName);

                /* ********************************************** */
                // TODO: This should only open when evaluating AWS - for Storage.NET repo
                // if (curTestCaseName.contains("AzureEmulatedBlobStorageTest") && projectName.equals("storage"))
                //     continue;

                if (!curTestCaseName.contains("Aws") && projectName.equals("storage"))
                    continue;


                if (curTestCaseName.contains("(")) {
                    if (!includePUTTestFlag)
                        continue;
                    else {
                        if (projectName.contains("fhir")) {
                            int count = StringUtils.countMatches(curTestCaseName, "(");
                            System.out.println("number of open brackets: "+count);
                            if (count == 1) {
                                curTestCaseName = curTestCaseName.split("\\).")[1];
                            }
                            else if (count == 2) {
                                // Two brackects occurrence
                                curTestCaseName = StringUtils.substringBetween(curTestCaseName, ").", "(");
                                System.out.println("curTestCaseName:");
                                System.out.println(curTestCaseName);
                                // fhit tests are so time consuming, so ignore the PUT which has param except Cosmos config 
                                continue;
                            }
                            else
                                curTestCaseName = curTestCaseName.split("\\(")[0];

                            if (curTestCaseName.length() <= 5) 
                                continue;
                        }
                        else {
                            curTestCaseName = curTestCaseName.split("\\(")[0];
                        }
                    }
                }

                String curTestStatDir = "stat/"+projName+"/"+curTestCaseName;
                curTestOutcomeDir = "outcome/"+projName+"/"+curTestCaseName;
                new File(curTestStatDir).mkdirs();
                new File(curTestOutcomeDir).mkdirs();

                int totalInjectNum;
                if (vanillaRun)
                    totalInjectNum = 1;
//                else if (!fullTestFlag)
//                    totalInjectNum = 1;
                else if (projName.contains("AWSTest"))
                    totalInjectNum = 10;
                else {
//                    System.out.println(injectTestCallSitesMap.get(curTestCaseName).toString());
                    totalInjectNum = injectTestCallSitesMap.get(curTestCaseName).size() * validationRound;
                }


//                System.out.println(injectTestCallSitesMap.get(curTestCaseName));
                System.out.println("Total injection rounds would be: "+totalInjectNum);
//                System.out.println(injectTestCallSitesMap.get(curTestCaseName));
//                System.exit(0);
                boolean RESTres = false;
                for (int seq=0; seq < totalInjectNum; seq++) {
                    seqToInject = seq / validationRound;

                    if (vanillaRun)
                        injectCallSiteStr = "VANILLA_RUN_NO_INJECTION_STRING";
                    else if (appFlag)
                        injectCallSiteStr = configCallSiteStr;
                    else
                        injectCallSiteStr = injectTestCallSitesMap.get(curTestCaseName).get(seqToInject);

                    if (appFlag) 
                        curTestStatDirWithSeq = "stat/"+projName+"/"+"AppTesting"+"/"+seqToInject;
                    else
                        curTestStatDirWithSeq = "stat/"+projName+"/"+curTestCaseName+"/"+seqToInject;
                    
                    new File(curTestStatDirWithSeq).mkdirs();

                    callSiteList = new ArrayList<String>();
                    SDKAPIList = new ArrayList<String>();
                    RestList = new ArrayList<String>();
                    System.out.println("Setting forwarding expectations for an incoming test...");
                    Instant eachRoundStartTime = Instant.now();
                    setForwardExpectation();
                    System.out.println("=========================================");
                    System.out.println("Current test case: " + curTestCaseName);

                    // -p:ParallelizeTestCollections=false
                    // parallel parameter cannot be used?
//                    ProcessBuilder procBuilder = new ProcessBuilder("cmd.exe", "/c",
//                            "dotnet test "+ testDLL + " --logger trx --filter FullyQualifiedName=" + curTestCaseName);
//                    ProcessBuilder procBuilder = new ProcessBuilder("cmd.exe", "/c",
//                            "dotnet test" + " --blame-hang-timeout 10m --logger trx --filter FullyQualifiedName=" + curTestCaseName);
                    ProcessBuilder procBuilder;                
                    if (!includePUTTestFlag) {
                        if (projectName == "masstransit")
                            procBuilder = new ProcessBuilder("cmd.exe", "/c", "dotnet test " + testDLL +
                                    " --blame-hang-timeout 10m --logger trx --filter " + curTestCaseName +
                                    " --settings " + projPath + "\\" + "test.runsettings");
                        else
                            procBuilder = new ProcessBuilder("cmd.exe", "/c",
                                    "dotnet test "+ testDLL + " --blame-hang-timeout 10m --logger trx --filter FullyQualifiedName=" + curTestCaseName);
                    }
                    else if (includePUTTestFlag) {
                        procBuilder = new ProcessBuilder("cmd.exe", "/c",
                                "dotnet test "+ testDLL + " --blame-hang-timeout 20m --logger trx --filter " + curTestCaseName);
                    }
                    else {
                       //TODO: branch for different .net
                       procBuilder = new ProcessBuilder("cmd.exe", "/c",
                           "dotnet test "+ testDLL + " --blame-hang-timeout 5m --logger trx --filter FullyQualifiedName=" + curTestCaseName);
                        // procBuilder = new ProcessBuilder("cmd.exe", "/c",
                        //         "\"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\CommonExtensions\\Microsoft\\TestWindow\\vstest.console.exe\" "
                        //                 + "/logger:trx /TestCaseFilter:" + curTestCaseName + " " + testDLL);
                    }

                    procBuilder.directory(dirTest);

                    procBuilder.redirectErrorStream(true);

                    Process process = procBuilder.start();

//                    TODO: find the child PID of the Powershell process
//                    long pid = process.pid();
//                    System.out.println("PowerShell Process PID: "+pid);
//                    process.children().filter(ProcessHandle::isAlive)
//                            .forEach(ph -> System.out.println("PID: "+ph.pid()+"Cmd: "+ph.info().command()));
//                    System.exit(0);

                    BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
                    String line;
                    while ((line = in.readLine()) != null) {
                        //                    If comment out the following line, the press enter issue will appear?
                        // Press button issue may be highly related to quick edit
                        System.out.println(line);

                        if (line.contains("Failed:     1")) {
                                resultNameSpecializedEnum = 0;
                                testFail += 1;
                            } else if (line.contains("Skipped:     1")) {
                                resultNameSpecializedEnum = 1;
                                testSkipped += 1;
                            } else if (line.contains("Passed:     1")) {
                                resultNameSpecializedEnum = 2;
                                testSuccess += 1;
                            }

//                        This is for another test output format
//                        if (line.contains("Failed!  - Failed:")) {
//                            resultNameSpecializedEnum = 0;
//                            testFail += 1;
//                        } else if (line.contains("Skipped:     1,")) {
//                            resultNameSpecializedEnum = 1;
//                            testSkipped += 1;
//                        } else if (line.contains("Passed:     1,")) {
//                            resultNameSpecializedEnum = 2;
//                            testSuccess += 1;
//                        }
                    }

                    process.waitFor();
                    injectionCNT = 0;

                    File folder = new File(rainmakerPath + "/TestResults");
                    File[] listOfFiles = folder.listFiles();

                    assert listOfFiles != null;
                    if (listOfFiles.length == 0) {
                        System.out.println("Test result folder should not be empty.. going to exit");
                        System.exit(0);
                    }
//                    When blaming timeout hang, there would be a dir under TestResults, so this check should be invalid
//                    else if (listOfFiles.length > 1) {
//                        System.out.println("Test result folder should only contain one file for a specific .NET framework (currently the file number is larger than 1).. " +
//                                "going to exit; please delete the files under TestResults folder inside the target project");
//                        System.exit(0);
//                    }
                    else {
                        int fCNT = 0;
                        for (File listOfFile : listOfFiles) {
                            if (listOfFile.isFile()) {
                                //                            System.out.println("File " + listOfFile.getName());
                                String resultString;
                                if (resultNameSpecializedEnum == 0) {
                                    resultString = "outcome/" + projName + "/" + curTestCaseName + "/0-failed-test-result-"
                                            + seq + "-" + fCNT + ".trx";
                                }
                                else if (resultNameSpecializedEnum == 1) {
                                    resultString = "outcome/" + projName + "/" + curTestCaseName + "/1-skipped-test-result-"
                                            + seq + "-" + fCNT + ".trx";
                                }
                                else {
                                    resultString = "outcome/" + projName + "/" + curTestCaseName + "/test-result-"
                                            + seq + "-" + fCNT + ".trx";
                                }
                                Files.deleteIfExists(Paths.get(resultString));
                                listOfFile.renameTo(new File(resultString));
                            }
                            else if (listOfFile.isDirectory()) {
//                                System.out.println("Directory: " + listOfFile.getName());
                                continue;
                            }
                            fCNT++;
//                            TODO: why PUT will generate more than one result file?
//                            if (fCNT > 1) {
//                                System.out.println("Number of test results should not be larger than 1");
//                                System.exit(0);
//                            }
                        }
                    }

                    int serviceInUse;
                    // Waiting for all the pending injection callback to finish before retrieving all the requests
                    boolean isLockAcquired = lock.tryLock(2*sleepTime, TimeUnit.SECONDS);
                    if (isLockAcquired) {
                        try {
                            serviceInUse = checkWhichServiceUsed();
                        }
                        finally {
                            lock.unlock();
                        }
                    }
                    else {
                        serviceInUse = exceptionHappenedWhenRetrieving;
                        System.out.println("Unable to acquire the lock when preparing to retrieve requests");
                        System.exit(0);
                    }

                    System.out.println("=========================================");
                    if (!exemptFromRetrieving && serviceInUse != exceptionHappenedWhenRetrieving) {
                        //                    testSuccess += 1;
                        retrieveRequestsInAllServers(curTestCaseName, serviceInUse);
                    } else if (!exemptFromRetrieving) {
                        testSuccess -= 1;
                        skippedTestCaseExceptionHappens.add(curTestCaseName);
                        System.out.println("Skip test " + curTestCaseName + " due to exception when retrieving!");
                    }
                    Instant eachRoundEndTime = Instant.now();
                    eachRoundTimeElapsed = Duration.between(eachRoundStartTime, eachRoundEndTime);
                    //                System.out.println("eachRoundTimeElapsed: " + eachRoundTimeElapsed.toString());
                    testRoundTimeMap.put(curTestCaseName, humanReadableFormat(eachRoundTimeElapsed));
                    exemptFromRetrieving = false;
                    System.out.println("Resetting all expectations for the finished test (clear all the expectations and logs)... test name:" + curTestCaseName);
                    resetMockserver();
                    //                if (needInvestigation) {
                    //                    System.out.println("Need further investigation for test: " + curTestCaseName);
                    //                    System.exit(0);
                    //                }

                    singleTestStat(curTestCaseName);
                    if (curTestCaseName.contains("AwsSQSTest") && projectName.equals("storage")) {
                        System.out.println("********Sleep 61 seconds when it is a AWS SQS test (consistency model)********");
                        TimeUnit.SECONDS.sleep(61);
                    }
                }
            }
            Instant finishTime = Instant.now();
            timeElapsed = Duration.between(startTime, finishTime);
            fwReqWithMissingHeader.close();

            System.out.println("*****************************************");
//            statServices();
            statsOfRESTAPIs();
//            System.out.println("The total number of requests is: " + totalRequestNum);
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    public void retrieveRequestsInAllServers(String testName, int serviceInUse) {
        System.out.println("Going to retrieve all the requests..");
        RESTHandlers requestHandler = new RESTHandlers(testName, recordedRequests);
    }
    
    public static String humanReadableFormat(Duration duration) {
//        System.out.println("Entering humanReadableFormat");
        return duration.toString()
                .substring(2)
                .replaceAll("(\\d[HMS])(?!$)", "$1 ")
                .toLowerCase();
    }

    public void singleTestStat(String curTestCaseName) throws IOException {
//        String locString = "stat/"+projName+"/"+curTestCaseName+"/"+testSeq;
//        new File(locString).mkdirs();
        FileWriter fwTestStat = new FileWriter(curTestStatDirWithSeq+"/overview.txt");
        fwTestStat.write("Running time for this test: " + testRoundTimeMap.get(curTestCaseName) + "\n");
        fwTestStat.close();
    }

    public void statsOfRESTAPIs() throws IOException {
        FileWriter fwTestTime = new FileWriter("test-running-time-stats.txt");
        for (Map.Entry<String,String> entry : testRoundTimeMap.entrySet())
            fwTestTime.write(entry.getKey() + "\t" + entry.getValue() + "\n");
        fwTestTime.close();

        FileWriter fwExcp = new FileWriter("skipped-tests.txt");
        for (String entry : skippedTestCaseExceptionHappens)
            fwExcp.write(entry + "\n");
        fwExcp.close();

        FileWriter fw = new FileWriter("test-stats.txt");
        fw.write("Total Running Time: " + humanReadableFormat(timeElapsed));
        fw.close();

        System.out.println("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
        System.out.println("Total Running Time: " + humanReadableFormat(timeElapsed));
        System.out.println("total number of Failed tests: " + testFail);
        System.out.println("total number of Succeeded tests: " + testSuccess);
        System.out.println("total number of Skipped tests: " + testSkipped);
    }
}

