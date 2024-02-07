### Mock object creation for test factoring

**What problem is the paper trying to solve?**

How to automatically generate mock objects and Introduce Mock test factoring.

**Why is this problem important?**

In the context of the paper, creation of mock objects is used to enable test factoring. Test factoring, generally, is important to reduce large system-wide tests into smaller and focused unit tests. The factored tests will run more quickly than the original test and they will also test lesser functionality than the original test. This is useful in scenarios where developers for example want to quickly identify regressions within their code based on the new changes they have made. In general, however, mocking is useful in testing as it allows isolating bugs and errors between different components and allows for simulating complex components with simpler interfaces which improves test performance or cost. 

**How does the paper solve this problem?** 

The paper proposes an automatic approach to implement a specific type of factoring called the Introduce Mock test factoring. The idea is that a test is divided into two realms: the tested realm is the code which is being changed, the mocked realm is the code which is simulated for the purpose of testing. The procedure through which this happens has 3 phases: transformation, trace capture, mock code generation. 
Transformation: The code undergoes semantics-preserving changes which makes it easier to instrument. 
Trace Capture: The original test is executed and traces are collected of calls from the tested realm into the mocked realm and vice versa. 
Mock Code Generation: The traces are analyzed and code generated for mock objects. 

**How is it related to our work?** 

I believe this work is orthogonal to our work. The main focus of this work is to generate mock objects which in turn can allow for test factoring. Our work, on the other hand, focuses on testing the fidelity and accuracy of the mock object (considering emulator is the mock for the cloud). Additionally, our work focuses on this testing in a very specific context, the context of cloud services (that too some select storage services). 

**Meeting notes:**
Contribution: To provide a general framework to automate the generation of mock objects. You can use these objects to factor in the tests. What is test factor in this context? You break down large unit tests into smaller ones.
Small unit tests has quite some benefits: test lesser functionalities.
API fuzzing


<!-- <br>
<hr/> -->
