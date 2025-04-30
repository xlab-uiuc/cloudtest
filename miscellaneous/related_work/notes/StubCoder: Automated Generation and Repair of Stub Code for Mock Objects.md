### StubCoder: Automated Generation and Repair of Stub Code for Mock Objects
**Main idea:**

- Previous techniques for Stub code generation: 

    - capture-and-replay approach.
    - Execute the test cases capturing the interactions b/w CUT and dependencies
    - Replace the dependencies with mock objects,
    Create stub code according to the captured interactions.
- Synthesize stub code for mock objects without capturing the actual behaviors
 of the dependencies because the actual dependencies are hard to set up,
 flaky, or unavailable.

**Challenges:**

Mock objects are often test-specific because the same dependency class often has
 different behaviors in different test cases

**Solution:**

- Given an incomplete test case without stub code, StubCoder leverages the CUT execution code
 and test oracles as specifications to guide the synthesis of stub code to make the tests pass for
 the current implementation.
- Infeasible to randomly explore all the possible candidate stub code to find a test-passing one;
 StubCoder employs a novel fitness function that captures how close a candidate stub code is to a
 test-passing stub code.

**Limitations:**

- Only works for regression testing
- Assumes knowledge of app source code
- Language specific
- Evolution — Unit tests can change over time
- Error prone — StubCoder is more likely to be successful for subjects with simple stub code.
Good for very basic mocks, not for complex emulators
- Execution time can be really slow

<br>
<hr/>
