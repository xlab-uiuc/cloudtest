package com.planner;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

import static com.Rainmaker.injectTestCallSitesMap;
import static java.lang.Integer.parseInt;

public class STFPlanner {
    static String _statDir;
    static String _resultDir;
    static float _budgetTime;

    public STFPlanner(String budget, String resultDirectory, String statDirectory) {
        _resultDir = resultDirectory;
        _statDir = statDirectory;
        _budgetTime = getTimeFloatFromReadableFormat(budget);
    }

    public static List<String> pickTests(){
        List<String> testsToBeRun = new ArrayList<>();
        Map<String, Float> testTimeMapping = constructTestTimeMapping();

        Map<String, List<String>> injectTestCallSitesMapLocal = new HashMap<>(injectTestCallSitesMap);
        Map<String, Float> testEfficiencyValueMapping = new HashMap<>(testTimeMapping);

        for (float collectedTime = 0; collectedTime < _budgetTime && !testEfficiencyValueMapping.isEmpty();) {
            String pickedTest = pickTest(testEfficiencyValueMapping);
            List<String> pickedTestCallSites = injectTestCallSitesMapLocal.get(pickedTest);
//            Update efficiency value map
            for (Map.Entry<String, List<String>> mapEntry : injectTestCallSitesMapLocal.entrySet()) {
                String testName = mapEntry.getKey();
                List<String> callSites = mapEntry.getValue();
                callSites.removeAll(pickedTestCallSites);
                injectTestCallSitesMapLocal.put(testName, callSites);
                float testRunningTime = testTimeMapping.get(testName);
                int faultInjectionRound = injectTestCallSitesMap.get(testName).size();
                float value =  testRunningTime * faultInjectionRound / callSites.size();
                testEfficiencyValueMapping.put(testName, value);
            }
            collectedTime += testTimeMapping.get(pickedTest);
            testEfficiencyValueMapping.remove(pickedTest);
            injectTestCallSitesMapLocal.remove(pickedTest);
        }
        return testsToBeRun;
    }

    public static String pickTest(Map<String, Float> testEfficiencyValueMap){
        Map.Entry<String, Float> min = null;
        for (Map.Entry<String, Float> entry : testEfficiencyValueMap.entrySet()) {
            if (min == null || min.getValue() > entry.getValue()) {
                min = entry;
            }
        }
        assert min != null;
        return min.getKey();
    }


    public static Map<String, Float> constructTestTimeMapping() {
        Map<String, Float> testTimeMap = new HashMap<String, Float>();

        // TODO: maybe should not rely on this PASSED_test.csv
        Path passedFilePath = Paths.get(_resultDir, "PASSED_test.csv");
        try (BufferedReader csvBufferReader = new BufferedReader(new FileReader(passedFilePath.toString()))) {
            String testName;
            while ((testName = csvBufferReader.readLine()) != null) {
                Path callSiteFilePath = Paths.get(_statDir, testName, "0", "overview.txt");
                try (BufferedReader callSiteReader = new BufferedReader(new FileReader(callSiteFilePath.toString()))) {
                    String line;
                    if ((line = callSiteReader.readLine()) != null) {
                        String[] values = line.split(": ");
                        if (values[1].isEmpty()) {
                            System.out.println("Does not have time record in the overview.txt for test" + testName);
                            System.exit(0);
                        }
                        String durationStr = values[1].trim();
                        float timeFloat = getTimeFloatFromReadableFormat(durationStr);

                        testTimeMap.put(testName, timeFloat);
                    }
                    else {
                        System.out.println("Empty overview file for test" + testName);
                        System.exit(0);
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return testTimeMap;
    }

    public static float getTimeFloatFromReadableFormat(String durationString) {
        float timeFloat = 0;
        String[] hourMinSecStringArr = durationString.split("h");
        String hourString = hourMinSecStringArr[0];
        if (!durationString.equals(hourString)) {
            timeFloat += 3600 * Integer.parseInt(hourString.trim());
        }

        String minSecString = hourMinSecStringArr[hourMinSecStringArr.length - 1];
        String[] minSecStringArr = minSecString.split("m");
        String minString = minSecStringArr[0];
        if (!minString.equals(minSecString)) {
            timeFloat += 60 * Integer.parseInt(minString.trim());
        }

        String secString = minSecStringArr[minSecStringArr.length - 1].split("s")[0];
        timeFloat += Float.parseFloat(secString.trim());
        return timeFloat;
    }
}
