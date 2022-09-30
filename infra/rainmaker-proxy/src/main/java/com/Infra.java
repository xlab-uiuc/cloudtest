package com;

import com.Rainmaker;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.io.*;

import static org.mockserver.configuration.ConfigurationProperties.rebuildServerTLSContext;
import static org.mockserver.model.HttpOverrideForwardedRequest.forwardOverriddenRequest;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

public class Infra {
    public static void main(String[] args) throws Exception {
        final File configFile = new File(System.getProperty("user.dir"), "config.json");
        InputStream is = new DataInputStream(new FileInputStream(configFile));

        JSONTokener tokener = new JSONTokener(is);
        JSONArray configArray = new JSONArray(tokener);

        for (int i=0; i < configArray.length(); i++) {
            JSONObject config = configArray.getJSONObject(i);
            boolean skipFlag = config.getBoolean("skip");
            if (skipFlag)
                continue;
            Rainmaker rainMaker = new Rainmaker(config);
            try {
                rainMaker.startMockServer();
                System.out.println("Start mock server successfully");
                rainMaker.testIteration();
            } catch (Exception e) {
                e.printStackTrace();
            }
            rainMaker.stopMockServer();
        }
    }
}