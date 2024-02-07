### An Automatic Refactoring Framework for Replacing Test-Production Inheritance by Mocking Mechanism

**Main idea:**

- Existing frameworks create mock objects and verify the execution of the mock object.
- Despite these powerful tools, developers usually end up adopting inheritance approach i.e., create a subclass of dependent production class and control things using method overriding.
    - Why is this a problem? 
        - Implementation is tedious
        - Poor quality code
        - Introducing maintenance problems
- Goal is to develop a fully automated refactoring framework to identify and replace the usage of inheritance by using Mockito for mocking in unit testing. Mockito is well received mocking framework for JAVA apps.

**Challenges:**
- The key challenge is to preserve the test behaviors before and after the refactoring.
- Gain empirical experience of whether it is feasible and how
to perform refactoring following an automated procedure.

**Solution:**
- Automatically search for the usage of inheritance and replace it by Mockito for mocking.
- Built upon the empirical experience from five open source projects that use inheritance for
mocking.
- Decouples test code from production code.

**Limitations:**
- Limited in leveraging the advanced features of Mockito.
- Based on static code analysis.
- Limited to Java and Mockito.
- Inheritance is a req.
- Inheritance is easier to understand and use, tool requires prior knowledge.

<!-- <br>
<hr/> -->
