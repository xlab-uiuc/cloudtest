package com;

import com.policies.*;

import org.json.JSONArray;
import org.json.JSONObject;
import org.apache.commons.lang3.StringUtils;

import org.mockserver.model.Format;
import org.mockserver.integration.ClientAndServer;
import org.mockserver.configuration.ConfigurationProperties;
import static org.mockserver.model.HttpClassCallback.callback;
import static org.mockserver.model.HttpRequest.request;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import static java.nio.charset.StandardCharsets.UTF_8;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.LogManager;

public class Rainmaker {
    private static ClientAndServer mockServer;
    private static ClientAndServer blockRequestServer;

    private static final int noServiceUse                   = -1;
    public static final int exceptionHappenedWhenRetrieving = -3;

    public static List<String> skippedTestCaseExceptionHappens;
    private static int resultNameSpecializedEnum = 2;


    public static int testSuccess=0, testFail=0, testSkipped=0;

    JSONArray recordedRequests;

    public static Map<String, List<String>> injectTestCallSitesMap;
    public static Map<String, Integer> requestNumMapping;
    public static int injectionCNT = 0;
    public static int seqToInject = 0;
    public static String injectCallSiteStr;
    public static ReentrantLock lock = new ReentrantLock();
    public static final int sleepTime = 4;

    Duration timeElapsed;
    Duration eachRoundTimeElapsed;
    public static Map<String, String> testRoundTimeMap;

    public static FileWriter fwReqWithMissingHeader;

    public static String projPath;
    public static String projPathRoot;
    public static String projName;
    public static String testDLL;
    public static String rainmakerPath;
    public static String rainmakerPolicy;
    public static String resultDir;
    public static String projectName;

    private static String vanillaDir;

    private static boolean emulatorRun = false;
    private static boolean realRun = false;
    private final boolean includePUTTestFlag;
    private final boolean fullTestFlag;
    
    private final List<String> partialTestList;

    public static final SimpleDateFormat runTimestampFormat = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss");

    public static String curTestStatDirWithSeq;
    public static String curTestOutcomeDir;

    /**
     * Rainmaker configuration construction.
      * @param config
     */
    public Rainmaker(JSONObject config) {
        projPath = System.getProperty("user.home")+"\\"+config.getString("project_test_path");
        projPathRoot = config.getString("project_path_root");

        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        System.out.println(runTimestampFormat.format(timestamp));

        testDLL         = config.getString("test_dll");
        rainmakerPolicy = config.getString("policy");

        // Flag for emulator and real service runs
        emulatorRun     = Objects.equals(rainmakerPolicy, "vanilla");
        realRun         = Objects.equals(rainmakerPolicy, "vanilla_real");

        projectName     = config.getString("project").toLowerCase();

        rainmakerPath = System.getProperty("user.home")+"\\"+config.getString("rainmaker_path");

        resultDir     = Paths.get(System.getProperty("user.dir"), "..\\..\\results", config.getString("project").toLowerCase()).toString();

        
        if (config.has("include_PUT_test"))
            includePUTTestFlag = config.getBoolean("include_PUT_test");
        else
            includePUTTestFlag = false;

        if (config.has("full_test"))
            fullTestFlag = config.getBoolean("full_test");
        else
            fullTestFlag = true;


        if (emulatorRun)
            projName = config.getString("project") + "-emulator_" + runTimestampFormat.format(timestamp);
        else if (realRun){
            projName = config.getString("project") + "-realService_" + runTimestampFormat.format(timestamp);
        }
        else {
            System.out.println("Should specify whether it is a emulator run or real_service run");
            System.exit(0);
        }
        
        System.out.println(projName);

        JSONArray jsonArray = config.getJSONArray("partial_test");
        partialTestList = new ArrayList<String>();
        for (int i=0; i<jsonArray.length(); i++){
            // Adding each element of JSON array into ArrayList
            partialTestList.add(jsonArray.getString(i));
        }
        

        File statFile = new File("stat/"+projName);
        if(statFile.mkdir()){
            System.out.println("stat folder is created successfully");
        }
        else {
            System.out.println("Error Found!");
        }

        File outcomeFile = new File("outcome/"+projName);
        if (outcomeFile.mkdir()){
            System.out.println("outcome folder is created successfully");
        }
        else {
            System.out.println("Error Found!");
        }
    }

