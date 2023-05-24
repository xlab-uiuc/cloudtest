# Coverage with Istanbul

## How to get coverage of the emulator with Istanbul CLI tool "nyc"?

<br>

### Azurite

Install Azurite using npm:

```bash
npm install -g azurite
```

Navigate to Azurite root folder and include nyc package in the node_modules with the following command:

```bash
npm i -D nyc
```

Open package.json and add the following line to the scripts:

```bash
coverage": "nyc --reporter=lcov --reporter=text azurite --skipApiVersionCheck",
```

Now, instead of running `azurite` to start the emulator, run the following command in the project directory:

```bash
npm run coverage
```

Perform actions and operations on the Azurite emulator that you want to capture coverage for.

Stop the Azurite emulator to finalize the coverage collection.

In your project directory, generate the coverage report using the following command:

```bash
nyc report --reporter=html
```

This command generates an HTML coverage report based on the coverage data collected during the execution.

Open the generated HTML report in your web browser to analyze the coverage results.