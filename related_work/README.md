# Cloudtest Related Work

## List of Content

- Mock Testing
    - StubCoder: Automated Generation and Repair of Stub Code for Mock Objects [[paper]](https://arxiv.org/pdf/2307.14733.pdf) [[notes]](./notes/StubCoder:%20Automated%20Generation%20and%20Repair%20of%20Stub%20Code%20for%20Mock%20Objects.md) 
        - StubCoder leverages the CUT execution code and test oracles as specifications to guide the synthesis of stub code.
    - Mock object creation for test factoring [[paper]](https://homes.cs.washington.edu/~mernst/pubs/mock-factoring-paste2004.pdf) [[notes]](./notes/Mock%20object%20creation%20for%20test%20factoring.md) 
        - Automatically generate mock objects and introduce Mock test factoring.
    - An Automatic Refactoring Framework for Replacing Test-Production Inheritance by Mocking Mechanism [[paper]](https://dl.acm.org/doi/abs/10.1145/3468264.3468590)
        - An fully automated refactoring framework to identify and replace the usage of inheritance by using Mockito for mocking in unit testing.

- API fuzzing
    - Deriving semantics-aware fuzzers from web API schemas [[paper]](https://dl.acm.org/doi/abs/10.1145/3510454.3528637)
    - Differential regression testing for REST APIs [[paper]](https://dl.acm.org/doi/10.1145/3395363.3397374) [[notes]](./notes/Differential%20regression%20testing%20for%20REST%20APIs.md) 
        - Apply differential regression testing to different versions of the Azure network APIs based on RESTler fuzzer.

<!-- **Main idea:**

**Challenges:**

**Solution:**

**Limitations:** -->


## Papers' compilation

REST API Testing: 

Paper 1: Differential Regression Testing for REST APIs
Link: https://dl.acm.org/doi/10.1145/3395363.3397374 (ISSTA’20)

Paper 2: Metamorphic Testing of RESTful Web APIs 
Link: https://dl.acm.org/doi/10.1145/3180155.3182528 (ICSE’18)

Paper 3: Testing RESTful APIs: A Survey 
Link: https://dl.acm.org/doi/pdf/10.1145/3617175 (TOSEM’23)

Paper 4: Pythia: Grammar-based Fuzzing of REST Apis with Coverage-guided Feedback and Learning Based Mutations 
Link: https://arxiv.org/abs/2005.11498 (arXiv) 

Paper 5: Automated Generation of Test Cases for REST APIs: a Specification Based Approach 
Link: https://ieeexplore.ieee.org/document/8536162 (EDOC’18)

Paper 6: Deriving Semantic Aware Fuzzers from Web API Schemas 
Link: https://dl.acm.org/doi/abs/10.1145/3510454.3528637 (ICSE’22)

Paper 7:  QuickREST: Property-based test generation of OpenAPI described RESTful APIs. 
Link:  

Paper 8: RESTest: Automated Black-box Testing of RESTful WEB APIs  
Link: https://dl.acm.org/doi/10.1145/3460319.3469082 (ISSTA’21) 

Paper 9: Testing Cloud Services Using the Test Cast Tool 
Link: https://link.springer.com/chapter/10.1007/978-3-319-54978-1_101 

Paper 10: REST Api Fuzzing by Coverage Level Guided Black Box Testing 
Link: https://arxiv.org/abs/2112.15485 (QRS’21)

Paper 11: RESTTESTGEN: Automated black-box testing of RESTful APIs. 
Link: https://ieeexplore.ieee.org/abstract/document/9159077 (ICST’20)

Mocking and Test Factoring: 

Paper 1: Automatic Test Factoring for Java
Link: https://dl.acm.org/doi/10.1145/1101908.1101927 (ASE’05)

Paper 2: Mock object creation for test factoring
Link: https://homes.cs.washington.edu/~mernst/pubs/mock-factoring-paste2004.pdf (PASTE’04)

Paper 3: A Framework for Automated Test Mocking of Mobile Apps
Link: https://dl.acm.org/doi/10.1145/3324884.3418927 (ASE’2020) 

Paper 4: Mimicking Production Behavior with Generated Mocks 
Link: https://arxiv.org/pdf/2208.01321.pdf (arXiv’22) 

Paper 5: MODA: automated test generation for database applications via mock objects 
Link: https://dl.acm.org/doi/10.1145/1858996.1859053 (ASE’10)

Paper 6: Generating Mock Skeletons for Lightweight Web-Service Testing
Link: https://ieeexplore.ieee.org/document/8945647 (APSEC’19)

Paper 7: Environmental Modeling for Automated Cloud Application Testing 
Link: https://ieeexplore.ieee.org/document/6095493 (IEEE Softw.’12) 

Paper 8: An automatic refactoring framework for replacing test-production inheritance by mocking mechanism 
Link: https://dl.acm.org/doi/abs/10.1145/3468264.3468590 (FSE’19)

Paper 9: MockSniffer: Characterizing and Recommending Mocking Decisions for Unit Tests 
Link: https://dl.acm.org/doi/10.1145/3324884.3416539 (ASE’20)

Paper 10: Mock objects for testing java systems 
Link: https://dl.acm.org/doi/10.1007/s10664-018-9663-0 (Empirical Software Engineering’19)

Paper 11: Mock object models for test driven development 
Link: https://ieeexplore.ieee.org/document/1691384 (SERA’06)

Paper 12: Modeling with mocking 
Link: https://ieeexplore.ieee.org/document/9438574 (ICST’21)

Paper 13: Private API access and functional mocking in automated unit test generation 
Link: https://ieeexplore.ieee.org/document/7927969 (ICST’17) 

Paper 14: Mock-object generation with behavior 
Link: https://ieeexplore.ieee.org/document/4019611 (ASE’06)

Paper 15: AUTOMOCK: Automated Synthesis of a Mock Environment for Test Case Generation 
Link: https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.10111.3 (DagSemProc’10) 

Paper 16: Moles: tool-assisted environment isolation with closures 
Link: https://link.springer.com/chapter/10.1007/978-3-642-13953-6_14  

Paper 17: Using model learning for the generation of mock components
Link: https://uca.hal.science/hal-03048336 

Paper 18: Declarative mocking 
Link: https://dl.acm.org/doi/abs/10.1145/2483760.2483790 (ISSTA’13) 

Paper 19: Jmocker: Refactoring test-production inheritance by mockito 
Link: https://dl.acm.org/doi/10.1145/3510454.3516836 (ICSE’22)

Paper 20: StubCoder: Automated Generation and Repair of Stub Code for Mock Objects 
Link: https://arxiv.org/pdf/2307.14733.pdf (TOSEM’23)

Empirical Studies on Mocking: 

Paper 20: An Empirical Study of Testing File-System-Dependent Software with Mock Objects 
Link: https://ieeexplore.ieee.org/document/5069054 (AST’09) 

Paper 21: An Empirical Study on the Usage of Mocking Frameworks in Software Testing 
Link: https://ieeexplore.ieee.org/document/6958396  

Paper 22: Assessing mock classes: An empirical study 
Link: https://ieeexplore.ieee.org/document/9240675 (ICSM’20) 

Paper 23: To mock or not to mock? An empirical study on mocking practices
Link: https://ieeexplore.ieee.org/abstract/document/7962389 (MSR’17)

Tools and Fuzzers: 
Tool 1: RESTler 
Link: https://ieeexplore.ieee.org/document/8811961 (ICSE’19) 

Tool 2: vREST (Automated REST API Testing Tool)
Link: https://vrest.io/ 

Tool 3: Apigee (RESTful and HTTP based API proxies) 
Link: https://docs.apigee.com/ 

Tool 4: VCR (Record HTTP interactions of test suites) 
Link: https://github.com/vcr/vcr

Tool 5: API Fuzzer (HTTP Api Testing Framework)
Link: https://github.com/KissPeter/APIFuzzer 

Tool 6: Qualys Web Application Scanning (WAS) (Cloud-based application security product) 
Link: https://www.qualys.com/apps/web-app-scanning/ 

Tool 7: TnT Fuzzer (Swagger spec fuzzing) 
Link: https://github.com/Teebytes/TnT-Fuzzer
