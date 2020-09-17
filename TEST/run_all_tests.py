import os
from unittest import TestLoader
from unittest import TestResult

results = TestResult()
results.buffer = True

loader = TestLoader()
suite  = loader.discover(start_dir = os.path.abspath('./'),
                         pattern   = '*test.py')
suite.run(result = results)

print ('\n\n\n')
print ('-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-')
print ('SUMMARY:')
print ('- Tests Run:            \t', results.testsRun)
print ('- Errors:               \t', len(results.errors))
print ('- Failures:             \t', len(results.failures))
print ('- Skipped:              \t', len(results.skipped))
print ('- Expected Failures:    \t', len(results.expectedFailures))
print ('- Unexpected Successes: \t', len(results.unexpectedSuccesses))
if len(results.errors) > 0:
    print ('\n\nThese are the ERRORS:')
    for error in results.errors:
        print ('#######################################')
        print ('WHERE:\n\t', error[0])
        print ('WHAT:\n',    error[1])
        
if len(results.failures) > 0:
    print ('\n\nThese are the FAILURES:')
    for failure in results.failures:
        print ('#######################################')
        print ('WHERE:\n\t', failure[0])
        print ('WHAT:\n',    failure[1])


