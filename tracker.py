import coverage
import uuid

def runUsingCoverage(testFunction):
    cov = coverage.Coverage(data_file=None)
    cov.start()
    try:
        testFunction()
    finally:
        cov.stop()
    return cov.get_data().measured_files()

