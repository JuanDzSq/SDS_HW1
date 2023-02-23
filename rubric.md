
# Rubric

| Requirement                                                 | Points              | Comments
| ----------------------------------------------------------- | ------------------- | -------------------------- |
| Add functionality to commit the changes                     | 0/5                 | I didn't see an impelmentation for this.
| Modules, classes and methods commented                      | 5/5                 | 
| Participant class passing unit test                         | 5/5                 |
| At least partially correct Poller class                     | 5/5                 |
| Working attempted/correct/excused/missing/stop/total method | 11/12               | -1 for style. See line 102 in poller.py
| Working __enter__/__exit__ (open/save) methods              | 8/8                 | 
| Working __next__ method                                     | 20/20               | 
| Working mock_open                                           | 10/10               |
| Working test for iterator                                   | 7/10               | -3. Full testing for iter/next missing. Case for when multiple participants have the same poll count needed.
| Working tests for all other behaviors                       | 18/20               | -2. Style. Generally bad style to call dunder (__METHOD__) methods in tests. Use the object in the way that calls these instead. i.e with statements, for loops, etc.
| Working test_random                                         | +0/Bonus!!!         |

## 79/90