    /**
     * Find the test cases at the beginning of the reference round.
     * @return
     * @throws Exception
     */
    private static List<String> findTestCases() throws Exception {
        List<String> listTestCaseNames = new ArrayList<String>();
        skippedTestCaseExceptionHappens = new ArrayList<String>();
        File dirTest = new File(projPath);
        try {

            System.out.println(projPath + "\\" + "test.runsettings");
            ProcessBuilder procBuilder;

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
                // ould flag the second "Test run for" (there are three "test run for")
                // TODO: if it is using NUnit test framework, then it does not have this key sentence
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
        } catch (Exception e){
            e.printStackTrace();
        }
        return listTestCaseNames;
    }

    /**
     * Start Rainmaker proxies.
     * @throws IOException
     */
    public void startRainmakerProxy() throws IOException {
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

    /**
     * Stop Rainmaker proxies.
     */
    public void stopRainmakerProxy() {
        mockServer.stop();
    }

    /**
     * Set the Mockserver request expectation according to the Rainmaker configuration.
     */
    private void setForwardExpectation() {
        if (Objects.equals(rainmakerPolicy, "vanilla"))
            mockServer.when(
                            request()
                    )
                    .forward(
                            callback().withCallbackClass(VanillaPolicy.RequestForwardAndResponseCallback.class)
                    );
        else if (Objects.equals(rainmakerPolicy, "vanilla_real"))
            mockServer.when(
                            request()
                    )
                    .forward(
                            callback().withCallbackClass(RealServicePolicy.RequestForwardAndResponseCallback.class)
                    );

    }

    /**
     * Reset the Rainmaker proxy after each test run.
     */
    private void resetMockserver() {
        mockServer.reset();
    }

    /**
     * Check which cloud service the current test had used.
     * @return
     */
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


    /**
     * Start the test round for the application under test.
     * @throws Exception
     */
    public void rainmakerTest() throws Exception {
        List<String> listTestNames = new ArrayList<String>();
//        out of memory exception???
//        listTestNames.add("UnitTests.StreamingTests.StreamLimitTests.SMS_Limits_Max_Producers_Burst");
        if (emulatorRun || realRun) {
            if (fullTestFlag) {
                listTestNames = findTestCases();
                System.out.println("Collected test cases' names:" + listTestNames);
                System.out.println("Collected test cases list size:" + listTestNames.size());
                // Debug
                // System.exit(0);
            }
            else {
                if (partialTestList.size() == 0) {
                    System.out.println("When doing test data collection partially, should specify some test case name(s) in the config.json file!");
                    System.exit(0);
                }
                else {
                    listTestNames = partialTestList;
                    System.out.println("Going to run partial test cases:" + listTestNames);
                }
            }
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

            for (String curTestCaseName: listTestNames) {


                if (curTestCaseName.contains("StreamLimitTests")
                        || (!curTestCaseName.contains("AzureEmulatedBlobStorageTest") && projectName.equals("storage")))
                    continue;
                System.out.println(curTestCaseName);


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

                int totalInjectNum = 1;
                    
                System.out.println("Total injection rounds would be: "+totalInjectNum);

                for (int seq=0; seq < totalInjectNum; seq++) {
                    seqToInject = seq;

                    if (emulatorRun || realRun)
                        injectCallSiteStr = "VANILLA_RUN_NO_INJECTION_STRING";

                    curTestStatDirWithSeq = "stat/"+projName+"/"+curTestCaseName+"/"+seqToInject;
                    new File(curTestStatDirWithSeq).mkdirs();

                    System.out.println("Setting forwarding expectations for an incoming test...");
                    Instant eachRoundStartTime = Instant.now();
                    setForwardExpectation();
                    System.out.println("=========================================");
                    System.out.println("Current test case: " + curTestCaseName);

                    ProcessBuilder procBuilder;                
                    if (!includePUTTestFlag) {

                        procBuilder = new ProcessBuilder("cmd.exe", "/c",
                                "dotnet test "+ testDLL + " --blame-hang-timeout 10m --logger trx --filter FullyQualifiedName=" + curTestCaseName);
                    }
                    else if (includePUTTestFlag) {
                        procBuilder = new ProcessBuilder("cmd.exe", "/c",
                                "dotnet test "+ testDLL + " --blame-hang-timeout 20m --logger trx --filter " + curTestCaseName);
                    }
                    else {
                       // TODO: branch for different .net
                       procBuilder = new ProcessBuilder("cmd.exe", "/c",
                           "dotnet test "+ testDLL + " --blame-hang-timeout 5m --logger trx --filter FullyQualifiedName=" + curTestCaseName);

                    }

                    procBuilder.directory(dirTest);
                    procBuilder.redirectErrorStream(true);
                    Process process = procBuilder.start();

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
                    else {
                        int fCNT = 0;
                        for (File listOfFile : listOfFiles) {
                            if (listOfFile.isFile()) {
                                // System.out.println("File " + listOfFile.getName());
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
                            // System.out.println("Directory: " + listOfFile.getName());
                                continue;
                            }
                            fCNT++;
                            // TODO: why PUT will generate more than one result file?
                            // if (fCNT > 1) {
                            //      System.out.println("Number of test results should not be larger than 1");
                            //      System.exit(0);
                            // }
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
                    if (serviceInUse != exceptionHappenedWhenRetrieving) {
                        //                    testSuccess += 1;
                        retrieveHTTPTrafficInAllServers();
                    } else{
                        testSuccess -= 1;
                        skippedTestCaseExceptionHappens.add(curTestCaseName);
                        System.out.println("Skip test " + curTestCaseName + " due to exception when retrieving!");
                    }
                    Instant eachRoundEndTime = Instant.now();
                    eachRoundTimeElapsed = Duration.between(eachRoundStartTime, eachRoundEndTime);
                    //                System.out.println("eachRoundTimeElapsed: " + eachRoundTimeElapsed.toString());
                    testRoundTimeMap.put(curTestCaseName, humanReadableFormat(eachRoundTimeElapsed));
                    System.out.println("Resetting all expectations for the finished test (clear all the expectations and logs)... test name:" + curTestCaseName);
                    resetMockserver();

                    singleTestStat(curTestCaseName);
                }
            }
            Instant finishTime = Instant.now();
            timeElapsed = Duration.between(startTime, finishTime);
            fwReqWithMissingHeader.close();

            System.out.println("*****************************************");
            // statServices();
            statsOfRESTAPIs();
            // System.out.println("The total number of requests is: " + totalRequestNum);
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    /**
     * Collect al the requests during the test round.
     */
    public void retrieveHTTPTrafficInAllServers() {
        System.out.println("Retrieving all the HTTP traffic..");
        CollectHTTPTraffic trafficCollector = new CollectHTTPTraffic(recordedRequests);
        trafficCollector.truncateRequestBody();
        trafficCollector.saveHTTPTraffic();
    }

    /**
     * Convert the time cost to human-readable format.
     * @param duration
     * @return
     */
    public static String humanReadableFormat(Duration duration) {
        // System.out.println("Entering humanReadableFormat");
        return duration.toString()
                .substring(2)
                .replaceAll("(\\d[HMS])(?!$)", "$1 ")
                .toLowerCase();
    }

    /**
     * Statistics for a single test - output to the overview file.
     * @param curTestCaseName
     * @throws IOException
     */
    public void singleTestStat(String curTestCaseName) throws IOException {
        // String locString = "stat/"+projName+"/"+curTestCaseName+"/"+testSeq;
        // new File(locString).mkdirs();
        FileWriter fwTestStat = new FileWriter(curTestStatDirWithSeq+"/overview.txt");
        fwTestStat.write("Running time for this test: " + testRoundTimeMap.get(curTestCaseName) + "\n");
        fwTestStat.close();
    }

    /**
     * On-the-fly statistics for the REST API usage.
     * @throws IOException
     */
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

