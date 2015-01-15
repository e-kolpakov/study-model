# Overview

This project aims to provide means for simulating and exploring student interactions within MOOC courses.

# Testing

[pytest][pytest-home] with [pytest-cov][pytest-cov-home] are used for testing. Running tests is explained extensively 
at pytest's [Usage and Invocations][pytest-usage] page.

Here are some examples:

    py.test  # runs all tests without coverage
    py.test tests/agents   # runs all tests in `tests/agents` package
    py.test tests/infrastructure/observers_test.py  # runs all tests in single file
    py.test tests/infrastructure/observers_test.py::TestObserver #  runs single test class
    py.test tests/infrastructure/observers_test.py::TestObserver::test_observe_missing_topic_throws_value_error  # runs single test
    
    py.test --cov model  # runs all tests with coverage collected for `model` package
    py.test --cov-report html --cov model  # run all tests with coverage for `model` and generate html report (htmlcov folder)
    
 
[pytest-home]: http://pytest.org/latest/
[pytest-cov-home]: https://pypi.python.org/pypi/pytest-cov
[pytest-usage]: http://pytest.org/latest/usage.html